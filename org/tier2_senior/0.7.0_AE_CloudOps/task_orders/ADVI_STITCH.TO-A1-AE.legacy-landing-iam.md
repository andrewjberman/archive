# TO ADVI_STITCH.TO-A1-AE — PHASE A, AE lane: landing IAM on the three NEW legacy prefixes

<task_order id="ADVI_STITCH.TO-A1-AE" project="ADVI_STITCH">
<decomp_ref>workflows/atom_decomposition/runs/advi-stitch/20260824T222500Z/DECOMP.md @3ee0bec43b — cells STI-b-4, STI-inv-1</decomp_ref>
<decomp_context>Reads the DS lane's declared migration scope set (STI-b-0) as its input — the prefixes to grant on are DECLARED there, never inferred here. NOT in this TO: every copy, census and key cell (TO-A1-DS); the CVO firm-separation control; all Phase-B surfaces. *(Sibling element per the issuer fix on AE~G's harvest finding: an id inside `decomp_ref` reads as a cell this TO CLAIMS.)*</decomp_context>
<certification>**CERTIFIED DECOMP** — `3.0.0_SA_CVO` @43f9aaaeee (32/32, no P1).</certification>
<issued_to>AE-class (cloud/IAM). **Seated: a FRESH `0.7.0_AE_CloudOps~<letter>` for ADVI_STITCH ONLY, MSTR-assigned. ⛔ STAGED, NOT IMMEDIATE — capacity posture per MSTR (15 seats / 4.0 GB free). ⛔ AND EXPLICITLY NOT THE PERFRP LANE'S: `0.7.0_AE_CloudOps~G` holds ADVI_PERFRP and one project per instance binds.**</issued_to>
<executor_class>AE-class</executor_class>
<seating_trigger>**OBSERVED: the DS lane's `STI-b-0` scope-set declaration is COMMITTED** (the grant needs the prefix list to exist before it can be scoped to it). Verify it yourself by git, never on a message.</seating_trigger>
<placement>LAPTOP (Rule 26 — the apply runs on the device that owns the work, under the normal wrappers; nothing ferried).</placement>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-25T00:0xZ</issued>
<status>ACTIVE (start condition above; seating staged)</status>
<priority>P2 — Phase A gates nothing.</priority>
<scope_guard>ONE PROJECT, TWO CELLS. **No alarm, no monitor, no freshness checker** (moratorium). No bucket-policy edit on your own word — see AC3. Surprises: one line by MCP to `3.0.0_SA_CVO`, cc `2.0.0_SA_COO`. **Nothing to `4.0.0_SA_CRO*`.**</scope_guard>
<authority>PRD `ADVI_STITCH_PRD.md` v0.2 s.11 #1 (the landing) + CLAUDE.md Rule 22a (STATE/IAM grounding) + CTO's Q-s1/Q-s2 rulings (66836).</authority>
<proof_of_spec>
  <criterion id="STIA1AE-AC1" cell_refs="STI-b-4"/>
  <criterion id="STIA1AE-AC2" cell_refs="STI-b-4, STI-inv-1"/>
  <criterion id="STIA1AE-AC3" cell_refs="STI-b-4"/>
  <expected_criteria>STIA1AE-AC1,STIA1AE-AC2,STIA1AE-AC3</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ADVI_STITCH.TO-A1-AE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>cells declared: 2; criteria: 3; every criterion ≥1 cell_ref; both cells reachable. Unmapped 0; untraceable 0.</alignment_denominators>
</proof_of_spec>
</task_order>

## ⛔ SPEC-AT-PICKUP

| # | Premise | Oracle |
|---|---|---|
| O-1 | The three landing prefixes are NEW paths (no existing grant covers them) | `aws s3 ls s3://opal-data-assets/blackdiamond/49financial/` `# rail-checked` → EMPTY at issuance. ⚠ **EMPTY here means UNMINTED, which is the DECLARED expectation — NOT evidence about the live tree.** An unminted tree and a misnamed one are BYTE-IDENTICAL at this oracle, so this premise says nothing about where 49F data actually lives. **AC2's deny arm targets `blackdiamond/49f/` for exactly that reason.** |
| O-2 | The DS lane's scope set is committed (your start condition) | `git log` on the DS lane's commit; read the declared prefix list from the FILE |
| O-3 | A neighbouring grant exists to control against | an existing `blackdiamond/49f/silver/*` key, used as the positive control **in a separate invocation** |

## Cells

- **`STI-b-4` LANDING IAM** on `blackdiamond/49financial/bronze_legacy/*`, `.../silver_legacy/*`, and the 49F gold home's `gold/advi/reference/bd_legacy_*`.
- **`STI-inv-1` (IAM half)** — the grant is scoped so it CANNOT write the live `bronze/` or `silver/` tiers of that vendor tree. **The legacy tiers being unmistakably distinct is his ruling's load-bearing half; at the IAM layer that means a grant that cannot reach the live tiers even by mistake.**

⛔ **THE INSTRUMENT DISCIPLINE, because this is a NEW resource and `comp-iam` fails GREEN on exactly this shape** (it models `(action)`, never `(action, resource)` — a role holding `s3:PutObject` on ANY bucket reports GRANTED for every other):
- `aws iam simulate-principal-policy --policy-source-arn <role> --action-names <action> --resource-arns <ONE exact key>` — **ONE resource per call** (2+ ARNs flips the held ones to `implicitDeny`).
- **The positive control runs as a SEPARATE INVOCATION** — a control batched with the target is corrupted by its own presence.
- Validate action-name spelling with `aws accessanalyzer validate-policy`, **never** by reading a simulate result: a NONEXISTENT action also returns `implicitDeny`, so a typo is indistinguishable from a missing grant.
- Ground on **live `aws iam get-role-policy`** for APPLIED truth; a `comp-iam` view is DESIRED (parsed Terraform) and cannot tell landed from planned.

## Acceptance criteria

| id | criterion | cell_refs | grounding (Rule 22a) |
|---|---|---|---|
| **STIA1AE-AC1** | Write allowed on EACH of the three new prefixes: one `simulate-principal-policy` per exact key, ONE `--resource-arns` per call, positive control in a SEPARATE invocation, action names validated by `validate-policy`; plus live `get-role-policy` (APPLIED) and the TF plan 0-diff (DESIRED) | STI-b-4 | DESIRED + APPLIED + EXERCISED |
| **STIA1AE-AC2** | ⛔ **NEGATIVE, and it is the criterion that carries his ruling into IAM:** the same principal is DENIED on **`blackdiamond/49f/bronze/*` and `blackdiamond/49f/silver/*`** — one resource per call, deny shown, with the positive control from AC1 proving the instrument discriminates. **Cite a REAL KEY under each tier in your evidence.** *Optional ADDITIONAL arm, labelled PROSPECTIVE and NEVER a substitute for the live-tree arm: the mint's future `49financial/{bronze,silver}/*` leaves.* | STI-b-4, STI-inv-1 | EXERCISED |
<!-- AMENDED 2026-08-25 ~20:46Z by 2.0.0_SA_COO (issuer), on 0.7.0_AE_CloudOps~J's ARMED surprise 71404, disarmed same-turn.
     THE DEFECT: this row said "the LIVE `blackdiamond/49financial/bronze/*` and `.../silver/*` tiers". THOSE ARE NOT LIVE -- they are
     UNMINTED. `blackdiamond/` has EXACTLY TWO children, `49f/` and `cottonwood/` (denominator 2 of 2 enumerated, positive control run).
     The live 49F data sits under `blackdiamond/49f/{bronze,silver}/` -- real keys sampled in both.
     WHY IT MATTERED: run as written, AC2 returns a TRUE, well-controlled, correctly-denominated DENY on a path holding NOTHING, and ships
     GREEN on the criterion that carries the ruling into IAM -- while STI-inv-1's actual protective property goes COMPLETELY UNTESTED.
     A FALSE GREEN ON A PROTECTIVE CONTROL, which is the worst direction for this class to fail in.
     NOT AMENDED, because it is NOT a defect: the `blackdiamond/49financial/` landing prefix is a DELIBERATE MINT (Rule 17b
     {vendor}/{firm}/{medallion}; `49f/` is the legacy alias and nothing under it moves; ADVI_INSURE mints into the same tree). O-1's
     EMPTY is the DECLARED expectation for an unminted tree, not a vacuous pass. The DS lane's STI-b-0 root is UNCHANGED and ~Q was told so.
     No cell_ref, criterion id, alignment denominator or acceptance row count changed -- this row's TARGET moved, nothing else. -->
| **STIA1AE-AC3** | ⛔ **Q-s1 — THE BUCKET POLICY'S REACH, MEASURED NOT ASSUMED:** the parquet-deny policy is SEGMENT-matched on `bronze`, and `bronze_legacy` is a DIFFERENT segment. Run one denied-write probe under `bronze_legacy/` plus an ISOLATED positive control under a real `bronze/` segment, and REPORT which way it lands. **If the guard does not reach the legacy tier, the widening is a one-line policy segment addition PROPOSED TO CTO WITH THE PROBE RESULT — never self-applied (bucket policy is the infra lane).** Until then the no-parquet property rests on the DS lane's `inv-2` and the report says so | STI-b-4 | EXERCISED |

## Law that binds
Rules 1–6 (Terraform is the only mechanism; commit before apply; source map) · Rule 18 (`safe-apply`, never bare) · NEVER#4 · **NEVER#6 — a begun deploy FINISHES in-session or rolls back loud; open a deploy-completion ledger entry at start and CLOSE it** · NEVER#2 (no cross-firm read) · Rule 22a · Rule 26 (apply on this box).
⛔ **Q-s2, RULED BY CTO AND RECORDED HERE SO A BUCKET-KEYED AUDIT CANNOT RE-OPEN IT:** `opal-data-bd` → `opal-data-49financial/gold/advi/reference/bd_legacy_*` is a cross-BUCKET copy INSIDE ONE FIRM (both are 49F-firm trees). **NEVER#2 binds FIRMS, not buckets.** State that reading in your evidence.

## Status + reporting
Cell-level `<cell_status>`; proof instance + flip in one commit. Report to COO with hash + push state; cc `3.0.0_SA_CVO` at AC2 and AC3 (the negative control and the policy-reach probe are the two that carry the ruling).
