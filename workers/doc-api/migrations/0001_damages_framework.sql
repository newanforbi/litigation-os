-- 8-case damages framework (v2) — PUBLIC exposure ranges only.
-- low_usd = expected value (approx.), high_usd = working loaded.
-- Never store probabilities, demands, target/settlement ranges, line items,
-- insurance floors, or settlement notes in this table.
-- Mirrors internal/src/data/damagesFramework.js. Idempotent.
--
-- NOT APPLIED. Apply only with explicit approval:
--   cd workers/doc-api && npx wrangler d1 execute litigation-portfolio --remote --file=migrations/0001_damages_framework.sql

CREATE TABLE IF NOT EXISTS damages_framework (
  id            TEXT PRIMARY KEY,
  label         TEXT NOT NULL,
  matter_number INTEGER,            -- portfolio matter the employer maps to
  low_usd       INTEGER,            -- expected value; NULL when not valued
  high_usd      INTEGER,            -- working loaded; NULL when not valued
  valuation     TEXT NOT NULL,      -- range | contingent | none
  status_override TEXT,
  note          TEXT,
  sort          INTEGER NOT NULL
);

INSERT OR REPLACE INTO damages_framework
  (id, label, matter_number, low_usd, high_usd, valuation, status_override, note, sort) VALUES
  ('amazon',     'Amazon',                             29, 216000,  480918, 'range',      NULL,         NULL,                     1),
  ('ups',        'UPS',                                26, 720000, 1108194, 'range',      NULL,         NULL,                     2),
  ('home-depot', 'Home Depot',                         37, 483000, 1072695, 'range',      NULL,         NULL,                     3),
  ('best-buy',   'Best Buy',                           39, 529000, 1510242, 'range',      'Pre-filing', NULL,                     4),
  ('att',        'AT&T',                               36, 111000,  247400, 'range',      NULL,         NULL,                     5),
  ('fedex',      'FedEx',                              25, 236000,  472764, 'range',      NULL,         NULL,                     6),
  ('staples',    'Staples',                            42, NULL,    NULL,   'contingent', NULL,         'Contingent, not valued', 7),
  ('accurate',   'Accurate (background-check vendor)', 29, NULL,    NULL,   'none',       NULL,         'No standalone range',    8);
