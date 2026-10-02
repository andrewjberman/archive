# DSGN_AMGTV1 -- ROUNDS 24-26 CLOSE (issuer `2.0.0_SA_COO~D`, 2026-10-02 ~10:2xZ)

**Inputs:** CTO ruling msg 28350 (Z-S14) -> round 24 @1549ca8bcc; CTO round-23 analysis @876dfcadb8 (msg 28356) rows 1 and 3 -> round
25 @67c77d30a4 (a second issuance into round 24 was refused by to-pipeline-gate: ONE ISSUER PER ROUND); the issuer's round-25
close-walk finding -> round 26 @0355c048fa. Deadline 11:30Z: all four orders were drained and merged by ~10:0xZ.

## 1. ORDERS (4 of 4 terminal, all drained)

| order | round | cell | worker | portal | outer drain |
|---|---|---|---|---|---|
| `AV-zc-1` | 24 | Exec contact-enrichment line says it once (Z-S14) | ~74 | e60e5ba8 | d6bc787d76 |
| `AV-zc-2` | 25 | each absent column states its reason, 5 classes over 11 served reasons | ~75 | 27cf5662 | 501a052d15 |
| `AV-zc-3` | 25 | posture check renamed `claims_resolved_count_stated`; PLANT=zero + LEGACY_PREDICATE | ~76 | c06d140c | 35382a76c0 |
| `AV-zd-1` | 26 | the 5 live served reasons (RESAPP ak-3 registry labels) classed | ~77 | c41861b4 | 2d4dbda157 |

All four instances are VALID; the blobs are LF with no 0x08.

## 2. THE CANDIDATE -- portal `0ab75973` (worktree 70, branch `dsgn-r24-onto-dev`, LOCAL)

41eeda55 (CTO-approved) -> b73d0a3e (zc-1) -> 7b2e120a (zc-3) -> 5f9265a8 (zc-2) -> 7889655a (+ remote DEV 0531cc65) -> 23bd1c2d
(+ remote DEV 06bc6f85, CTO msg 28379) -> **0ab75973** (zd-1). It is a fast-forward over 06bc6f85 (re-read 10:0xZ).

**Battery on 0ab75973:** liveclass, reasonclass, lushaline, posturezero, peerwords, accession, postureharness, codeface, subjectrow,
starredclaims, tipface and namecard, 3 of 3 each; bound 14 of 14; `tsc -b --noEmit` rc 0.

## 3. REAL RUNS (signed-in walks; ARM / DISARMED notices to 0.0.0_AB_MSTR~Z; site Z only)

| walk | build | read |
|---|---|---|
| 20261002T094604Z | 7889655a | VLO Exec: the Lusha line once (zc-1 REALIZED); the SERP sentence gone (RESAPP B5 live). VLO Peers: **5 of 12 absent columns read the generic `unmapped` clause**, because RESAPP ak-3 now serves registry-label strings the fixture-graded check could not see. This became round 26 |
| 20261002T101105Z | 0ab75973 | VLO Peers: **12 of 12 absent columns state a class reason, 0 generic** (Cash "only a ratio is reported, not the amount."; P/E 2027 "estimates go out one year only."; Debt/Equity "the source's leverage measure is not defined as debt to equity."). One API issue: a 503 on `GET /api/scoped/amgt/security/BA_US_Equity/timeline/day/2026-09-08` (a served route, not a page defect) |

## 4. ISSUER NOTES

- **Gate refusals honoured, not overridden.** to-pipeline-gate refused a second round-24 issuance, so it was relabelled round 25.
  surprise-row-gate refused an in-place `surfaced_at` edit, so correction row Z-S16 records the true times of W71-S1/S2.
- **Instrument gap, named.** A fixture-graded check cannot see a producer that changes its served strings after the capture. Here
  that was RESAPP ak-3 between capture and walk. Only the live walk caught it; round 26 closed it.
- **Process deviation.** The round-25 worker prompts (~75, ~76) pointed at the order file plus a summary instead of carrying the face
  verbatim. Each worker read its full face from its worktree.

## 5. OPEN

- The CTO's re-read of 0ab75973 is asked (RE 28379). The DEV push and the PROD promote are Andrew's word; rollback `b3a1d8a6`.
- Worktrees wk-69 and wk-71..77 are measured safe to remove (outer in CLOUD; portal in the candidate; only `.scratch/` untracked).
  Removal is a recursive delete held for Andrew's word. wk-70 holds the candidate and serves 5174.
