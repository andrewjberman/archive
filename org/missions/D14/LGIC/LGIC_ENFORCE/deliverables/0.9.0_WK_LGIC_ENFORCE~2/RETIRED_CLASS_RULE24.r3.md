# `refused_keys.retired` -- Rule 24 (TAXONOMY LAW) record, EN-r-5-r3

**Author:** `0.9.0_WK_LGIC_ENFORCE~2`, round-3 cell `EN-r-5`. **Binds on:** R-6
(`org/tier1_exec/1.0.0_SA_CTO/deliverables/SELF_DRIVE_LGIC_RULINGS_20260916.md` :204-238).

## The change

`infra/logic/registry/systems.json` `refused_keys` gains a fourth class, `retired`, with `imo` as
its first (and, at this cut, only) member, and a sibling `retired_basis` string carrying its
citation (same JSON, immediately beside the `basis`/`find_basis` siblings the existing three
classes already share one `basis` field for).

## (i) MECE over a DECLARED domain -- hunt the uncovered member, by SUBTRACTION

**Domain:** `refused_keys`'s declared population is *tokens that may never fill a `systems.json`
row* -- CLAUDE.md Rule 24 requires the domain be the claim's population, falsified before the
subtraction runs. `_about.what` names the registry's row population ("every token that may fill a
resource name's `{system}` slot or a key's `{source}`"); `refused_keys` is the registry's own
declared EXCLUSION set over that population, so `refused_keys`'s existing three classes are the
domain to subtract against, not a wider one.

**Printed denominator, before excluding:** `refused_keys` at the cut (EN-r-2's drain) held exactly
THREE classes -- `workstream_code` (10 members), `generic_noun` (78 members), `purpose_word` (8
members) -- 96 members total, read directly off the file at HEAD before this cell's edit
(`git show HEAD:infra/logic/registry/systems.json` before this commit).

**Subtraction:** the six tokens EN-r-2 left `unresolved` are `find, harvest, imo, astn, trade,
news` (`systems.json` `unresolved`, six entries, printed denominator = 6). R-6 dispositions all
six: `find` -> `workstream_code` (a project code is never a system, V3); `harvest, astn, news,
trade` -> PRODUCT rows or stay `unresolved` with a measured `why` (this cell's `EN-r-5` sibling
work, same commit); `imo` -> RETIRED on Andrew's card 9. `imo` is the ONE member of the six that
fits NONE of the three existing classes: it is not a project code (`workstream_code`), not a
common English noun or AWS-service-shaped word never naming a system
(`generic_noun`/`purpose_word`) -- it is a token Andrew struck from the live estate by direct card,
independent of what kind of word it is. **That is the uncovered member the subtraction surfaces: a
fourth axis the three-class domain does not cover.**

## (ii) SAME GRAIN

Every `refused_keys` class is a list of lowercase kebab-case token strings that may never resolve
as a `systems.json` `key`, checked the same way at the same call site
(`lib/opal_naming.py` validate() :398-402, `r5_imo_retired`/`r5_find_refused` here). `retired`
carries `imo` at that identical grain -- a bare string in a bare list -- not a richer object, so the
validator's `isinstance(members, list)` branch recognizes it exactly as it recognizes the other
three classes (confirmed live: `python lib/opal_naming.py validate` reads OK with `retired` present
and does not raise on it, `RC=0` at this commit).

## (iii) INTENT COHERENCE -- one axis, one intent

`workstream_code`'s intent: "this is a project/macro code, and a project code is never a system"
(V3). `generic_noun`'s and `purpose_word`'s intent: "this is a common word / an AWS-service-shaped
word that never names a system" (V3). **`retired`'s intent is `a token Andrew retired by card`** --
disjoint from all three: it says nothing about the token's grammatical shape (noun vs. code vs.
service-word) and everything about its LIVE STATUS (struck by direct sovereign act,
`org/tier1_exec/4.0.0_SA_CRO/deliverables/04_SCOPE_TICKLIST.md` :15, :66, card 9). A token could in
principle be BOTH a project code and later retired, or a generic noun and later retired -- the axes
do not compete for the same member, which is the DISJOINTNESS Rule 24(iii) asks a proposal to show.
One intent per class; `retired`'s is exactly one (retirement), matching the shape of the other
three (each exactly one).

## (iv) STATE COHERENCE -- which values one remedy does NOT move

Retiring `imo` moves exactly one state: `imo` leaves `systems.json` `unresolved` and can never
again resolve as a `key` there. It does NOT move: `opal-data-imo`'s live bucket state (still
LIVE, 304 per-company planes, unretired at the storage layer -- R-6 s.1 "imo" row; retirement here
is a NAMING-REGISTRY act, not a bucket deletion); the other five EN-r-2 tokens' disposition (each
graded on its own evidence, this cell's `EN-r-5` sibling work); and the THREE pre-existing
`refused_keys` classes, which are untouched by this edit (`workstream_code` gains `find` as a
SEPARATE act in the same commit, `generic_noun`/`purpose_word` untouched). Its resources grade as
class (d) rule gaps until the R19 retirement project removes them (R-6 :225) -- loud, by design,
not silently absorbed by this taxonomy change.

## The uncovered member, named directly (Rule 24(i)'s "hunt it")

**`imo`** is the member the three-class domain does not cover, found by subtracting the six
`unresolved` tokens against the three existing classes' combined membership (96 + 6 = 102 checked;
`find` fits `workstream_code`'s V3 rule and is added there in this same commit; `harvest`, `astn`,
`news`, `trade` are PRODUCT-shaped, not exclusion-shaped, and are this cell's separate `systems`/
`unresolved` edits; `imo` alone matches none of the three exclusion rules and needs the new axis).

## Citations

- `org/tier1_exec/1.0.0_SA_CTO/deliverables/SELF_DRIVE_LGIC_RULINGS_20260916.md` :204-238 (R-6, the
  ruling binding this cell) @ HEAD of this worktree's base, `24bae9d9da`.
- `org/tier1_exec/4.0.0_SA_CRO/deliverables/04_SCOPE_TICKLIST.md` :15, :66 (Andrew's card 9, RETIRE)
  @ `24bae9d9da`.
- `infra/logic/registry/systems.json` `refused_keys` @ this commit (the edit itself).
- `lib/opal_naming.py` :398-402 (the validator's `refused_keys` extraction, list-shape only) @
  `24bae9d9da`.
