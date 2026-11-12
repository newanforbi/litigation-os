# Private documents (auth-only)

Owner denylist of 14 paths. Bytes here must never be copied to
`documents/` or `internal/public/`. The Worker serves them only to a
caller with a valid `read` or `write` token; everyone else gets 404.

List: `internal/src/data/documents/private-documents.json`.

`doj-uvisa-filexchange-2026-11/` is private DOJ FileXchange production (no public projection).

The twelve HOPE_000 discovery productions also exist as three disagreeing
byte sequences (D1 hash, manifest hash, repo-root Bates copies). This
folder keeps the copies that are in git; D1/manifest versions stay in R2
under their own hashes. Do not collapse them.
