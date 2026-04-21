---
layout: post
title: 'Indexing Spec-Driven Integrations: When the Spec Is the Integration'
image: /assets/images/sdi-indexing-spec-driven-integrations.png
---
APIs.json indexes APIs. The format provides a machine-readable declaration of what APIs exist, where their documentation lives, and how to access them. It solves the discovery problem at the API layer.

[Spec-Driven Integration](https://github.com/naftiko/framework/wiki/Spec%E2%80%90Driven-Integration) introduces a new indexable artifact: the capability spec. A capability spec declares what an integration consumes from upstream APIs and what it exposes to downstream consumers. When the spec is the integration — executable, not just descriptive — then indexing it means indexing a running integration surface.

## What Changes for APIs.json

An APIs.json index for SDI capabilities points to artifacts that are both documentation and implementation:

```json
{
  "name": "Payment Processing Capabilities",
  "apis": [
    {
      "name": "Transaction Discovery",
      "description": "Search and retrieve payment transactions shaped for AI analytics workflows.",
      "properties": [
        { "type": "Naftiko", "url": "capabilities/transaction-discovery.yaml" },
        { "type": "MCP", "url": "http://localhost:3001" }
      ]
    }
  ]
}
```

The `Naftiko` property type points to the capability spec — the executable artifact. The `MCP` property points to the live tool endpoint. Discovery and execution are connected in a single index entry.

## The SDI Discovery Pipeline

With Spec-Driven Integration, the discovery pipeline becomes:

1. **APIs.json index** points to capability specs
2. **Capability specs** declare what they consume and expose
3. **AI agents** read the specs to discover available tools
4. **The engine** serves the specs as live MCP tools and REST endpoints

The index tells you where capabilities live. The specs tell you what they do. The engine makes them callable. End-to-end machine-readable discovery, from index to execution.

This is the natural evolution of APIs.json: indexing not just APIs but the governed integration layer built on top of them.

[Read the SDI methodology](https://github.com/naftiko/framework/wiki/Spec%E2%80%90Driven-Integration) | [Explore the Naftiko Fleet](https://github.com/naftiko/fleet?utm_source=apis-json&utm_medium=blog&utm_campaign=methodology-spec-driven-integration&utm_content=sdi-indexing-apis-json)
