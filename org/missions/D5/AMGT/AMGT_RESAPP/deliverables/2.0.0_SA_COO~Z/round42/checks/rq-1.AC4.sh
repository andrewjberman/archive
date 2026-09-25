#!/usr/bin/env bash
# AMGT_RESAPP round 42, AMGT-rq-1 AC4 -- JUDGMENT, RECORDED, NO VERDICT: the rebuilt export's Company Description, Investment
# Thesis, Exec Management and Posture sections and its fiscal-year headings, for three names that span the round-41 classes
# (ASML the 16-absence signature, NOVN the figure extras, 9433 JP the figure drop), printed for a person to read beside the
# page's own words. usage: bash <this>   (from the repo root, after rq-1.AC1.sh has run once)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
for k in ASML_NA_Equity NOVN_SW_Equity 9433_JP_Equity; do
  f="C:/tmp/amgt-r42-cache2/$k/local.rich.md"
  echo "=================== $k ($f)"
  [ -f "$f" ] || { echo "no rebuilt export for $k -- run rq-1.AC1.sh first"; continue; }
  awk '/^## (Company Description|Investment Thesis|Risks|Recommendation|Exec|Management|Posture)/{p=1} /^## Fiscal year/{print; next} /^## /&&!/^## (Company Description|Investment Thesis|Risks|Recommendation|Exec|Management|Posture)/{p=0} p' "$f" | head -60
done
