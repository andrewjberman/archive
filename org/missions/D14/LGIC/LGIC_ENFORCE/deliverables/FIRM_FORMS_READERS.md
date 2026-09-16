# FIRM_FORMS_READERS -- every tracked file that names `firm_forms`, and its disposition (LGIC_ENFORCE EN-r-3 item 5)

**Author:** `0.9.0_WK_LGIC_ENFORCE~1`, on `LGIC_ENFORCE.TO-EN-r-3-r2` (RULING ONE: one carrier). **Built by** an unscoped
`git grep -l firm_forms` over tracked files, run at four vintages, with nothing narrowed but the two exclusions below.

**What changed.** NAMING_SCHEMA.json v1.9 removed the schema's list of firm forms. `infra/logic/registry/scopes.json` is now
the ONE home of a firm's forms: a FIRM row's own long and short are the only spelling source. The only code that read
the list is `lib/opal_naming.py`, which now reads the scope rows. Every other file below names the word and reads no
list: each is a historical record (a round's record, a review, an adjudication, a log) or another project's file.

**The population, by subtraction.** Files naming the token at each vintage (tracked files, `git grep -l`):

- `eae996fb8e` (the checker's spawn base, git merge-base HEAD CLOUD (row LGIC_ENFORCE-S20)): 55
- `bf506e53be` (lgic-v19-landing, NAMING_SCHEMA.json v1.9 ADMITTED): 38
- `bd0f5d2c6c` (lgic-v19-group, this worktree's base): 56
- the tip (this branch's worktree, plus this order's own proof and result): 57

Their union is 59 files, MINUS 1 issuer instrument(s) under `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/` (excluded by the order; R3-AC1 prints the exclusion: `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_en_r2.py`) MINUS this record itself = **57 files, each listed below**.

**Dispositions:** another-project 29, historical-record 26, repointed 2. `repointed` means the file no longer names the token at the tip;
no file marked `repointed` names it there (checked when this file was built).

**Readers that are code and not this order's.** Three files outside this order's paths still READ the schema list as code: LGIC_NAMING round 3's `blind_seat.py` and `check_ln_r3.py` (row LGIC_ENFORCE-W1-S23, for the issuer) and LGIC_CANON round 1's `check_canon_r1.py` (row LGIC_ENFORCE-W1-S24). A fourth, LGIC_CANON's `render_naming_section.py`, reads it only while it exists and falls back to the registry. None is edited here.

```json
{
 "readers": [
  {
   "path": "docs/briefs/sources/LGIC_CANON_L4_BRIEF_REVIEW_20260914.md",
   "disposition": "historical-record",
   "why": "An L4 brief review: the dated record of one PRD version's review, read by no code."
  },
  {
   "path": "docs/briefs/sources/LGIC_ENFORCE_L4_BRIEF_REVIEW_v1_2_20260915.md",
   "disposition": "historical-record",
   "why": "An L4 brief review: the dated record of one PRD version's review, read by no code."
  },
  {
   "path": "docs/briefs/sources/LGIC_NAMING_L4_BRIEF_REVIEW_v1_7_20260915.md",
   "disposition": "historical-record",
   "why": "An L4 brief review: the dated record of one PRD version's review, read by no code."
  },
  {
   "path": "docs/briefs/sources/LGIC_NAMING_L4_BRIEF_REVIEW_v1_9_20260915.md",
   "disposition": "historical-record",
   "why": "An L4 brief review: the dated record of one PRD version's review, read by no code."
  },
  {
   "path": "infra/logic/02_DOCTRINE.md",
   "disposition": "another-project",
   "why": "LGIC_CANON's doctrine. Its generated naming section is stamped NAMING_SCHEMA.json v1.8 (:163) and says the forms are read from the schema list (:190): a text, which render_naming_section.py re-renders from the registry once run. Outside this order's paths; row LGIC_ENFORCE-W1-S24."
  },
  {
   "path": "infra/logic/10_ONBOARDING_CHECKLIST.md",
   "disposition": "another-project",
   "why": "LGIC_CANON CN-o-1's onboarding checklist. Its firm-forms step (:72-77) tells a seat to append to the schema list and quotes the validate warning this cell removes: a text read by no code. Outside this order's paths; row LGIC_ENFORCE-W1-S24."
  },
  {
   "path": "infra/logic/registry/scopes.json",
   "disposition": "repointed",
   "why": "_about.row_fields named the schema list as the owner of which firm short forms exist (row S19), and demo's note cited it. _about now states DEC-1's required fields and names this registry as the one home of a firm's forms; demo's note cites X6. Nothing in the file names the list at the tip."
  },
  {
   "path": "infra/logic/render_naming_section.py",
   "disposition": "another-project",
   "why": "LGIC_CANON CN-k-1's renderer of 02_DOCTRINE.md's naming section. It reads schema.get('firm_forms') only while the field exists (:98-101), and otherwise the FIRM rows of scopes.json (:102-107), so under v1.9 it takes the registry branch with no edit. Outside this order's paths; row LGIC_ENFORCE-W1-S24."
  },
  {
   "path": "lib/opal_naming.py",
   "disposition": "repointed",
   "why": "The one code reader (1.0.0_SA_CTO 97200; 4.0.0_SA_CRO note b). Its four reads -- the schema read, validate's FIRM check and its warning, the system-key collision map, and that refusal's text -- now read the scope rows, where a FIRM row's own short form is the only spelling source. Nothing in the file names the list at the tip (R3-AC1 prints its lines)."
  },
  {
   "path": "org/audit/archive/laptop/2026-09-14T160021Z/org_mcp_comp-which-rail.log",
   "disposition": "historical-record",
   "why": "An archived tool log (the comp-which rail), a dated record read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_CANON/decompositions/LGIC_CANON_DECOMP.md",
   "disposition": "another-project",
   "why": "LGIC_CANON's round record (a decomposition, a task order, a proof, a result or its channel), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_CANON/deliverables/0.9.0_WK_LGIC_CANON~1/LGIC_CANON.TO-CN-k-1.canon.proof_of_spec.json",
   "disposition": "another-project",
   "why": "LGIC_CANON's round record (a decomposition, a task order, a proof, a result or its channel), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_CANON/deliverables/0.9.0_WK_LGIC_CANON~1/canon.r1.result.md",
   "disposition": "another-project",
   "why": "LGIC_CANON's round record (a decomposition, a task order, a proof, a result or its channel), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/CN_JUDGE_NAMING_KEY.json",
   "disposition": "another-project",
   "why": "LGIC_CANON round 1's issuer answer key, read-only to this order: it names the schema list in its text, and no code reads a list from it."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/CN_NAMING_KEY.json",
   "disposition": "another-project",
   "why": "LGIC_CANON round 1's issuer answer key, read-only to this order: it names the schema list in its text, and no code reads a list from it."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_canon_r1.py",
   "disposition": "another-project",
   "why": "LGIC_CANON round 1's issuer instrument, read-only to this order: :226 iterates s.get('firm_forms') or [], empty under v1.9. Row LGIC_ENFORCE-W1-S24."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_CANON/surprise-channel/investigations/INVESTIGATION_v1.md",
   "disposition": "another-project",
   "why": "LGIC_CANON's round record (a decomposition, a task order, a proof, a result or its channel), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_CANON/task-orders/LGIC_CANON.TO-CN-k-1.canon.md",
   "disposition": "another-project",
   "why": "LGIC_CANON's round record (a decomposition, a task order, a proof, a result or its channel), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_ENFORCE/decompositions/LGIC_ENFORCE_DECOMP.md",
   "disposition": "historical-record",
   "why": "This project's decomposition (v2.1), the round's record of the cells; it names the list as the thing EN-r-3 removes. Read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/LGIC_ENFORCE.TO-EN-r-1.registry-and-generator.proof_of_spec.json",
   "disposition": "historical-record",
   "why": "A round-1 record of this project (a proof, a result, or an exercise or census record), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/LGIC_ENFORCE.TO-EN-r-3-r2.one-carrier.proof_of_spec.json",
   "disposition": "historical-record",
   "why": "This order's proof-of-spec instance: it quotes the checker's output, which names the list. Read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/LGIC_ENFORCE.TO-EN-x-1.fwd2-real-resource.proof_of_spec.json",
   "disposition": "historical-record",
   "why": "A round-1 record of this project (a proof, a result, or an exercise or census record), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/fwd2-real-resource.result.md",
   "disposition": "historical-record",
   "why": "A round-1 record of this project (a proof, a result, or an exercise or census record), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/one-carrier.r2.result.md",
   "disposition": "historical-record",
   "why": "This order's result file: it records the checker's output verbatim, which names the list. Read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~8/LGIC_ENFORCE.TO-EN-d-1.fwd7-demo-firm.proof_of_spec.json",
   "disposition": "historical-record",
   "why": "A round-1 record of this project (a proof, a result, or an exercise or census record), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~8/fwd7-demo-firm.result.md",
   "disposition": "historical-record",
   "why": "A round-1 record of this project (a proof, a result, or an exercise or census record), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/EXERCISE_FWD2.md",
   "disposition": "historical-record",
   "why": "A round-1 record of this project (a proof, a result, or an exercise or census record), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/EXERCISE_FWD7.md",
   "disposition": "historical-record",
   "why": "A round-1 record of this project (a proof, a result, or an exercise or census record), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/FENCE_WRITER_CENSUS.md",
   "disposition": "historical-record",
   "why": "A round-1 record of this project (a proof, a result, or an exercise or census record), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_ENFORCE/prd/LGIC_ENFORCE_PRD.md",
   "disposition": "historical-record",
   "why": "This project's PRD v1.2 (ADMITTED), the ratified text that predates NAMING_SCHEMA.json v1.9. Read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_ENFORCE/surprise-channel/adjudications/ADJUDICATION_v1.md",
   "disposition": "historical-record",
   "why": "This project's surprise channel (investigation rows, adjudications, remediations), an append-only record. Read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_ENFORCE/surprise-channel/investigations/INVESTIGATION_v1.md",
   "disposition": "historical-record",
   "why": "This project's surprise channel (investigation rows, adjudications, remediations), an append-only record. Read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_ENFORCE/surprise-channel/remediations/REMEDIATION_v1.md",
   "disposition": "historical-record",
   "why": "This project's surprise channel (investigation rows, adjudications, remediations), an append-only record. Read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_ENFORCE/task-orders/LGIC_ENFORCE.TO-EN-r-3-r2.one-carrier.md",
   "disposition": "historical-record",
   "why": "This order's own text, which names the list it repoints. Read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/decompositions/LGIC_NAMING_DECOMP.md",
   "disposition": "another-project",
   "why": "LGIC_NAMING's record (a PRD, a decomposition, a task order, a proof, a result, an exercise or its channel), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/0.9.0_WK_LGIC_NAMING~1/LGIC_NAMING.TO-LN-f-1.firm-patterns.proof_of_spec.json",
   "disposition": "another-project",
   "why": "LGIC_NAMING's record (a PRD, a decomposition, a task order, a proof, a result, an exercise or its channel), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/0.9.0_WK_LGIC_NAMING~4/LGIC_NAMING.TO-LN-f-1-r2.firm-patterns.proof_of_spec.json",
   "disposition": "another-project",
   "why": "LGIC_NAMING's record (a PRD, a decomposition, a task order, a proof, a result, an exercise or its channel), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/0.9.0_WK_LGIC_NAMING~5/reader.result.md",
   "disposition": "another-project",
   "why": "LGIC_NAMING's record (a PRD, a decomposition, a task order, a proof, a result, an exercise or its channel), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r3/blind_seat.py",
   "disposition": "another-project",
   "why": "LGIC_NAMING round 3's issuer instrument: :109 indexes s['firm_forms'], a KeyError under v1.9. Not edited: the face forbids it. Row LGIC_ENFORCE-W1-S23 is for the issuer."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r3/check_ln_r3.py",
   "disposition": "another-project",
   "why": "LGIC_NAMING round 3's issuer instrument: :281 reads s.get('firm_forms', []), an empty list under v1.9. Not edited: the face forbids it. Row LGIC_ENFORCE-W1-S23 is for the issuer."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md",
   "disposition": "another-project",
   "why": "LGIC_NAMING's grading rule, which LN-g-1 rewrites on its own branch this round. It names the schema field in its text. Not this order's file."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n4-firm-patterns.md",
   "disposition": "another-project",
   "why": "LGIC_NAMING's record (a PRD, a decomposition, a task order, a proof, a result, an exercise or its channel), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r2/n4-firm-patterns.md",
   "disposition": "another-project",
   "why": "LGIC_NAMING's record (a PRD, a decomposition, a task order, a proof, a result, an exercise or its channel), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r2/seats/e1.prompt.txt",
   "disposition": "another-project",
   "why": "LGIC_NAMING's record (a PRD, a decomposition, a task order, a proof, a result, an exercise or its channel), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r2/seats/e2.prompt.txt",
   "disposition": "another-project",
   "why": "LGIC_NAMING's record (a PRD, a decomposition, a task order, a proof, a result, an exercise or its channel), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r3/seats/e1.prompt.txt",
   "disposition": "another-project",
   "why": "A seat prompt among LGIC_NAMING round 3's fixed inputs: it shows its seat the schema list, and scopes.json's bucket_basis, which DEC-1 removes. Not edited: the face forbids it. Row LGIC_ENFORCE-W1-S23 is for the issuer."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r3/seats/e2.prompt.txt",
   "disposition": "another-project",
   "why": "A seat prompt among LGIC_NAMING round 3's fixed inputs: it shows its seat the schema list, and scopes.json's bucket_basis, which DEC-1 removes. Not edited: the face forbids it. Row LGIC_ENFORCE-W1-S23 is for the issuer."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r3/seats/e4.prompt.txt",
   "disposition": "another-project",
   "why": "A seat prompt among LGIC_NAMING round 3's fixed inputs: it shows its seat the schema list, and scopes.json's bucket_basis, which DEC-1 removes. Not edited: the face forbids it. Row LGIC_ENFORCE-W1-S23 is for the issuer."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/prd/LGIC_NAMING_PRD.md",
   "disposition": "another-project",
   "why": "LGIC_NAMING's record (a PRD, a decomposition, a task order, a proof, a result, an exercise or its channel), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/surprise-channel/investigations/INVESTIGATION_v1.md",
   "disposition": "another-project",
   "why": "LGIC_NAMING's record (a PRD, a decomposition, a task order, a proof, a result, an exercise or its channel), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/task-orders/LGIC_NAMING.TO-LN-e-4-r3.reader.md",
   "disposition": "another-project",
   "why": "LGIC_NAMING's record (a PRD, a decomposition, a task order, a proof, a result, an exercise or its channel), read by no code."
  },
  {
   "path": "org/missions/D14/LGIC/LGIC_NAMING/task-orders/LGIC_NAMING.TO-LN-g-1-r4.grading-rule.md",
   "disposition": "another-project",
   "why": "LGIC_NAMING's record (a PRD, a decomposition, a task order, a proof, a result, an exercise or its channel), read by no code."
  },
  {
   "path": "org/standards/NAMING_SCHEMA.json",
   "disposition": "historical-record",
   "why": "The carrier this ruling removed. At v1.9 (1.0.0_SA_CTO, @645725150b on lgic-v19-landing) it has no firm_forms key: the word survives only in its changelog (v1.7, v1.9) and in the key firm_forms_source, which says the registry is the one home. No code reads a list from it."
  },
  {
   "path": "org/tier1_exec/1.0.0_SA_CTO/deliverables/ROUND_ANALYSIS_LGIC_ENFORCE_ROUND1_20260915.md",
   "disposition": "historical-record",
   "why": "A round analysis by 1.0.0_SA_CTO: the dated ruling record, and RULING ONE's source for this project. Read by no code."
  },
  {
   "path": "org/tier1_exec/1.0.0_SA_CTO/deliverables/ROUND_ANALYSIS_LGIC_NAMING_ROUND2_20260915.md",
   "disposition": "historical-record",
   "why": "A round analysis by 1.0.0_SA_CTO: the dated ruling record, and RULING ONE's source for this project. Read by no code."
  },
  {
   "path": "org/tier1_exec/2.0.0_SA_COO/drive_log_20260915T1655Z~G.md",
   "disposition": "historical-record",
   "why": "2.0.0_SA_COO~G's drive log, a dated record read by no code."
  },
  {
   "path": "org/tier1_exec/3.0.0_SA_CVO/deliverables/PRD_REVIEW_LGIC_NAMING_v1.1_RATIFIED_TEXT_HALF_20260913.md",
   "disposition": "historical-record",
   "why": "A PRD review by 3.0.0_SA_CVO, a dated record read by no code."
  }
 ]
}
```
