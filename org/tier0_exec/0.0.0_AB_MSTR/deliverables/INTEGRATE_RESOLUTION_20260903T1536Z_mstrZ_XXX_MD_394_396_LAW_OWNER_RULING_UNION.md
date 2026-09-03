# /integrate CLOUD -> SITEZ -- the org/XXX.md 394-396 collision: LAW OWNER'S RULING, and the resolution this seat will execute

**Why this file exists:** the ruling arrived on the agent bus, and a bus body lives only in a
SESSION-SCOPED Monitor output file. The resolution is needed at MERGE time, which is a later window.
A session-scoped carrier for an obligation that outlives the session is the defect; this is the
durable carrier. Recorded by `0.0.0_AB_MSTR~Z` (site-Z integrator).

**Provenance:** laptop `1.0.0_SA_CTO` (the law owner for `org/XXX.md`), msg 93754 @15:34Z, relayed
by `0.0.0_AB_MSTR` on the bus as MessageId `ca319e47-1553-4eab-be1e-b5ea37182154` @2026-09-03T15:36:32Z,
read in full and ACKed by this seat the same turn. Measured char-by-char against the merge base
`3bd8d2ef04` FROM BOTH ENDS -- not read off a conflict hunk.

## THE RULING: UNION, NOT A PICK -- on all three rows

The `/integrate` Step-4 table sends IDENTICAL base-side ranges to PICK and DISJOINT ranges to UNION.
The owner's measurement says these ranges are DISJOINT, including on the row that looked contested:

| Step 1b-F row | HEAD (CLOUD) | SITEZ | UNION |
|---|---|---|---|
| `0.0.0_AB_MSTR` | == base (8,521 chars) | base + APPENDED clause at char 8,520 (this seat's ~06:4xZ `/govern` arm) | SITEZ's row |
| `1.0.0_SA_CTO` | == base (12,514 chars) | base + APPENDED clause at char 12,462 (`1.0.0_SA_CTO~Z`'s `/self-drive` arm @`36786251af`) | SITEZ's row |
| `2.0.0_SA_COO` | base + APPENDED clause at char 18,002 (`2.0.0_SA_COO~A`'s scoped `/drive CLDGRPH to completion` arm, 13:08Z) | base with the 08-28 COO~Z `D1+D4` clause STRUCK IN PLACE at char 7,459 (wrapped `~~...~~` on Andrew's word), nothing appended | SITEZ's row WITH THE STRIKE **+** HEAD's appended clause at the end, VERBATIM |

**The COO row is the whole reason this needed an owner, and the answer is that it was never a
contest:** a MID-ROW STRIKE at char 7,459 and an END-OF-ROW APPEND at char 18,002 are two edits to
one row with ZERO shared characters. The conflict was adjacency inside a single long row -- the
same class as the 2026-08-12 CLAUDE.md rules-22/22a false escalation, one grain finer (rows within a
file, then spans within a row). **No pick anywhere; nothing is lost on either side.**

## ONE MORE HUNK, disclosed BEFORE the merge rather than discovered in it

Landing on the base this turn, non-overlapping with 394-396, and to be TAKEN:

1. `org/XXX.md` Step 1b **CODEX SEATS** block (~lines 151-159) -- one sentence: a shared branch
   (CLOUD / DEV / PROD / main / SITEZ) is pushed ONLY by `0.0.0_AB_MSTR` or `0.0.0_AB_MSTR~Z`, and
   only on Andrew's word while he is at the terminal; every other seat commits and states push state
   LOCAL.
2. `org/mcp/codex-skills/load/SKILL.md` -- the same sentence.

This is the law-file half of the finding this seat measured at 14:11Z: **a push from a checkout with
the pre-push `safe-deploy` gate armed IS a deploy**, whoever pushes it. The proposal that a
non-integrator push be REFUSED mechanically stays RESERVED at Andrew; this sentence is the written
rule that precedes it.

**This disclosure is the `/integrate` Step-4 vintage obligation working as designed** -- the base
moved after this seat's assessment was taken, and the owner said so unprompted instead of leaving a
live verdict pointing at a vintage that no longer exists.

## THE OTHER THREE FILES -- unchanged, and both pre-agreed picks now have a REASON, not a preference

- `.tools/surprise-row-gate.py` -- **PICK THE BASE.** The base carries the equivalent fix
  (`ebe3a4caea` REMEDIATED exemption, `6ec8f32d50` override honour, `2f5918982b` + `d54a2dee7e`
  foreign-row sweep arm). `1.0.0_SA_CTO~Z`'s cp1252 decode fix (`c3ef3a2530`) is the ONE hunk to
  check survives the pick -- audit the losing rendering for content, per Step 4.
- `.tools/proof-of-spec-check.py` -- **PICK THE BASE.** `_parse_to` cell_refs
  `re.split(r"[,\s]+", ...)` (`50ff3d674a`, SITEZ) vs the base's equivalent at `:651`
  `re.split(r"[\s,;]+", ...)` (`7b649df39d`). Two independent corrections of ONE defect; the base's
  is strictly wider (it also splits on `;`).
- `.tools/deploy_ledger.py` -- SITEZ's pattern-5 markdown TABLE-ROW status form (`79c0e68071`)
  is an ADD, not a collision.

## STATE OF THE LEG AT THIS RECORD

**ASSESS-ONLY, and the blockers are named rather than implied:**
1. Site Z is NOT quiet -- three worker faces in flight at Tier-2 on NFRA_OPSEC202609 (L7, 4 of 8
   task orders terminal). `/integrate` Step 0 wants a quiet window; a merge into a live tree on a
   SHARED checkout is how uncommitted seat work is lost.
2. The push half was PUT UP AND DECLINED at this terminal at ~15:32Z. Two `1.0.0_SA_CTO~Z` lane
   commits (`8a88085266`, `f091fc8c54`) are LOCAL; deploy ceiling on that range is ZERO.

Neither blocker is a defect and neither needs anyone's word to clear on its own. **What this record
buys: when the window opens, the merge is mechanical -- three rows union per the table above, two
gate files pick the base with one content audit each, two law-sentence hunks taken, one add.**

`0.0.0_AB_MSTR~Z`

---

## AMENDMENT 2026-09-03T17:25Z -- two additions to the resolution, neither disturbing the ruling above

Recorded by `0.0.0_AB_MSTR~Z` as the leg's owner. The leg is still ASSESS-ONLY; this keeps the
resolution complete rather than letting it age against a base that keeps moving.

### 1. `infra/aws/terraform/shared-infra/dynamo.tf` -- NEW conflict, resolution: TAKE SITEZ

Relayed from the laptop `1.0.0_SA_CTO` (msg 93826, 17:16Z) as shared-infra's module owner: CLOUD
adds ONE line at `14fbeace00` (`deletion_protection_enabled = true`); SITEZ adds the IDENTICAL
line under an eight-line OPSEC comment. The regions overlap, so if git does not merge it clean,
**take SITEZ's hunk -- it is the SUPERSET**, same declaration plus the reasoning.

This is the *identical-correction* case the `/integrate` Step-4 table warns about (two fabrics
independently correcting one defect, where a union stacks two renderings of one change), with the
tie broken by superset rather than by preference. The losing rendering carries nothing the winner
lacks -- one line against the same line plus a comment -- so the mandatory content audit of the
discarded side is satisfied by inspection and is recorded here as done, not skipped.

### 2. `org/XXX.md` -- SITEZ's side gained a hunk; MEASURED, and it does NOT touch the ruled region

`1.0.0_SA_CTO~Z` committed `3bde8d1bac` promoting Step 1b-F from bold text to a `###` heading --
FORMAT ONLY, one insertion and one deletion, no row, clause, table or arming state touched.

Base-side ranges re-measured at `--unified=0` against merge-base `3bd8d2ef04`:

| side | base-side hunk ranges |
|---|---|
| CLOUD | `{396}` |
| SITEZ | `{388, 394-396}` |

The new `388` hunk is **DISJOINT** from CLOUD's single line, so it unions by construction and adds
nothing to adjudicate. The `394-396` against `396` overlap is the one the law owner already ruled
UNION on, and that ruling is unchanged.

**DISCLOSED UNPROMPTED TO THE PEER, because the obligation runs in this direction too:** the
laptop's verdict on this file was measured at a vintage that has since moved. Stated as re-based,
not invalidated -- the substance is unchanged.

### Why 3bde8d1bac matters beyond the merge

A Tier-2 worker enumerated Step 1b at startup, found A through E, and reported that **Step 1b-F
does not exist** -- because F was the ONE subsection written as bold text rather than a heading, and
a heading-shaped probe cannot see it. The failure is asymmetric: it fails SAFE for a seat with no
loop authorization, which arms nothing, and UNSAFE for a seat that HAS one, which goes to the only
address it was ever given, finds nothing, and cannot tell "my authorization was revoked" from "I am
looking in the wrong place". Both fabrics' launch prompts name that same address.

### Leg state at this amendment

ASSESS-ONLY, unchanged, and the blockers are the same two: the tree is busy (both CloudOps lanes
seated and committing), and the push was declined at this terminal at ~15:32Z and has not been
re-put. Local unpushed lane commits: 29 at this write. Deploy ceiling across that range: ZERO.
