---
name: ContentSignal
description: A ContentSignal property references the Content-Signals directive a provider publishes in robots.txt — a machine-readable statement of how their content may be used for search, AI input, and AI training. It is distinct from AgenticAccess, which declares whether agents may call an API, and from LLMsTxt, which declares what an agent should read. ContentSignal is where a provider states the terms; the other two state the surface.
image: /images/common.png
url: '#'
machineReadable: true
source: well-known
tags:
  - Consent
  - AI
  - Content Policy
yaml_example: |
  - type: ContentSignal
    url: https://example.com/robots.txt
---
