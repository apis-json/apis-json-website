#!/usr/bin/env python3
"""
Maintain the "Who Is Using APIs.json?" list on apisjson.org.

Two jobs, both idempotent and safe to re-run:

  1. DISCOVER — scan the api-evangelist all/* network for providers that publish
     an authoritative APIs.json (an index served on the same DNS domain as the
     APIs it describes, per section 3.2.1 of the spec). Candidates come from
     declared `common[].type: APIsJSON` / `APIsYAML` pointers and from harvested
     copies under `all/<slug>/well-known/`.

  2. VERIFY — fetch every URL already in _data/showcase.yaml plus every new
     candidate, confirm it still returns a parseable APIs.json (or apis.yml),
     and stamp each entry with `verified` and `status`.

Nothing is ever silently dropped. An entry that fails is kept with
`status: unreachable` and its last-good `verified` date, so the home page can
choose to hide it while the history survives in git.

Usage:
    python3 scripts/verify-showcase.py               # verify existing only
    python3 scripts/verify-showcase.py --discover    # also scan all/* for new
    python3 scripts/verify-showcase.py --write       # persist changes
    python3 scripts/verify-showcase.py --images      # also fetch missing logos
"""

import argparse
import datetime
import glob
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request

import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(SITE_DIR, '_data', 'showcase.yaml')
IMAGES_DIR = os.path.join(SITE_DIR, 'images', 'showcase')

# commons/apis-json-website -> commons -> GitHub -> all
ALL_DIR = os.path.join(os.path.dirname(os.path.dirname(SITE_DIR)), 'all')

UA = 'APIs.json-Showcase-Verifier/1.0 (+https://apisjson.org)'
TIMEOUT = 20

# Hosts that are ours, or a registry rather than a provider. An index served
# from one of these is not a third-party adoption signal.
SKIP_HOSTS = {'raw.githubusercontent.com', 'github.com', 'gist.github.com'}


def today():
    return datetime.date.today().isoformat()


def registrable(host):
    h = (host or '').lower().lstrip('.')
    return h[4:] if h.startswith('www.') else h


def same_domain(a, b):
    a, b = registrable(a), registrable(b)
    if not a or not b:
        return False
    return a == b or a.endswith('.' + b) or b.endswith('.' + a)


def fetch(url):
    """Return (status, content_type, body_bytes). status is 0 on transport error."""
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, r.headers.get('Content-Type', ''), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get('Content-Type', '') if e.headers else '', b''
    except Exception:
        return 0, '', b''


def parse_index(body, content_type, url):
    """Parse an APIs.json (or apis.yml) document. Returns the dict, or None."""
    if not body:
        return None
    text = body.decode('utf-8', 'replace')
    doc = None
    looks_yaml = url.lower().endswith(('.yml', '.yaml')) or 'yaml' in content_type
    try:
        doc = yaml.safe_load(text) if looks_yaml else json.loads(text)
    except Exception:
        # A server may mislabel the content type; try the other parser once.
        try:
            doc = json.loads(text) if looks_yaml else yaml.safe_load(text)
        except Exception:
            return None
    if not isinstance(doc, dict):
        return None
    # The one structural requirement the spec places on an index.
    if not isinstance(doc.get('apis'), list):
        return None
    return doc


def load_showcase():
    with open(DATA_FILE) as f:
        entries = yaml.safe_load(f) or []
    return [e for e in entries if isinstance(e, dict)]


def discover():
    """Yield candidate dicts from the all/* network."""
    if not os.path.isdir(ALL_DIR):
        print(f'  ! {ALL_DIR} not found — skipping discovery', file=sys.stderr)
        return []

    found = {}

    def note(slug, url, provider_site, name, description):
        if not url or url.startswith(('well-known/', './', '../')):
            return
        host = urllib.parse.urlparse(url).hostname
        if not host or registrable(host) in SKIP_HOSTS:
            return
        # Authoritative means the index sits on the domain it describes.
        if provider_site and not same_domain(host, urllib.parse.urlparse(provider_site).hostname):
            return
        # One entry per provider. A provider commonly serves the same index at
        # both /apis.json and /.well-known/apis.json; that is one adopter, not
        # two. Key on the registrable domain and prefer the root path, which is
        # what the rest of the showcase links to.
        key = registrable(host)
        prev = found.get(key)
        cand = {'slug': slug, 'url': url, 'name': name, 'description': description}
        if prev is None:
            found[key] = cand
        elif prev['url'] != url:
            depth = lambda u: len(urllib.parse.urlparse(u).path.strip('/').split('/'))
            if depth(url) < depth(prev['url']):
                cand['also_at'] = prev['url']
                found[key] = cand
            else:
                prev.setdefault('also_at', url)

    for path in sorted(glob.glob(os.path.join(ALL_DIR, '*', 'apis.yml'))):
        slug = os.path.basename(os.path.dirname(path))
        try:
            d = yaml.safe_load(open(path))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue

        site = ''
        for c in (d.get('common') or []):
            if isinstance(c, dict) and c.get('type') in ('Website', 'Homepage'):
                site = c.get('url') or ''
                break
        if not site:
            for a in (d.get('apis') or []):
                if isinstance(a, dict):
                    site = a.get('humanURL') or a.get('baseURL') or ''
                    if site:
                        break

        name = d.get('name') or slug
        desc = (d.get('description') or '').strip().split('. ')[0]

        def scan(props):
            for c in (props or []):
                if isinstance(c, dict) and c.get('type') in ('APIsJSON', 'APIsYAML'):
                    note(slug, c.get('url'), site, name, desc)

        scan(d.get('common'))
        for a in (d.get('apis') or []):
            if isinstance(a, dict):
                scan(a.get('properties'))

        # Harvested copies: the file records the URL it came from.
        for f in glob.glob(os.path.join(os.path.dirname(path), 'well-known', '*.json')):
            try:
                doc = json.load(open(f))
            except Exception:
                continue
            if isinstance(doc, dict) and isinstance(doc.get('apis'), list) and doc.get('url'):
                note(slug, doc['url'], site, doc.get('name') or name, desc)

        # Probe artifacts: a recorded 2xx on an apis.json path.
        for f in glob.glob(os.path.join(os.path.dirname(path), 'well-known', '*.yml')):
            try:
                doc = yaml.safe_load(open(f))
            except Exception:
                continue
            if not isinstance(doc, dict):
                continue
            for h in (doc.get('hosts') or []):
                if not isinstance(h, dict):
                    continue
                for dd in (h.get('documents') or []):
                    if not isinstance(dd, dict):
                        continue
                    p = str(dd.get('path', ''))
                    try:
                        st = int(dd.get('status'))
                    except (TypeError, ValueError):
                        continue
                    if 200 <= st < 300 and re.search(r'apis\.(json|ya?ml)$', p, re.I):
                        note(slug, urllib.parse.urljoin(h.get('host', ''), p), site, name, desc)

    return list(found.values())


def identifier_for(name, url, taken):
    base = re.sub(r'[^a-z0-9]+', '-', (name or '').lower()).strip('-')
    if not base:
        base = re.sub(r'[^a-z0-9]+', '-', urllib.parse.urlparse(url).hostname or '').strip('-')
    ident = base
    n = 2
    while ident in taken:
        ident = f'{base}-{n}'
        n += 1
    return ident


def image_candidates(entry, doc):
    """Logo sources, best first.

    A provider's own APIs.json `image` is the most authoritative, then whatever
    the all/* profile recorded. Open Graph cards are accepted last — they are
    wide social banners rather than logos and render small in a 44px tile.
    """
    srcs = []
    if isinstance(doc, dict) and doc.get('image'):
        srcs.append(doc['image'])
    if entry.get('image_source'):
        srcs.append(entry['image_source'])
    src_repo = entry.get('source') or ''
    if src_repo.startswith('all/'):
        profile = os.path.join(ALL_DIR, src_repo[4:], 'apis.yml')
        if os.path.exists(profile):
            try:
                d = yaml.safe_load(open(profile))
                if isinstance(d, dict) and d.get('image'):
                    srcs.append(d['image'])
            except Exception:
                pass
    seen, ordered = set(), []
    for u in srcs:
        if u and u.startswith('http') and u not in seen:
            seen.add(u)
            ordered.append(u)
    social = re.compile(r'(^|[/_-])(og|opengraph|og-image|social)([/_.-]|$)', re.I)
    return sorted(ordered, key=lambda u: 1 if social.search(u) else 0)


def fetch_image(entry, doc):
    """Save a logo to images/showcase/<identifier>.<ext>. Returns the site path."""
    for src in image_candidates(entry, doc):
        got = _save_image(entry, src)
        if got:
            return got
    return None


def _save_image(entry, src):
    status, ctype, body = fetch(src)
    if status != 200 or not body or len(body) < 200:
        return None
    ext = {'image/png': 'png', 'image/jpeg': 'jpg', 'image/svg+xml': 'svg',
           'image/webp': 'webp', 'image/gif': 'gif'}.get(ctype.split(';')[0].strip())
    if not ext:
        ext = os.path.splitext(urllib.parse.urlparse(src).path)[1].lstrip('.').lower() or 'png'
    if ext not in ('png', 'jpg', 'jpeg', 'svg', 'webp', 'gif'):
        return None
    os.makedirs(IMAGES_DIR, exist_ok=True)
    dest = os.path.join(IMAGES_DIR, f"{entry['identifier']}.{ext}")
    with open(dest, 'wb') as f:
        f.write(body)
    return f"/images/showcase/{entry['identifier']}.{ext}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--discover', action='store_true', help='scan all/* for new providers')
    ap.add_argument('--images', action='store_true', help='fetch logos for entries missing one')
    ap.add_argument('--write', action='store_true', help='persist changes to _data/showcase.yaml')
    args = ap.parse_args()

    entries = load_showcase()
    by_url = {e.get('url'): e for e in entries}
    taken = {e.get('identifier') for e in entries}

    added = []
    if args.discover:
        listed_domains = {registrable(urllib.parse.urlparse(u or '').hostname) for u in by_url}
        for cand in discover():
            if cand['url'] in by_url:
                continue
            if registrable(urllib.parse.urlparse(cand['url']).hostname) in listed_domains:
                continue
            ident = identifier_for(cand['name'], cand['url'], taken)
            taken.add(ident)
            e = {
                'view_sort': f"N-{ident}",
                'name': cand['name'],
                'identifier': ident,
                'url': cand['url'],
                'description': cand['description'],
                'image': None,
                'source': f"all/{cand['slug']}",
            }
            if cand.get('also_at'):
                e['also_at'] = cand['also_at']
            entries.append(e)
            by_url[cand['url']] = e
            added.append(e)
        print(f'discovered {len(added)} new candidate(s)')

    live = unreachable = 0
    rejected = []
    for e in entries:
        status, ctype, body = fetch(e['url'])
        doc = parse_index(body, ctype, e['url'])
        if doc:
            e['status'] = 'live'
            e['verified'] = today()
            e['api_count'] = len(doc.get('apis') or [])
            sv = doc.get('specificationVersion')
            if sv:
                e['spec_version'] = str(sv)
            if not e.get('description') and doc.get('description'):
                e['description'] = doc['description'].strip().split('. ')[0]
            live += 1
        else:
            e['status'] = 'unreachable'
            e['last_http_status'] = status
            if e.get('verified'):
                unreachable += 1
            else:
                # Never validated, so it was never an adopter. A declared
                # pointer can be a mistyped OpenAPI, a soft-200 HTML shell, or
                # a host that is simply down.
                rejected.append(e)
        flag = 'ok  ' if doc else 'FAIL'
        print(f"  {flag} {status:<4} {e['identifier']:<34} {e['url']}")

        if args.images and not e.get('image'):
            got = fetch_image(e, doc)
            if got:
                e['image'] = got
                print(f"       logo -> {got}")

    if rejected:
        entries = [e for e in entries if e not in rejected]
        print(f'\nrejected {len(rejected)} candidate(s) that never returned a valid APIs.json:')
        for e in rejected:
            print(f"  - {e['identifier']} ({e.get('last_http_status')}) {e['url']}")

    print(f'\n{live} live · {unreachable} unreachable · {len(entries)} listed')

    if args.write:
        entries.sort(key=lambda e: str(e.get('view_sort') or e.get('identifier')))
        with open(DATA_FILE, 'w') as f:
            f.write('---\n')
            yaml.safe_dump(entries, f, sort_keys=False, allow_unicode=True, width=100)
        print(f'wrote {DATA_FILE}')
    else:
        print('(dry run — pass --write to persist)')


if __name__ == '__main__':
    main()
