---
name: AuthorizationServerMetadata
description: An AuthorizationServerMetadata property points to an OAuth 2.0 Authorization Server Metadata document (RFC 8414), served at /.well-known/oauth-authorization-server. Registered in 0.25. It publishes the endpoints, grant types and scopes a client needs to obtain a token without hard-coding them.
image: /images/security.png
url: '#'
machineReadable: true
source: well-known
tags:
- Authentication
- OAuth
yaml_example: |
  - type: AuthorizationServerMetadata
    url: https://auth.example.com/.well-known/oauth-authorization-server
---
