-- Purpose: proposed local review-cache projection, not an authoritative canon DB.
-- Usage: review this example; do not execute against live D1 as part of this goal.
-- Prerequisites: approved schema/ownership plan before any real migration.
CREATE TABLE rank_candidate_projection (
  id TEXT PRIMARY KEY,
  branch_id TEXT,
  grade TEXT NOT NULL,
  raw_title TEXT NOT NULL,
  pattern_id TEXT,
  record_json TEXT NOT NULL CHECK (json_valid(record_json)),
  source_hash TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'CANDIDATE' CHECK (status = 'CANDIDATE'),
  canonical INTEGER NOT NULL DEFAULT 0 CHECK (canonical = 0),
  published INTEGER NOT NULL DEFAULT 0 CHECK (published = 0)
);

-- Production promotion needs a separate approved authoritative workflow and
-- coordinated canon-service/worker/UI type support, not a flag flip here.
