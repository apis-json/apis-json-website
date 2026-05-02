---
name: Vocabulary
description: A Vocabulary property references a published data model or semantic vocabulary that defines the terms, types, and relationships used in the API. This can be a JSON-LD context, an OWL ontology, or a plain-language glossary. Publishing a vocabulary makes API semantics explicit and machine-interpretable, which is increasingly important for AI agents that need to reason about what an API's data means.
image: /images/schema.png
url: #
machineReadable: true
source: technical
tags:
  - Vocabulary
  - Semantics
  - Data Model
yaml_example: |
  - type: Vocabulary
    url: https://developers.example.com/vocabulary.jsonld
    mediaType: application/ld+json
---
