# 01 - Threat Model

## Overview

This folder contains the threat modelling artefacts for the SecureNova AI Identity Security project.

The purpose of this phase is to identify identity-related assets, trust boundaries, attack surfaces, threats, and security risks before implementing authentication, authorization, detection, and defensive controls.

The threat model establishes the security foundation for the remaining project phases.

## Objectives

The threat modelling phase focuses on:

- Identifying human and machine identity assets
- Understanding authentication and authorization trust relationships
- Identifying identity-related attack surfaces
- Analysing threats using structured security methodologies
- Prioritising risks based on likelihood and impact
- Establishing security requirements for later implementation phases
- Providing traceability between identified threats and implemented controls

## Artefacts

| Artefact | Description |
|---|---|
| `identity-inventory.md` | Inventory of identities, identity attributes, credentials, tokens, services, and other identity-related assets |
| `stride-matrix.md` | STRIDE-based threat analysis covering potential threats to the SecureNova identity architecture |
| `threat-model.json`| Threat Dragon threat model defining SecureNova AI identity types, data flows, trust boundaries, and key security threats. |
| `AT-1-key-exfiltration.drawio`| Attack tree modelling potential paths an attacker could use to obtain or exfiltrate sensitive cryptographic keys. |
| `AT-2-scope-escalation.drawio`| Attack tree modelling potential paths for escalating identity, token, or authorization scope beyond intended permissions |
| `AT-3-rag-poisoning.drawio`| Attack tree modelling potential paths for poisoning RAG data and influencing AI agent responses or behaviour. |


## Threat Modelling Approach

The analysis considers the SecureNova environment from an identity-security perspective, including:

- Human identities
- AI agents and machine identities
- Authentication mechanisms
- Authorization and permissions
- Access tokens and credentials
- APIs and service-to-service communication
- AI agent interactions
- Trust boundaries
- Security-sensitive operations

Threats are evaluated to support prioritisation and subsequent defensive implementation.

