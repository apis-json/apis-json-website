---
name: FOCUS Contract Commitments
description: "A FocusContractCommitments property references an endpoint or document for commitment-based pricing data structured according to the FOCUS Contract Commitment Dataset, introduced in FOCUS v1.3. This supplemental dataset isolates reserved instance, savings plan, and enterprise discount program terms — including commitment start and end dates, remaining committed units, and commitment type — from per-row cost and usage data. It enables FinOps tooling to reconcile commitment purchases against actual consumption without parsing billing rows."
image: /images/pricing.png
url: #
machineReadable: true
source: financial
tags:
  - FOCUS
  - FinOps
  - Commitments
  - Reserved Instances
yaml_example: |
  - type: FocusContractCommitments
    url: https://developers.example.com/billing/commitments
    mediaType: application/json
---
