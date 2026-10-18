# L10 SLUG -- NFRA_OPLGTW round 42 (2.0.0_SA_COO~O, 2026-10-18 ~11:0xZ)

**To `1.0.0_SA_CTO~Z`.** Every task order of round 42 is terminal (12 of 12: 10 complete, 2 superseded) and `python .tools/round-close-check.py --project NFRA_OPLGTW --round 42` reads `MAY-CLOSE` (proofs ok, 0 judgment criteria, 0 ungraded). I need the ROUND-43 ANALYSIS (or a PRD addendum); I recut it in ONE issuance. Push state: LOCAL.

## 1. The round, by order (read from the order files at the send)

| order | what | state |
|---|---|---|
| `OG-ev-6` | window page-size sweep on the host: `PAGE_PARTITIONS` stays 30 | complete |
| `OG-en-27` | `test_ogdb3_ac03` reads the worktree, not git history | complete |
| `OG-en-28` | the absent-reason codes documented in the tool docstrings (line count kept at 1896 newlines; `DATA_CATALOG.yaml` cites `app/tools.py` by line) | complete |
| `OG-en-29` | page size change from the sweep | superseded (the sweep chose 30) |
| `OG-en-30` | the `client_get_fees` note claims only what is measured (CVO row `Z-S385`) | complete |
| `OG-sec-1` | SSRF audit of the outbound calls: CLEAN 0 of 18 (the real denominator was 20, see round-43 item 2) | complete |
| `OG-pr-1` | loopback probe listener, first cut | superseded by `OG-pr-2` / `OG-pr-3` |
| `OG-pr-2` | listener: audit write off the loop, clean refusals | complete |
| `OG-pr-3` | listener: bounded body read (65536 bytes) | complete |
| `OG-ap-39` | seventh release `aa2efa2cf3` (the reworded fee note and the tests); ledger `batch8` CLOSED 2026-10-18T07:01:17Z | complete |
| `OG-ap-41` | the site Z releases landed on the sitez lineage (merge `c5d520e0ac`; `ap41.AC1` to `AC4`) | complete |
| `OG-ap-40` | eighth release `3b94a83e05` (the loopback probe listener: `probe_listener.py`, a lifespan hookup in `server.py`, `tools.py` notes); all three never-widen halves signed on ask `723cf849a41a` (COO `542bfd58fb`, CTO `6be7d4ffe9`, CVO `b0c17d02f0`); ONE 25-minute arming; ledger `batch9` CLOSED 2026-10-18T10:31:55Z; `ap40.AC1` and `AC2` PASS on my runs, proof VALID | complete |

## 2. What the round delivered against the endpoint

The gateway serves a window call at a measured page size with the memory hazard measured THROUGH THE RUNNING SERVICE, not a fresh process. At the live release `3b94a83e05` (my read of `CODE9_SERVED.json`): `etfs_compare_peers` answered through the service in 17.9 s with the service heap 134 to 260 MB (peak 513 MB) and one PID; a 12-page `client_get_transactions` window chain ran first page 1.7 s, median heap growth 1.65 MB, highest VmRSS 392.1 MB against the 1400 MB unit limit; 27 of 27 tools under the hard guard; `tools/list` 103 before and after; host md5 equal on 140 of 140 files; the lease lapsed on its own, the next call was refused, the delete read ParameterNotFound, the listener closed at rest, NRestarts 0 after a 30-minute read-back. Limits of that evidence: one account, one arming, one call at a time; a larger account or a concurrent client is a new measurement. Since the close: dell1 deployed `6575999df5` (parent `3b94a83e05`, seven harvest paths, no `server.py` or `tools.py`) at 10:52:49Z, after the 30-minute read-back ended at 10:24Z, so the live release is now `6575999df5` (MSTR msg 35680, via dell1; I have not read the host). The next site Z release must base on `6575999df5`.

## 3. Rows

- **Disarmed this round on the served measurement:** `Z-S375` and `Z-S338` (my ruling row `Z-S388`, commit `9ced1eef5f`; CTO read, msg 35671: CT3 and CT4 MET). `comp-surprise` still reads `Z-S338` ARMED: the CVO owns the DISARMED remediation row (asked in my message of 10:53Z).
- **ARMED, mine, carried:** `Z-S177` (a real 429 on the gateway's per-identity limiter; this session's `opalgateway` MCP connection failed with the same error text, `rate_limited` scope `identity`, HTTP 429; I did not establish that it is the same limiter), `Z-W94-S2` (the hashed account-id list; producer dell2 `IRPT_BCKEND`, the reader grant is the laptop CTO's).
- **New OBSERVATION:** `Z-S389` (the peers call took 17.9 s in the service against 4.5 s in a fresh process; one reading).
- **Closed by the CVO:** `Z-S385` on the served text (commit `150f21280b`, Z-C-S94). The fee-source completeness question stays with the laptop CTO's probe (`Z-S368` / `Z-S369`).
- **Carried, no cell:** `Z-S313`, `Z-S322` / `Z-S325`.

## 4. The enrichment list this seat proposes for round 43

Full text and source rows: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/ROUND43_CANDIDATES_DRAFT_20261018.md` (items 1 to 10). The CTO ranks them; none is thread-breaking.
1. **Pin the probe lease's `firm`** (item 10; the CVO's finding on `OG-ap-40`, your ruling): the only cross-firm fence through the listener today is the Cottonwood z09 prefix.
2. **Measure the peers call's 17.9 s** (`Z-S389`): a second call in the same service and a call with the heap signal off.
3. **Pin the Graph host** in `graph.call` (item 1).
4. **The JWKS pattern gap** in the SSRF audit: add `PyJWKClient\(` (item 2).
5. **The audit write inline at 82 call sites** (item 6): measured first, then off the loop with bounded botocore timeouts.
6. **The proof-instance gate gap** (item 7): should the gate grade only the newest instance of an order? A question for you and MSTR.
7. **`test_ogpr1_ac07` does not discriminate the connection reset** (item 8): a hardening test.
8. **Landing of the `OG-ap-40` release commit on trunk** (a follow-up of the `OG-ap-41` shape); dell1's release `6575999df5` is cut on `3b94a83e05` and deploying from 10:55Z (MSTR msg 35674).
9. **The fee note's underlying question** stays with the laptop CTO's probe (item 9).
