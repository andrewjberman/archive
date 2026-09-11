# PRESERVED 2026-09-11 -- at-risk UNCOMMITTED diff, `seed-etf-constituents.py`

**archetype:** SCRIBE

**Why this file exists:** site Z's shared worktree **loses uncommitted work**, and this diff had already
survived the 14:10:36Z reboot as an unstaged modification. It is **hand-written work carrying measured
reasoning**, and one crash from gone. This record puts the exact bytes on origin so the reasoning
survives independently of the worktree.

**Surfaced by:** `2.0.0_SA_COO~Z` (msg 21493), which measured it, did not touch it, and correctly
declined to act -- the path is outside every POSN_ASTTAX task order's `<paths>`.
**Preserved by:** `0.0.0_AB_MSTR~Z`, 2026-09-11 ~17:2xZ.

## ⛔ WHAT THIS RECORD IS AND IS NOT

- It is a **COPY OF A DIFF**, for recovery. It is **NOT** a commit of the change.
- **THE WORKING TREE WAS NOT TOUCHED.** Not staged, not committed, not stashed, not checked out, not
  cleaned. The file is still ` M` exactly as found. `git stash` is prohibited on this shared tree and
  is the reflex this record exists to avoid.
- **NO AUTHORSHIP IS CLAIMED.** `0.0.0_AB_MSTR~Z` did not write these bytes and does not know which
  seat did. The last COMMITTER of the file is `1.0.0_SA_CTO~Z` @`b3d830094c` (2026-08-25); the author
  of the UNCOMMITTED edit is **unresolved** and may be a seat that died at the reboot.
- **IT IS NOT ENDORSED.** Neither hunk has been reviewed or tested by this seat. Preservation is not
  approval, and whoever owns the file decides whether these bytes land.

## PROVENANCE

```
path            infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-constituents.py
state           ` M` MODIFIED, NOT STAGED, NOT COMMITTED, shared worktree
diffstat        19 lines changed (13 insertions, 6 deletions)
base blob       d489a61071
working blob    01b2005690
last committer  b3d830094c  1.0.0_SA_CTO~Z  2026-08-25
preserved at    origin/SITEZ d0efe81ca8 (the integrator read immediately before this record)
```

Present and dirty in this session's opening `git status` at ~15:0xZ, so it **predates the relaunch**
and survived the reboot.

## THE DIFF, VERBATIM

```diff
diff --git a/infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-constituents.py b/infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-constituents.py
index d489a61071..01b2005690 100644
--- a/infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-constituents.py
+++ b/infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-constituents.py
@@ -88,11 +88,12 @@ NAME_CORRECTIONS: dict[str, str] = {
     # FXFXX drops a FABRICATED maturity date -- a money-market fund has none.
     "SALXX": "State Street U.S. Government MMKT",
     "FXFXX": "First American Treasury Obligations Fund",
-    # The DERIVED NAV-residual line this estate emits for issuers that do not itemize their cash.
-    "CASH": "Cash & Other Assets",
-    # The issuer-REPORTED equivalent. Kept distinct from CASH on purpose: one is a row we were
-    # given, the other one we derived, and the ticker is the only thing that still says which.
-    "CASH&OTHER": "Cash & Other",
+    # THE ONE CANONICAL CASH LINE, identical in every book (Andrew-direct 2026-08-25: "it should
+    # always be managed the same way: Fixed Income for Asset Class, Ultra Short Duration for Sub
+    # Asset, CASH for ticker, and Cash & Cash Equivalents for Name"). The producer normalises BOTH
+    # the derived residual row and the issuer sentinel onto this ticker, so CASH&OTHER no longer
+    # reaches the served artifact and needs no row here.
+    "CASH": "Cash & Cash Equivalents",
 }
 
 # THE ONE CORRECTION THAT IS A RULE, NOT A ROW.
@@ -220,7 +221,13 @@ def main() -> int:
     wrote = 0
     with table.batch_writer() as batch:
         for r in creates + updates:
-            batch.put_item(Item={k: v for k, v in r.items() if v is not None})
+            # DROP EMPTY VALUES, NOT JUST None. `sub_asset_class` backs a GSI
+            # (sub-asset-class-index) and DynamoDB REFUSES an empty string for an indexed key
+            # attribute -- measured: ValidationException on the first real write. An ABSENT
+            # attribute is valid; the item simply does not appear in that index, which is the
+            # correct outcome for a security we could not classify. Writing "" to make the
+            # shape uniform is what the table itself rejects.
+            batch.put_item(Item={k: v for k, v in r.items() if v is not None and v != ""})
             wrote += 1
     print("\nWROTE %d item(s) to %s" % (wrote, TABLE))
     return 0
```

## WHY IT IS WORTH PRESERVING RATHER THAN SHRUGGING AT

**Both hunks carry their own reasoning, and one of them carries a MEASUREMENT that would have to be
re-earned by re-triggering a production failure:**

1. **The cash-line collapse** quotes an **Andrew-direct of 2026-08-25 verbatim** -- *"it should always
   be managed the same way: Fixed Income for Asset Class, Ultra Short Duration for Sub Asset, CASH for
   ticker, and Cash & Cash Equivalents for Name"*. It folds the DERIVED NAV-residual row and the
   issuer-REPORTED sentinel onto one canonical ticker.
2. **The empty-value filter** (`v is not None` -> `v is not None and v != ""`) is justified by a
   measured failure: `sub_asset_class` backs the `sub-asset-class-index` GSI, and **DynamoDB refuses an
   empty string for an indexed key attribute -- "ValidationException on the first real write."**
   ⭐ **That is the expensive half.** The sentence is cheap to read and was NOT cheap to learn: losing
   it means the next author writes `""` again and rediscovers it by breaking a real write.

## IT INTERSECTS A LIVE ARMED ROW -- READ THIS BEFORE MEASURING THAT FILE

`POSN_ASTTAX-Z-W8-S2` (ARMED, `disarm_owner` `1.0.0_SA_CTO~Z`) found three registry rows carrying a
BLANK `sub_asset_class` for 17 days as **STALENESS, not missing data** -- all three values were present
upstream (0 of 189 upstream rows blank) because this seeder **writes only on CREATE and preserves
existing rows**.

⚠ **These uncommitted bytes are in exactly that file and exactly that write path.**

**NOT CLAIMED:** that the diff fixes W8-S2. It changes the empty-value **FILTER**, not the
**create-only** behaviour, and nobody has tested it. The point is narrower and it is the reason this
record is cross-linked: **whoever disarms W8-S2 must know these bytes exist and are NOT at HEAD**, or
they will measure the committed version and reason about a producer someone has already partly revised.
That framing is `2.0.0_SA_COO~Z`'s and is adopted here unchanged.

## THE REST OF THE DIRTY TREE -- SURVEYED SO THIS ONE IS NOT MISTAKEN FOR THE WHOLE PROBLEM

| path | lines | disposition |
|---|---|---|
| `seed-etf-constituents.py` | 19 | **AT RISK -- hand-written. Preserved above.** |
| `org/modules/graph/nerves-risk-edges.json` | 54,660 | REGENERATED artifact (`Regenerate: nerves_lexical build`) -- not hand work. **See the warning below.** |
| `org/mcp/.last-drive-2.0.0_SA_COO{,~ZZ}` | 2 | runtime markers (unix ts / ISO stamp). Not work. |
| `org/tier0_utility/0.0.3_BG_BBGTerminal/threads/INDEX.md` | 1 | that seat is **LIVE** and owns the file. Not at risk. |
| `portal` | pointer | ⛔ **MUST STAY UNCOMMITTED** -- see below. |

⚠ **`nerves-risk-edges.json` CARRIES A SILENT NARROWING AND SHOULD NOT BE COMMITTED UNREAD.** Its own
stats block moves **`docs_scanned` 1825 -> 1225** -- the regeneration read **600 fewer documents** than
the committed artifact. A regenerable file is normally safe to discard or recommit, but committing this
one would **narrow the danger-zone graph by a third while looking like a routine rebuild**, and a
lexical graph that scans less finds less without saying so. Plausible cause: it was regenerated from a
sparse or partial checkout. **NOT investigated and NOT fixed here** -- surfaced for its owner
(`NFRA_NERVES`), and flagged because the failure mode is a quiet coverage loss, not an error.

⛔ **`portal` IS FROZEN AND ITS DIRTINESS IS CORRECT.** Andrew-direct ~15:0xZ: *"nobody does any portal
promotes until i say so is the takeaway here."* The submodule pointer has moved in the worktree
(`e85f6eb84f` -> `30ca034bba`) and **that move must NOT be staged, committed or pushed by anyone** until
he names it. Every integrator push tonight measured `portal: 0` files in range, deliberately.

## OWNERSHIP AND WHAT HAPPENS NEXT

**Not this seat's to commit.** The path is `infra/aws/lambda/**` -- DT/AE territory under Rule 13, not
MSTR's, and committing another seat's uncommitted work under this seat's author line would misattribute
it. **The bytes stay in the worktree; this record is the insurance, not the resolution.**

**UN-PARKING CONDITION:** the file's owner (or Andrew) decides whether these two hunks land. If the
worktree is lost first, the diff above is recoverable from origin and can be re-applied with
`git apply` against base blob `d489a61071`.
