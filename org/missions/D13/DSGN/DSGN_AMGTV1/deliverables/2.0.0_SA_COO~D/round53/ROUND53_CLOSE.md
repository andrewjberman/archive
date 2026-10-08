# DSGN_AMGTV1 -- ROUND 53 CLOSE (issuer 2.0.0_SA_COO~D, 2026-10-08 ~22:3xZ)

**Round:** decomposition v53, issued @28e9169504. Three cells, three orders, all complete:
- AV-zze-1 (SAUX-41, FWD-27), the Seeking Alpha column: slot ~115, portal d3e2d791, drained @9772d8623f.
- AV-zze-2 (SAUX-42 + SAUX-43, FWD-4), the segment table and the five research-note sections: slot ~116, portal 2b8cbe4c, drained @be7e764945.
- AV-zze-3 (the built thing's name in postureCites.ts, direct act): slot ~117, portal 2c8562a0, drained @c1506ea72e.

Each proof instance reads VALID (rc=0) when checked from inside its own worktree.
`round-close-check.py --project DSGN_AMGTV1 --round 53` reads MAY-CLOSE: 3 of 3 orders, proofs 3 ok / 0 bad, 0 judgment criteria.

## The candidate

Portal branch `dsgn-amgtv1-r53-candidate` at **84e13d0f**: base DEV 38cc0ecf + 2b8cbe4c + be3c3547 (cherry-pick of d3e2d791) +
84e13d0f (cherry-pick of 2c8562a0). 9 files, product and harness. DEV is still 38cc0ecf (ls-remote read ~22:2xZ), so the candidate
fast-forwards DEV.

Read on the candidate (slot ~116 tree):

| check | result |
|---|---|
| `round53/checks/r53a.cjs` | 3 of 3 |
| `round53/checks/r53b.cjs` | 4 of 4 |
| `round53/checks/r53c.cjs` | 3 of 3 |
| `round51/checks/r51a/r51a.cjs` (prior round, still holds) | 4 of 4 |
| `round52/checks/r52/r52.cjs` (prior round, still holds) | 3 of 3 |
| `round29/checks/battery29.sh` | ALL PASS (0 skipped): 14 of 14 harnesses, tsc rc=0, eslint rc=0 |
| `bun test src/pages/Freshness/Freshness.test.tsx` | 18 pass, 0 fail |

## The one real run

`round53/walk/walk53.mjs` (round 35's walk head + `walk53.tail.mjs`; built by `build_walk53.py`) ran against a local build of
84e13d0f (`bun run dev:live --port 5174`) talking to the live function. The walker account was armed and then disarmed (login refused
after the disarm). Port 5174 had 0 listeners before the run and 0 after it.

Output: `round53/walk/read-20261008T222437Z/`. READS 7: PASS 7, FAIL 0, ERROR 0.

- AMD US, segment: 6 rows x 5 columns as served, 6 operating rows; "Source: Bloomberg product segments, pulled October 7th, 2026".
- AMD US, sections: 5 of 5 in order, all absent; each prints its served reason.
- ASML NA, segment: 12 rows x 5 columns as served.
- ASML NA, sections: 5 of 5 served, each with one closed opener.
- NU US, segment: the served reason is drawn ("No Bloomberg segment table has been stored for this name yet.").
- NU US, sections: 3 of 5 served, 2 absent.
- /freshness: 95 of 95 rows carry the served state and sentence (no_record 67, checked 15, read 13); 0 cells print "Not collected".
  Examples: Lenovo 992 HK "Seeking Alpha last read 2026-09-22."; Hon Hai 2317 TT "Seeking Alpha was checked on 2026-10-05 and no
  article is held for this company."; AIA Group "No Seeking Alpha collection record is held for this company yet."

The issuer looked at the screenshots: `r53-AMD-US-thesis.png`, `r53-ASML-NA-thesis.png` and `r53-freshness.png`. On white, in navy
ink, the page shows:
- the notes block under the pillars;
- the revenue and operating-income tables with grouped column notes;
- the source line;
- the filing segment prose below.

## Surfaced at the real run (rows, all OBSERVATION / INERT)

- **DSGN_AMGTV1-Z-S24** (disarm_owner 2.0.0_SA_COO~Z). AMD's served filing-segment reason still says "A segment table with figures needs
  a separate segment data pull". It is drawn directly under the table that now exists. The text is the producer's.
- **DSGN_AMGTV1-Z-S25** (2.0.0_SA_COO~D). On /freshness, the day cells wrap now that the Seeking Alpha cell carries a sentence. This is
  cosmetic.
- **DSGN_AMGTV1-Z-S26** (2.0.0_SA_COO~D). The Freshness column header "Research pack" names the built analysis. This is the same class
  as AV-zze-3.

## Own defects this round

- The three orders said the files were CRLF. They are LF at 38cc0ecf; `grep -c $'\r'` counted every line. Each worker kept the file's
  real line endings.
- The order for AV-zze-2 promised "four fixed words" and then listed five phrases.

## Next

1. CTO review of candidate 84e13d0f.
2. ONE DEV push on Andrew's word, by the integrator.
3. Rows S25 and S26 are candidates for the next DSGN round. S24 goes to AMGT_RESAPP's issuer.
