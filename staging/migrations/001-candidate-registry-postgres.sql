-- Purpose: proposed disposable review-cache projection, not monarch type DDL.
-- Usage: review only; no production execution authorized by the current goal.
-- Prerequisites: coordinated type/approval/ownership plan before deployment.
CREATE TABLE rank_candidate_projection (
  id text PRIMARY KEY,
  branch_id text,
  grade text NOT NULL,
  raw_title text NOT NULL,
  pattern_id text,
  record jsonb NOT NULL,
  source_hash text NOT NULL,
  status text NOT NULL DEFAULT 'CANDIDATE' CHECK (status = 'CANDIDATE'),
  canonical boolean NOT NULL DEFAULT false CHECK (canonical = false),
  published boolean NOT NULL DEFAULT false CHECK (published = false)
);

-- Extend rank/uniform enum values, ledger CHECKs, maps, validation, clients,
-- worker instances and the editorial serving gate together in a later change.
