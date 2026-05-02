---
name: Spectral Rules
description: A SpectralRules property references the Spectral ruleset file that governs how the API's OpenAPI or AsyncAPI spec is validated. Publishing this alongside the spec makes governance rules discoverable and enables consumers to understand the quality standards the API is held to. It also supports meta-governance workflows — checking whether a provider has published their own API design rules.
image: /images/schema.png
url: #
machineReadable: true
source: governance
tags:
  - Spectral
  - Governance
  - Linting
  - Rules
yaml_example: |
  - type: SpectralRules
    url: https://developers.example.com/.spectral.yaml
    mediaType: application/yaml
---
