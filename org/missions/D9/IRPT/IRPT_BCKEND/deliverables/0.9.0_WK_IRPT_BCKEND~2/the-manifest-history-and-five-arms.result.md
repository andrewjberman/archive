# IB-rte-5 RESULT -- THE MANIFEST HISTORY CENSUSED, FWD-7's FIVE ARMS DRIVEN, THE FRESH-DISPATCH CASE MEASURED

**TO:** `IRPT_BCKEND.TO-IB-rte-5` | **serial:** `0.9.0_WK_IRPT_BCKEND~2` |
**branch:** `wk-irpt_bckend-5-2` | **worktree:** `/c/tmp/wk-irpt-5-2` | **base:** `391e4ad948`
**Battery:** `battery_ib_rte_5.py` (git hash-object `200da4f476beadaeaeeb14a27693187fed43d303`)
**Battery output:** `IB-rte-5_R55-AC1_battery_output.txt` (git hash-object `153add6cbcc41daf7ff5ab2631110c280aeacec4`)
**Detail JSON:** `IB-rte-5_full_census_and_arms.json` (git hash-object `7ae93f1cf2692c67fef137876d07d2d7f4b23b99`)
**Result:** `rc=0`, **16 of 16 graded checks PASS**, token `IBR55-MANIFESTS-CENSUSED-AND-FIVE-ARMS-DRIVEN`.
**R55-AC1 = PASS-by-output.** R55-AC2 recorded below for `3.0.0_SA_CVO`.

Every count below is RE-DERIVED live against S3/Lambda/SSM on every battery run -- nothing is
read from a prior run's own output (bound 12). READ-ONLY throughout: no manifest rewritten, no
directory written, no source fixture placed in a live source prefix, no apply, no deploy, no IAM.

---

## (a) THE CENSUS -- rtd-2's own Q2, closed

**Instrument correction made before this could be answered.** rtd-2 left Q2 unrun because
answering it from the CURRENT object at each key cannot see whether an earlier COMPLETED-family
manifest was overwritten -- and one was (below). All three destination buckets
(`opal-data-bd`, `opal-data-cot`, `opal-data-inf`) carry `Versioning: Enabled`
(`battery a0`, confirmed live) and no lifecycle rule has yet purged a version (noncurrent-version
expiry is 14d on cot/inf and 90d on bd; this project's whole history is <7 days old) -- so
`s3api list-object-versions` on `investor-reporting/directory/_refresh/` returns the FULL,
un-purged write history of every manifest key ever touched, not just the current object. That is
the population this census reads.

**M = 84 of 84 manifest-object-VERSIONS fetched and parsed without error** (28 per firm across 6
keys each; `battery a2`), spanning every fire since this project's genesis (`2026-09-12T08:49:30Z`,
the oldest version on record for any key, confirmed no lifecycle purge has run) through the current
moment. `a3b` confirms 0 of 84 same-date re-writes carry inconsistent `prev`/`cur` values (a later
fire re-landing byte-identical content at an unmoved frontier re-writes the same manifest with the
same counts every time -- collapsed to ONE chain position per distinct business date before the
misstatement check runs, or every one of the ~8 repeated re-writes per key would false-positive
against itself).

**The re-derived chain, per firm, under the FIXED previous-state rule** (`last_manifest()`,
`refresh.py:225-257 @c4ec6e4984d30d61b5a6b1cf6dd4615e430e2294`, the byte-identical, currently-served
module): 5 distinct completed-family business-dates exist across all 3 firms, in 2 chains:

| firm | date | reason_code | prev | cur | first-ever? | correct? |
|---|---|---|---|---|---|---|
| 49financial | 2026-09-16 | REFRESH_COMPLETED_WITH_ADDITIONS | 0 | 4562 | YES | prev=0 correct (no earlier completed-family write exists anywhere in 49financial's full 28-version history) |
| 49financial | 2026-09-17 | REFRESH_COMPLETED_WITH_ADDITIONS | 4562 | 4576 | no | prev=4562 == prior date's cur=4562, correct |
| cottonwood | 2026-09-16 | REFRESH_COMPLETED_WITH_ADDITIONS | 0 | 248 | YES | prev=0 correct (no earlier completed-family write exists anywhere in cottonwood's full 28-version history) |
| cottonwood | 2026-09-17 | REFRESH_COMPLETED_WITH_ADDITIONS | 248 | 249 | no | prev=248 == prior date's cur=248, correct |
| inflection | 2026-09-17 | REFRESH_COMPLETED_WITH_ADDITIONS | 0 | 291 | YES | prev=0 correct (no earlier completed-family write exists anywhere in inflection's full 28-version history) |

**k = 0 of 5. Q2 CLOSES: no manifest, anywhere in the full un-purged version history of any of
the 3 firms, misstates previous state.** Every `prev=0` write is the firm's genuine first-ever
completed build, not a pre-fix-masked one -- verified by walking every version of every key back
to this project's own genesis timestamp, not merely reasoning from what the current object shows.
**No reconciliation is declared** because none is needed.

**Mutant control on the detector itself (`battery a5`):** a k=0 real-world result is worth
nothing if the detector cannot also return k>0 on a chain that genuinely misstates. The same
`find_misstating()` function graded against two synthetic chains, neither touching AWS: a clean
one (0 misstating, as expected) and one with a genuine gap planted at the second date (`prev=0`
where the immediately preceding date's `cur=100` -- row W2-S57's exact symptom, reproduced on a
chain that DOES have a real prior) -- 1 of 1 planted defects caught, reason text matches. FIRED
AS EXPECTED.

**A finding surfaced by the deep read that a current-object-only census could not have seen** (not
filed as a new row -- it changes no served artifact and the design is sound, reasoned through
below): inflection's ORIGINAL `REFRESH_COMPLETED_WITH_ADDITIONS` manifest at the `2026-09-17` key
(`prev=0, cur=291`, written `2026-09-18T09:06:23Z`, PRE-fix-R1) is no longer the CURRENT object at
that key -- eight subsequent `REFRESH_NOOP_SAME_FRONTIER` re-fires overwrote it in place, because
`new_manifest()` keys a NOOP write by the SAME date the runner already accounted
(`refresh.py:877-894`). The CURRENT object at that key therefore carries no entry counts at all.
This is not a defect: `REFRESH_NOOP_SAME_FRONTIER` is itself a member of
`PREVIOUS_STATE_REASON_CODES` (`refresh.py:217-222`) and its own delta still carries the real
`directory_key` (`refresh.py:886-888`), so a future fire's `previous_entries()` still reads the
real artifact via that key (`refresh.py:773-777`), never via the manifest's own (absent) count
fields -- the design already accounts for exactly this overwrite pattern. cottonwood's and
49financial's 09-16 keys were NOT overwritten this way only because a SECOND, distinct completed
date (09-17) exists for them and NOOP re-fires since have landed at the LATER date's key instead.

---

## (b) THE FIVE ARMS -- driven, 5 of 5, against the CURRENT deployed bytes

**Binding (R-40):** the deployed `CodeSha256` at T0 is
`q7O3GGjK2PBHkNo6KfJOAVaJhUW4cwxtWQFZgTqSO/o=` (read `2026-09-18T21:12:27Z`), equal to
`lambda-source-map.json`'s registered `artifact_sha256` for `irpt-directory-refresh`
(`battery b2`). `git log 91faa85f41..HEAD -- refresh.py expiry.py handler.py` returns 0 commits
(`battery b1`) -- the repo's `refresh.py` (git hash-object
`c4ec6e4984d30d61b5a6b1cf6dd4615e430e2294`) and `expiry.py` (git hash-object
`811545e8ce77c3d924b2c355174109d06968cec4`) are BYTE-IDENTICAL to what is currently deployed.

**PLANE:** the controlled-clock harness (`ib_s_4_controlled_clock.py`, git hash-object
`1258192be10a543402feaafaf620019e449eaedd`) calls `refresh.refresh_firm` / `refresh.serve_read`
IN-PROCESS -- never a copy, never a wrapper (bound 12) -- against those same, currently-deployed
bytes. The deployed Lambda itself is never invoked for this half: `refresh_firm`'s `now`,
`build_fn` and S3 client are all injectable BY DESIGN (`refresh.py:984-996`'s own docstring: "the
controlled-clock harness drives the identical code path with no AWS and no real-calendar wait"),
so the in-process plane is the CORRECT one for a driven arm and the live-Lambda plane is reserved
for (a)'s real reads and (c)'s real accounting checks.

**5 of 5 arms fired, 5 of 5 distinct reason codes, 5 of 5 distinct (state, code) pairs, 1.393s
wall clock, no sleep, no network, no vendor call** (`battery b3-b7`):

| arm | reason_code | state | observable |
|---|---|---|---|
| (a) ADDED CLIENT | REFRESH_COMPLETED_WITH_ADDITIONS | READY | new client present, added=1, nobody asked |
| (b) CHANGED ELIGIBILITY | REFRESH_COMPLETED_WITH_ELIGIBILITY_CHANGE | READY | eligibility_changed=1, disappeared=0, terminated client STILL VISIBLE |
| (c) MISSED TRIGGER | REFRESH_TRIGGER_MISSED | UNCERTAIN | 3 expected trading days carry no manifest; not papered over |
| (d) FAILED REFRESH | REFRESH_FAILED | FAILED | build raised RuntimeError; exception text withheld from the manifest |
| (e) OVER-AGE REQUEST | DIRECTORY_OVER_AGE | STALE | 4 trading days behind a ceiling of 2; last_good_as_of carried, RETRY+WAIT offered |

The trading calendar is REAL (`calendar_source=NYSE/pandas_market_calendars`, `battery b7`) --
the arms are driven against the actual NYSE frontier via injected `now`/fixture values, never
against a real-calendar wait.

---

## (c) THE FRESH-DISPATCH CASE -- measured, named, NOT driven (0 of 1)

**What a scheduled fire needs to perform a FRESH SSM dispatch:** `SsmBuildDispatcher.__call__`
(`refresh.py:710-771`) only reaches its dispatch branch (step 3) when NEITHER of the first two
steps short-circuits it: (1) no in-flight or unresolved prior command, and (2) the runner's own
pointer does NOT already name the artifact this fire has accounted for. In practice that means the
firm's real gold/silver SOURCE must have produced a genuinely NEW completed business date beyond
what is already landed.

**Measured live, read-only, right now (`battery c1`):** the real trading calendar's
`expected_last_trading_day` is `2026-09-18` (today itself), but all three firms' actual, LANDED,
accounted business date is still `2026-09-17` -- T-1, per the estate's own convention
(CLAUDE.md NEVER-4). For each firm the battery read (i) the CURRENT pointer
(`investor-reporting/directory/latest.json`, a real GET) and (ii) the CURRENT
`_refresh/2026-09-18/manifest.json`'s recorded `ssm_command_id`, then (iii) that command's REAL,
LIVE status via `ssm:GetCommandInvocation` (a READ, never a send):

| firm | accounted date | pointer key | recorded cid (stale, pre-fix) | live status | would land |
|---|---|---|---|---|---|
| 49financial | 2026-09-17 | `.../2026-09-17/directory.json` | `df2054c5-...` | Success | REFRESH_NOOP_SAME_FRONTIER |
| cottonwood | 2026-09-17 | `.../2026-09-17/directory.json` | `d30f42e3-...` | Success | REFRESH_NOOP_SAME_FRONTIER |
| inflection | 2026-09-17 | `.../2026-09-17/directory.json` | `e0f6a54c-...` | Success | REFRESH_NOOP_SAME_FRONTIER |

**3 of 3 firms: the deployed dispatcher's own real accounting would land on
`REFRESH_NOOP_SAME_FRONTIER` for every firm if invoked for real right now** -- exactly what every
fire since IB-rtc-7 has already found (rtd-1, rtc-3 AMENDMENT 3). A fresh dispatch is not
currently reachable through the honest, unmodified mechanism.

**Even setting that aside, the controlled clock CANNOT drive a fresh dispatch without a
destination-bucket write, and this is unconditional, not merely likely (`battery c2`).**
`runner_script()` (`refresh.py:522-593`) is HARD-CODED to end
`python3 $R/directory_runner.py --firms <firm> --upload` -- `--upload` is literal, present in
every recipe this dispatch ever sends, and no `--dry-run` branch exists in `refresh.py`'s own
recipe (verified by direct source inspection: `"--upload"` present, `"--dry-run"` absent from
`refresh.py`, even though `directory_runner.py` itself supports `--dry-run` -- the deployed
DISPATCH never offers it). `SsmBuildDispatcher.dispatch()` (`refresh.py:664-707`) sends a REAL
`ssm:send_command` to the real, already-running host (`i-02448edb624a7a7cf`); once sent, the host's
own build performs a real `s3:PutObject` of `directory.json` and `latest.json` to the firm's
destination bucket, entirely outside this cell's Python process and outside this cell's ability to
stop it (past builds on this same host completed in 9-14 seconds per the SSM transcripts already
on record in this project -- IB-rtc-3's own result). This order's READ-ONLY bound forbids exactly
that write, and this cell cannot decouple "send the command" from "the command uploads" because
the recipe it sends is not this cell's to edit (it is `refresh.py`'s, deployed, and outside this
cell's mandate to change for this measurement).

**CONCLUSION: BLOCKED, NAMED, NOT DRIVEN. 0 of 1 new command ids driven.** The exact blocking
write: `s3:PutObject` on the firm's destination bucket (`directory.json` + `latest.json`),
performed by the host's own `directory_runner.py --upload` step, an unavoidable consequence of
`ssm:SendCommand` once issued. This is the measurement the order asks for when driving is not
possible -- not a gap in this cell's work.

---

## R55-AC2 -- JUDGMENT, FOR `3.0.0_SA_CVO`, NO VERDICT

**Is FWD-7's DONE WHEN (EXERCISED on a controlled clock, all five arms, no real-calendar wait)
now met as written, or what remains?**

The controlled-clock half is fully met: 5 of 5 arms fired this round, 5 of 5 distinct reason
codes, against the CURRENT deployed bytes (bound by `CodeSha256`, `part_b` above), with no sleep,
no network, no vendor call (`ib_s_4_controlled_clock.py`, unchanged since round 1,
git hash-object `1258192be10a543402feaafaf620019e449eaedd`). What remains, if the CVO reads
"EXERCISED" as requiring the LIVE deployed Lambda itself (not the in-process harness) to produce
all five outcomes: only THREE of the five have ever been observed on the live path --
`REFRESH_COMPLETED_WITH_ADDITIONS` (IB-rtc-3/rtd-1, live, real), `REFRESH_NOOP_SAME_FRONTIER`
(IB-rtd-2, live, real), and `REFRESH_FAILED`'s hand-over-failure variant
(`W2-S49`/`W2-S53`'s `AccessDenied`, live, real). `REFRESH_TRIGGER_MISSED` and a live
`REFRESH_DISPATCHED`-then-genuinely-new-build have never fired on the real schedule, and per
part (c) above, cannot be forced onto the real path without either a real calendar advance (a
wait) or a forbidden bucket write. That gap is a property of the WORLD (the source data has not
yet lagged three days, and the frontier has not yet advanced past what is landed), not of this
cell's instrument -- it was already named in these terms by rtd-1's own R41-AC2.

**Is the manifest history sound as the missed-trigger detector's input?**

Yes, as far as this cell's census can determine. Q1 (rtd-2's own, partially answered) concerned
whether `_last_recorded_business_date`'s lack of a `not_before` bound could let a stray old write
shift `missed_business_dates`; this cell's full-version census found NO such stray write in the 84
versions read (every version at every key is either a genuine, chronologically-ordered fire record
or a byte-identical re-landing of one), so the residual risk rtd-2 flagged remains theoretical
and unexercised in this population, not confirmed absent in general. Q2 (this cell's own charge)
is now definitively closed at k=0: no manifest anywhere in this project's full history misstates
previous state, so the detector's input is sound for every date this project has ever recorded.

**Does the fresh-dispatch case need a design change (a driven reset) or only patience?**

Only patience for the case actually observed today (the source frontier has not advanced past
09-17 for any firm) -- no design change is indicated by anything this cell found: the
`same_frontier` gating is working exactly as designed (`W2-S57`'s own fix), and the manifest
history it reads is sound (above). If the CVO wants a LIVE, driven observation of a genuinely NEW
dispatch without waiting on the real calendar, that would require a design change this cell's
`<paths>` grant does not cover: either a `--dry-run`-capable recipe variant reserved for
non-production exercises, or an isolated test host/bucket pair outside the three live firm
buckets -- both are standing-moratorium-adjacent (a shadow/parallel pipeline) and neither is this
cell's call to make.

---

## FILES

`battery_ib_rte_5.py`, `IB-rte-5_R55-AC1_battery_output.txt` (token
`IBR55-MANIFESTS-CENSUSED-AND-FIVE-ARMS-DRIVEN`, 15/15 PASS, rc=0),
`IB-rte-5_full_census_and_arms.json` (the full per-firm chain + arm + fresh-dispatch detail this
result summarizes).

## BOUNDS HONOURED

READ-ONLY throughout: every AWS call this cell made is `list-object-versions`, `get-object`,
`get-bucket-versioning`, `get-function-configuration`, or `ssm get-command-invocation` (all
reads); no `put-object`, no `send-command`, no `terraform apply`, no IAM change. No code file was
edited. Every invocation ran under a bound (`subprocess.run(..., timeout=...)` throughout the
battery; the battery itself under `timeout 1800`).

## SURPRISE ROWS FILED

None. Every finding in this result answers a clause this order itself names (Q2's census, the
five arms, the fresh-dispatch measurement); nothing surfaced a premise that failed, a path
elsewhere, an invocation that failed to produce its named result, or a capability this cell
lacked. (The `.tools/aws` bash shim is not directly executable from a native-`py` subprocess on
this box -- `.tools/aws.cmd` is the ALREADY-DOCUMENTED companion for exactly this caller class,
per its own header comment, so this is a known mechanism this cell used correctly, not a surprise.)
