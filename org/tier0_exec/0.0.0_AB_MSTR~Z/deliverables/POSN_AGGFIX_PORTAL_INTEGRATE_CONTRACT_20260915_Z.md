# POSN_AGGFIX portal /integrate -- the agreed contract between the two MSTRs

- author: `0.0.0_AB_MSTR~Z`
- peer: `0.0.0_AB_MSTR` (laptop)
- date: 2026-09-15, agreed 22:07Z-22:16Z
- authority: Andrew-direct, relayed: *"see POSN_AGGFIX through to validated completion. At that
  point, have MSTR~Z coordinate on a portal repo /integrate merge so the repo updates are included
  on both fabrics. | Once this is done, you may run a /prod-deploy."*
- why this file exists: the agreement was reached on the agent bus, and **a bus body lives only in
  the receiving session's Monitor output file**. It is recoverable while that session lives and is
  not claimed to survive session end. The contract has to outlive a session death on either box, so
  it is committed here. The MCP half of the exchange is durable by construction (`org/mcp/inbox/`);
  the bus half is not, and that is the half this record carries.

## The object

| field | value | how it was read |
|---|---|---|
| branch (portal repo) | `sitez/aggfix-1-portal` | `git ls-remote --heads origin` |
| head at this writing | `3ec1f83cabb1780d4468c4f80fd16453df800f00` | equal to local `refs/drains/aggfix-1-portal` |
| base | `edf85ce503aad961b84b5ea3b2074eb84d416a16` | `git merge-base <drain> origin/PROD`, and `--is-ancestor` YES |
| base identity | `1.0.0_SA_CTO~A`'s DEV->PROD merge, 2026-09-15T08:03:58-04:00, DEV `9adad7ce` | `git log -1` |
| content | 2 commits by `0.9.0_WK_POSN_AGGFIX~3` (TO-B1-1, TO-B2-1), 5 files, +370/-44 | `git diff --stat origin/PROD <drain>` |

The base was verified **against the ref**, not adopted from the decomposition's s.1.4. The
decomposition's claim is confirmed, not assumed. `2.0.0_SA_COO~Z`'s citation of `3ec1f83c` and
`PORTAL_REFS.md`'s `refs/drains/aggfix-1-portal` resolve to the SAME OBJECT; there was no
ref-name discrepancy.

## The assessment (vintage `3ec1f83c` / DEV `acdb02e917f5`, 2026-09-15 22:0xZ)

- overlap set: **0 files of 7 touched** (5 drain under `src/`, 2 DEV under `.github/workflows/`) = 0.0%
- `origin/PROD..origin/DEV` = 1 commit, `acdb02e9` (`1.0.0_SA_CTO~A`, project-reference-aware portal
  typecheck), touching `ci.yml` and `promote-to-prod.yml` only
- `git merge-tree --write-tree --name-only origin/DEV refs/drains/aggfix-1-portal` -> rc=0
- **the discriminating read, because rc=0 only says "no conflict":** the drain is PROD-based and
  `origin/PROD` is NOT an ancestor of `origin/DEV` (`DEV..PROD` = 25 commits, every one of them a
  DEV->PROD merge commit -- this repo's normal shape back to 2026-07-29, not a defect). Merging a
  PROD-based branch into DEV therefore drags that spine in, so the RESULT TREE was measured:
  - `T = de013cf176b703d6e21bf1a27a724f10ef36bcaf`
  - `git diff --stat origin/DEV $T` -> exactly the 5 Positioning files, 370 insertions, 44 deletions.
    **The 25-commit spine carries ZERO tree content into DEV.**
  - negative control: `git diff --stat <drain> $T` -> `ci.yml` + `promote-to-prod.yml`, 2 files. The
    instrument does show DEV's side when DEV's side differs, so the empty result is a measurement.
- corroborating grain: the drain's five files are byte-identical on `origin/DEV` and at the promoted
  tip `9adad7ce`.
- laptop side, answered 22:12Z: **no** laptop portal branch carries unmerged work
  (`codex/cto-a-portal-typecheck-20260915` is at `acdb02e917f5`, the object DEV already carries);
  `origin/DEV` agrees; nothing held back from travel.
- the laptop independently ran `merge-tree` and landed on the SAME tree oid. **It stated, before this
  seat could, that this is the same instrument on a different box -- agreement on the bytes at this
  vintage, NOT independent corroboration of the method.** That qualifier is accepted and recorded
  rather than the agreement. A genuinely different instrument would be a real merge in a throwaway
  worktree diffed against DEV; it was not run, and the reason is stated: overlap 0 with a printed
  denominator and a negative control that fires is sufficient for an act changing 5 files no one
  else touched.

## What "both fabrics" means here

The portal repo has **no CLOUD/SITEZ analogue** -- both fabrics push to one origin with `DEV` and
`PROD` as the shared trunks. So the act that puts this on both fabrics is the **merge into DEV**,
not a cross-branch reconcile. The cross-branch reconcile is the WORKSPACE repo, and **Andrew's
portal sentence does not release the site-Z workspace push hold** (391+ local commits). Agreed by
both MSTRs and by `1.0.0_SA_CTO~Z`.

## The contract

| step | owner | condition |
|---|---|---|
| gate | `1.0.0_SA_CTO~Z` | sends a message beginning **"POSN_AGGFIX step 2 due"**, stating every order terminal in every round, the CVO slug landed, its L10 grading REALIZED every outcome gradable before the promote, and the exact ref and head. **Nothing else starts (b)** -- not a COO drain notice, not this seat's own read of the ref moving, not a request from the laptop. |
| pre-(b) | `0.0.0_AB_MSTR~Z` | re-read `refs/drains/aggfix-1-portal`; **re-push** `origin/sitez/aggfix-1-portal` to that head; re-run the whole pass at that vintage (merge-tree, result-tree diff vs `origin/DEV`, negative control). |
| (b) | `0.0.0_AB_MSTR~Z` | merge `sitez/aggfix-1-portal` into DEV and push DEV. **The laptop MSTR will NOT push DEV in that window** (agreed 22:14Z), which is what keeps ONE resolution and ONE actor and avoids a non-fast-forward race. Pushing DEV fires `ci.yml`; expected. |
| post-(b) | `0.0.0_AB_MSTR` | read `origin/DEV`, diff against the pre-push head it names, confirm the change is exactly the Positioning files, and report **before** (c) starts. It also undertakes to tell this seat at once if DEV moves on the laptop side before step-2-due, so the re-run uses the right base. |
| (c) | `1.0.0_SA_CTO~Z` | `/prod-deploy` (the DEV->PROD promote). **Not an MSTR act.** That seat will read BOTH copies of `promote-to-prod.yml` first and name which one runs. |

DEV is a shared branch, so (b) is an MSTR act by LD-0367/LD-0368.

## The hazard this seat created, disclosed unprompted to both parties

`origin/sitez/aggfix-1-portal` is a **SNAPSHOT at `3ec1f83c`**, pushed 22:0xZ, ahead of validated
completion. `POSN_AGGFIX` TO-B3-1 is still open and a round 2 may touch the portal. If either adds
commits, the LOCAL drain ref moves and **the origin branch does not** -- it reads current and is
stale, with nothing to signal the gap. This is the stale-vintage class one layer over from a stale
citation: the claim is fine, the thing it was measured against moved.

Mitigation, bound in the table above: the re-push happens BEFORE any merge, and **the 0-overlap /
5-file / +370-44 assessment is treated as perishable, not as a standing verdict.**

## Open, and not blocking any of the above

- `promote-to-prod.yml` exists changed only on DEV, so a PROD push runs PROD's copy. Flagged to
  `1.0.0_SA_CTO~A`'s side; visible here as one of DEV's two touched files; owned for (c) by
  `1.0.0_SA_CTO~Z`.

## Push state

The portal branch is ON ORIGIN (`ls-remote` read). This record and every other workspace commit are
LOCAL under the site-Z push hold, pending Andrew's word.

---

## AMENDMENT 1 -- the verification moves BEFORE the merge (laptop down)

- recorded by: `0.0.0_AB_MSTR~Z`, 2026-09-16 ~00:5xZ
- source: agent bus, MessageId `7a8ac897-0e78-4509-80b6-c59af6214f3f`, sent 2026-09-16T00:55:41Z by
  `0.0.0_AB_MSTR` as its FINAL frame before stopping its own consumer.
- why this is written down: same reason as the parent file. A bus body lives only in the receiving
  session's Monitor output file, and the sender's consumer is now STOPPED, so neither box holds this
  agreement anywhere durable. Recovered in full from the consumer task's output file, not from the
  chat notification, which was truncated mid-sentence.

**WHAT CHANGED.** The contract table above puts the laptop's verification at **post-(b)** -- it reads
`origin/DEV` after this seat merges and pushes. The laptop has now moved its verification to
**pre-(b)**, verbatim:

> *"STANDING BETWEEN US, unchanged: POSN_AGGFIX step 2 -- on 1.0.0_SA_CTO~Z's 'step 2 due' you HOLD
> at the gate, you do not merge unverified, and you send me the frame; I verify when Andrew restarts
> this box."*

It is offered as "unchanged". **It is not unchanged, and the difference is operational, not
semantic:** under the parent table this seat merges on the gate and the peer checks afterwards; under
this frame this seat **stops at the gate, sends the frame, and does not merge** until the peer has
verified -- and the peer cannot verify until **Andrew restarts the laptop**. So a step that was
self-serviceable now has an external precondition nobody on this box controls.

**THE READ THIS SEAT IS ACTING ON, AND IT IS THE NARROW ONE:** hold. Do not merge on the gate alone.
The narrow read is also the safe one here -- the cost of holding is delay, the cost of merging early
is an unverified push to a shared branch (DEV) with the peer unable to catch it. Where the two
documents differ, this amendment governs, because it is later and because its author is the party
whose act was moved.

**WHAT IS NOW REQUIRED TO FINISH STEP 2 -- three preconditions, not one:**

1. `1.0.0_SA_CTO~Z` sends "POSN_AGGFIX step 2 due" naming the ref and head. (unchanged)
2. This seat re-reads the drain, re-pushes `origin/sitez/aggfix-1-portal`, re-runs the whole
   assessment at that vintage, and **sends the frame to the laptop. Then stops.** (changed: stops)
3. **Andrew restarts the laptop** and `0.0.0_AB_MSTR` verifies and answers. (new, and it is the
   binding one)

Only then does (b) run. (c), the `/prod-deploy`, remains `1.0.0_SA_CTO~Z`'s and is unaffected.

**SURFACED, NOT ADJUDICATED:** precondition 3 is a dependency on Andrew restarting a machine, which
is not a fabric act and has no owner inside the fabric. If he wants the promote to proceed without
the laptop, that is his call to make and this seat will not infer it from the fact that waiting is
inconvenient. The alternative he may want to consider is naming a different verifier on this box;
`1.0.0_SA_CTO~Z` is the obvious candidate and is already the (c) owner.

## Corroboration this frame also supplied, unasked

`origin/CLOUD` is **unchanged at 2033ff3ea6** with no laptop push. This seat had independently read
`origin/CLOUD` at `2033ff3ea6` during its `/integrate` assessment ~00:2xZ, on a different box, before
this frame arrived. Same object, two boxes, two instruments -- so the `/integrate` divergence numbers
(CLOUD +685, base `56608aadd4`) are anchored on a head the producing fabric confirms it did not move.

Laptop state at the frame: all six working seats parked and exited, `1.0.0_SA_CTO~A` parked with its
Codex TUI held open for Andrew, every loop and cron deleted, every monitor stopped, **nothing
half-landed** (`2.0.0_SA_COO~O`'s OG-i-1 apply FINISHED -- 4 added, 2 changed, 0 destroyed, ledger
CLOSED, fresh plan "No changes"). Disk on that box: 5.0 GB free at the worst point tonight, 50 GB
free after seat worktree drains plus an Andrew-authorized cleanup. Nothing of this fabric's was
touched. The CLOUD<->SITEZ workspace merge and the laptop's CLOUD push both stay at Andrew.

---

## AMENDMENT 2 -- step (b) IS DONE. Amendment 1 was already stale when committed.

- recorded by: `0.0.0_AB_MSTR~Z`, 2026-09-16 ~01:2xZ, on `1.0.0_SA_CTO~Z`'s msg 23317 (FREEZE WINDOW OPEN)
- **AMENDMENT 1 IS SUPERSEDED AS A FORWARD INSTRUCTION.** Kept, because what was believed and when is
  the point of this file, but NOTHING ARMS FROM IT.

**MEASURED AT THE REMOTE, not taken from any seat's report** (`git ls-remote`, then `git log` / `git
diff` against fetched refs, in `portal/`):

| object | value |
|---|---|
| `origin/DEV` | `be8cf218743af0c04a4d57b908b28cf7435e119d` |
| `origin/PROD` | `edf85ce503aad961b84b5ea3b2074eb84d416a16` (unmoved) |
| content delta `PROD..DEV` | 7 files, 379 insertions, 46 deletions |
| the files | the 5 Positioning files + `.github/workflows/ci.yml` + `promote-to-prod.yml` |
| drain tip `3ec1f83c` on DEV | YES (`merge-base --is-ancestor`) |
| the merge's own tree effect vs the drain | the 2 CI files ONLY -- it dragged in no other content |

Consistent with this file's `+370/-44` measured on the drain alone; the extra `+9/-2` is `be8cf218`
(Andrew's two post-smoke items) plus the CI pair. **Step (b) is COMPLETE at `be8cf218`.**

## WHO PUSHED DEV -- and a wrong answer this seat nearly committed

`1.0.0_SA_CTO~Z` **pushed DEV under an AUDITED OVERRIDE**, which is a recorded escape, not a silent
violation. The decisive record, `org/git-author-override-audit.log`, last line:

```
2026-09-16T01:03:38Z NEVER-OVERRIDE serial=1.0.0_SA_CTO~Z rule=PUSHPULL_AUTHORITY
  reason=Andrew-direct 2026-09-15 "Q" -- non-DT CTO~Z admitted by Step 0 Andrew-direct clause
  cmd=git push origin HEAD:DEV
```

So msg 23317's *"1.0.0_SA_CTO~Z merged it forward onto current DEV and pushed at be8cf218"* is
**CORRECT**, and it is the account to believe.

**THE WRONG ANSWER, RECORDED BECAUSE IT IS THE REUSABLE PART.** This seat first read the commit
identity lines and drafted an amendment concluding the opposite -- that `0.0.0_AB_MSTR` (laptop) had
performed both pushes and *"the shared-branch law is SATISFIED"* -- and prepared to correct 23317's
author on that basis. The evidence looked strong and was well-formed:

- `a4ef8853` (the merge of the drain into DEV): author AND committer `0.0.0_AB_MSTR`, 00:56:51Z
- `be8cf218`: author `1.0.0_SA_CTO~Z`, **committer `0.0.0_AB_MSTR`**, 01:02:12Z

**A COMMIT'S AUTHOR AND COMMITTER LINES ARE NOT AN ORACLE FOR WHO PUSHED A SHARED BRANCH.** They
record the git identity configured in whatever tree the work happened in -- here a portal worktree
carrying the MSTR identity -- and a push leaves no trace in them at all. **Commit identity answers
"who wrote this object"; it cannot answer "who moved this ref", which is the only question
LD-0367/LD-0368 asks.** The instrument for that question is the **push-authority audit log**, and it
answered in one `tail`.

The near-miss was a **FALSE ALL-CLEAR on a shared-branch law question** -- the most expensive
direction to be wrong in, because a clean finding closes the question and nobody re-opens it. It was
caught only because a peer's message and this seat's inference DISAGREED, and the disagreement was
worth one more read instead of a correction to the peer. **A peer contradicting your measurement is
evidence about your instrument, not only about their claim.**

## The freeze window -- ACKNOWLEDGED AND HONOURED

`1.0.0_SA_CTO~Z` opened a FREEZE on **portal/DEV pushes only** until it posts FREEZE CLOSED, because
its DEV->PROD merge runs against LIVE `origin/DEV` at GO time, so any push landing in the window rides
into PROD as an unverified passenger. **This seat holds, and has no portal/DEV push pending -- step
(b) is done, so it never will for this round.** Explicitly unaffected, per 23317 and agreed here: the
LD-0522 **workspace** push hold is a different object and is untouched.

## Where step 2 now stands

(b) COMPLETE at `be8cf218`, pushed by `1.0.0_SA_CTO~Z` under the audited override above.
(c) `/prod-deploy` is `1.0.0_SA_CTO~Z`'s and is unchanged. The laptop's verification is **no longer a
precondition of anything** -- Amendment 1's precondition 3 is DISCHARGED, not waived. Round 1's L8/L9
obligations at `3.0.0_SA_CVO~Z` are untouched by the promote and are not gated on it (23317).

**OPEN, AND SURFACED RATHER THAN ADJUDICATED:** as of its 01:09Z bus frame the laptop MSTR still
believed step (b) was pending and said it would *"re-read 9998f2a760 before I act on any step-2 leg."*
It is being told on the bus, in the same turn as this commit, that (b) has landed. Two live MSTRs
holding different beliefs about whether a shared-branch merge has happened is the condition worth
clearing fast; it is cleared by this record plus that send, and nothing is asked of Andrew.
