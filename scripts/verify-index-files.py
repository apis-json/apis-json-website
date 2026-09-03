#!/usr/bin/env python3
"""
Enumerate every live APIs.json FILE the showcase knows about, and write the
result to _data/index_files.yaml.

The showcase counts PROVIDERS -- one row per organization, deduped by domain,
because "who publishes an authoritative index" is a question about
organizations. This script counts DOCUMENTS. A provider commonly serves the
same index at more than one location, and a few serve genuinely different
indexes from different hosts, so the two numbers are not the same and neither
one is wrong.

Every host the showcase names is asked for all three locations an index
conventionally lives at. Nothing is inferred: a URL is listed only if it
returned bytes that parsed into a document with an `apis` array.

Usage:
    python3 scripts/verify-index-files.py            # dry run
    python3 scripts/verify-index-files.py --write    # persist
"""

import argparse
import datetime
import json
import os
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.dirname(SCRIPT_DIR)
SHOWCASE = os.path.join(SITE_DIR, '_data', 'showcase.yaml')
OUT = os.path.join(SITE_DIR, '_data', 'index_files.yaml')

UA = 'APIs.json-Showcase-Verifier/1.0 (+https://apisjson.org)'
PATHS = ('/apis.json', '/.well-known/apis.json', '/apis.yml')
socket.setdefaulttimeout(20)


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.headers.get('Content-Type', ''), r.read()
    except urllib.error.HTTPError as e:
        return e.code, '', b''
    except Exception:
        return 0, '', b''


def parse_index(body, content_type, url):
    """Parse the bytes. A status code is not evidence that a document exists --
    hosts that soft-200 every path hand back an HTML shell for /apis.json."""
    if not body:
        return None
    text = body.decode('utf-8', 'replace')
    looks_yaml = url.lower().endswith(('.yml', '.yaml')) or 'yaml' in content_type
    order = (yaml.safe_load, json.loads) if looks_yaml else (json.loads, yaml.safe_load)
    for parser in order:
        try:
            doc = parser(text)
        except Exception:
            continue
        if isinstance(doc, dict) and isinstance(doc.get('apis'), list):
            return doc
    return None


def candidates():
    """Every URL worth asking for, seeded from the showcase and expanded to the
    three conventional locations on each host it names."""
    entries = [e for e in (yaml.safe_load(open(SHOWCASE)) or []) if isinstance(e, dict)]
    seeds = {}
    for e in entries:
        for u in (e.get('url'), e.get('also_at')):
            if not u or not u.startswith('http'):
                continue
            seeds[u] = e
            p = urllib.parse.urlparse(u)
            for path in PATHS:
                seeds.setdefault(f'{p.scheme}://{p.netloc}{path}', e)
    return seeds


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()

    seeds = candidates()
    print(f'{len(seeds)} candidate urls across {len(set(urllib.parse.urlparse(u).netloc for u in seeds))} hosts')

    def check(url):
        status, ctype, body = fetch(url)
        doc = parse_index(body, ctype, url)
        if not doc:
            return None
        e = seeds[url]
        return {
            'url': url,
            'provider': e.get('name') or e.get('identifier'),
            'identifier': e.get('identifier'),
            'api_count': len(doc.get('apis') or []),
            'spec_version': str(doc.get('specificationVersion') or ''),
        }

    live = []
    with ThreadPoolExecutor(max_workers=16) as ex:
        futs = {ex.submit(check, u): u for u in sorted(seeds)}
        for f in as_completed(futs):
            r = f.result()
            print(f"  {'ok  ' if r else 'FAIL'} {futs[f]}")
            if r:
                live.append(r)

    live.sort(key=lambda r: ((r['provider'] or '').lower(), r['url']))
    hosts = {urllib.parse.urlparse(r['url']).netloc for r in live}
    print(f'\n{len(live)} live documents · {len(hosts)} hosts · '
          f'{len(set(r["identifier"] for r in live))} providers')

    if not args.write:
        print('(dry run — pass --write to persist)')
        return

    with open(OUT, 'w') as f:
        f.write('---\n')
        yaml.safe_dump({'verified': datetime.date.today().isoformat(), 'files': live},
                       f, sort_keys=False, allow_unicode=True, width=120)
    print(f'wrote {OUT}')


if __name__ == '__main__':
    main()
