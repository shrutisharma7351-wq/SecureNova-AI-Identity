# 02 - IAM Design

## Overview

This folder contains the Identity and Access Management (IAM) implementation for the SecureNova AI Identity Security project using Auth0.

## Features

- OAuth 2.0 authentication
- PKCE authentication flow
- Multi-Factor Authentication (MFA)
- Single Sign-On (SSO)
- JWT-based authentication
- Credential rotation
- Secure session handling

## Structure

```text
02-iam-design/
└── auth0-implementation/
    └── web-app/
        ├── .env.example
        ├── .gitignore
        ├── credential_rotation.py
        ├── package-lock.json
        ├── package.json
        ├── server.js
        └── sso-client.js
