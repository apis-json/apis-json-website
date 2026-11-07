---
name: MCPServerCard
description: 'An MCPServerCard property points to a machine-readable card describing a Model Context Protocol server: its endpoint, transport and capabilities, so an agent can connect without reading documentation. Registered in 0.25. Use MCPServer for the server itself and MCPServerCard for its description.'
image: /images/common.png
url: '#'
machineReadable: true
source: ai
tags:
- AI
- Agents
- MCP
yaml_example: |
  - type: MCPServerCard
    url: https://example.com/mcp/server-card.json
---
