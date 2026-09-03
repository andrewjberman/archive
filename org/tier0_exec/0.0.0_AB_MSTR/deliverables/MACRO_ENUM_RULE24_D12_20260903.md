# MACRO ENUM for D12 -- the Rule 24 four-postulate record + word-boundary token census

**Author:** `0.0.0_AB_MSTR~Z`, 2026-09-03 ~02:0xZ, as site-Z register owner (lane `TREE_MACROS`:
COO, MSTR, CTO). **Carrier (DATA):** `org/missions/MACROS.yaml` -- read by
`.tools/missions-tree-index.py` refusal R2. **Follows the form of** the D0/D8/D11 record
(`org/tier1_exec/2.0.0_SA_COO/deliverables/MACRO_ENUM_RULE24_D0_D8_D11_20260902.md`), deliberately,
so the two are comparable rather than each inventing a shape.

**Ratification status:** Andrew APPROVED `[NFRA]` FOR D12 IN ADVANCE, 2026-09-03 ~01:5xZ at the
laptop COO terminal, VERBATIM AND ENTIRE: *"All recs approved, ratify D0 and D8"* -- answering an
`/open-calls` whose card 3 read *"Ratify D12's enum when MSTR~Z's proposal lands? Expected [NFRA]"*
with the rec *"[NFRA], one word when the record is in front of you"*. Relayed by `2.0.0_SA_COO`
standing in for `0.0.0_AB_MSTR` (bus id `e8421d1a-4e33-4b7d-a6d3-0558bab6a752`), whose exact
instruction was: when this record lands, set `directives.D12.ratification` to RATIFIED citing BOTH
records; **no further word is needed for `[NFRA]`, and any WIDER D12 list needs a fresh one.**

---

## 1. The proposal

| directive | macros (the enum) | evidence (rows with `directive: D12`, 354-row register read 2026-09-03 ~02:0xZ) |
|---|---|---|
| D12 | `NFRA` | 3 of 3 rows; 1 carries `macro_code: NFRA`, 2 carry `PLATFORM_OPS` which is not a macro (s.2a) |

---

## 2. The declared domain (postulate i needs one before MECE means anything)

**Domain:** *the macro a NEW project may register under, INTO THE TREE, for D12.* Nothing else.

The 354 flat rows are OUTSIDE the domain -- spec s.8, prospective only, no migration. This is not a
convenience: it is what makes the two `PLATFORM_OPS` rows below legal rather than violations.

### 2a. The two rows that look like counter-evidence and are not

`D12_PHONE_OTP_ALL_AWS` and `PLATFORM_OPS_USERMGMT` both carry `macro_code: PLATFORM_OPS`. That
value is **12 characters and cannot match the ratified macro grammar `^[A-Z]{4}$`** -- so it is not
a macro that this enum declines to list, it is **not a macro at all**. Both are pre-macro flat rows
the enum does not govern.

**FORWARD CONSEQUENCE, stated here rather than discovered later** (the same shape the D0/D8/D11
record recorded for `GLOBALALARM`): neither row can ever be moved INTO the D12 tree while it carries
`PLATFORM_OPS`. A tree home for either needs a ratified 4-char macro first, and that is a fresh
Rule 24 record plus Andrew's word -- never a bare edit, and never a macro invented to make this
sentence come out even.

### 2b. And the one conforming row still cannot enter the tree -- for a DIFFERENT reason

`NFRA_SECURITY202609` carries `macro_code: NFRA` and conforms to this enum exactly. It is
nonetheless barred from the tree by **refusal R1**: the ratified project-code grammar is
`^[A-Z]{4}_[A-Z0-9]{4,12}$` and `SECURITY202609` is **14 characters**. Andrew named that code
personally 2026-09-02 (*"id call it NFRA_SECURITY202609"*) and it is registered FLAT, which is legal.
**Recorded because the two constraints are independent and a reader who checks only the macro will
conclude the project is tree-ready.** Any move needs a rename on his word first.

---

## 3. The four postulates

**(i) MECE over the declared domain -- and the uncovered-member hunt found a real one.**
Exhaustive over what exists: the only conforming macro among D12's rows is `NFRA`, and one enum
value cannot overlap itself, so mutual exclusivity is trivial here.
**THE HUNT, and it does not come back empty:** D12's own register text names remaining scope that
`NFRA` does NOT describe -- remembered-device policy, onboarding/account-creation redesign, a
front-end admin UI, and partner-admin delegated user-add. That is **platform / user-management**, not
infrastructure.
**The honest answer is not that `NFRA` covers it. It is that no such project is being registered into
the tree**, so it is not yet a member of the DOMAIN -- which is a different thing from being covered,
and is exactly the distinction the D8 record drew for `GLOBALALARM`. Andrew's word is `[NFRA]`
EXACTLY, and he said a wider list needs a fresh word. **So the first D12 platform-management project
that wants a tree home will need a new macro, a new Rule 24 record and a new word from him.** Naming
that now is the point of the hunt; a proposal that reported "MECE, no uncovered members" would be
false, and would fail silently the day someone tried to register that project.

**(ii) Same grain.** One value, a four-letter NAMESPACE, identical in kind to `NFRA`/`ETFS`/`MDPF`/
`AUTH` in the ratified sets. No entry is a project, a status, or a phase.

**(iii) Intent coherence.** One axis: *which product/system line does this project belong to.* Not
lifecycle, not ownership, not priority.

**(iv) State coherence -- which values one remedy does NOT move.** Ratifying D12's list moves NO
other directive's list. `NFRA` already appears under D0 and D11, ratified separately and on their own
records; this record does not touch them and ratifying it changes nothing about either. That a macro
repeats across directives is by design (Rule 24 iv, and MACROS.yaml says so on its own face).

---

## 4. Word-boundary token census (denominators printed; my own read, 2026-09-03 ~02:0xZ)

**DENOMINATOR: 354 flat rows parsed of 354 files in `org/projects/*.json`; 0 parse errors.**

| token | `macro_code` whole-value | code prefix | both agree | active (both) | by directive (`macro_code`) |
|---|---|---|---|---|---|
| `NFRA` | 89 | 87 | 85 | 9 | D0 5, D11 3, D12 1, none 80 |

**Whole-value, not substring:** counted by equality on `macro_code` and by the code's first
underscore-delimited field, never by `grep NFRA`, which would also match `NFRA` inside prose.
**The 80 `none` rows are the pre-directive population** and are outside the domain (s.8).

⛔ **THIS CENSUS IS MINE AND IS NOT THE D0/D8/D11 RECORD'S.** That record read 87/85/83/9 at
~21:2xZ on 2026-09-02 at @d413196285. I re-measured rather than quoting it: the register gained rows
between the two vintages (352 -> 354), and a relayed measurement loses the qualifier that makes it
true. The two disagree by exactly the drift and neither is wrong.

---

## 5. What makes the enum BIND (the consuming half)

`.tools/missions-tree-index.py` refusal **R2**: a project may not register under a macro absent from
this carrier, or under a directive whose enum is not RATIFIED. **Until D12 is ratified the tree
accepts NOTHING under it** -- and that is a refusal, not a gap. The enforcement is the pre-commit
stage installed per device (`.tools/git-hooks/install-missions-tree-check.sh`); git hooks are not
versioned, so on any device the refusal is DESIRED until that installer runs. It was installed on
site Z 2026-09-03 ~02:0xZ.

---

## 6. Alternatives named and rejected

- **`[NFRA, PLAT]`** -- mint a 4-char macro now for the platform/user-management scope in s.3(i).
  REJECTED: Andrew's word is `[NFRA]` exactly and he said a wider list needs a fresh one. Minting a
  macro to close an uncovered member that has no project behind it yet is inventing a taxonomy value
  for a population of zero -- and the D0/D8/D11 record rejected the mirror of this move
  (`GLOB` for GLOBALALARM) for the same reason.
- **`[PLATFORM_OPS]`** -- adopt the value two of the three rows already carry. REJECTED: 12
  characters, cannot match `^[A-Z]{4}$`. Not a live option; recorded because it is the value a
  reader censusing D12 would reach for first.
- **No D12 enum at all** -- leave it absent, since nothing can enter the tree under D12 today.
  REJECTED: absent and ratified-empty are different states, and the absent one gives a future
  registrant no signal about which of the two it is hitting. The enum also costs nothing while
  unused: prospective scope means it governs no existing row.

---

## 7. Ratification mechanics (so the flip is a record, not an edit)

`directives.D12.ratification` in `org/missions/MACROS.yaml` moves from absent to
`RATIFIED <this record> <date>` **citing BOTH** this record and Andrew's 2026-09-03 ~01:5xZ word as
relayed at bus id `e8421d1a-4e33-4b7d-a6d3-0558bab6a752`. Per his instruction no further word is
needed for `[NFRA]`. **Any addition to this list is a NEW record, a NEW census and a NEW word from
him.** Nobody else flips it, and this record does not flip itself: the carrier edit is the act.
