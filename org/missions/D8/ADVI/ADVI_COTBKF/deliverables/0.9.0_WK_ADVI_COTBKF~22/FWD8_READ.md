# FWD-8 read -- the applied crosswalk, one account lined up, the near-matches awaiting a person

Applied crosswalk: `s3://opal-data-assets/commonwealth/cottonwood/silver/crosswalk/date=2026-06-23/crosswalk.parquet` (MATCHED rows read: 439).

## One MATCHED account, in three lines

1. Old Commonwealth account 04003450617; advisor id(s) HKJ; last activity 2026-06-16 (table: silver transactions).
2. Matched by rule R2-in-kind-transfer, score 1.0 (table: silver crosswalk).
3. Today's Cottonwood account z0927272491; 7 of its 7 old positions carried over (holdings from 2026-06-30).

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
| B3S606724 | z0927980101 | 0.7857 | AWAITING A PERSON |
| RGY007491 | z0926819471 | 0.7778 | AWAITING A PERSON |
| 0QF883612 | z0927234221 | 0.7647 | AWAITING A PERSON |
| RGY003642 | z0927303741 | 0.7647 | AWAITING A PERSON |
| 00089513495 | z0927128191 | 0.75 | AWAITING A PERSON |
| 04001608008 | z0927128201 | 0.75 | AWAITING A PERSON |
| 04003024531 | z0927171211 | 0.75 | AWAITING A PERSON |
| 6EQ029047 | z0926748301 | 0.7273 | AWAITING A PERSON |
| 04003330314 | z0926837771 | 0.6667 | AWAITING A PERSON |
| 04005048006 | z0926838031 | 0.6667 | AWAITING A PERSON |
| 0QF878980 | z0926704461 | 0.6667 | AWAITING A PERSON |
| 0QF879507 | z0927331161 | 0.6667 | AWAITING A PERSON |
| 0QF879617 | z0926725641 | 0.6667 | AWAITING A PERSON |
| 0QF879620 | z0926725641 | 0.6667 | AWAITING A PERSON |
| 0QF890772 | z0926726081 | 0.6667 | AWAITING A PERSON |
| RGY003024 | z0927533711 | 0.6667 | AWAITING A PERSON |
| RGY003440 | z0926726341 | 0.6667 | AWAITING A PERSON |
| RGY005363 | z0926704541 | 0.6667 | AWAITING A PERSON |
| RGY006818 | z0926628491 | 0.6667 | AWAITING A PERSON |
| RGY007437 | z0926725551 | 0.6667 | AWAITING A PERSON |
| RGY003303 | z0926725031 | 0.65 | AWAITING A PERSON |
