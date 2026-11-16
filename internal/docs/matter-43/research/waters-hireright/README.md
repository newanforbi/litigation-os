# Waters v. HireRight research corpus

This branch preserves a model-readable authority set for Matter 43 (Hertz/HireRight). The corpus isolates the nonduplicate originals, records provenance, and exposes page-marked text for search, retrieval, citation review, and adversarial analysis.

## Contents

| Source | Document | Text status |
|---|---|---|
| WaterHireRIght650.pdf | ECF 65 — HireRight reply supporting summary judgment | Complete |
| WatersHireRight6020.pdf | ECF 60-20 — HireRight summary-judgment memorandum | Complete |
| WatersRight760.pdf | ECF 76 — order granting HireRight summary judgment | Complete |
| WatersHireRight240.pdf | ECF 24 — Rule 12(c) motion and supporting materials | Complete |
| WatersHireright400.pdf | ECF 40 — order on Rule 12(c) motion | Complete |
| WatersHireRight830.pdf | ECF 83 — Fourth Circuit Rule 42(b) mandate | Complete |
| HireRight South Carolina.pdf | Image-only 10-page source | OCR needed |

## Model workflow

1. Read `SOURCE_MANIFEST.json` for document identity and provenance.
2. Search `text/` for FCRA sections, procedure, causation, damages, willfulness, pardons, public-record sources, and adverse-action proof.
3. Retain `<PARSED TEXT FOR PAGE: n / N>` markers when building pin cites.
4. Verify any quotation against the original PDF before using it in a filing.

Duplicate Library copies carrying a `(1)` suffix were intentionally excluded.
