---
name: FinOps
description: A FinOps property references a provider's financial-operations artifact for an API — the document or dataset describing how the API's consumption is metered, allocated, and billed so consumers can reason about cost. It complements Plans, Pricing, and RateLimits by pointing to the operational FinOps surface (cost allocation, unit economics, billing exports). This is the most widely-used type in the wild that was not previously reserved, and is distinct from FinOpsFramework, which references a provider's alignment to the FinOps Foundation framework.
image: /images/documentation.png
url: #
machineReadable: true
source: financial
tags:
  - FinOps
  - Cost
  - Billing
  - Metering
yaml_example: |
  - type: FinOps
    url: https://developers.example.com/finops/example-finops.yml
    mediaType: application/yaml
---
