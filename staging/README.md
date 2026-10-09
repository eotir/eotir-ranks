# Future canonical transfer examples

These files are review examples outside the watched codex-monarch content tree. They are not deployed migrations, adopted frontmatter contracts, uniform regulations, or approved rank definitions.

Destination after approval and coordinated type support: codex-monarch/content/ranks and content/uniforms. Keep rank records flat or self-named as described in [the integration plan](../docs/INTEGRATION.md); arbitrary branch subfolders are excluded by the current worker.

The sample schemas deliberately distinguish hierarchy decisions, design/asset approval, assignment approval and publication. The existing canon-service defaults/worker can publish records regardless of approval metadata, so flags shown here cannot be treated as a serving gate without implementation changes.

- canon/ranks/navy-ensign.example.md: proposed human-readable Markdown/frontmatter record, not a file to copy straight into production.
- canon/uniforms/navy-service.example.md: empty regulation template with unresolved placement, not invented lore.
- schemas/rank-candidate.schema.json: draft interchange schema.
- migrations/001-candidate-registry-d1.sql and 001-candidate-registry-postgres.sql: local review-cache examples, not monarch's authoritative type migration.

The SQLite example was syntax/execution checked only in an in-memory local database. No production migration, PostgreSQL execution or canonical ingestion has been run. Do not create a second editable canon authority from these projections.
