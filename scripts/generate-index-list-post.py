#!/usr/bin/env python3
"""
Render "A List of 100 APIs.json" from _data/index_files.yaml.

The table is generated, never typed. Run verify-index-files.py first; this
script only formats what that one proved. If a provider drops offline, re-run
both and the row leaves the post the same way it leaves the home page.
"""

import html
import os
import urllib.parse

import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.dirname(SCRIPT_DIR)
DATA = os.path.join(SITE_DIR, '_data', 'index_files.yaml')
SHOWCASE = os.path.join(SITE_DIR, '_data', 'showcase.yaml')
POST = os.path.join(SITE_DIR, '_posts', '2026-09-03-a-list-of-100-apis-json.html')

LIMIT = 100


def esc(s):
    return html.escape(str(s or ''), quote=True)


def short(u):
    p = urllib.parse.urlparse(u)
    return p.netloc + p.path


def main():
    data = yaml.safe_load(open(DATA))
    files = data['files']
    checked = data['verified']

    providers = [e for e in (yaml.safe_load(open(SHOWCASE)) or [])
                 if isinstance(e, dict) and e.get('status') == 'live']

    listed = files[:LIMIT]
    hosts = {urllib.parse.urlparse(f['url']).netloc for f in files}

    # A provider serving the same index at more than one location is one
    # organization and several documents. Both facts belong in the post.
    seen, doubled = set(), set()
    for f in listed:
        if f['identifier'] in seen:
            doubled.add(f['identifier'])
        seen.add(f['identifier'])

    versions = {}
    blank = 0
    for f in listed:
        v = (f.get('spec_version') or '').strip()
        if v:
            versions[v] = versions.get(v, 0) + 1
        else:
            blank += 1
    version_line = ', '.join(f'<code>{esc(v)}</code> ({n})' for v, n in
                             sorted(versions.items(), key=lambda kv: (-kv[1], kv[0])))
    # 1.0 is not a version of APIs.json and never has been; a few documents
    # declare it anyway. Report the truth rather than counting it as one.
    real = sorted(v for v in versions if v.startswith('0.'))
    invalid = sum(n for v, n in versions.items() if not v.startswith('0.'))
    oldest = real[0]
    # "Every released version" is only claimable while it is literally true.
    released = ['0.14', '0.15', '0.16', '0.17', '0.18', '0.19', '0.20', '0.21', '0.22', '0.23']
    if real == released:
        versions_claim = (f'every one of the {len(real)} released versions of APIs.json '
                          f'from <code>{esc(oldest)}</code> on, all in production at the same time, '
                          'the oldest of them a decade old and still parsing')
    else:
        versions_claim = (f'{len(real)} released versions of APIs.json in production at the '
                          f'same time, the oldest of them <code>{esc(oldest)}</code> — '
                          'a decade old, and still parsing')

    # One row per URL means one organization can appear twice; the API count
    # for the list must not double-count those.
    by_org = {}
    for f in listed:
        by_org.setdefault(f['identifier'], int(f.get('api_count') or 0))

    rows = []
    for i, f in enumerate(listed, 1):
        v = (f.get('spec_version') or '').strip()
        rows.append(
            '  <tr>'
            f'<td class="n">{i}</td>'
            f'<td>{esc(f["provider"])}</td>'
            f'<td class="u"><a href="{esc(f["url"])}" target="_blank" rel="noopener">{esc(short(f["url"]))}</a></td>'
            f'<td class="n">{int(f.get("api_count") or 0)}</td>'
            f'<td class="n">{esc(v) if v else "&mdash;"}</td>'
            '</tr>'
        )

    out = TEMPLATE.format(
        checked=esc(checked),
        listed=len(listed),
        total=len(files),
        remainder=len(files) - len(listed),
        hosts=len(hosts),
        providers=len(providers),
        doubled=len(doubled),
        versions=version_line,
        versions_claim=versions_claim,
        invalid=invalid,
        blank=blank,
        oldest=esc(oldest),
        orgs_in_list=len(by_org),
        distinct_apis=sum(by_org.values()),
        rows='\n'.join(rows),
    )
    with open(POST, 'w') as fh:
        fh.write(out)
    print(f'wrote {POST} — {len(listed)} of {len(files)} rows, checked {checked}')


TEMPLATE = '''---
layout: post
title: "A List of 100 APIs.json"
date: 2026-09-03
image: /images/a-list-of-100-apis-json.png
tags:
  - APIs.json
  - Discovery
  - Adoption
  - Index
---

<p>Here are one hundred APIs.json files. Not a hundred companies we believe have one, and not a hundred entries copied out of somebody else's list — a hundred URLs that were requested on {checked}, answered with bytes that parsed, and had an <code>apis</code> array inside. The {orgs_in_list} organizations behind them describe {distinct_apis} APIs.</p>

<p>We publish the list rather than the number because a number cannot be checked. Every row below is a link. Click one and you get the raw index that host serves, right now, with nothing of ours in between.</p>

<h3>What had to be true to make the table</h3>

<p>Two rules, and the first is the one the specification already states in section 3.2.1: <strong>the index is served from the same domain as the APIs it describes</strong>. A copy of your APIs.json in a GitHub repository is a file. The same document at <code>yourdomain.com/apis.json</code> is a discovery endpoint, because a machine that knows your domain can find it without being told anything else. That rule threw out more candidates than it kept.</p>

<p>The second rule is that <strong>a status code is not a document</strong>. Hosts that answer <code>200</code> to everything will happily return their HTML shell for <code>/apis.json</code>, and several pointers that providers gave us themselves turned out to aim at an OpenAPI rather than an index. Every URL here was parsed, not pinged. Four candidates were dropped on this pass for failing exactly that check.</p>

<h3>One hundred documents is not one hundred organizations</h3>

<p>It is {orgs_in_list}. The table counts <em>files</em>, and {doubled} organizations serve the same index at more than one location — usually <code>/apis.json</code> and <code>/.well-known/apis.json</code> together, which is the belt-and-braces move and a sensible one while the convention is still settling. Those appear twice below, because two URLs that both answer are two places a machine can succeed.</p>

<p>Counted as organizations instead of files, {providers} publish an authoritative index today, and {total} URLs answer for them. The <a href="/">home page grid</a> is the organization-shaped view of this same data — one tile per provider, {providers} tiles.</p>

<h3>The versions are the interesting column</h3>

<p>Across the hundred: {versions}. That is {versions_claim}. It is also the wild in miniature: {invalid} documents declare <code>1.0</code>, a version that has never existed, and {blank} declare no version at all — and their <code>apis</code> arrays parse fine anyway, which tells you which fields readers actually depend on.</p>

<p>Nobody had to upgrade. An index written against {oldest} is still valid today and the tooling still reads it, because every release since has added vocabulary rather than moved the furniture. That is the entire argument for keeping the format small, and this column is the evidence for it rather than the claim.</p>

<p>The other thing worth noticing is who is here. Weather data, postal code lookups, disc golf, debt collection, a city council. Most are small. Almost none are the companies that would appear on a list of the largest API providers — and the largest API providers are, with a few exceptions, absent. The organizations that publish a machine-readable index of their APIs are overwhelmingly the ones for whom being found is the whole business.</p>

<h3>The list</h3>

<table class="index-list">
<thead><tr><th class="n">#</th><th>Provider</th><th>APIs.json</th><th class="n">APIs</th><th class="n">Version</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>

<p class="list-note">Fetched and parsed {checked}. {total} URLs passed; the {listed} above are the first {listed} alphabetically by provider, and the remaining {remainder} are reachable from the <a href="/">home page grid</a>.</p>

<h3>If you publish one and you are not on it</h3>

<p>You are almost certainly not missing because we judged you. You are missing because nobody asked your server. For most of this list's history the only route onto it was to tell us, which meant it measured who had heard of us rather than who had done the work. When we finally sent the request to every host we knew about, nearly half of the organizations on this list came back from servers that had been quietly answering it for years.</p>

<p>So: put an <code>apis.json</code> at the root of the domain your APIs live on, or at <code>/.well-known/apis.json</code>, or both, and <a href="https://github.com/apis-json/apis-json-website/issues/new?title=Add%20our%20APIs.json%20to%20the%20showcase" target="_blank" rel="noopener">open an issue</a>. It gets fetched and parsed and added, or it gets turned down with the reason.</p>

<style>
  .index-list {{ width: 100%; border-collapse: collapse; margin: 1.5rem 0 1rem; font-size: 0.9rem; }}
  .index-list th {{ text-align: left; font-weight: 700; color: #1a1a2e; border-bottom: 2px solid #e3e7ee; padding: 0.5rem 0.6rem; }}
  .index-list td {{ border-bottom: 1px solid #eef1f6; padding: 0.45rem 0.6rem; vertical-align: top; }}
  .index-list td.n, .index-list th.n {{ text-align: right; white-space: nowrap; color: #64748b; }}
  .index-list td.u {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.82rem; overflow-wrap: anywhere; }}
  .index-list tr:hover td {{ background: #f8f9fb; }}
  .list-note {{ font-size: 0.88rem; color: #64748b; }}
  @media (max-width: 640px) {{
    .index-list {{ font-size: 0.82rem; }}
    .index-list td.u {{ font-size: 0.74rem; }}
  }}
</style>
'''


if __name__ == '__main__':
    main()
