---
name: APIKeys
description: An APIKeys property references how a consumer obtains, rotates, and revokes API keys — the credential lifecycle, rather than the authentication scheme. Authentication describes which scheme is in use; APIKeys describes how you get the credential in the first place, which is the step that actually blocks an integration. The spellings APIKey, "API Key" and "API Keys" are accepted as synonyms.
image: /images/common.png
url: '#'
machineReadable: false
source: documentation
tags:
  - Authentication
  - Credentials
  - Onboarding
yaml_example: |
  - type: APIKeys
    url: https://developers.example.com/api-keys
---
