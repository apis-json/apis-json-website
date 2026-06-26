---
name: Workflows
description: A workflows collection references multi-step API workflows — most commonly OpenAPI Arazzo descriptions, but also ServerlessWorkflow or other workflow definitions — that chain individual API calls into complete jobs-to-be-done. Where OpenAPI describes the operations, a workflow describes the sequence — authenticate, create, poll, then act. Publishing workflows makes an API's real usage patterns discoverable and executable by tooling and agents. Entries use a type of Arazzo, ServerlessWorkflow, or Workflow, and may apply at the top level (across all APIs) or to an individual API.
image: /images/schema.png
url: #
machineReadable: true
source: contracts
tags:
  - Workflows
  - Arazzo
  - Orchestration
  - Agents
yaml_example: |
  workflows:
    - type: Arazzo
      url: https://developers.example.com/workflows/create-and-charge.yml
      mediaType: application/yaml
---
