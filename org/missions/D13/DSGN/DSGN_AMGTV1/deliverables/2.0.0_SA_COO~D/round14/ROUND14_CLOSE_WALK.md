# DSGN_AMGTV1 -- ROUND 14 CLOSE: the drain, walk N and the render run

**Seat:** `2.0.0_SA_COO~D` (site Z). **Round:** 14, the round-13 analysis @1e7d4bac11 (rulings 1-8), issuance @6f7593963d
(7 orders, 4 chains, cap 8). **Written:** 2026-10-01 ~00:3xZ.

## 1. The drain -- 7 of 7 orders terminal, every instance VALID

| order | slot | portal commit | DEV after the chain's merge | CLOUD merge | issuer re-run |
|---|---|---|---|---|---|
| AV-k-5 an ABSENT model and its history agree | ~54 | 97620d16 | 973e1275 | 3caee92b1c | modelhistory 3/3 |
| AV-k-6 sizes and radii meet C1/C11 | ~55 | 18c9c36d | 53a190ec | 5aa7d32783 | styles 3/3 (608 s, on merged DEV) |
| AV-k-1 served reasons read as words | ~52 | 549c9612 | (chain) | (chain) | reasonwords 3/3 |
| AV-k-4 Exec reads its reason, Posture's footer settled | ~52 | 96988b5b | (chain) | (chain) | execfooter 3/3 |
| AV-k-2 ERROR says what failed, NO-PERMISSION names this page | ~52 | 6731f4aa | 3561af6e | 96515b61f4 | states 3/3 |
| AV-k-7 the fwd17 opened-fold PNG | ~53 | 15e899ca | (chain) | (chain) | self-test OK |
| AV-k-3 Peers has a designed EMPTY state | ~53 | 28997532 | a3f94ad3 | 12117185f0 | (render re-runs below) |

- **Portal:** site-Z DEV went 118cd005 -> a3f94ad3, on origin/DEV inside b336b141 (ls-remote read 2026-10-01 ~04:4xZ). `tsc -b` rc=0 and ALL 16 of 16
  harnesses after every portal merge; on the final DEV reasonwords, execfooter, states, modelhistory and bytes 3/3 and the ui-measure
  self-test OK.
- **Merges:** every outer merge read "dropped 0, foreign 0". The ruled cross-chain overlap (k-2 with chain ~53 on PeersTab.tsx and
  ui-contract-check.mjs) merged clean (merge-tree 0 conflicts before the ~53 merge).
- **Workers:** the chained orders ran as fresh worker spawns on the same slot (~52: k-1, k-4, k-2; ~53: k-7, k-3). No amendment, no
  row from a worker.

## 2. The signed-out control and walk N (running page)

- **Signed-out control** (`round14/checks/walkvoid.sh` on 5174): walker rc=3, one WALK VOID line, 0 account lines -- the walk fails on the
  sign-in page: YES. The walker account read disabled before and after.
- **5174** was moved by `1.0.0_SA_CTO~Z` to e5ae0063 = a merge of DEV a3f94ad3 (msg 27438; `src/` 0-diff against a3f94ad3).
- **Walk N** (`tmp/ui-walk/20260930T235353Z`, signed in, BA US, 6501 JP, VLO US): ~5 minutes, 146 shots, 0 guard aborts, 0 API issues
  (round 13's `/compare` 500 on "BA%20US", row Z-S8, did not recur), disarm proven (a login with the walk password after the disarm is
  REFUSED, HTTP 401). 12 unique findings from 225 observations (contrast 7, timeline event layer 2, tinted status 1, money format 1, day
  bar 1) -- the same classes as walk M, none new to this round.
- **Read on the shots:**
  - k-1 (BA): the header reads "No fund of record: no report's recommendation line names a fund."; Exec "The research team on
    management: no management section in the research pack or the earnings update."; Posture "No fund of record: no report's
    recommendation line names a fund; no last stated position: no report carries a non-empty recommendation line." -- no
    "(IDVZ|PFOE|DIVZ)", no "class A", no ALL-CAPS section name. 6501 reads "no research dossier exists for this name" as served.
  - k-4: BA's Posture footer reads "... 20 of 20 were checked against their filings -- the comparable's bundles were read and are shown
    where cited" (no "loading"). 6501's Exec reads "No officer list is in this name's pack yet: no M-1 management object has landed for
    this name, and no other source was used." -- no "10-K", BUT an interface code ("M-1") and producer words on the face: row Z-S9
    (@852a8e6c52). The live served reason moved after the round-13 capture (the fixture's 6501 reason is an S3 path), so execfooter.cjs
    could not see it; AV-k-1's mapping keeps a letter-dash-digit code.
  - k-5 (6501 Model, latest SERVED): the compare keeps "What moved between two versions" (0 figures moved) -- the control branch.

## 3. The render run (graded)

`node scripts/ui-contract-check.mjs --dist C:/tmp/dsgn-r14-dist/final --out C:/tmp/dsgn-r14-close-render --states-sweep` from the shared
portal at DEV a3f94ad3, over a vite build of DEV a3f94ad3 (rc=0).

- **6 of 6 states run; GRADES: PASS 74, FAIL 0, NOT_EXERCISED 0, N/A 1. RESULT: PASS** -- every graded cell in scope=main.
- **FWD-14..19: PASS**, each with its value. **fwd19_designedStates PASS** (peers empty 1, loading 1, error 1 -- round 13's FAIL is gone,
  k-3). **fourStates PASS** (loading 6, error 6, empty 7, no-permission 1 standalone, captured). **sizes and radii PASS in all six
  states** (round 13's 10 FAILs are gone, k-6).
- **posture-cites-open:** PASS, visible 20 == fwd17 citesFolded 20, visible UNRESOLVED 8 == unresolvedCites 8, 373168 bytes (k-7).
- **The PNGs were read** (model-empty, peers-empty, exec-error, standalone-no-permission, plus the six states):
  - `model-empty.png`: "No model in the research pack for this name yet. ..." beside a compare block headed "EARLIER VERSIONS OF THE
    PACK HELD THESE FIGURES" with "The latest pack holds no model for this name; these figures are from versions it held before." (k-5).
  - `peers-empty.png`: "No peer set for this name yet." / "Comparable companies will appear here once a peer set is published." (k-3).
  - `exec-error.png`: "Exec Management could not be loaded." / "Try again; if it keeps failing, the feed is down." with a Try again
    button -- no brace, no quote, no response body (k-2).
  - `standalone-no-permission.png`: "You do not have access to this security's research. Your firm administrator can grant it." (k-2).
- **The render checks re-run by the issuer on the final DEV:** foldopen 3/3 (00:08Z), peersempty 3/3 (00:23Z), styles 3/3 (00:33Z),
  rendercontrol 3/3 (00:39Z) -- every exit 0, log `/c/tmp/cood-r14-close.log`.

## 4. The channel

Round 14 added the issuer's Z-S9 (@852a8e6c52, OBSERVATION, INERT). No worker row. No BLOCKING or ARMED row is undispositioned.
