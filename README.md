# APIs.json

APIs.json is a machine readable specification that API providers can use to describe their API operations, similar to how web sites are described using sitemap.xml. Providing an index of internal, partner, and public APIs, which includes not just the the OpenAPI, JSON Schema, and other machine readable artifacts, but also the currently only human readable elements like documentation, pricing, and terms of service.

Visit http://apisjson.org for more information, or submit a GitHub issue on the repository to ask a question, or submit a bug.

## Who Is Using APIs.json?

`_data/showcase.yaml` is the maintained list of providers that publish an **authoritative**
APIs.json — an index served on the same DNS domain as the APIs it describes, per section 3.2.1
of the specification. It drives the showcase grid on the home page.

Each entry carries the date it was last fetched and parsed:

```yaml
- name: AppsMax
  identifier: appsmax
  url: https://appsmax.ru/apis.json
  image: /images/showcase/appsmax.png
  status: live          # or 'unreachable' — nothing is ever silently dropped
  verified: '2026-08-26'
  api_count: 3
  spec_version: '0.23'
```

Only `status: live` entries render. An entry that starts failing keeps its row and its last-good
`verified` date, so the history stays in git rather than disappearing from the page.

### Refreshing the list

```bash
python3 scripts/verify-showcase.py                      # re-fetch what is listed (dry run)
python3 scripts/verify-showcase.py --write              # ...and persist the results
python3 scripts/verify-showcase.py --discover --write   # also scan the all/* network for new ones
python3 scripts/verify-showcase.py --discover --images --write   # ...and fetch missing logos
```

`--discover` reads `../../all/*/apis.yml` from the api-evangelist network, collecting declared
`common[].type: APIsJSON` / `APIsYAML` pointers, harvested copies under `well-known/`, and probe
artifacts that recorded a 2xx on an apis.json path. Candidates whose index is not on the same
domain as the provider — GitHub raw URLs, third-party mirrors — are rejected as non-authoritative.

The scan is a few minutes over the full network; `--discover` is optional, so the plain verify
run stays fast.
