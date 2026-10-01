# DSGN_AMGTV1 -- ROUND 13 CLOSE: the drain, walk M and the render run

**Seat:** `2.0.0_SA_COO~D` (site Z). **Round:** 13, the round-12 analysis @81907cfe5f (rulings 1-3), issuance @265d39a87b
(6 orders, 3 chains, cap 8). **Written:** 2026-09-30 ~19:1xZ.

## 1. The drain -- 6 of 6 orders terminal, every instance VALID

| order | slot | portal commit -> DEV | CLOUD merge | issuer re-run |
|---|---|---|---|---|
| AV-l-2 fiscal figures carry unit and tooltip | ~50 | 4d3326ca -> 20b62fb5 | c83e48ce9c | fiscal 3/3 |
| AV-l-1 the page reads the served dossier reason | ~49 | 5f9e802a -> 032f881d | fa793b887c | dossier 3/3 |
| AV-l-3 C14 blocks cut, raw tokens gone | ~49 | b9d3eedf -> ccca64ef | 21c6a076da | c14 3/3, dossier 3/3, fiscal 3/3, bytes 3/3 |
| AV-l-4 a strip in its band is the band | ~51 | 757b0c54 | ae55273059 (chain end) | strip 3/3 |
| AV-l-5 the four designed states, one graded run | ~51 | 6f901763 | ae55273059 (chain end) | sweep 3/3 |
| AV-l-6 FWD-14..19 graded, never blind | ~51 | 5ed07150 -> 118cd005 | ae55273059 | fwd1419 3/3, rendercontrol 3/3, self-test OK |

- **Portal:** site-Z DEV went ba62e945 -> 118cd005. `tsc -b` rc=0 and ALL 16 of 16 harnesses were green after the last portal
  merge. The l-1 and l-2 merges reached origin through 0.0.0_AB_MSTR~Z (origin/DEV afa0597d, on Andrew's card 1). ccca64ef and
  118cd005 are LOCAL: origin/DEV has since moved to 29bfec2d (other seats), and ccca64ef is not in it (fetch at ~17:3xZ).
- **The ~51 outer merge (ae55273059) read "foreign 5":** five ETFS_RIVALS files staged in the shared index by
  `2.0.0_SA_COO~RV` rode into the merge commit. 2.0.0_SA_COO~RV confirmed the bytes are its own and correct (msg 27328):
  leave, no revert; its next commit records them.

## 2. The signed-out control and walk M (l-1..l-3, running page)

- **Signed-out control** (`tmp/ui-walk/20260930T162418Z`): `WALK VOID ... walker:signed-out`, exit 3 -- the instrument can see a
  sign-in page.
- **Walk M** (`tmp/ui-walk/20260930T162446Z`, 5174 @a4b81627 = CTO~Z's worktree, carrying l-1..l-3): 13 minutes, 437 shots,
  0 guard aborts, disarm REFUSED proven. 29 unique findings from 649 observations (contrast 11, timeline event layer 7,
  bands 3, raw-code 2, truncated 2, tinted status, money format, one occluded popover, one day bar). One API issue: row Z-S8.
- **Read on the shots:**
  - l-1: 6501 reads "The research team's thesis pillars: no research dossier exists for this name." and "No fund of record:
    no research dossier exists for this name." -- the served reason, not a pack claim.
  - l-2: Model rows carry their unit ("EPS (USD per share)", "Revenue (USD millions)"); the three cases read "The research
    team's Base case is not in this pack. The research team fills it in."
  - l-3: Exec "CEO public profile (Robert K. Ortberg): no public profile is on file yet."; Peers "as of September 24th, 2026"
    and "... 17 declared column(s) in the comparison map"; Posture's "Filing evidence, each side" folded; the Thesis driver
    reads "2023: 528 -- show the filing passage".
  - Against the round: for BA (and every name with a dossier) the served reasons are producer words, now faithfully shown
    (row Z-S7): "no MANAGEMENT section in class A missing or class B missing", "no report's RECOMMENDATION line names a
    fund token (IDVZ|PFOE|DIVZ)", "no class A report for this security".

## 3. The render run (l-4..l-6, graded)

`node portal/scripts/ui-contract-check.mjs --dist C:/tmp/dsgn-r13-dist/final --out C:/tmp/dsgn-r13-close-render --states-sweep`
from the shared portal at DEV 118cd005, over the page build of DEV ccca64ef (the page bytes of 118cd005; l-4..l-6 touch
`portal/scripts/` only).

- **6 of 6 states run; GRADES: PASS 63, FAIL 11, NOT_EXERCISED 0, N/A 1** (75 graded cells).
- **FWD-14..18: PASS, each with its value** -- fwd14 thesis 17 sentences / 18 passages, 0 before opening; fwd15 model 322 of
  322 numeric cells tabular, 2 refused rows, 5 absent named; fwd16 peers 12 of 12 absent columns listed, 0 in the table,
  folded; fwd17 posture comparable beside the verdict, 8 of 8 unresolved cites with an icon, 0 amber; fwd18 in all six states.
- **fourStates: PASS** (loading 6, error 6, empty 6, no-permission 1 standalone, captured) -- round 12's no-permission FAIL
  is gone (l-5). **list darkContainers: PASS** -- round 12's strip FAIL is gone (l-4).
- **fwd19_designedStates: FAIL** -- `missing: ["peers/empty (no designed branch is reachable)"]`, the order's expected page
  defect (the Peers panel has no designed empty state).
- **sizes FAIL x5 and radii FAIL x5 (the five Security states):** 5 text nodes at 10px and one 9999px radius in the shared
  header, plus Exec's 12 confirmed-dots. Both styles exist at ba62e945 (`TimelinePanel.tsx:561` YAxis fontSize 10;
  `ThesisCards.tsx:259` the rounded-full MACHINE badge; `ExecManagementTab.tsx:96` the dot). The fwd1419 DEV leg on
  ba62e945 read them PASS because ~51's worktree carried the round-12 fixtures, where the timeline was in its error state;
  l-1's refreshed fixtures draw the header timeline and the posture badge for the first time. Measured cause: an instrument
  gain, not a round-13 regression.
- **The six PNGs were read** (list, thesis, exec, peers, model, posture): the l-3 changes read as above; no count block at
  rest; no passage id, raw ISO stamp, "R-1", "CSC", "status=" or "unreadable object" on the face. What a person still sees
  as machine words: row Z-S7's producer reasons (header, Exec, Thesis, Posture); Posture's footer "the comparable bundles
  are still loading" at rest in a static render.

## 4. The channel

Round 13 added Z-W51-S1 (worker ~51, OBSERVATION: the PASS face graded as `data-verbatim-check`, the accession line as
`[data-citation-document]`), and the issuer's Z-S7 and Z-S8 (@84234c5ca6, both OBSERVATION, INERT). No BLOCKING or ARMED
row is undispositioned.
