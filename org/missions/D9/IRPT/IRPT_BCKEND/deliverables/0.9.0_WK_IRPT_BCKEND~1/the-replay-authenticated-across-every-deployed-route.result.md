# IB-rtb-1 RESULT -- THE REPLAY, AUTHENTICATED, ACROSS EVERY DEPLOYED ROUTE

**TO:** `IRPT_BCKEND.TO-IB-rtb-1` | **worker:** `0.9.0_WK_IRPT_BCKEND~1` (COLD START -- round 1's
subagent died with its session; this is a fresh context executing the same face) | **branch:**
`wk-irpt_bckend-2-1` | **base commit:** `cd3bf01fcd3a42159db0a2c3307a8b0b12e0b73f` (HEAD of `CLOUD`
at hand-off, unchanged through this run).

Read-only against the deployed plane throughout, as bounded. No infrastructure applied. The
authenticated served/swap read stands HUMAN-GATED (RT2's own record, cited verbatim, never
re-derived) beside the POST-AUTHORIZER in-process replay and the REAL-PATH boundary measurement.

## Criteria

| id | verdict | invocation | deciding line |
|---|---|---|---|
| `RTB1-AC1` | **PASS-by-output** | `timeout 900 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/battery_ib_rtb_1.py` | rc=0, `"overall_pass": true` then `IBRTB1-REPLAY-AUTHENTICATED` |
| `RTB1-AC2` | **RECORDED (judgment)** -- no verdict | evidence assembled for `3.0.0_SA_CVO` at L9 | in the proof-of-spec instance under `UNVERIFIABLE-BY-INSTRUMENT` |

Transcript committed beside this file: `IB-rtb-1_RTB1-AC1_battery_output.txt` (28,124 bytes).

## (a) The plane -- two planes, the authenticated one HUMAN-GATED, cited not re-derived

`RT2_test_principal_human_gated.md` (`0.9.0_WK_IRPT_BCKEND~2`) is the ONE investigation of whether
a worker may mint a test principal, and nothing in round 2 changed its premises: minting one is
still out of this order's `<paths>`, still a write to `opal-users-v2` (the production auth plane),
and the only worker-side alternative is signing a token with `opal/auth/jwt-private-key`, which
bound 6 forbids. This cell re-checked the record's 8 required elements verbatim (8 of 8 present, 0
secret values) rather than re-deriving the investigation, and independently re-verified, fresh this
turn, that the edge the record depends on is applied and live: `get-distribution-config` on
`EVTSA9VEHNZVH` reads 28 cache behaviors.

- **Plane 1 -- POST-AUTHORIZER** (the six-swap authorization proof, arm (b), and arms (c)/(e)):
  each real entry point, resolved through `_authz/routetable.py` (the production route-table
  resolver IB-rt-2 built) and invoked in-process with the header set the edge validator injects --
  the same plane IB-rt-2's own terminal 15-of-15 battery exercises, re-derived fresh this run
  rather than cited.
- **Plane 2 -- REAL PATH** (the live boundary measurement): all 12 declared routes (holdings added
  since round 1's 11) through the real distribution, unauthenticated -> `401` on 12 of 12, 0
  protected bytes; a malformed bearer token and a forged-shaped JWT both `401`; the
  CloudFront-bypass control (straight to API Gateway, no origin-verify header) also `401`, with API
  Gateway's own generic message, confirming `isOriginVerified()` is a real, separately-enforced
  gate. Authenticated replay is NOT RUN on this plane -- the same test-JWT gap.

## (b) Every route, six swaps -- 12 of 12 covered

Six dispatched functions (`irpt-directory-search`, `irpt-performance-adapter`,
`irpt-ycharts-generate`, `irpt-narrative`, `irpt-export-render`, `irpt-status`, covering 11 routes)
each re-run fresh this turn through `_authz/tests/test_guarded_entries.py` (pytest, 96 passed):
served for the authorized principal on 6 of 6 functions; 36 of 36 swaps refused (0 protected bytes,
serialised and searched for every other firm's/advisor's/account's/relationship's/report's/pdf's
identifiers). **This is the round-2 improvement IB-rtb-1 measures**: all six of these routes were
UNGUARDED, VACUOUS or STRUCTURALLY EXEMPT in round 1's IB-sb-3 (rows W1-S9, W1-S10); IB-rt-2's
`guard()` + `FirmBinding` wrapper now reauthorizes every one of them, and this cell's own fresh
pytest run is the re-derivation (bound 12: never re-use a stale reading).

Holdings (`irpt-holdings`, the twelfth route, added by IB-rt-7 since round 1) carries its own
served+swap arm against the LIVE API route and the landed QA holdings snapshot (IB-rt-7's
`arm_served`, re-run fresh): authorized request served, 6 of 6 swaps refused, 0 protected bytes.

**12 of 12 routes covered; every route served for the authorized principal; every route's six
swaps refused.**

## (c) Revoked against a warm cache; Opal vs firm; the download -- on the new plane

- **Revoked vs warm cache**: served -> revoked (`EMPTY_GRANT`, cache untouched, 0 protected bytes)
  -> restored (served again from the SAME warm cache entry, `cache_hit=True`). Re-run fresh through
  IB-sb-3's own `arm_revoked_against_warm_cache()`.
- **Opal vs firm**: an Opal principal reaches firm A and firm B, one at a time, never a union; a
  firm advisor (49financial) replaying the same request against firm B is refused `FIRM_BINDING`.
  Re-run fresh through IB-sb-3's own `arm_opal_vs_firm()`.
- **The download**: **a premise from round 1 no longer holds, and it is filed (row
  `IRPT_BCKEND-W1-S18`).** IB-sb-3's own four synthetic export objects
  (`firms/49financial/generations/GENIBS14SYN/attempts/1/exports/*/report.pdf`) are now GONE from
  `opal-data-ycharts` -- 0 of 4 answer an ordinary read AND 0 of 4 carry any entry in
  `list-object-versions`, contradicting `RT8-g_synthetic_delete_record.md`'s own stated
  recoverability (that record predicted the marker-delete would keep the bytes retrievable by
  VersionId; a fresh check this turn shows the underlying version is gone too, and no substitute
  real PDF export exists anywhere else in the estate at this vintage). This arm therefore splits:
  **(c3a) the real-object grounding reads BLOCKED, 0 of 4, printed and filed, never silently
  substituted**; **(c3b) the reauthorization MECHANISM is measured independently** -- the real
  `Enforcer`, the real `guard()`, the real `download()` dispatcher and the real `FixtureSigner` are
  exercised with a labelled FIXTURE artifact-metadata record standing in for the storage boundary
  (the same pattern bound 1 sanctions and IB-rt-2's own `Entry.deps` swap already uses elsewhere in
  this project): authorized served, swapped pdf id refused `OBJECT_NOT_COVERED` (0 protected
  bytes), revoked grant then the right id refused `EMPTY_GRANT`. RTB1-AC1's own bar names "every
  swap refused" and "0 unguarded" as its mechanical properties; the download's AUTHORIZATION
  mechanism meets that bar, and the missing real-object grounding is reported and filed rather than
  either silently passed or allowed to fail the whole criterion on a fact outside this order's
  control (bound 8).

## (d) Zero unguarded, and the control

`unguarded_routes()` over the REAL `docs/contracts/investor-reporting/v1/routes.json`, resolved
through `_authz/routetable.py`'s production entry-point resolver (never a hand-typed table): **0 of
12**. The throwaway control -- one route's table entry replaced by an unwrapped stub, never a
handler -- moves the verdict to **1 of 12** (victim: `GET
/api/scoped/investor-reporting/analysis/{jobId}/sections`), so the zero above is a measurement and
not a constant.

## (e) Keys and ids

- **S3 keys**: every synthetic export key this project minted, censused for name/email-shaped
  components: **0 of 16**.
- **The id-space seam**, through IB-rt-3's real normalizer (`_ids.py`), re-run fresh this turn
  against the landed QA directory+holdings objects for all three firms (`arm_three_producers`):
  49financial 5,860 of 5,877 holdings ids found in the directory (5,860 of 7,480 the other
  direction); cottonwood 837 of 971 (837 of 837 the other direction); inflection 874 of 874 (874 of
  874 both directions). All three firms' populations grew slightly since IB-rt-3's own committed
  numbers (5,856/5,873, 837/961, 790/790) -- consistent with the QA fixtures being live and
  re-generated between runs, not a defect of the join; printed as measured.

## Rows filed

- `IRPT_BCKEND-W1-S17` (OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~B`) -- IB-rt-2's own
  terminal record ("7 of 7 VERIFIED") does not reproduce from a fresh worktree at the same HEAD; a
  fresh re-run reads 3 of 7, and the cause is the verifier's own local layer-zip cache, absent in a
  fresh worktree -- the three-way sha256 chain (declared/S3/live) still reads EQUAL on 7 of 7, so
  the served bytes are not in question. Not this cell's to fix; IB-rtb-1 does not depend on that
  specific check anywhere.
- `IRPT_BCKEND-W1-S18` (OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~B`) -- the four synthetic
  export PDFs IB-sb-3's own download arm used are now permanently gone (not merely marker-hidden as
  a prior record predicted), and no substitute real PDF export fixture exists anywhere in the
  estate at this vintage.

## Bounds observed

Read-only against the deployed plane throughout (S3 reads of landed QA/synthetic objects and their
version history; live HTTPS probes refused at the edge before any handler runs; `aws lambda
invoke` reused only through already-committed batteries). No protected value printed anywhere. No
credential read or logged -- every secret cited by NAME only. Deploys nothing; no infrastructure
applied. No live vendor call. `.tools/commit-gate.sh` rc=0 on the new battery file. Every invocation
ran under `timeout`, none retried more than once. No existing surprise row edited -- two rows
appended.
