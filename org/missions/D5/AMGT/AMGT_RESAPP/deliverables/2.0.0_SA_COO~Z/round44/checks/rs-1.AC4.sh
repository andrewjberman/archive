#!/usr/bin/env bash
# AMGT_RESAPP round 44, AMGT-rs-1 AC4 -- JUDGMENT, RECORDED, NO VERDICT: the rebuilt export's Model Cases section for a London name
# (RKT, price in GBp), a US name (AMD) and a name added this week (GOOGL), for a person to judge beside the Model tab whether each
# served value now reads as a price in a named currency. usage: bash <this>   (after rs-1.AC1.py has run once)
set -u
for k in RKT_LN_Equity AMD_US_Equity GOOGL_US_Equity; do
  f="C:/tmp/amgt-r43-live95/$k/rs1.local.rich.md"
  echo "=================== $k"
  [ -f "$f" ] || { echo "no rebuilt export for $k -- run rs-1.AC1.py first"; continue; }
  awk '/^## Model Cases/{p=1} /^## /&&!/^## Model Cases/{p=0} p' "$f"
done
