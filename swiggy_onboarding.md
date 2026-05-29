# Swiggy MCP — Developer Onboarding

Swiggy MCP is invite-only for external builders. This document covers what you need to apply, what to register, and what Swiggy reviews before granting production access.

---

## Access Flow

1. Build a working end-to-end experience using the local mock servers in this repo
2. Record a demo video (Loom or YouTube unlisted) showing the full flow
3. Fill in the application at [mcp.swiggy.com/builders/access](https://mcp.swiggy.com/builders/access/)
4. Email the demo link to [builders@swiggy.in](mailto:builders@swiggy.in)

---

## What Swiggy Reviews

They look for:

- A real, concrete use case with identifiable end-users
- Proper error handling — 401 (expired token), 429 (rate limit), 5xx (retry with idempotency check)
- Consumer-safe behaviour — no orders placed without user confirmation, no raw IDs exposed
- Alignment with Swiggy's experience guidelines (restaurant-card widgets, correct confirmation copy)

---

## Application Form Fields

### MCP Servers to request

Tick all three:

- `food`
- `instamart`
- `dineout`

### Redirect URI(s) for auth flows

Register these URIs in the form. They are used if Swiggy implements a browser-based OAuth callback — you don't need to build a server for them, just register them so the OAuth flow is allowed to redirect there.

```
http://localhost
http://localhost/callback
http://127.0.0.1
http://127.0.0.1/callback
```

> You **do not** need to implement a redirect URI handler for the local dev or mock phase. If Swiggy's production onboarding requires a full OAuth browser flow, you will be given instructions at that point. For now, listing the URIs above is sufficient.

---

## Production Credentials

Once approved, you receive a bearer token. Set it as an env var before starting `adk web`:

```bash
# Windows PowerShell
$env:SWIGGY_ENV = "production"
$env:SWIGGY_TOKEN = "your_bearer_token_here"

# macOS / Linux
export SWIGGY_ENV=production
export SWIGGY_TOKEN=your_bearer_token_here
```

`tools/mcp.py` reads these and automatically switches all three MCP connections from the local stubs to the live endpoints.

---

## Production MCP Endpoints

| Server | Endpoint | Auth |
|--------|----------|------|
| Food | `https://mcp.swiggy.com/food` | `Bearer <token>` |
| Instamart | `https://mcp.swiggy.com/im` | `Bearer <token>` |
| Dineout | `https://mcp.swiggy.com/dineout` | `Bearer <token>` |

Full API reference: [mcp.swiggy.com/builders/docs/reference](https://mcp.swiggy.com/builders/docs/reference/)
