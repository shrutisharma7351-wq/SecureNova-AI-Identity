# Identity Inventory

| Identity Type | Description | Authentication Mechanism | Privilege Level |
|---|---|---|---|
| Human User | Person interacting with the SecureNova AI application | Auth0 / OIDC | User |
| AI Agent | AI component acting on behalf of the application | OAuth 2.0 M2M access token | Agent |
| OAuth M2M Client | Machine application communicating with protected APIs | OAuth 2.0 Client Credentials | Service |
| LLM API Key | Credential used to access an external LLM provider | API Key | Restricted Service |
| RAG Pipeline Service Identity | Service identity used to retrieve and process knowledge-base content | OAuth 2.0 service token | Service |
| MCP Server Identity | Identity representing an MCP server/tool service | OAuth 2.0 / signed service credentials | Privileged Service |

## Security Principle

All identities follow the principle of least privilege.

Credentials should be short-lived where possible, securely stored, regularly rotated, monitored, and revoked when no longer required.
