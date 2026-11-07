---
name: ProtectedResourceMetadata
description: A ProtectedResourceMetadata property points to an OAuth 2.0 Protected Resource Metadata document (RFC 9728), served at /.well-known/oauth-protected-resource. Registered in 0.25. It tells a client, and an agent connecting to an MCP server, which authorization servers and scopes protect the API.
image: /images/security.png
url: '#'
machineReadable: true
source: well-known
tags:
- Authentication
- OAuth
- Agents
yaml_example: |
  - type: ProtectedResourceMetadata
    url: https://api.example.com/.well-known/oauth-protected-resource
---
