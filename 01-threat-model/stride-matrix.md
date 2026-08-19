## STRIDE Matrix

| Identity Type | Spoofing | Tampering | Repudiation | Information Disclosure | Denial of Service | Elevation of Privilege |
|---|---|---|---|---|---|---|
| **Human User** | Stolen credentials used to impersonate user | Session/token manipulation | Missing login and authentication audit logs | Access/ID token or personal data leaked | Brute-force or credential-stuffing attacks | User obtains a higher role without authorization |
| **AI Agent** | Stolen agent token used to impersonate agent | Prompt injection or manipulated agent instructions | Agent actions not properly logged | Agent exposes sensitive prompts, data, or context | Excessive agent requests consume resources | Agent gains access to unauthorized tools or models |
| **OAuth M2M Client** | Stolen client secret/token reused by attacker | Modified API request payload or claims | M2M API calls not properly logged | Client exposes sensitive internal API data | Excessive API requests without rate limiting | Client receives broader OAuth scopes than required |
| **LLM API Key** | Stolen API key used by unauthorized party | Altered API requests or key configuration | API-key usage not properly attributed | API key, prompts, PII, or context leaked | Token abuse causes cost or resource exhaustion | API key gains access to unauthorized models/projects |
| **RAG Pipeline Service Identity** | Spoofed service identity queries vector database | Poisoned or manipulated documents/embeddings | Missing audit trail for ingestion and updates | Sensitive documents retrieved by unauthorized queries | Vector DB query or ingestion flooding | Read-only identity escalated to write/delete access |
| **MCP Server Identity** | Forged or stolen MCP server/service token | Malicious tool parameters or API payloads | Tool invocations not properly logged | MCP tool responses expose internal data | MCP server flooded with tool requests | MCP identity invokes admin/restricted tools |

## STRIDE Categories

- **Spoofing** — attacker impersonates an identity.
- **Tampering** — attacker modifies data or requests.
- **Repudiation** — actions cannot be reliably attributed to an identity.
- **Information Disclosure** — sensitive information is exposed.
- **Denial of Service** — a service or identity flow is made unavailable.
- **Elevation of Privilege** — an identity gains permissions beyond those intended.
