# 03 - Red Team

## Overview

This folder contains controlled red-team attacks used to test the security of the SecureNova AI Identity Security project.

## Attack Scenarios

- Indirect Prompt Injection
- Agent Identity Spoofing
- System Prompt Extraction
- RAG Poisoning and MCP Abuse

## Structure

```text
03-red-team/
├── attacks/
│   ├── attack1_indirect_injection.py
│   ├── attack2_agent_spoofing.py
│   ├── attack3_prompt_extraction.py
│   └── attack4_rag_mcp_poisoning.py
├── docs/
├── llm.py
├── mcp_tool.py
├── rag_retriever.py
└── simulated_agent.py
