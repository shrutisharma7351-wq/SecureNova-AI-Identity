# Identity Inventory

| Identity Type | Authentication Mechanism | Privilege Level |
|---|---|---|
| Human User | Auth0 OIDC / OAuth 2.0 Authorization Code + PKCE + MFA | User-level; admin privileges only if assigned an admin role |
| AI Agent | OAuth 2.0 Client Credentials / M2M access token | Agent-level; limited to explicitly assigned API scopes |
| OAuth M2M Client | OAuth 2.0 Client Credentials using client ID + client secret | Service-level; limited to assigned API scopes |
| LLM API Key | Provider-issued API key / bearer-style credential | Restricted access to approved LLM operations |
| RAG Pipeline Service Identity | OAuth 2.0 service/M2M access token | Service-level; read access to approved RAG/knowledge-base resources |
| MCP Server Identity | Service authentication credential such as OAuth access token or API key | Tool-specific privileged service access; limited to approved MCP operations |

