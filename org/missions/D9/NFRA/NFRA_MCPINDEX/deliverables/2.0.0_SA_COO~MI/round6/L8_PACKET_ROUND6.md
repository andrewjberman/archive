# NFRA_MCPINDEX round 6 -- the issuer's drain-end packet for L8/L9 (2.0.0_SA_COO~MI, 2026-10-01 ~14:3xZ)

Addressed to `3.0.0_SA_CVO~O`.
- **Source:** `ledger/ROUND_ANALYSIS.round5.md` @1edec80f63, section 5. Issuance @f797d8594a. Battery
  `deliverables/2.0.0_SA_COO~MI/round6/checks/`.
- **State:** 5 of 6 orders are terminal, drained and issuer-graded on CLOUD. MX-s-16 is open on its scheduled
  acceptance run tonight (2026-10-02 ~00:1xZ) and closes then. The judgment criteria below can be graded now.

## 1. Orders -- grade on CLOUD (issuer re-run after each drain)

| order | risk | status | mechanical (issuer re-grade on CLOUD) | judgment owed at L9 |
|---|---|---|---|---|
| MX-d-6 (discover reads `silver_datasets`; Schwab rows; reachability) | WORLD | complete, drained @abf979b2cf (A1 fail-closed) | d6.AC1 2/2, AC2 ROUTING 24/27, AC3 REACHABILITY 10/10; proof VALID @378ee1d635 | none |
| MX-g-3 (G-RDR) | WORLD | complete @abf979b2cf | g3.AC1 unrouted=0, AC2 3/3 | none |
| MX-r-8 (slot-4 release) | WORLD | complete, drained @d68390694a; LIVE e3567ce5f7 since 12:36:17Z | r8.AC1 PASS; r8.AC2 PASS (2 of 3 runs; 1 empty instrument read, row Z-S75); ledger 5/5 | none |
| MX-v-7 (thread re-run) | WORLD | complete, drained @e00d3e15bc | v7.AC1 PASS: served 63.43 == source 63.43 by VersionId `Qp7FdHII...`, as_of 2026-09-29, denominators equal | **J1** (r7.J1 re-grade), **J2** (r6.J1) |
| MX-x-4 (batch repair) | WORLD | complete, drained @42a8147e45 | x4.AC1 8 passed, AC2 3 arms, AC3 10 passed | none |
| MX-s-16 (one BD writer) | WORLD | OPEN: PHASE B done, ledger HELD for the scheduled run | AC1 2 of 4 by ruling (realized and transactions HELD); AC2 PASS; AC3 after close | none |

MX-t-12 is CANCELLED (analysis section 3).

## 2. The one real run of each outcome

- **The thread, live, through a principal session** (`deliverables/2.0.0_SA_COO~MI/round6/R7_J1_PRINCIPAL_SESSION_ROUND6_20261001.md`
  @384bd1ee00). This seat's opalgateway session ran as Andrew, an admitted Opal principal; its tool list refreshed to
  include `blackdiamond_list_fees`.
  - `what fees did Black Diamond charge`: catalogued true, `next_tool` `blackdiamond_list_fees`.
  - `Schwab positions`: catalogued true, `schwab_query`.
  - Tool call: as_of 2026-09-29, rows_matched 22,853, de-duplicated 22,221, transaction_fee 63.43.
  - Round 5's FAIL condition ("catalogued: false") no longer holds.
- **The figure against its source** (MX-v-7, `deliverables/0.9.0_WK_NFRA_MCPINDEX~22/THREAD_RERUN_round6.json`):
  - `silver/fees/2026-09-29.parquet` read by VersionId `Qp7FdHII2X4JQYzDSOAB9wGi1UcNJfpt` (the only version, 1,084,791 B);
  - de-duplicated `transaction_fee` 63.43 == served 63.43; trade_date 2026-09-29 == as_of; 22,853 / 22,221 / 632 on
    both sides.
  - The compared figure is the per-date total, not one row (row Z-W22-S11). The host call used `answer()` with an
    OPAL_INTERNAL principal, not the MCP wrapper (Z-W22-S12); the principal-session call above is the wrapper path.
- **A1 on the served host** (MX-r-8 read-back): OPAL_INTERNAL gets `blackdiamond_list_fees` and `schwab_query`; each of
  49financial, inflection and cottonwood gets 0 silver matches (8 of 8 legs).
- **MX-s-16:** unrealized and allocations retired behind `bd-silver-merge` (DS deploy 91eaf248, apply 0/3/0). The
  acceptance is tonight's scheduled run reading `failures=0 empty_stub=6` on unrealized.

## 3. Judgment criteria

- **J1 (r7.J1 RE-GRADE, FWD-4 for Black Diamond):** the route through a principal session plus the figure and as-of
  against the source by VersionId. Material in section 2.
- **J2 (r6.J1, FWD-1/FWD-3, Alyssa's cold run):** NOT RUN. It needs her, a person (rulings B1/B2, A5), in a fresh
  session with only the MCP connected: one position question, one transaction question. The prerequisite (the
  Z-W21-S22 discover repair) is now SERVED, so her run can proceed. Booking it goes through 0.0.0_AB_MSTR~Z for Andrew.

## 4. Drain hygiene (item 5): the gateway suite, each red named with its owner

13 red tests are common to the live ref and the release; 0 are new; 1 was fixed by MX-d-6
(`test_index_vocabulary_routes_the_real_catalog`). Per-file sweep across 58 files, from `probes_r8/tests_perfile_*`.

| test | owner |
|---|---|
| `test_browser_oidc::test_oga3_ac01`, `::test_oga3_ac07`; `test_principal_cutover::test_oga2_ac04`; `test_data_entitlement_guard::test_ogz1_ac05`, `::test_ogz1_ac08`; `test_entitlement_admin::test_ogz2_ac06`; `test_schwab_audit::test_ogo1_ac07`; `test_schwab_engine::test_ogq1_ac07`; `test_schwab_export_stream::test_ogx4_ac03` | NFRA_OPLGTW (2.0.0_SA_COO~O) -- its OG-* criteria |
| `test_portal_grant::test_asker_portal_scope_admits_granted_channel`, `::refuses_other_channel` | NFRA_OPALAI (2.0.0_SA_COO~AI) -- the asker scope (G-ASKER) |
| `test_schwab_host_inputs::test_printf_names_the_five_host_inputs_and_no_secret_value`; `test_schwab_transactions::test_mx_s15_dataset_registered` | NFRA_MCPINDEX (this seat) -- stale against the live template; repair to the round-7 batch cell |

## 5. Rows this round, and the issuer's rulings

| row | in-file | ruled by |
|---|---|---|
| Z-W22-S1 (cross-firm visibility of silver rows) | OBSERVATION/ARMED | MX-d-6 A1 @5a3f56291d, fail-closed; proven on the host (8/8) |
| Z-W22-S4 (MAIL_SENDER_TABLE blanking) | OBSERVATION/ARMED | derived from the repo (COO~O 27813); 3/67 before and after (Z-W22-S9) |
| Z-W24-S2 (sentinel-less days) | BLOCKING/ARMED | MX-s-16 A1/A2; cause Z-W24-S4; realized HELD |
| Z-W24-S8 (transactions consumer) | BLOCKING/ARMED | transactions HELD; its premise is contradicted by Z-S74 |
| Z-S72 (bd-silver-merge unrealized failures=6) | OBSERVATION/ARMED | fix deployed (91eaf248); disarms on tonight's run |
| Z-S73 (OTP bearer echoed) | OBSERVATION/ARMED | rotated by OG-rl-1 (COO~O 27769: the old value returns 401) |
| Z-S74 (freshness gate non-blocking in production) | OBSERVATION/INERT | carried (section 6) |
| Z-S75 (r8.AC2 empty instrument read) | OBSERVATION/INERT | check hardened @273e5832cb |
| Z-W22-S2..S3, S5..S12; Z-W23-S1..S3; Z-W24-S1, S3, S5..S7 | OBSERVATION/INERT | recorded; carried where named in section 6 |

## 6. Carried to the round-6 L10 slug (enrichment candidates for 1.0.0_SA_CTO~O)

1. **The catalog firm field** (C1 schema + emitter), so firm-scoped silver rows can serve firm principals (A1 is
   fail-closed until then).
2. **The BRONZE_COMPLETE sentinel** for realized and transactions on BD's late-posting Mon/Tue (the shared `data/cot`
   ingest; owner per the CTO half's placement), then re-rule realized and transactions.
3. **Z-S74:** which skip path production's bd gold chain takes past the freshness gate; and the 48h daily threshold on
   weekly tables (allocations, unrealized).
4. **BD ExternalId option A** (a runtime secret read), still unfolded.
5. **Round-7 batch cell:** the 2 stale MCPINDEX tests (section 4); proof-of-spec-check flagging a re-committed instance
   that still carries PENDING rows; the cp1252 SSM-output trap (Z-S75).
6. **FWD-4 coverage:** Orion, Eclipse and SmartX tools (FWD-6..10 enter no earlier than round 7).

## 7. Push state

LOCAL. CLOUD is ahead of origin (`0abf99fcd4`, ls-remote read 13:56Z). The site-Z push is MSTR~Z's on Andrew's word.
