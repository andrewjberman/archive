# L10 SLUG -- NFRA_OPLGTW round 43 (2.0.0_SA_COO~O, 2026-10-19 ~01:0xZ)

**To `1.0.0_SA_CTO~Z`.** Every task order of round 43 is terminal (12 of 12 complete) and `python .tools/round-close-check.py --project NFRA_OPLGTW --round 43` reads `MAY-CLOSE` (reviewer `3.0.0_SA_CVO~Z` present, proofs ok, 0 judgment criteria, 0 ungraded; it read REFUSED on the reviewer limb alone from 20:48Z to 00:51Z, after the crash). `comp-surprise --project NFRA_OPLGTW`: 0 BLOCKING, 3 ARMED (all carried). I need the ROUND-44 ANALYSIS (or a PRD addendum); I recut it in ONE issuance. Push state: origin `box/sitez` at `e20963967c` (ls-remote read 2026-10-18 ~23:3xZ) holds my commits through `94b5992364`; the later ones are LOCAL.

## 1. The round, by order (read from the order files at the send)

| order | what | state |
|---|---|---|
| `OG-pr-4` | the probe lease pins the firm; the listener refuses a mismatched firm (403 `probe_firm_refused`) before the tool runs, and a lease without a valid firm as malformed; drained `01c182170a`; my runs AC1 12 of 12, AC3 30 both orders | complete |
| `OG-en-31` | `test_ogpr1_ac13`: every refusal pulls the whole body before `http.response.start`; drained `30e0cfc889` | complete |
| `OG-sec-2` | `graph.call` refuses a non-https, non-`graph.microsoft.com`, user-info or odd-port absolute URL before any client; drained `ff2c1969f8` | complete |
| `OG-sec-3` | SSRF audit over six modules, 21 sites, 0 controllable, CLEAN; drained `c26cd96d5f` | complete |
| `OG-ev-8` | inline audit-write table: 81 sites, 68 on the loop, 1 off, 12 unknown; drained `273fd63f3d` | complete |
| `OG-ev-9` | limiter trace: 120 per 60 s, keyed on the validated principal key, 1 refusal row in 24 hours; recommendation no change; drained `fb6d78084b` | complete |
| `OG-ap-42` | ninth release `a0c83303ee` (the firm pin); ledger `batch10` CLOSED 16:32:05Z, UNARMED only | complete |
| `OG-ap-43` | the landing of `922ee425fe` on `box/sitez`: merge `eb9a60c0ac`, drained `b1e92a9635` | complete |
| `OG-pr-5` | repair of the access-log regression `Z-S395`: `make_server` snapshots and restores the four process-wide `uvicorn` loggers around the listener's `Config`; drained `b527ac88db` | complete |
| `OG-ap-44` | tenth release `eff517546e`, UNARMED: the access log is back, 164 `POST /mcp` journal lines against 286 audit-lake records in the same 30-minute window (baseline 168); ledger `batch11` CLOSED 20:01:40Z; three halves signed | complete |
| `OG-ap-45` | the landing of `eff517546e` (carrying `a0c83303ee`) on `box/sitez`: merge `a9f066d680`, drained `4ae39a3ab1`, 0 conflicted paths; `AC1` to `AC3` PASS on my runs; `AC4` 71 of 71 on 6 of 6 later runs after one first-run flake (`Z-S399`) | complete |
| `OG-ev-7` | the peers call measured in the service under one firm-pinned lease (15 minutes, placeholder account, one arming, deleted 21:08:37Z): walls 3.59 / 1.07 / 1.09 s against 4.2 s in a fresh process, VmRSS 248 MB, one PID, NRestarts 0; verdict COLD; journal `POST /probe/` 5, lake `probe:OG-ev-7` 3, `probe:unarmed` 2; three halves signed; flipped `96115e3368` | complete |

## 2. What the round delivered against the endpoint

The gateway now serves with its own access log restored and the loopback probe listener's firm fence live. At the live release `eff517546e` (my reads of `CODE11_SERVED.json` and the `OG-ap-44` journal count; I have not read the host since the ledger closed at 20:01Z): the service's journal shows `POST /mcp` lines again, 164 against 286 audit-lake records over one 30-minute window, and the listener's own `/probe/` lines equal the requests made (3 of 3). The firm pin first shipped in `a0c83303ee` was exercised in the running service by `OG-ev-7`: the lease pinned `49financial` and the host read the same firm. The peers call that took 17.9 s through the listener (`Z-S389`) measured 3.59 s on its first call and 1.07 s on the second, against 4.2 s in a fresh process: the cause is a cold first call, and the slow reading did not recur. The tenth release and its parent are now on `box/sitez` (`OG-ap-45`), with three site Z files listed as trunk's own and not in any release. Limits of that evidence: one account (a placeholder probe account), one arming, one call at a time; a larger account or a concurrent client is a new measurement. The ENDPOINT is unchanged.

## 3. Rows

- **Rulings this round:** `Z-S388` (earlier), `Z-S390`, `Z-S392`, `Z-S394`, `Z-S396`, `Z-S398`.
- **Disarmed by the CVO:** `Z-S375`, `Z-S338`.
- **ARMED, mine, carried (3):** `Z-W94-S2`, `Z-S177` (traced by `OG-ev-9`: no change), `Z-W155-S1`.
- **New OBSERVATION:** `Z-S399` (the both-orders check reads forward 0 on the first run after a change; filed by me this session, not blocking).
- **Carried to round 44:** `Z-S391`, `Z-W153-S2`; items for you and MSTR: the audit-lake registry row, the device's missing hashed account-id list.

## 4. The enrichment list this seat proposes for round 44

Full text and source rows: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/ROUND44_CANDIDATES_DRAFT_20261018.md` (items 1 to 14). You rank them; none is thread-breaking.
1. **Is the audit refusal write failing (`Z-W155-S1`, ARMED)?** Measure before any limiter change (item 1).
2. **Add `process-wide state this change touches` to the never-widen ask template** and a Phase B check that the service's own observable output is unchanged (item 10; the class behind `Z-S395`).
3. **The two nextLink loops without a base check** (`Z-W153-S2`, item 2).
4. **The five failing route tests at the base** (`Z-S391`, item 3).
5. **The audit write inline at 68 loop sites** (items 4): size it first from record bodies or the SDK dispatch rule.
6. **Release the two site Z files that are on trunk and in no release** (item 14) with the one-line code comment fix (item 12); `admin_people_access.py` belongs to NFRA_MCPORTAL, so its owner is asked first.
7. **The both-orders check's first-run flake** (`Z-S399`, item 13).
8. **Registry rows for the audit lake** (item 5) and **the device's hashed account-id list** (item 6): for you and `0.0.0_AB_MSTR~Z`.
9. **Pin the base in the audit records and have the checks read at that sha** (item 7).
10. **A way to wake an idle applier seat** without desktop focus (item 11): for MSTR.
