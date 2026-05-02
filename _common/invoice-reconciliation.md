---
name: Invoice Reconciliation
description: "An InvoiceReconciliation property references documentation that explains how an API provider's billing data maps to issued invoices — including how to match billing export rows to invoice line items using invoice identifiers. FOCUS 1.2 introduced dedicated Invoice ID columns specifically to enable this reconciliation. For enterprise API consumers, the ability to tie API usage records to financial invoices is a compliance and audit requirement. Linking reconciliation documentation from an APIs.json index makes this mapping discoverable alongside the API itself."
image: /images/pricing.png
url: #
machineReadable: false
source: financial
tags:
  - Invoice
  - FinOps
  - Billing
  - Reconciliation
yaml_example: |
  - type: InvoiceReconciliation
    url: https://developers.example.com/billing/reconciliation
---
