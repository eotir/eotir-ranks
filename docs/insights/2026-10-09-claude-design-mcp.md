# Claude Design MCP connection test in Codex
Date: 2026-10-09
Project: Imperial Republic ranks
Tags: claude-design, mcp, oauth, codex, handoff

## Context
Ryan requested a connectivity test for future assistance with Claude Design project b4d2bcdf-bd54-4918-b9a4-29d2b0899b6c. This did not request importing or editing that project. Credential rotation was explicitly excluded by Ryan.

## What we tried
1. Checked exposed Codex tools and filtered local MCP configuration: no existing claude_design connection.
2. Probed https://api.anthropic.com/v1/design/mcp without credentials. GET returned 405; a JSON-RPC initialize POST returned 401 with OAuth resource discovery.
3. Read public protected-resource metadata. Resource is that MCP URL; authorization server is https://claude.ai/v1/design/mcp; advertised scopes are user:design:read and user:design:write.
4. Registered claude_design through codex mcp add, then tested codex mcp login claude_design --scopes user:design:read using codex-cli 0.162.0.
5. Probed public authorization metadata URLs separately; claude.ai requests returned 403 and the alternate api.anthropic.com metadata path returned 404.
6. Disabled only the new test entry in C:/Users/ryanm/.codex/config.toml; preserved all other bytes and validated TOML.

## What happened
Server registration succeeded. Native OAuth login failed before browser authorization with: OAuth authorization server issuer does not match authorization metadata origin. No successful authentication, callable Claude Design tools or project access was established. The configured URL remains saved with enabled=false.

## Root cause / why
The observed blocker is Codex's authorization metadata issuer/origin validation. Separate discovery probes could not retrieve the claude.ai metadata, so the precise server/client compatibility defect is unresolved. Endpoint reachability and standard-looking discovery are not proof of successful OAuth or usable project tools. Do not bypass issuer validation or assume /design-login is a Codex command.

## Takeaway
Current Codex native connection is unverified and blocked at OAuth discovery; use the supplied local design exports for now. Retest after a documented compatible authentication route or server/client fix is available, distinguishing registration, login, tools/list and actual project access.

## References
- https://claude.ai/design/p/b4d2bcdf-bd54-4918-b9a4-29d2b0899b6c
- https://api.anthropic.com/v1/design/.well-known/oauth-protected-resource
- ../CLAUDE-CODE-HANDOFF.md
