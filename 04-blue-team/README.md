# 04 - Blue Team

## Overview

This folder contains defensive security controls developed to detect and mitigate attacks identified during the Red Team phase.

## Components

### Anomaly Detection

Detects and analyses suspicious or abnormal agent activity.

- `anomaly_monitor.py`
- `replay_project3_attacks.py`

### Cryptographic Identity

Provides cryptographic identity verification for AI agents.

- `agent_identity.py`
- `agent_public_key.pem`

### Guardrails

Implements security rules and controls for agent actions.

- `guardrail_runner.py`
- `config/actions.py`
- `config/config.yml`

### Auth0 Security

- `auth0_rotation_test.py` — Tests credential rotation.

## Structure

```text
04-blue-team/
├── anomaly-detection/
│   ├── anomaly_monitor.py
│   └── replay_project3_attacks.py
├── crypto_identity/
│   ├── agent_identity.py
│   └── agent_public_key.pem
├── guardrails/
│   ├── config/
│   │   ├── actions.py
│   │   └── config.yml
│   └── guardrail_runner.py
└── auth0_rotation_test.py
