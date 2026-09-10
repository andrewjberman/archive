# IB-s-18 RESULT -- THE FOUNDATION: eleven contract schemas, three code homes, the path/owner manifest, the nine Terraform roots

**TO:** `IRPT_BCKEND.TO-IB-s-18` | **worker:** `0.9.0_WK_IRPT_BCKEND~1` | **branch:** `wk-irpt_bckend-1-1`
**base commit:** `261c8d2080` (HEAD of `CLOUD` at hand-off) | **PRD pin:** `62301f71e0`
**Deploys nothing.** No `terraform init`, no `plan`, no `apply`, no AWS write, no vendor call, no network call.

## Criteria

| id | verdict | invocation | deciding line |
|---|---|---|---|
| `S18-AC1` | **PASS-by-output** | `timeout 300 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/battery_ib_s_18.py` | rc=0, `arms: 5 of 5 evaluated; arms holding: 5 of 5; assertions failed: 0` then `IBS18-FOUNDATION-COMPLETE` |
| `S18-AC2` | **RECORDED (judgment)** -- no verdict | evidence assembled for `3.0.0_SA_CVO` at L9 | in the proof-of-spec instance under `UNVERIFIABLE-BY-INSTRUMENT` |

Full transcript: `IB-s-18_S18-AC1_battery_output.txt` (85 lines), committed beside this file so a reader gets every
denominator without re-running the battery.

## The five arms, with their numbers

- **(a) ELEVEN OF ELEVEN, FROM THE TABLE.** 11 of 11 contract rows parsed from
  `git show 62301f71e0:.../IRPT_BCKEND_PRD.md`; **72 of 72** required-meaning items carried by a property whose
  description quotes the item VERBATIM; **384 of 384** description quotes resolve verbatim in the CONTRACTS section
  at that pin (the backward anti-fabrication control); `additionalProperties: false` at the top level on 11 of 11.
- **(b) EVERY FIXTURE PAIR DISCRIMINATES.** 11 of 11 valid fixtures ACCEPTED, 11 of 11 invalid fixtures REFUSED by
  `jsonschema` Draft 2020-12. Each invalid fixture is aimed at that contract's own hazard, not at a generic type
  error: `CLIENT` in a cohort enum, a duplicated permitted account, a return rendered as `"2.11%"`, a missing
  `destination_policy_revision`, a section with no `units`, `asserts_causation: true`,
  `live_vendor_request_during_render: true`, `vendor_signed_url_exposed: true`, an invented state `done`, a package
  with no print entry point.
- **(c) THE MANIFEST COVERS THE PRD'S PATHS TABLE.** 31 PATHS rows (26 reuse, 5 new) expanding to **74 tokens**;
  **74 of 74** present in `PATH_MANIFEST.json` with a non-empty `kind`, `cell`, `owner` and `use`. Coverage is
  matched on the RAW TABLE TOKEN so a resolution bug cannot make the arm pass falsely; the 44 entries claiming
  `PRESENT_AT_PIN` are then verified independently with `git cat-file -e 261c8d2080:<path>`, 44 of 44. Presence
  breakdown sums to the denominator: PRESENT_AT_PIN 44, NOT_A_REPO_PATH 15, SUBMODULE_NOT_CHECKED_OUT 9,
  ABSENT_AT_PIN_GITIGNORED 3, ABSENT_BY_DESIGN_NEW_HOME 3 = 74. The three new homes are ABSENT-BY-DESIGN at the base
  commit, 3 of 3.
- **(d) NINE ROOTS, NINE DISTINCT STATE KEYS, ZERO STATE.** 9 roots, 9 of 9 keys pairwise distinct and all under
  `investor-reporting/`, bucket/region/provider/default-tags correct on 9 of 9; **0** `.terraform/` directories and
  **0** `terraform.tfstate*` files under the tree -- 0 of 9 roots initialised.
- **(e) THE REGISTER CARRIES PART V.** 7 of 7 Part V items parsed from BRIEF COVERAGE entry 25 and carried VERBATIM
  by `DEPENDENCY_REGISTER.md`, 7 of 7 with a non-empty owner.

## What was built

**Generated, not authored.** The eleven schemas, the manifest, the register and the nine `main.tf` skeletons are all
emitted from parsed sources -- the PRD at `62301f71e0` and the decomposition's section 6 table -- so no number in any
of them is a transcription. The generators live in this worker's `.scratch/` and are not deliverables; every
artifact they produce is re-checked by the battery from the SOURCE rather than from the generator.

- `infra/aws/lambda/investor-reporting/_contracts/` -- 11 schemas + 22 fixtures. 361 named properties, each citing
  its table item.
- `infra/aws/lambda/investor-reporting/{README.md, PATH_MANIFEST.json, DEPENDENCY_REGISTER.md}`.
- `infra/aws/terraform/investor-reporting/README.md` + 9 `<root>/main.tf`.
- `data/assets/scripts/gold/investor_reporting/README.md`.
- `.../deliverables/0.9.0_WK_IRPT_BCKEND~1/{battery_ib_s_18.py, IB-s-18_S18-AC1_battery_output.txt, this file}`.

Two design decisions worth a reader's attention:

1. **The cohort enums have no `CLIENT` member and no boolean.** `DirectoryEntry.cohort` and
   `HoldingsSnapshot.nodes[].classification` each carry `fee_taking_status`, `advisory_status` and
   `vendor_account_supervised` as three SEPARATE enums, each with an explicit `UNKNOWN`. The semantics paragraph says
   an unknown value is never false and never Client; the missing enum member is what makes that machine-checkable,
   and it is what both cohort invalid fixtures exercise.
2. **The manifest records presence with a measured instrument, not a boolean.** A gitignored brand asset, a file
   inside an unchecked-out submodule, a proposed S3 layout and a genuinely absent path all look identical to
   `os.path.exists()`. They are five distinct values here, and the difference is the subject of row
   `IRPT_BCKEND-W1-S2`.

## Rows filed

- `IRPT_BCKEND-W1-S1` (OBSERVATION, INERT) -- the face's L5 note says the manifest expands "27 reuse rows"; the table
  at the pin carries 26 reuse rows (31 in total, 74 tokens). The manifest is built from the parsed table, so the
  deliverable is unaffected; recorded so nobody hunts a 27th row.
- `IRPT_BCKEND-W1-S2` (OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~B`) -- 12 of the 74 PATHS tokens are not
  readable from a worker's fresh worktree: 3 brand sources are gitignored at `deck_generation/.gitignore:14-15`, and
  9 portal tokens sit inside the `portal` submodule (gitlink `5907cbca98`, no checkout). `IB-s-18` needed none of
  them; `IB-s-14`, `IB-s-15` and `IB-s-2` will.

## Bounds observed

No `terraform init`/`plan`/`apply`. No AWS call of any kind. No vendor call, no mailbox read. No monitor, alarm, SNS
or SES send. No credential in any artifact, fixture or commit. No served output touched -- the only writes are the
three new homes this cell creates plus this worker's own deliverables and the appended surprise rows. Every path
written is inside the order's `<paths>` grant. No existing surprise row edited. `.tools/commit-gate.sh` rc=0 on the
one `.py` file. Every invocation ran under `timeout`.
