# NFRA_IAMROLES202609 -- `IAM-t-1`: the owner finding, and the escalation it raises

Cell `IAM-t-1`, outcome `FWD-4` (round 2's analysis calls it `R3-A`). Worker
`0.9.0_WK_NFRA_IAMROLES202609~7`, worktree `/c/tmp/wk-iamroles-7`, branch
`wk-NFRA_IAMROLES202609-7`, base `39fc7680c6`.

**THE SUBSTANCE OF THIS CELL IS IN THE GOVERNANCE DOCUMENT, NOT HERE.** The value, its four-postulate
record, its token census and the four planes of the owner search are written into
`../0.9.0_WK_NFRA_IAMROLES202609~3/GOVERNANCE_DISPOSITION.md`, section **THE OWNER FINDING**, because
that is the document `FWD-4` is read against and a finding filed beside it would be a second copy to
drift. This file exists for the one thing the cell told this worker to do HERE: raise the escalation.

## WHAT THE CELL DID

| row set | before | after |
|---|---|---|
| 9 `ADOPT` rows | **no `owner=` field at all** -- invisible to the `owner=UNASSIGNED` metric | `owner=NO-ACCEPTING-SEAT` + a per-row `reason=` |
| rows 7, 8, 10 | `owner=UNASSIGNED` | `owner=NO-ACCEPTING-SEAT`, amended in the open, reasons extended |
| rows 4, 12, 15 | `owner=1.0.0_SA_CTO~Z` | **untouched** -- that seat accepted those three, in writing |
| row 13 | `DECLARED` | **untouched** -- in code, so nothing is owed and no owner is needed |
| row 8's attachment count | "through three" | "through five", re-read at source, five line citations |

Member-row owner census after the edit: **3 a seat serial + 12 `NO-ACCEPTING-SEAT` + 1 `DECLARED`
row carrying no owner field = 16 of 16.** No disposition token moved; no research was re-opened; no
Terraform was modified; no permission was assessed in either direction.

## THE ESCALATION, RAISED HERE BECAUSE ROUND 2 SAYS IT IS RAISED WHEN A CELL FINDS IT

`ledger/ROUND_ANALYSIS.round2.md` section 9: *"`R3-A` may FIND that some exemption owners do not
exist inside this fabric. If it does, that escalation is the recut's finding and is raised then --
not pre-emptively here."* This cell found something adjacent to that and sharper, and the difference
is what makes it cheap to fix:

⛔ **THE OWNERS EXIST. THE ASK DOES NOT.**

- The lane that can perform these acts exists and is enumerated: `CLOUD_OPS_OR_ETL` owns
  `infra/aws/**` (`.owned-paths.yaml:1845-1847`, membership `:342-353`, spawn admission
  `.tools/owned-paths-validate.py:278-287`).
- It is the busiest family in this estate: **935 commits by 41 distinct AE serials in 14 days**,
  against a window denominator of 5,785 commits by 120 authors; **1,486 commits by 74 authors** on
  `infra/aws/terraform/` all-history, led by `0.7.0_AE_CloudOps` at 533.
- **Zero of them has ever touched this project**: 0 of **65** commits on the mission directory, and
  `6 hit(s) across 63 file(s) scanned` for any AE serial across the project -- every one a citation
  or a git vintage, none an acceptance. Positive control on that search: `9 hit(s)` for `accepted`
  across the same 63 files, one of which IS `1.0.0_SA_CTO~Z`'s acceptance of the other three rows.

So the binding constraint is not a missing owner and not a shallow search. **It is one message that
an L7 worker is structurally unable to send** -- a worker holds no send tool and cannot be messaged,
which the task order states in terms. The remedy is an **ISSUANCE** to a seat in that lane, and
issuance is L6.

**WHAT IS ASKED, AND OF WHOM.** Nothing is asked by this worker: a worker cannot task a seat, and
naming a route is not taking one. Recorded so the next issuer can act on it in one step:

- **`2.0.0_SA_COO~ZI`** holds the recut and is the disarm owner on the row. Twelve rows need a seat
  in the `CLOUD_OPS_OR_ETL` lane to be ASKED whether it accepts them -- nine adoptions, two
  serving-path sign-offs, one retirement.
- **Two of the twelve are nearly free.** Rows 8 and 10's adopting Terraform is already written and
  inert at `infra/aws/terraform/data-refresh/zz_adoption_candidate.tf.proposed` (`:29-30`, `:66-67`,
  `IAM-r-5`, with a recorded plan). On those two rows the text is not the blocker; an acceptance is.
- **Row 7 needs one thing no agent seat can supply alone.** Its terminal act deletes a live IAM
  object, which this estate reserves for human confirmation (`CLAUDE.md`, Agent Autonomy). That is a
  pre-existing constitutional stop being READ, not a gate being built -- none was built.
- **Nothing is owed by Andrew** on this cell's account. The one owner statement the estate's own IAM
  inventory carries is at file grain (`infra/aws/manifests/iam/iam-roles.yaml:3`,
  `# Owner: Andrew Berman`, `Last Updated: 2026-01-02`, `total_roles: 8`); it covers 1 of the twelve
  rows and none of the other 11, and this cell recorded that rather than converting it into an owner
  field.

Filed as `NFRA_IAMROLES202609-Z-W7-S1` (OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~ZI`) in
`../../surprise-channel/investigations/INVESTIGATION_v1.md`.

## WHAT THIS CELL DID NOT DO

No seat was named as an owner anywhere. No Terraform was created, modified, imported or deleted --
`infra/aws/terraform/` was a READ surface and every citation is a read. No role was created, changed
or deleted. No grant on any of the sixteen was assessed or moved in either direction (`C-TWO-REMEDIES`, bound
D6): the negative regression bar that measures this reads 0 after the edit as it did before. No
alert, alarm, monitor, schedule or notification was minted (`G-21` stays ARMED and untouched). No
AWS Access Analyzer was called or priced. The document was extended, never restructured: rows 1-16
keep their authors' research, the class ruling, the membership note and both earlier four-postulate
records stand exactly as written.

## THE ONE THING A LATER READER MOST NEEDS

`owner=NO-ACCEPTING-SEAT` is **not** `UNASSIGNED` with a longer name, and it is **not** a claim that
these rows are unownable. `UNASSIGNED` says a slot is empty and cannot distinguish *nobody looked*
from *we looked and found nobody*. This value is the second of those, with its denominator attached.
One acceptance moves one row's owner field to that seat's serial, and nothing else in the document
moves.
