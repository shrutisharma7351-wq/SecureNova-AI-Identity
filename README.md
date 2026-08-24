# SecureNova AI Identity Security

## Overview

SecureNova is an AI identity security capstone project focused on securing human and machine identities in an AI-powered application.

The project demonstrates an end-to-end security lifecycle covering threat modelling, Auth0-based identity and access management, AI identity attacks, security guardrails, detection, hardening, policy, and compliance.

## Project Areas

### 01 - Threat Model

Threat modelling of the SecureNova AI identity system, including identity enumeration, authentication and privilege analysis, STRIDE analysis, data-flow and trust-boundary identification, attack trees, risk scoring, and MITRE ATLAS mapping.

### 02 - IAM Design

Auth0-backed authentication and authorization including OAuth 2.0, PKCE, RBAC, MFA, M2M authentication, JWT validation, Auth0 Actions, SSO, and credential rotation.

### 03 - Red Team

Controlled simulations of AI identity attacks including indirect prompt injection, agent identity spoofing, system prompt extraction, and RAG poisoning/MCP abuse.

Each attack was documented with evidence, risk assessment, CVSS scoring, and relevant MITRE ATLAS/OWASP mappings.

### 04 - Blue Team

Security controls for detecting and mitigating AI identity attacks, including AI guardrails, cryptographic agent identity binding, Auth0 hardening, anomaly detection, credential protection, and attack prevention.

Project 3 attacks were replayed against the hardened application to evaluate control effectiveness.

### 05 - Policy

AI Identity Security Policy covering identity lifecycle, credential governance, and incident response.

This section also includes NIST AI RMF compliance mapping, OWASP LLM Top 10 mapping, risk analysis, and prioritized security recommendations.

## Security Objective

The objective is to demonstrate an end-to-end AI identity security lifecycle:

**Threat Model → IAM → Red Team → Blue Team → Compliance**

The project connects security architecture, offensive testing, defensive controls, and governance into a single AI identity security workflow.

## Repository Structure

```text
SecureNova-AI-Identity/
├── 01-threat-model/
├── 02-iam-design/
├── 03-red-team/
├── 04-blue-team/
└── 05-policy/
