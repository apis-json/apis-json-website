---
name: Prompts
description: A prompts collection references reusable AI prompts that help humans and agents work with an API — onboarding prompts, task prompts, and prompt templates that encode how to accomplish common jobs against the API. Publishing prompts alongside the index makes an API's agentic surface discoverable, so AI tooling can find vetted, provider-blessed prompts rather than guessing. Entries use a type of Prompt, AgentPrompt, or PromptTemplate, and may apply at the top level (across all APIs) or to an individual API.
image: /images/documentation.png
url: #
machineReadable: true
source: ai
tags:
  - Prompts
  - AI
  - Agents
  - Spotlight
yaml_example: |
  prompts:
    - type: AgentPrompt
      url: https://developers.example.com/prompts/getting-started.md
      mediaType: text/markdown
---
