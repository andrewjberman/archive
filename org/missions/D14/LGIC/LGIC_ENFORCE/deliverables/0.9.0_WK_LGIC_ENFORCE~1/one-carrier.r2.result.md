# LGIC_ENFORCE.TO-EN-r-3-r2 -- one carrier for a firm's forms: result

**Worker:** `0.9.0_WK_LGIC_ENFORCE~1` (slot ~1, queue position 1) · **Branch:** `wk-lgic-enforce-2-1`, cut from
`lgic-v19-group` @bd0f5d2c6c (which carries `lgic-v19-landing` @bf506e53be merged with CLOUD @eae996fb8e) ·
**Artifacts commit:** `22e86e55f5` · **Cell:** `EN-r-3` (RULING ONE, RULING DEMO, DEC-1) · **Nothing live moved:**
no AWS write, no Terraform apply.

## WHAT LANDED

1. **Every reader of the schema's firm-forms list is on the scope rows.** `lib/opal_naming.py` had four
   (`validate`'s schema read, its FIRM check, its warning, the system-key collision map, and that refusal's text).
   The schema read and the collision-map loop are gone -- the scope rows already carry every FIRM spelling through
   `_spellings()` -- the refusal text names only `scopes.json`, and the FIRM check is now a read of the row's own
   `note`. A FIRM row's own short form is the only spelling source `name()`, `fence_patterns()`, `grade()` and the
   generated views read. No code, comment or string in the file names the removed field.
2. **The Terraform test is generated.** `infra/aws/terraform/modules/opal_name/tests/opal_name.tftest.hcl` is a
   `generate` target (`--target ...opal_name.tftest.hcl`), carrying the GENERATED mark in HCL comment syntax, one
   `run "vector_NN"` block per vector and the `coverage` run holding the count the generator read, so **no count is
   typed** (row W1-S12). Its negative arms take their scopes from the registry -- a FIRM row's short form, and the
   first PRODUCT row that is not the arm's own system -- so no firm or product spelling is typed either. Twenty
   lines move against HEAD: the header block and one error message. The 32 vector runs and the four negative arms
   are byte-identical to the hand-kept file.
3. **DEC-1 (row W1-S8).** `bucket_basis` (the global row) and `label` (both MASTER rows) are removed: nothing read
   them. `note` is now READ by `validate` -- refused when present and not a non-empty string -- because RULING DEMO
   requires demo's note to carry a citation; that choice is row `LGIC_ENFORCE-W1-S25`. `scopes.json` `_about` now
   states the REQUIRED list (`key`, `class`, `long`, `short`, `tenancy`, `bucket`, `bucket_provisioned`, plus
   `firm` and `vendor` on a MASTER), names each further field with the reader that earns it, and carries an
   `one_home` line naming this registry as the one home of a firm's forms. It no longer names the schema's list
   (row S19).
4. **RULING DEMO.** `demo.tenancy` is `DEMO-TENANT`; `tiers.json` carries its home rule -- bronze and silver in
   `opal-data-assets` (R4), gold, platinum, `state/` and code in the demo tenant's own bucket `opal-data-demo`
   (doctrine s.1 "demo tenant", R5, R6, R21, R16; ledger X6 GRANTED, `infra/logic/06_CONFORMANCE_LEDGER.md` :94 and
   :137). Demo's note cites X6 and no longer says the doctrine does not define the class. Its `class` stays `FIRM`,
   so naming still reads `demo` in the firm slot (RULING DM).
5. **The reader census** is `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/FIRM_FORMS_READERS.md`: prose, then one
   fenced json block, **55 files** -- built by SUBTRACTION from an unscoped `git grep -l firm_forms` at four
   vintages (union 56) minus the one issuer instrument under `.../fixed_inputs/` and the record itself. 2
   `repointed`, 24 `historical-record`, 29 `another-project`. No file marked `repointed` names the token at the tip.

**Choices the order did not name** (each recorded): the `note` read (row W1-S25); the negative arms' scopes derived
from the registry rather than typed, which is why `refuses_product_scope` had to skip the arm's own system to keep
reading `etfs`; and `DEMO-TENANT`'s gold, `state/` and code homes, which the doctrine states for the demo tenant only
as its one bucket -- each rule string in `tiers.json` names the doctrine rule it applies.

**Base (row LGIC_ENFORCE-S20).** `check_en_r2.py`'s `spawn_base()` is `git merge-base HEAD CLOUD` = `eae996fb8e`,
CLOUD's side of the group merge, not `bf506e53be`. **No verdict turned on it:** the set of files naming the token at
`eae996fb8e` (54), at `bf506e53be` (38), at `bd0f5d2c6c` (55) and at the tip has a union of 56, and the only file at
`bf506e53be` that is not at `eae996fb8e` (`LGIC_NAMING_PRD.md`) is present at the tip, so the census's population is
the same either way; `lib/`, `infra/logic/registry/` and the `opal_name` module are byte-identical between
`eae996fb8e` and this branch's base (`git diff --stat` empty), so R3-AC10's base swap is this branch's own bytes.
No row was owed and none is filed for it.

## CRITERIA -- 10 of 10 mechanical PASS by output, 1 judgment RECORDED

Every invocation ran as `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/
2.0.0_SA_COO~G/fixed_inputs/r2/check_en_r2.py <sub>` (R3-AC10 at `timeout 300`, run alone, as it swaps the library
to the base's bytes while it runs). The checker exits 0 even on a FAIL verdict, so the VERDICT line is the reading.

```
===== r3-one-carrier                                                                     R3-AC1  rc=0
NAMING_SCHEMA.json v1.9 carries firm_forms: False
lib/opal_naming.py: CODE NAMING firm_forms (names and non-docstring strings) at lines []; comment or docstring mentions, not reads: 0
UNSCOPED: 35214 tracked file(s) scanned (git ls-files); naming firm_forms besides lib/opal_naming.py: 55, of which the issuer's instruments under org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs, excluded: 1, and the record itself
NOT A RECORDED NON-READER (historical-record or another-project) in org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/FIRM_FORMS_READERS.md: 0 []
VERDICT: PASS-ONE-CARRIER

===== r3-validate-clean                                                                  R3-AC2  rc=0
rc=0  REFUSED: 0  WARNINGS: 9, of which not an inferred-owner warning: 0 []
VALIDATE: OK 17 system row(s), 9 scope row(s), 9 warning(s) at registry@c68e07ef7044de07
VERDICT: PASS-VALIDATE-CLEAN

===== r3-new-firm-clean                                                                  R3-AC3  rc=0
WITHOUT the row: rc=0, 9 warning(s)  WITH one FIRM row quillwater/qwt: rc=0, 0 refusal(s), 9 warning(s)
WARNINGS NAMING THE NEW FIRM: []  REFUSALS: []
VERDICT: PASS-NEW-FIRM-CLEAN

===== r3-short-moves                                                                     R3-AC4  rc=0
ONE CHANGE: scopes.json 49financial short 49f -> f49 (in a scratch copy)  validate rc=0 refusals=0
name('mdpf','49financial','publisher','role') = mdpf-f49-publisher-role  fence_patterns('49financial') = ['arn:aws:iam::313476888478:role/*-f49-*']
VERDICT: PASS-ONE-CHANGE-MOVES-BOTH

===== r3-tftest-generated                                                                R3-AC5  rc=0
MARK PRESENT: True  VECTOR RUN BLOCKS: 32  VECTORS: 32  generate rc=0  REPRODUCED BYTE-FOR-BYTE: True
GENERATE: 1 written, 0 skipped, into C:\Users\ANDREW~1\AppData\Local\Temp\check_en_r2_gen_e07p011x at registry@c68e07ef7044de07
VERDICT: PASS-TFTEST-GENERATED

===== r3-dec1-fields                                                                     R3-AC6  rc=0
SCOPE-ROW FIELDS: 16  NAMED BY NO STRING IN lib/opal_naming.py: []
VERDICT: PASS-EVERY-FIELD-READ

===== r3-about-one-home                                                                  R3-AC7  rc=0
scopes.json _about mentions firm_forms: False
VERDICT: PASS-ABOUT-NAMES-ONE-HOME

===== r3-demo-tenant                                                                     R3-AC8  rc=0
demo tenancy: DEMO-TENANT  tiers.json homes: ['COMPOSITE', 'DEMO-TENANT', 'FIRM', 'PRODUCT']
demo note: tenancy DEMO-TENANT: neither a firm nor general, it serves prospective users with demo accounts (infra/logic/02_DOCTRINE.md s.1 demo tenant; ledger X6 GRANTED, Andrew ~01:3xZ 09-13 card 8, infra/logic/06_CONFORMANCE_LEDGER.md; RULING DEMO); its homes are tiers.json homes.DEMO-TENANT. Its class stays
VERDICT: PASS-DEMO-TENANT

===== r3-reader-census                                                                   R3-AC9  rc=0
FILES NAMING firm_forms: at the spawn base 54, here 53; LISTED 55
UNLISTED: []  LISTED BUT NEVER A READER: []  BAD DISPOSITION: []  'repointed' YET STILL NAMING IT: []
VERDICT: PASS-READERS-CENSUSED

===== r3-tests                                                                           R3-AC10 rc=0
FAILING HERE: 0  FAILING AT THE BASE'S BYTES: 0  NEW: []
VERDICT: PASS-NO-NEW-LIB-TEST-FAILURE
```

`R3-J1` is a judgment criterion: **RECORDED, no verdict.** It is graded at L9 by `3.0.0_SA_CVO`, and the proof
instance carries it `UNVERIFIABLE-BY-INSTRUMENT`. What the CVO reads: `FIRM_FORMS_READERS.md`'s 55 dispositions, and
whether DEC-1's required list as `_about` states it is the list `validate` enforces.

**Denominators.** R3-AC1: 35,214 tracked files scanned, 55 naming the token besides the library, 1 issuer instrument
excluded, 0 unrecorded. R3-AC9: 54 at the spawn base, 53 at the tip of commit `22e86e55f5`, 55 listed (the listed set
covers the union of both, which is why it exceeds each). R3-AC5: 32 run blocks for 32 vectors. R3-AC6: 16 scope-row
fields, 0 unread. R3-AC10: 77 tests, 0 failing here, 0 failing at the base's bytes, 0 new.

**Two counts move after this file is committed and are expected to:** `FIRM_FORMS_READERS.md` is rebuilt in the same
commit as this result and the proof instance, to list them both (each quotes the checker's output, so each names the
token once tracked). At the final tip the census reads 55 files here and 57 listed, and R3-AC1 and R3-AC9 were re-run
there to confirm both still PASS.

## ROWS FILED (surprise channel, `INVESTIGATION_v1.md`)

| id | class / hazard | what |
|---|---|---|
| `LGIC_ENFORCE-W1-S23` | OBSERVATION / **ARMED**, disarm owner `2.0.0_SA_COO~G` | LGIC_NAMING round 3's fixed inputs read the removed field as CODE: `blind_seat.py`:109 indexes `s["firm_forms"]` (KeyError under v1.9), `check_ln_r3.py`:281 reads `s.get("firm_forms", [])` (silently empty); the three r3 seat prompts carry a registry snapshot including `bucket_basis`. Not edited: the order forbids it. |
| `LGIC_ENFORCE-W1-S24` | OBSERVATION / **ARMED**, disarm owner `2.0.0_SA_COO~G` | LGIC_CANON's carriers still teach the removed field: `10_ONBOARDING_CHECKLIST.md`:72-77 tells a seat to APPEND a new firm to the schema list and to wait for a warning `validate` can no longer print; `02_DOCTRINE.md`:190 (generated, stamped v1.8); `check_canon_r1.py`:226. All outside this order's `<paths>`. |
| `LGIC_ENFORCE-W1-S25` | OBSERVATION / INERT | DEC-1 and RULING DEMO meet on `note`, which nothing read: the read was added to `validate` rather than the field removed. |

## INSTRUMENTS AND CONTROLS

- **Negative control (mutant):** the same nine subcommands were run on the pre-edit tree at `bd0f5d2c6c` before any
  edit; all nine printed FAIL (`FAIL-TWO-CARRIERS`, `FAIL-VALIDATE`, `FAIL-NEW-FIRM-WARNS`,
  `FAIL-ONE-CHANGE-DOES-NOT-MOVE-BOTH`, `FAIL-TFTEST-HAND-KEPT`, `FAIL-FIELD-NOTHING-READS`,
  `FAIL-ABOUT-NAMES-SECOND-LIST`, `FAIL-DEMO`, `FAIL-READER-CENSUS`). The instrument discriminates.
- **Determinism:** each of the nine ran twice, once before commit `22e86e55f5` and once after, with the same verdict
  both times; `r3-tftest-generated` re-derives the file with a second `generate` into a temp directory and reports
  `REPRODUCED BYTE-FOR-BYTE: True`.
- **Not re-measured:** nothing this cut already measures was re-derived, and no Terraform ran -- `terraform test` is
  not invoked here (the module's runner is EN-m-1's; this cell only generates the file).
