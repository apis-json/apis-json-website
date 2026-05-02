---
name: Tagging Policy
description: "A TaggingPolicy property references a document that defines the cost allocation tag taxonomy for an API or platform — including required tag keys such as CostCenter, Environment, Product, and Owner, along with allowed values and compliance requirements. Cost allocation tagging is a foundational FinOps practice, and the FinOps Foundation publishes working group guidance on tagging policy compliance. Publishing a tagging policy alongside an API makes cost attribution requirements discoverable by consumers who need to integrate the API into their own FinOps workflows."
image: /images/security.png
url: #
machineReadable: false
source: governance
tags:
  - Tagging
  - FinOps
  - Cost Allocation
  - Governance
yaml_example: |
  - type: TaggingPolicy
    url: https://developers.example.com/billing/tagging
---
