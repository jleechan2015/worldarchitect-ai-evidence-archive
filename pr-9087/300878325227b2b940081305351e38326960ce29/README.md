# PR #9087 Exact-Head Browser Evidence

- Tested commit: `300878325227b2b940081305351e38326960ce29`
- Run ID: `pr9087-live-browser-fd4207a986744889ba9a537b5b0ec404`
- Evidence layer: Layer 2 real browser against a real local Gunicorn server
- Result: 4 of 4 required cache-control/browser scenarios passed

Start with `evidence.md` for the claim map, `methodology.md` for execution and
acceptance criteria, `run.json` for scenario receipts, `metadata.json` for exact
Git/server provenance, and `artifacts/` for the raw HTTP, process, screenshot,
caption, and media evidence. `verification_report.json` and its publication
alias `report.json` record the aggregate verdict; `claim_map.json` is the
machine-readable claim-to-artifact ledger. Verify every substantive file with
its sibling `.sha256`, then verify
the complete package with `checksums.sha256`.

This package is sanitized for public review: it contains no credential values,
credential paths, primary-account identifiers, or non-local hostnames.

The raw browser WebM files are retained under `artifacts/video_*`. Fixed-name
`desktop-captioned` and `mobile-captioned` MP4/GIF/VTT/SRT artifacts are
publication derivatives from those same-run sources; no browser scenario was
rerun during media packaging.
