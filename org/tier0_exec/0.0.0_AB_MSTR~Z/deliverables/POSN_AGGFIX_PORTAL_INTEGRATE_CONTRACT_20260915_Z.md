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
