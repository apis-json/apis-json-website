---
name: GlobalPrivacyControl
description: A GlobalPrivacyControl property points to a provider's support for the Global Privacy Control signal, the browser-sent opt-out of the sale or sharing of personal data. Registered in 0.25. The GPC specification defines a machine-readable statement at /.well-known/gpc.json, which is the preferred target.
image: /images/privacy-policy.png
url: '#'
machineReadable: true
source: well-known
tags:
- Privacy
- Regulation
- Consent
yaml_example: |
  - type: GlobalPrivacyControl
    url: https://example.com/.well-known/gpc.json
---
