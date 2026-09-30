# TSM same-currency anchor: stored sources searched (round 24, CRPS-z-2)

Result: NO anchor. anchor = null. No TWD figure and no TWD/USD rate is stored for TSM US Equity; no rate is invented.

| source | where | objects searched | found |
|---|---|---|---|
| bronze/article | bloomberg/harvest/bronze/article/ | 30 | False |
| bronze/bestdata | bloomberg/harvest/bronze/bestdata/ | 261 | False |
| bronze/exec_officers | bloomberg/harvest/bronze/exec_officers/ | 4 | False |
| bronze/histdata | bloomberg/harvest/bronze/histdata/ | 303 | False |
| bronze/histdata_daily_px | bloomberg/harvest/bronze/histdata_daily_px/ | 2 | False |
| bronze/identity | bloomberg/harvest/bronze/identity/ | 67 | False |
| bronze/news_listing | bloomberg/harvest/bronze/news_listing/ | 2 | False |
| bronze/refdata | bloomberg/harvest/bronze/refdata/ | 303 | False |
| silver | bloomberg/harvest/silver/ | 34 | False |
| derived/model_block | derived/model_block/ | 769 | False |
| derived/model_block_fye | derived/model_block_fye/ | 3 | False |
| amgt/harvest | amgt/harvest/ | 3151 | False |
| crosswalk/v1 | crosswalk/v1/ | 6 | False |

Detail:

- bronze/article: 30 objects; keys matching TSM|2330|TWD|Curncy: 0
- bronze/bestdata: 261 objects; keys matching TSM|2330|TWD|Curncy: 2; security_key=TSM_US_Equity/20260924T214023Z.json: 1271 bytes, TWD tokens 0; security_key=TSM_US_Equity/20260925T043112Z.json: 2178 bytes, TWD tokens 0 TSM bestdata: 0 TWD tokens.
- bronze/exec_officers: 4 objects; keys matching TSM|2330|TWD|Curncy: 0
- bronze/histdata: 303 objects; keys matching TSM|2330|TWD|Curncy: 2; security_key=TSM_US_Equity/20260924T214023Z.json: 2 bytes, TWD tokens 0; security_key=TSM_US_Equity/20260925T043112Z.json: 7564 bytes, TWD tokens 0 TSM histdata carries price rows only; no Curncy security key exists (0 keys matching Curncy/TWD across the family).
- bronze/histdata_daily_px: 2 objects; keys matching TSM|2330|TWD|Curncy: 0
- bronze/identity: 67 objects; keys matching TSM|2330|TWD|Curncy: 1; security_key=TSM_US_Equity/20260924T211442Z.json: 337 bytes, TWD tokens 0
- bronze/news_listing: 2 objects; keys matching TSM|2330|TWD|Curncy: 0
- bronze/refdata: 303 objects; keys matching TSM|2330|TWD|Curncy: 2; security_key=TSM_US_Equity/20260924T214023Z.json: 73 bytes, TWD tokens 0; security_key=TSM_US_Equity/20260925T043112Z.json: 1339 bytes, TWD tokens 1 TSM refdata 20260925T043112Z carries EQY_FUND_CRNCY TWD (a currency label, no TWD figure) and CRNCY USD with CUR_MKT_CAP 2.3399e12 in the listing currency; no FX field.
- silver: 34 objects; key names matching TSM|2330|TWD|Curncy: 0 []
- derived/model_block: 769 objects; key names matching TSM|2330|TWD|Curncy: 6 ['derived/model_block/TSM_US_Equity/20260924T223202Z/model_block.json', 'derived/model_block/TSM_US_Equity/20260925T044038Z/model_block.json', 'derived/model_block/TSM_US_Equity/20260925T200211Z/model_block.json', 'derived/model_block/TSM_US_Equity/20260926T205908Z/model_block.json', 'derived/model_block/TSM_US_Equity/20260929T024714Z/model_block.json', 'derived/model_block/TSM_US_Equity/20260930T084113Z/model_block.json'] newest TSM model_block (20260930T084113Z) labels CUR_MKT_CAP currency TWD by basis 'reporting (EQY_FUND_CRNCY)' but its value equals the raw listing-currency CUR_MKT_CAP (currencies.converted=false); a derived copy of the same raw, not an independent same-currency figure; not used.
- derived/model_block_fye: 3 objects; key names matching TSM|2330|TWD|Curncy: 0 []
- amgt/harvest: 3151 objects; key names matching TSM|2330|TWD|Curncy: 24 ['amgt/harvest/bronze/research-report-extract/security_key=TSM_US_Equity/a0c07ba2a0bea860/extract.json', 'amgt/harvest/bronze/research-report-extract/security_key=TSM_US_Equity/a0c07ba2a0bea860/extract.v2.json', 'amgt/harvest/bronze/research-report-extract/security_key=TSM_US_Equity/f1aedae3a90e5a49/extract.json', 'amgt/harvest/bronze/research-report-extract/security_key=TSM_US_Equity/f1aedae3a90e5a49/extract.v2.json', 'amgt/harvest/bronze/research-report/security_key=TSM_US_Equity/a0c07ba2a0bea860/TSMC earnings update 2Q26.pdf', 'amgt/harvest/bronze/research-report/security_key=TSM_US_Equity/f1aedae3a90e5a49/TSMC research pack 4_30_2026.pdf'] 4 research-report extract JSONs for TSM read: 0 TWD/NT$ tokens; extracted report text, not a stored cap or FX rate.
- crosswalk/v1: 6 objects; key names matching TSM|2330|TWD|Curncy: 0 [] newest 2026-09-29.json: exactly 1 record for TSM_US_Equity and no other record sharing its issuer (no 2330_TT_Equity line).
