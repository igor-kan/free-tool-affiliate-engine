# free-tool-affiliate-engine

Build affiliate-ready comparison pages for free tools and software reviews.

## What it does
- Ingests tool inventory from YAML
- Generates disclosure-first comparison page HTML
- Exports affiliate-ready CSV for tracking and distribution

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/build_engine.py --config examples/tools.yaml --out out
```

## Outputs
- `out/index.html`
- `out/affiliate_export.csv`

## Compliance notes
- Keep affiliate disclosures clear and prominent.
- Validate platform terms before automated publishing.
