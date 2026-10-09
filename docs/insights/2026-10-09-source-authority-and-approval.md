# Rank source authority and visual approval are separate
Date: 2026-10-09
Project: Imperial Republic ranks
Tags: ranks, canon, source-provenance, approvals, anchors, canon-service

## Context

Research the official rank chart/spreadsheet and external plaque references before establishing an Imperial Republic visual standard and canonical records.

## What we tried

1. Compared supplied HTML exports, archived TXT and local Nexus captures.
2. Inspected published Nexus plus bounded live Google Sheets cells with strikeout formatting.
3. Viewed all supplied images and decoded the saved Combine page's embedded plaques.
4. Traced current music anchor records/publication and canon-service ingestion/type support.

## What happened

The sources disagree, but the Navy/Marine/Army ladders agree from HC-4 to E-1 after retaining explicit spelling variants. Live General includes columns/rows missing from its saved HTML. Grand Vizier is struck out in live detailed sheets; plain text would incorrectly make it look active.

The current anchor system is per-file Markdown, with registry.json generated. Canon-service is files-authoritative/PostgreSQL-cache but current write defaults can mark records canonical and published without a visual approval workflow. Rank/uniform types are absent.

## Root cause / why

The supplied materials represent different revisions and purposes, including payroll, combined schemes and branch charts. Format conversion can discard source semantics. Publication flags describe serving behavior; they do not prove editorial approval. The assumption that a table labeled official or a document labeled approved settles every visual/grade conflict is false.

## Takeaway

Preserve source assertions and formatting, use the military intersection for initial design, and record hierarchy, visual-pattern assignment and publication approvals separately. Keep candidate material outside canonical watched content until explicit promotion and type/gate support exist.

## References

- ../MILITARY-BASELINE.md
- ../DISCOVERY.md
- ../INTEGRATION.md
- ../research/google-sheets-live-2026-10-09.json
- D:\eotir\projects\music\docs\ANCHOR-CONTRIBUTOR-GUIDE.md
- D:\eotir\projects\codex-monarch\canon-service\src\schemas.ts
- D:\eotir\projects\codex-monarch\sync-worker\src\sync-entities.ts

## Public review is a separate authorization

Ryan explicitly authorized public GitHub repository visibility and static Pages hosting after the private draft delivery. This permits candidate exposure while leaving visual/assignment approvals and canon-service published/canonical flags unchanged. Preserve historical receipts with their original scope and add a new deployment receipt; do not rewrite a private-checkpoint receipt to imply it always represented a public site. Excluded historical exports must remain outside Git history.
