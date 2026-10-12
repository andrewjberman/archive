# IRPT_BCKEND rounds 142, 143 and 144, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-11 ~19:3xZ. To: 3.0.0_SA_CVO. Four orders, all terminal, all READ ONLY.
`python .tools/round-close-check.py --project IRPT_BCKEND --round <n> --workstream "~P"` reads `verdict=MAY-CLOSE` for 142, 143
and 144 (judgment=0 each). Each criterion was re-run by the issuer at box HEAD after the merge and passes; all four proofs read
VALID. Nothing is built, re-graded or served by any of them; no class is admitted; no request was made to the vendor; no AWS
write was made.

| round | order | what it read | drained | criteria on the issuer run |
|---|---|---|---|---|
| 142 | IB-pr-445 | the unmoved-bar guard measured: the overlap table under it, three sizings, its cost (FWD-13) | @7d31765674 | 3 of 3 PASS |
| 143 | IB-pr-446 | the capture probe's transport, a job's calls after a capture, what changed since 2026-10-05 (FWD-4) | @cbb945d141 | 3 of 3 PASS |
| 144 | IB-pr-447 | does the running intake poller read the firm registry; from the live package's bytes (FWD-9) | @ac97d216b9 | 3 of 3 PASS |
| 144 | IB-pr-448 | the live poller package's version id among its artifact key's versions (FWD-9); applier 0.7.0_AE_CloudOps~IB2 | @804e22b7a9 | 3 of 3 PASS |

Every count below is the worker's or the applier's; the issuer re-ran the checks, not the measurements.

## Round 142 -- the guard (record `deliverables/0.9.0_WK_IRPT_BCKEND~303/IB142-1_UNMOVED_BAR_GUARD_READ.md`)

- Reproductions hold: guard off equals IB-pr-441's Table 1 (894 securities, 64,536 security-days, equal 63,720, one day off 5,
  neither 499, no bar 312); the seven-type sizing with no guard equals IB-pr-442's (blank 50.305 percent, never served 357,
  freed 5,666).
- Under the guard: equal 62,649; one day off 0; neither 440; no bar 312; not graded 1,135 (1.76 percent). All five earlier
  one-day-off days are not graded; on each the reader repeats the prior bar while the anchor moves.
- Sizing over 76,796 account-days: seven types under the guard, blank 51.753 percent, never served 357, freed 5,114 (552 fewer);
  seven plus the institutional class under the guard, 46.298 percent, 283, 10,164.
- Six institutional securities outside the first witness are un-graded on more than half their days (79 of 85 at worst); no
  admitted-type security is.
- Rows: `IRPT_BCKEND-D2-W303-S1` (to the cent is not the stricter reading), `-S2` (under the guard every type's one-day-off
  column is empty, so that column no longer discriminates).
- What followed: PRD v0.40 (guard adopted, institutional class not admitted, admission test read with the guard off) and v0.41
  (no prior bar, no grade), both signed. IB-pr-449 (round 145, the first moved bar after a repeated run, with v0.41's count) and
  IB-pr-450 (round 146, the guard as one pure function, nothing served) are issued and running; they are not in this packet.

## Round 143 -- the probe's transport (record `deliverables/0.9.0_WK_IRPT_BCKEND~304/IB143-1_PROBE_TRANSPORT_READ.md`)

- `node-port` is Node's built-in https client inside the capture process, sending cookies copied from the browser's jar; it is
  not the browser. The code states its reason (`ycharts_session.js:291-300`): it stands for the resident's client class. It is a
  different program from the replay's Python urllib client; whether the two look alike to the vendor has no record.
- A generation after a capture makes 12 vendor calls, all by Python urllib (10 with the stored cookies, 2 with none), none by
  node-port or the browser. Whether they would meet the probe's refusal: not told (claim absent). The Python read path was
  answered with a firewall challenge on five days, 2026-09-29 to 2026-10-05, on the status route.
- The probe, its transport, headers and reply classification are byte-identical from 2026-09-24 to HEAD. The one capture change
  is the new failure branch and kept receipt (st32, 2026-10-11), which did not fire. No release moved the host library between
  2026-10-03 and st32.
- **A correction to the issuer's own face:** it said captures worked until 2026-10-05. Not supported: that time is the secret's
  last change, which the resident also writes on a cookie rotation; a successful capture writes no journal line; the last
  recorded automated sign-in success is 2026-10-02. Rows `IRPT_BCKEND-D2-W304-S1` to `-S4`.
- Nothing is proposed about how the vendor is reached. The CTO has put that question to Andrew; the vendor path stays stopped.

## Round 144 -- the intake poller (records `deliverables/0.9.0_WK_IRPT_BCKEND~305/IB144-1_POLLER_FIRM_REGISTRY_READ.md`, `deliverables/0.7.0_AE_CloudOps~IB2/IB144-2_poller_rollback_artifact.json`)

- The live package was read by its bytes (its digest equals the function's CodeSha256; 28 members). `firm_registry.json` is a
  member and an environment variable points at it. The code opens it at `keys.py:293`.
- Reached at run time: false, measured by reading the call path, nothing exercised. The handler builds `LiveTransport`, whose
  constructor raises on every path (`graph_client.py:240`), and returns at `poller.py:492` before `run_scan` (`:503`); every
  registry read sits below `run_scan`.
- A release that drops the file: NO_EFFECT, inferred, and only while that refusal stands; a reached read would raise.
- The canon holds all six fields the code takes (`infra/logic/registry/scopes.json`). The live file parses equal to the tree's
  generated `data/firm_registry.json`; the bytes differ by one generated key. Rows `IRPT_BCKEND-D2-W305-S1`, `-S2`.
- The rollback artifact: FOUND, nothing written. One of the two versions of the function's artifact key holds the live bytes
  (digest by content equals CodeSha256); its version id is recorded. The bucket's only lifecycle rule aborts incomplete
  uploads; no rule expires a noncurrent version. It is a rollback target, not a rebuild path: row `IRPT_ANLREQ-D2-W53-S3` stands.
- The issuer read the CTO's "saved once" narrowly and said so on the order's record face: where a version already holds the
  live bytes, recording its id is the save and no second copy is made.
- The release of the poller is not cut. The result is with the CTO.

## Judgment criteria

None in these rounds.
