# mock_servers/

Local development stubs for all three Swiggy MCP endpoints. These run as independent FastMCP servers so the local topology mirrors production exactly.

> **Note:** All restaurant names, product names, prices, ratings, and order data returned by these servers are **AI-generated mock data** for testing purposes only. They do not represent real Swiggy listings or actual market prices.

---

## Servers & Ports

| Server | Port | SSE Endpoint | Tools |
|--------|------|--------------|-------|
| Food | 8001 | `http://localhost:8001/sse` | 14 |
| Instamart | 8002 | `http://localhost:8002/sse` | 13 |
| Dineout | 8003 | `http://localhost:8003/sse` | 8 |

---

## Starting the servers

```bash
uv run python mock_servers/main.py
```

This spawns all three as separate processes. You should see:

```
Starting Swiggy Mock MCP Servers...
  Food      → http://localhost:8001/sse
  Instamart → http://localhost:8002/sse
  Dineout   → http://localhost:8003/sse
```

You can also run them individually if you only need one:

```bash
uv run python -c "import uvicorn; from mock_servers.food_server import food; uvicorn.run(food.sse_app(), port=8001)"
```

---

## Response envelope

Every tool returns the same Swiggy-standard shape:

```json
// success
{ "success": true, "data": { ... }, "message": "Human-readable message" }

// error
{ "success": false, "error": { "message": "What went wrong" } }
```

---

## Fault injection

`place_food_order`, `checkout`, and `book_table` each have a ~20% chance of raising a simulated `UPSTREAM_ERROR: Simulated transient 503`. This is intentional — it lets you watch the ADK `ReflectRetryToolPlugin` recover from transient failures in your demo video without needing a real outage.

---

## Switching to production

Set two env vars and the ADK agents automatically point at the live Swiggy MCP endpoints:

```bash
export SWIGGY_ENV=production
export SWIGGY_TOKEN=<your_bearer_token>
uv run adk web
```

URL routing is handled centrally in `app/mcp.py` — nothing else needs to change.

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | Boots all 3 servers via `multiprocessing` |
| `food_server.py` | Food MCP stub — Discover, Cart, Order, Track, Support |
| `instamart_server.py` | Instamart MCP stub — Discover, Cart, Order, Track, Support |
| `dineout_server.py` | Dineout MCP stub — Find, Reserve, Manage, Support |
