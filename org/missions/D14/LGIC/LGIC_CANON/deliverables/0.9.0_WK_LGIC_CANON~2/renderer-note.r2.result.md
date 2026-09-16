# renderer-note.r2.result -- LGIC_CANON.CN-k-3-r2 (cell CN-k-3, the renderer), 0.9.0_WK_LGIC_CANON~2

Worktree `C:\Users\AndrewBerman\Desktop\ajb_workspace\.worktrees\wk-lgic-canon-2-9`, branch
`wk-lgic-canon-2-9`, base CLOUD @`7db18a4464`. Artifacts committed at `4ee952a3e4`.

## What the cell asked, and what landed

Row `LGIC_CANON-S3`: `render_naming_section.py` reads firm forms from `NAMING_SCHEMA.json`
`firm_forms` while that field exists and from `infra/logic/registry/scopes.json`'s FIRM rows once it
does not, and the two readers are not equivalent -- the schema path emits a per-firm `note`, the
registry path never read one. NAMING_SCHEMA v1.9 moved the forms, so the canon's generated section
lost the `demo` note carrying RULING DM, and `--check` went on reading FRESH because the section was
a faithful render of what the renderer chose to read.

1. **The registry path reads `note`.** `firm_rows()` @`4ee952a3e4` now builds its rows with
   `r.get("note", "") or ""`. The `note` flows into the same `notes` block the schema path used, so
   the `demo` bullet renders in exactly the old form. The re-render adds **two lines** to
   `infra/logic/02_DOCTRINE.md` and nothing else -- the bullet and its preceding blank line
   (`git show 4ee952a3e4 -- infra/logic/02_DOCTRINE.md`: `2 insertions(+)`, 0 deletions).
2. **`--content-diff`, the arm (ruling A-11).** It never renders. It enumerates the CONTENT of the
   SOURCE files and asks, item by item, whether the section carries that text, printing
   `CONTENT-DIFF: <n>` for the items it does not.
3. **Re-rendered with `--write`**, and `--check` still reads `CHECK: FRESH -- 0 failure(s)`.

## The arm, and why it is not the freshness check under a new name (K3-J1's question)

`--check` compares the section against a FRESH RENDER. It can therefore only ever see a difference
this script would itself produce: a field the renderer never reads produces a section `--check` calls
FRESH for as long as the renderer keeps not reading it. That is precisely how the `demo` note was
lost in silence. The arm reads the SOURCES instead and never calls `render()`.

**THE DISCRIMINATING PAIR -- one tree, one moment, two instruments, opposite readings.** A copy of
the renderer with the registry `note` read reverted to `""` (the pre-fix behaviour, i.e. the state of
`infra/logic/render_naming_section.py` at `7db18a4464`) was run from `.scratch/ctl/` -- two levels
deep, so `Path(__file__).resolve().parents[2]` still resolves to the worktree root and every default
path resolves identically -- against the section as it then stood:

```
=== control A: PRE-FIX renderer, --check on the section as it stands (expect FRESH)
OK: stamp infra/logic/registry/scopes.json - sha256:b2a54608f8ebbade98982de9fc8ae6a7d4e40ce83ee4f32c146f08cd69a0034b equals the live file
OK: the section's bytes equal a fresh render (134 lines, CRLF normalised)
CHECK: FRESH -- 0 failure(s)
rcA=0
=== control B: PRE-FIX renderer, --content-diff on the same section (expect 1)
items carried by the section: 197 of 198
DROPPED: infra/logic/registry/scopes.json scopes[demo]/note :: tenancy DEMO-TENANT: neither a firm nor general, it serves prospective users with demo accounts (infra/logic/02_DOCTRINE...
CONTENT-DIFF: 1
```

So: on the tree as it was at HEAD, `--check` says FRESH and the arm says the section is missing the
`demo` note, by name. **This arm would have caught the loss the moment v1.9 landed.** The control is
mine, not the checker's -- `k3_contentdiff`'s docstring claims it plants a removal and it does not
(row `LGIC_CANON-W2-S3`).

### The item set is a subtraction from a printed denominator, not a forward list

An item is a scalar leaf VALUE of a source, plus a dict KEY where the dict's keys are enumeration
MEMBERS rather than field names (node types, refused tokens, reserved words) -- the section presents
fields under its OWN prose labels, so a field NAME is not content it must carry. Both halves are
written as the printed denominator MINUS a DECLARED exclusion, and **every exclusion prints on every
run with its reason**, so a reader can dispute it. A source field named nowhere in the declaration is
IN the domain by default, which makes a newly added and unrendered field LOUD rather than silent.
Exclusions: 17 schema paths, 15 field-named dicts, 4 registry FIRM-row scalar fields.

Full run at `4ee952a3e4` (`python infra/logic/render_naming_section.py --content-diff`, rc=0):

```
CONTENT-DIFF ARM -- the section's content against its SOURCES' content, item by item.
  It never renders: a source field the renderer does not read is DROPPED here while --check
  still reads FRESH (row LGIC_CANON-S3). Exclusions are declared below, and a source field not
  named there is in the domain by default.
section: infra/logic/02_DOCTRINE.md, 136 lines between the markers
declared out-of-section, schema (17 paths):
  - /title -- the schema's own title; the section writes its own headings
  - /version -- carried by the section's stamp line, not as content
  - /ratified_by -- provenance of the schema, not naming content
  - /changelog -- the schema's own history
  - /authority -- who ratified which part; provenance, not naming content
  - /rows_owner -- points at the identity registry; ownership, not naming content
  - /node_type_vocabulary -- the vocabulary's provenance and denominator, not the enumerations
  - /firm_forms_source -- says where firm forms live; the forms themselves are the content
  - /tf_type_map -- the executable layer's type map, read by the grader, not presented by the canon
  - /tf_type_map_note -- prose about that map
  - /tf_unmapped_own_name -- same map's unmapped half
  - /tf_unmapped_own_name_note -- prose about that map
  - /kind/closed_at_l4 -- how the closed list was derived; provenance of the list, not the list
  - /key/legacy_served_paths/producer -- names the cell that will mint the list; provenance, not content
  - /aws_fixed/by_arn -- the grader's AWS-managed test, applied to live names, not presented
  - /aws_fixed/by_name -- the same test's name table
  - /aws_fixed/measured -- that table's measurement provenance
declared field-named dicts, schema (15; their KEYS are field names, only their VALUES are items): /, /key, /key/legacy_served_paths, /bucket, /resource, /kind, /cadence, /secret, /log_group, /iam_policy, /global_scope, /system, /grade, /aws_fixed, /firm_forms[]
schema org/standards/NAMING_SCHEMA.json: in-domain content items 185
declared out-of-section, a registry FIRM row's scalar fields (4):
  - class -- the row's class; the section renders only FIRM rows, so it is the selector, not content
  - tenancy -- the firm's tenancy, ruled in the canon's own prose (R-tenancy), not in this section
  - bucket -- the firm's bucket, an estate fact; the section renders the bucket GRAMMAR
  - bucket_provisioned -- whether that bucket exists; an estate fact
registry infra/logic/registry/scopes.json: FIRM rows 4, in-domain content items 13
items carried by the section: 198 of 198
CONTENT-DIFF: 0
```

### A second negative control, and the one item the domain excludes by judgment

Removing `/key/legacy_served_paths/producer` from the exclusion declaration and re-running on the
tree at `4ee952a3e4` prints `items carried by the section: 198 of 199` / `CONTENT-DIFF: 1`, naming
that path, while the live `--check` on the same tree prints `CHECK: FRESH -- 0 failure(s)`. That is a
SECOND live item of the same shape as the `demo` note: `key.legacy_served_paths` carries four fields
and the render prints three (`render_naming_section.py:157-160` @`7db18a4464`). It is declared
out-of-section rather than rendered because the cell says "No other output moves", and it is filed as
row `LGIC_CANON-W2-S4` so the choice is the CVO's to accept, not this worker's to bury. It doubles as
proof that the arm's exclusion list is the only thing standing between a real drop and a report.

## Criteria, verbatim output

All three run at HEAD `4ee952a3e4`, tracked worktree clean (`git status --porcelain` shows only the
untracked `.scratch/`), each under `timeout 120`, each rc=0.

**K3-AC1** -- `python .../check_canon_r2.py k3-note`
```
FIRM rows in the registry carrying a note, denominator 1: ['demo']
of those, rendered into the canon's generated section: 1 -- ['demo']
every FIRM note reaches the section: True
VERDICT: PASS-K3-FIRM-NOTE-RENDERED
```
Denominator: 1 of 1 FIRM rows carrying a note reaches the section. Measured independently of the
checker: of the registry's **4** FIRM rows (`49financial`, `inflection`, `cottonwood`, `demo`),
exactly one key list includes `note`, which is `demo`.

**K3-AC2** -- `python .../check_canon_r2.py k3-contentdiff`
```
renderer exposes --content-diff: True
...
registry infra/logic/registry/scopes.json: FIRM rows 4, in-domain content items 13
items carried by the section: 198 of 198
CONTENT-DIFF: 0
content-diff reads 0 dropped items on the true tree: True
VERDICT: PASS-K3-CONTENT-DIFF-ARM
```
Denominator: 198 of 198 in-domain source content items carried (185 schema + 13 registry), 0 dropped.

**K3-AC3** -- `python .../check_canon_r2.py k3-fresh`
```
OK: stamp infra/logic/registry/scopes.json - sha256:b2a54608f8ebbade98982de9fc8ae6a7d4e40ce83ee4f32c146f08cd69a0034b equals the live file
OK: the section's bytes equal a fresh render (136 lines, CRLF normalised)
CHECK: FRESH -- 0 failure(s)
render --check FRESH after the renderer edit: True
VERDICT: PASS-K3-RENDER-STILL-FRESH
```
Denominator: 2 of 2 stamped files hash equal to the live file, 0 failures; section 136 lines
(134 before the two-line re-render).

**K3-J1** -- judgment. RECORDED, no verdict; graded at L9 by `3.0.0_SA_CVO`. The record is the
discriminating pair above.

## Rows filed

| id | class | hazard | what |
|---|---|---|---|
| `LGIC_CANON-W2-S3` | OBSERVATION | INERT | `k3_contentdiff`'s docstring claims a planted-removal negative control; the subcommand (`check_canon_r2.py:245-260` @`7db18a4464`) plants nothing, so a constant `print("CONTENT-DIFF: 0")` passes K3-AC2 as cleanly as a real arm. The fixed input was not touched. |
| `LGIC_CANON-W2-S4` | OBSERVATION | INERT | `key.legacy_served_paths.producer` is a second source item the section drops the same way; declared out-of-section with its reason rather than rendered, because rendering it would move output the cell froze. |

## Bounds observed

No live name moved, no AWS call, no Terraform, no egress. Writes confined to the order's `<paths>`
(`infra/logic/render_naming_section.py`, `infra/logic/02_DOCTRINE.md`, the project's
`INVESTIGATION_v1.md`), this deliverables folder, and the order's own `<status>` line. The fixed
inputs under `.../2.0.0_SA_COO~G/fixed_inputs/r2/` were read and never written --
`git status --porcelain` lists none of them. `render_naming_section.py` stays pure ASCII (0
non-ASCII bytes, unchanged by this edit) and pure LF.
