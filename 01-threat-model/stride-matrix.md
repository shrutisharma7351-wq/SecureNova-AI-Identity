# STRIDE Threat Matrix

| Identity / Flow | Spoofing | Tampering | Repudiation | Information Disclosure | Denial of Service | Elevation of Privilege |
|---|---|---|---|---|---|---|
| Human User → Auth0 | Stolen credentials or session | Modified authentication request | User denies login activity | User/session data exposed | Login flooding | User escalates to admin |
| AI Agent → API | Agent token stolen | Agent request modified | Agent action cannot be traced | Agent receives unauthorized data | Agent API flooding | Agent obtains higher API scope |
| M2M Client → API | Client secret stolen | API request modified | Service action not logged | API response exposes sensitive data | Excessive service requests | Client obtains unauthorized scope |
| LLM API Key → LLM Provider | API key stolen | Prompt/request modified | LLM request cannot be attributed | Sensitive prompt/data exposed | Excessive API calls | Key gains excessive model permissions |
| RAG Service → Knowledge Base | Service token stolen | RAG data/chunks modified | Retrieval activity not logged | Restricted knowledge exposed | Retrieval service overloaded | Service gains write/admin access |
| MCP Server → Tools | MCP credential stolen | Tool request modified | Tool execution not logged | Tool exposes sensitive information | Excessive tool calls | Agent gains unauthorized tool privileges |

## STRIDE Categories

- **Spoofing** — attacker impersonates an identity.
- **Tampering** — attacker modifies data or requests.
- **Repudiation** — actions cannot be reliably attributed to an identity.
- **Information Disclosure** — sensitive information is exposed.
- **Denial of Service** — a service or identity flow is made unavailable.
- **Elevation of Privilege** — an identity gains permissions beyond those intended.
