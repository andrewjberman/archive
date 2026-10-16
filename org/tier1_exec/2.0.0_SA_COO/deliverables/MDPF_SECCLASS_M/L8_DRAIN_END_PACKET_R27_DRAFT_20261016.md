# L8 drain-end packet -- MDPF_SECCLASS round 27 -- DRAFT (2.0.0_SA_COO~M1, dell1, begun 2026-10-16 ~08:2xZ; NOT SENT)

**Status of this file:** a draft kept so the packet is a compile, not a rewrite, once leg G and the E_18 ship are read. It is not at the CVO. Sections marked **[OWED]** are filled when the act they name is read. Claim words: `measured` = read this session; `held` = cited from a record.

**For:** 3.0.0_SA_CVO (and the record for 1.0.0_SA_CTO~DELL1). **Decomposition:** `org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R27.md`. **Issuance:** @a027dd2c77 (`fanout: 2 of 2 chains, cap 8`), on the CTO round-26 analysis (msg 6482).
**Round-close check:** `round-close-check.py --project MDPF_SECCLASS --round 27`: MAY-CLOSE at 05:1xZ (`orders=19 judgment=0`); re-run at the close **[OWED]**.

| cell | order | slot | risk | drained | criteria |
|---|---|---|---|---|---|
| SC-e-107 | TO-SC-e107 (amended twice) | ~97 (three seats) | LOCAL, direct act | @283e087af6, @e6c7448985, @cea6e9b62c | AC1 `SEED22-SELFTEST ok=True` (35 of 35); AC2 `SEED22-PLAN ok=True planned=13 unresolved=0 seed_pending=9 dollars=413341.59`; AC3 `SEED22-FOLD ok=True` |
| SC-e-108 | TO-SC-e108 | ~98 | SERVED | @d812b466fd | AC1 6 passed; AC2 `CHAIN-NO-B01B ok=True`; AC3 0 old-list lines in E_18 (17 at the base); gold folder 203 passed at trunk |

## The served acts (the issuer's), in the CTO's order

1. **The seed -- DONE, read (measured).** Pair: request @aa5fd14834 (sha256 `737e43a0...`), CTO half @7b166cf360, COO half @0be4ff09ef. `0.7.0_AE_CloudOps~SC1` applied it 2026-10-16T06:27:08Z under TO-SC-e107b: `SEED22-APPLY written=13 refused=0`; I re-ran `E107-SEEDED ok=True present=13/13 absent_ok=9/9`, a paginated scan counts 11,375 keys (11,362 + 13), SC1's census of 200 existing keys moved none. Seeded: 4 equity (15,777.17), CUBE and GLPI alternatives / Real Estate (11,855.56), HPI, LCFYX, PFF, VRP, CPXIX fixed_income with no sub-class (120,888.00), EZET and HODL commodities / Commodities (22,008.57; HODL overrides the old row, recorded): 170,529.30 on the 10-09 lots. Held out (9, Unclassified, `seed_pending`): DODBX, BALCX, CIMAX, KAMIX, FSNQX, HBLFX, JBAWX, TRRNX, PCEF.
1b. **The seed through a second path (measured 09:2xZ):** the gateway tool `mdpf_get_security_classification` (a different reader from my boto3 checks) serves CUBE as alternatives / Real Estate, HODL as commodities / Commodities, HPI as fixed_income with a null sub-class (each `etf-classifications:<ticker>`, `last_updated` 2026-10-16, freshness not stale) and answers DODBX (held out) with no row (`absent_reason: no row for this ticker in the etf-classifications table`). It shows `classified_by: scheduled` for the seeded rows; the provenance attributes (`source_table`, `fold_rule`) are in the table but not in that tool's output.
2. **Leg G of the seed [OWED]:** the first scheduled fire after the seed (23:00Z 2026-10-16, chain end about 01:30Z 10-17), `seed22_legg_read.py read --pre-version-id 3BY8Etw3LetRaRFcOofjaAT98PSfp4Z3`. Expected: the 13 tickers' dollars in the ruled classes and out of `unclassified`/`other` on every window date; the 9 held out stay; no other class moves; totals = AUA.
3. **The E_18 / gold_dispatch.sh ship [OWED]:** pair request @5690597b29 (sha256 `527a2fbc...`), CTO half @d245ef138e, COO half @9de34e1632, TO-SC-e108b staged at 0.7.0_AE_CloudOps~DELL1 (re-addressed from ~SC1 @0adc09ef75 under CLAUDE.md rule 34, the MDPF macro lane per MSTR~DELL1 msg 6827; the signed halves cite the earlier ~SC1 path). Branch 1: `e108_shipped_check.py` and one E_18 dry run. Branch 2: the first fire without B_01b; W93-S2 / D1-S42 disarm on E_18's own output.

## What the round established (measured unless marked)

- The old-list-only set was 22 tickers ($413,341.59, 10-09 lots) and is now exactly the nine held out ($243,508.93 on the partition as rewritten since: 482,140 open real-ticker rows against 481,824).
- E_18's lookup was a no-op (E_18:247 skips old-list keys before the lookup); the repoint's real effect is that old-list-only tickers become live candidates the same night, hence seed first.
- The shared planner does not fold; the CTO's fold ruling (F1 yes, F2 narrowed, F3 no, F4/F5/F6 yes) is committed as a map (`R27_CHECKS/seed22_fold_map_20261016.json`). Planner dry run on the nine held out with no old-list lookup: PLANNED 0, UNRESOLVED 9.
- The old list does not stop growing with this round: 7 writer files, one deployed in the cottonwood chain (not shown to have completed a run: no watermark in opal-data-cot) and manual ones; readers outside the BD chain (partners-data, news layer 3) go blind to new BD securities, carried to round 28 by the CTO.

## Issuer's own defects this round (for the CVO to see)

- My `check_seed22_plan.py` demanded a non-empty sub-class on every planned row against the CTO's ruling (row D1-W97-S2): fixed @72d63fef7f, the worker's instance regraded by the worker (third seat, @0f480fe586).
- My order told the SC-e-105 worker (round 26) to add census-missed readers while the check refused extra rows (D1-W95-S2).
- Two runtime tick lines before 04:57Z were stamped ahead of `date -u`.

## Not shown **[OWED]**

Leg G and the ship's branches; whether the cottonwood `B_01b` ever runs; the unmeasured readers of the seeded rows (live portal lookups, positioning); the 9 held-out tickers' true classes (a multi-asset class design is a TAXONOMY LAW round-28 item).

## Rows at this packet **[OWED]**

D1-S41 (W93-S2 disarmed on its measurement), D1-S42 (ARMED, mine, until E_18 reads 0 old-list-only tickers after the ship), D1-S43 (W97-S1/S2 disarmed). Open at Andrew: the client-facing Black Diamond Mix restated-history PROD push.

## Owed at the round-28 recut (the CTO's carried items)

Repoint partners-data `etf_classifier.py` and news layer-3 curation to the canonical table, each under its own pair; take the cottonwood `B_01b` out of the cot canonical chain under its own pair (first act: read the cot-exporter step list); the multi-asset class design (CRO patterns); delete the BD `B_01b` file with its carriers, remove the shared lookup, add the standing FWD-4 test; the DEMQUE<->SECCLASS sync cell; e57e61.
