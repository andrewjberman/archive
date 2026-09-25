#!/usr/bin/env bash
# AMGT_RESAPP round 43, AMGT-rr-2 AC4 -- JUDGMENT, RECORDED, NO VERDICT: the rebuilt export's Model Cases section for three names
# spanning the case states (RKT base SERVED, ULVR base ABSENT currency_mismatch, BA base ABSENT forward_eps_not_positive), printed
# for a person to read beside the Model tab's own case block. usage: bash <this>  (after rr-2.AC1.sh has run once)
set -u
for k in RKT_LN_Equity ULVR_LN_Equity BA_US_Equity; do
  f="C:/tmp/amgt-r43-cache/$k/local.rich.md"
  echo "=================== $k"
  [ -f "$f" ] || { echo "no rebuilt export for $k -- run rr-2.AC1.sh first"; continue; }
  awk '/^## Model Cases/{p=1} /^## /&&!/^## Model Cases/{p=0} p' "$f"
done
