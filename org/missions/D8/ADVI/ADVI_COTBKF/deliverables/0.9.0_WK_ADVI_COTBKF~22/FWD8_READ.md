# FWD-8 read -- the applied crosswalk, one account lined up, the near-matches awaiting a person

Applied crosswalk: `s3://opal-data-assets/commonwealth/cottonwood/silver/crosswalk/date=2026-06-23/crosswalk.parquet` (MATCHED rows read: 439).

## One MATCHED account, in three lines

1. Old Commonwealth account acct#cdf76705; advisor id(s) HKJ; last activity 2026-06-16 (table: silver transactions).
2. Matched by rule R2-in-kind-transfer, score 1.0 (table: silver crosswalk).
3. Today's Cottonwood account acct#efafd1dc; 7 of its 7 old positions carried over (holdings from 2026-06-30).

## Positions

- 298706763 (FUEPX): old 671.983 -> Cottonwood 671.983 [from silver positions (as of 2026-06-23); Cottonwood current-side holdings]
- 399874742 (FAFGX): old 1272.956 -> Cottonwood 1272.956 [from silver positions (as of 2026-06-23); Cottonwood current-side holdings]
- 643822745 (FNEEX): old 751.094 -> Cottonwood 751.094 [from silver positions (as of 2026-06-23); Cottonwood current-side holdings]
- 648018745 (FFPNX): old 255.595 -> Cottonwood 255.595 [from silver positions (as of 2026-06-23); Cottonwood current-side holdings]
- 649280740 (FNFWX): old 301.218 -> Cottonwood 301.218 [from silver positions (as of 2026-06-23); Cottonwood current-side holdings]
- 831681747 (FSWFX): old 340.129 -> Cottonwood 340.129 [from silver positions (as of 2026-06-23); Cottonwood current-side holdings]
- 939330742 (FWMMX): old 1197.482 -> Cottonwood 1197.482 [from silver positions (as of 2026-06-23); Cottonwood current-side holdings]

## Near-matches (never linked by Opal)

Linked by Opal: 0. Source: the CB-d-3 near_matches.csv.

| Commonwealth account | Cottonwood candidate | Score | Status |
|---|---|---|---|
| acct#f13c4faf | acct#7e490d62 | 0.7857 | AWAITING A PERSON |
| acct#cfd8182f | acct#5ca8c551 | 0.7778 | AWAITING A PERSON |
| acct#268d9555 | acct#c7414de1 | 0.7647 | AWAITING A PERSON |
| acct#2c16c4a1 | acct#4f4e6d68 | 0.7647 | AWAITING A PERSON |
| acct#27a0bfb9 | acct#a841d70b | 0.75 | AWAITING A PERSON |
| acct#9842f2ac | acct#2b808831 | 0.75 | AWAITING A PERSON |
| acct#35e147ec | acct#396aa3d9 | 0.75 | AWAITING A PERSON |
| acct#982cf165 | acct#22bd32d8 | 0.7273 | AWAITING A PERSON |
| acct#067a8984 | acct#3b28d545 | 0.6667 | AWAITING A PERSON |
| acct#b1dcf364 | acct#f4458e2e | 0.6667 | AWAITING A PERSON |
| acct#3ea38af4 | acct#8c9b6079 | 0.6667 | AWAITING A PERSON |
| acct#89146847 | acct#35e979e3 | 0.6667 | AWAITING A PERSON |
| acct#4b78b222 | acct#a24c398f | 0.6667 | AWAITING A PERSON |
| acct#18f0a0bd | acct#a24c398f | 0.6667 | AWAITING A PERSON |
| acct#760a3a43 | acct#a75c1589 | 0.6667 | AWAITING A PERSON |
| acct#ae910ae7 | acct#a82f0ef1 | 0.6667 | AWAITING A PERSON |
| acct#9e28763b | acct#afdd2d3e | 0.6667 | AWAITING A PERSON |
| acct#815c2172 | acct#bc129132 | 0.6667 | AWAITING A PERSON |
| acct#82618c57 | acct#4e048dea | 0.6667 | AWAITING A PERSON |
| acct#b30b51ee | acct#f2a5d4be | 0.6667 | AWAITING A PERSON |
| acct#435f9230 | acct#14d4c68f | 0.65 | AWAITING A PERSON |
