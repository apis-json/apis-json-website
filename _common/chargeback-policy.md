---
name: Chargeback Policy
description: "A ChargebackPolicy property references a document that describes how an API provider or internal platform allocates and recovers costs across teams, cost centers, or business units — including both chargeback (actual cost transfer) and showback (visibility without transfer) methodologies. Chargeback and invoicing are formal capabilities in the FinOps Framework. Publishing a chargeback policy alongside an API makes internal billing transparency discoverable, which is especially important for platform APIs used across multiple organizational units."
image: /images/pricing.png
url: #
machineReadable: false
source: financial
tags:
  - Chargeback
  - FinOps
  - Cost Allocation
  - Showback
yaml_example: |
  - type: ChargebackPolicy
    url: https://developers.example.com/billing/chargeback
---
