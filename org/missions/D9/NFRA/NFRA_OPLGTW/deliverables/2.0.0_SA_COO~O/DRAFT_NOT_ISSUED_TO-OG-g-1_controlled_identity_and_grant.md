# DRAFT, NOT ISSUED -- TO NFRA_OPLGTW.TO-OG-g-1 -- G-C: the controlled identity's verified tid/oid and its one approved synthetic grant

> **SUPERSEDED 2026-09-29 by 2.0.0_SA_COO~O:** issued, re-cut at HEAD, as `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-g-1.controlled-identity-and-grant.md` to `0.7.0_AE_CloudOps~OG` on 1.0.0_SA_CTO~O msg 26435. This draft is history; the order is the authority.

⛔ **THIS IS NOT A TASK ORDER. IT IS A DRAFT THAT WAS NEVER ISSUED, AND IT IS DELIBERATELY NOT IN
`task-orders/`.** Andrew-direct 2026-09-22 ~18:2xZ at the `2.0.0_SA_COO~O` terminal, VERBATIM: *"Finish your work
and research on the OPLGTW project and do not go further with it. Close out anything you are working on and write a
/log on current state of the project."* The draft was complete and gate-ready when that word arrived; it is preserved
HERE rather than cut, because a file in `task-orders/` with any non-terminal status counts as an OPEN ORDER and would
have added a third open order to a project whose L10 arithmetic counts them per project (LD-0521). **A successor picks
this up by moving it into `task-orders/`, re-reading every pin in it at HEAD, and handing it -- not by trusting it.**
The tag lines below are left in their order shape ON PURPOSE so the move is a move and not a re-authoring; the
`<status>` reads `not-issued`, which no pipeline reader treats as live.

**What was true at the moment it was parked:** Andrew had authorized option (A) (*"Yes to Schwab"*, ~17:1xZ, record
@`465d591b25`); `1.0.0_SA_CTO` had given an unconditional no-objection to the seating override (99573, condition met at
99580); `2.0.0_SA_COO~B` had confirmed the recipient lane's five other orders are terminal-by-proof (99579). Nothing
about the draft was blocked. It was not issued because the word to stop arrived first.

<to_id>NFRA_OPLGTW.TO-OG-g-1</to_id>
<project>NFRA_OPLGTW</project>
<issued_to>0.7.0_AE_CloudOps~V</issued_to>
<issued_by>2.0.0_SA_COO~O</issued_by>
<issued_date>2026-09-22</issued_date>
<status>not-issued</status>

**Directive:** D9 | **Fabric:** laptop | **PRD:** `org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md` v0.9 @8a63c77b51 (ADMITTED, both halves SIGNED) | **Contract:** `org/standards/NFRA_OPLGTW_CONTRACT.json` v1.0 | **Gate:** `G-C` (decomposition s.6) | **outcome_ref:** FWD-1, FWD-3 .. FWD-8 (this order serves them only by unblocking `OG-v-4`; it grades none of them)

---

## WHY THIS ORDER EXISTS, AND WHAT IT IS NOT

`G-C` is a project GATE, not a decomposition cell. It holds `OG-v-4`, which is one of the two orders that convert this
project's build into proof. The gate requires THREE things and only the first is recorded:

| `G-C` requires | state at this cut | owner |
|---|---|---|
| an authorized identity/data administrator | RECORDED -- Andrew-direct ~00:5xZ 2026-09-21, option (b), delegation to `0.7.0_AE_CloudOps`, recorded by `1.0.0_SA_CTO` @`a35f175a59` | `1.0.0_SA_CTO` |
| the controlled identity's **verified `tid`/`oid`** | ABSENT -- this order produces it | `0.7.0_AE_CloudOps~V` produces; `1.0.0_SA_CTO` records |
| an **approved synthetic grant**, recorded | ABSENT -- this order produces it | same |

⛔ **THIS ORDER DOES NOT CLOSE `G-C`.** It produces the EVIDENCE. `1.0.0_SA_CTO` records the gate and closes it; those
are two different acts and this order performs only the first. ⛔ **AND IT DOES NOT TOUCH THE SWITCH.** Adding `schwab`
to `ENABLED_INTEGRATIONS` is a LATER, SEPARATE act gated on a never-widen sign-off signed by `1.0.0_SA_CTO` and
`2.0.0_SA_COO~O`, under Andrew-direct ~17:1xZ 2026-09-22 (*"Yes to Schwab"*, record @`465d591b25`) which authorizes
option (A) and nothing wider. A grant written while the switch is OFF serves nobody, which is exactly why it is safe to
write it first.

## THE ACT

Produce, in one evidence file in this seat's own deliverables folder:

1. **The controlled identity**, verified: its Entra `tid` and `oid` as canonical GUIDs, read from an AUTHORITATIVE
   tenant source, with the instrument named and the read's own output quoted. The identity is a CONTROLLED, non-privileged
   test principal -- ⛔ **NEVER a master-admin address**, and never Andrew's own account: the walkthrough it enables must
   exercise refusal paths, which a master-admin identity cannot demonstrate (row `NFRA_OPLGTW-S61`: the tier is decided by
   exact email match at four live sites, one of which mints token scopes).
2. **One synthetic grant**, prepared and activated through the committed operator command
   `infra/aws/ec2/opal-gateway/ops/schwab_entitlement_admin.py`, run under the `opal-gateway-access-admin` role. Its scope
   is DERIVED, not invented -- see SCOPE below -- and the derivation is written down beside it.

⛔ **IF THE TENANT ACT IS NOT YOURS TO PERFORM, THAT IS THE ANSWER AND IT IS A GOOD ONE.** If no controlled identity
exists and creating one needs a tenant administrator's interactive act, DO NOT improvise one, do not reuse a real
person's account, and do not widen an existing grant. File a BLOCKING row naming EXACTLY what a human must do, in one
paragraph a non-technical reader can act on, and stop. Andrew is at a console today; a precise ask is worth more than a
workaround.

## SCOPE OF THE GRANT -- derived from the walkthrough it must serve

The grant exists to let `OG-v-4`'s walkthrough run. It must therefore cover, and the evidence file must show the
derivation line by line against these sources:

- `infra/aws/ec2/opal-gateway/tests/acceptance/WALKTHROUGH_PROTOCOL.md` s.4 -- RQ1 through RQ6, at the FIXED business
  date `2026-09-15` and, for RQ5/RQ6, the qualified date immediately before it AS SEALED (never a fresh catalog read).
  Masters `08242234` (SmartX) and `08335338` (BlackDiamond); datasets `dim_balance` and `dim_position`.
- the same file's person-operated A-rows -- `dim_asset` for the describe journey, and A7's no-date request per master.
- `org/standards/NFRA_OPLGTW_CONTRACT.json` -- `fields`, `forbidden_field_classes`, `grant_date_modes`, `operations`,
  `disabled_operations`. Operations are `list`, `describe`, `query`, `download_filtered` only. `download_original` and
  any write are disabled at the model level and are never requested.

⛔ **BOUND IT SO THE DENIAL CASES STILL EXIST.** `OG-v-4` grades refusals as well as answers, so a grant wide enough to
answer everything destroys the evidence the walkthrough exists to produce. The accounts and columns stay a bounded
subset, and the evidence file NAMES at least one in-scope request that must SUCCEED and one adjacent request that must
be REFUSED, with the reason each way. A scope you cannot justify from the two sources above is not in the grant.

## ACCEPTANCE

<placeholders>WS</placeholders>

<criterion id="GCG1-AC1" cell_refs="OG-g-1"><invocation>cd <WS> && py -3.12 org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~V/probes/og_g1.py AC1</invocation><expect>(?m)^VERDICT: PASS-GCG1-AC1(?![0-9])</expect></criterion>
`GCG1-AC1` -- the evidence file exists at the path named in DELIVERABLE and records the controlled identity's `tid` and
`oid` as canonical GUIDs, the AUTHORITATIVE instrument that read them, and that instrument's own quoted output. The probe
prints each field it found against the denominator of fields required, and FAILS on a placeholder, an empty value or a
value that is not GUID-shaped.

<criterion id="GCG1-AC2" cell_refs="OG-g-1"><invocation>cd <WS> && py -3.12 org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~V/probes/og_g1.py AC2</invocation><expect>(?m)^VERDICT: PASS-GCG1-AC2(?![0-9])</expect></criterion>
`GCG1-AC2` -- the identity is NOT a master admin and NOT on the write-capable roster: the probe reads
`MASTER_ADMIN_EMAILS` and `WRITE_CAPABLE_EMAILS` from the deployed configuration source and prints the comparison, with
the denominator of addresses checked. A match either way is a FAIL, not a warning.

<criterion id="GCG1-AC3" cell_refs="OG-g-1"><invocation>cd <WS> && py -3.12 org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~V/probes/og_g1.py AC3</invocation><expect>(?m)^VERDICT: PASS-GCG1-AC3(?![0-9])</expect></criterion>
`GCG1-AC3` -- the grant candidate PASSES the committed operator command's own validation
(`schwab_entitlement_admin.py prepare`), and the evidence file carries that command's printed scope diff verbatim. The
probe re-runs the validation against the recorded candidate rather than trusting the transcript.

<criterion id="GCG1-AC4" cell_refs="OG-g-1"><invocation>cd <WS> && py -3.12 org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~V/probes/og_g1.py AC4</invocation><expect>(?m)^VERDICT: PASS-GCG1-AC4(?![0-9])</expect></criterion>
`GCG1-AC4` -- the grant is ACTIVE in the live table, read back with a STRONG consistent read against the principal's
`POLICY#<tid>#<oid>` keys: profile `status` is `active`, its `grant_revision` names the grant record that exists, and the
scope read back EQUALS the scope recorded in the evidence file, field by field, denominator printed. ⛔ The read-back is
the evidence; the command's own success line is not.

<criterion id="GCG1-AC5" cell_refs="OG-g-1"><invocation>cd <WS> && py -3.12 org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~V/probes/og_g1.py AC5</invocation><expect>(?m)^VERDICT: PASS-GCG1-AC5(?![0-9])</expect></criterion>
`GCG1-AC5` -- the scope covers what the walkthrough asks: for each of RQ1..RQ6 the probe checks the named master,
dataset and business date are inside the grant, denominator 6 printed; and A7's no-date request per master is inside it,
denominator 2. A gap is a FAIL naming the uncovered question -- the walkthrough would otherwise fail for a reason that
has nothing to do with the system under test.

<criterion id="GCG1-AC6" cell_refs="OG-g-1"><invocation>cd <WS> && py -3.12 org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~V/probes/og_g1.py AC6</invocation><expect>(?m)^VERDICT: PASS-GCG1-AC6(?![0-9])</expect></criterion>
`GCG1-AC6` -- NO SECRET AND NO CUSTOMER VALUE is in any artifact this order commits: the probe scans the evidence file,
the probe itself and the result file for a token, cookie, client secret, complete URL with a query string, raw account
identifier or customer amount, and prints the denominator of files scanned. The identity's `tid`/`oid` and the grant's
scope ARE recordable; a balance, a holding, an account title or a credential is not.

<criterion id="GCG1-J1" cell_refs="OG-g-1" judgment="true"/>
`GCG1-J1` -- graded at L9 by `3.0.0_SA_CVO`: the grant's scope is the NARROWEST that serves the walkthrough, and the
evidence file's named must-succeed and must-be-refused pair is a real discriminator rather than a restatement. RECORD; NO
VERDICT.

<expected_criteria>GCG1-AC1, GCG1-AC2, GCG1-AC3, GCG1-AC4, GCG1-AC5, GCG1-AC6, GCG1-J1</expected_criteria>

`<WS>` is your worktree's absolute path, given in your identity line.

## DELIVERABLE

- `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~V/G-C_CONTROLLED_IDENTITY_AND_GRANT_EVIDENCE.md` -- the
  evidence, in the shape AC1..AC6 grade.
- `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~V/probes/og_g1.py` -- the probe, taking the short id,
  printing its measurement WITH its denominator, then exactly one line `VERDICT: PASS-GCG1-AC<n>` or
  `VERDICT: FAIL-GCG1-AC<n> <reason>`.
- `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~V/controlled-identity-and-grant.result.md`.
- the proof-of-spec instance named in `<proof_of_spec>`.

## BOUNDS

- **Grant.** Your write surface is the `<paths>` block below, plus
  `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~V/` and this order's own file (for the `<status>`
  flip). Nothing else. A path you need that is not named is a BLOCKING row on that criterion -- never an override.
- **The live write you ARE authorized to make** is exactly one principal's `POLICY#` records through
  `ops/schwab_entitlement_admin.py`, under the `opal-gateway-access-admin` role. ⛔ **NOTHING ELSE IN AWS.** No IAM change,
  no Terraform apply, no change to `ENABLED_INTEGRATIONS`, no restart, no deploy, no edit to any existing principal's
  grant. The Gateway's own runtime role is refused by that command by design; do not work around it.
- **A change-management ledger entry** under `org/critical_paths/change_management/` is OPENED before the activation and
  CLOSED after it, naming the principal (by `tid`/`oid`, never a name or address in the ledger body) and the rollback:
  `revoke` at the next revision, which is a tombstone and never a delete.
- **Read-only everywhere else:** the records, the contract, the protocol, the table. You do not call the Gateway as a
  user, you do not sign in as the controlled identity, and you do not run the walkthrough -- that is a person's act at
  `G-D` and grading it is `OG-v-4`'s.
- **Branch.** Work in the worktree named in your identity line at hand-off, cut from `CLOUD`. Never push, merge, rebase,
  `checkout --` or `clean`. The issuer drains.
- **Commits.** `bash .tools/safe-commit.sh --author "0.7.0_AE_CloudOps~V <0.7.0_AE_CloudOps~V@opal.agent>" -F <msgfile> -- <paths>`,
  the message file written with the Write tool. Every `.py` you touch passes `.tools/commit-gate.sh`. Capture the output
  to a file; never pipe it to `tail`, never pair it with `$( )`.
- **No egress off Opal infrastructure.** No vendor API, no interactive third-party sign-in beyond the tenant read this
  order names.
- **Spec frozen; REFUSE what you cannot meet as written.** A criterion you cannot satisfy is refused WITH its
  measurement -- never repaired, widened, or satisfied by a route this order does not name.
- **Surprises** go to `org/missions/D9/NFRA/NFRA_OPLGTW/surprise-channel/investigations/INVESTIGATION_v1.md` as ONE row
  each, id `NFRA_OPLGTW-AE-S<k>`. Keep working after filing.
- **Numbers** in this order are context, never acceptance values, except where a criterion prints one.

<paths>
org/missions/D9/NFRA/NFRA_OPLGTW/surprise-channel/investigations/INVESTIGATION_v1.md
org/critical_paths/change_management/
</paths>

<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md</decomp_doc> v1 @8768f46770, gate `G-C` (section 6), round 1.
<owned_cells>OG-g-1</owned_cells>
</decomp_ref>

<proof_of_spec>
Criterion ids: `GCG1-AC1` .. `GCG1-AC6`, `GCG1-J1` (7). Instance at
`org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~V/NFRA_OPLGTW.TO-OG-g-1.controlled-identity-and-grant.proof_of_spec.json`
(phase `BUILD-GENERAL`, firm `FABRIC`, spec_ref.group `OTHER`, spec_ref.doc the PRD @8a63c77b51, decomp_ref.doc the
decomposition @8768f46770, decomp_ref.to_ref this order's path), validated with
`py -3.12 .tools/proof-of-spec-check.py <instance> GCG1-AC1,GCG1-AC2,GCG1-AC3,GCG1-AC4,GCG1-AC5,GCG1-AC6,GCG1-J1` BEFORE the
`complete` flip. The `judgment="true"` criterion is recorded `UNVERIFIABLE-BY-INSTRUMENT` with a `status_reason` naming
`3.0.0_SA_CVO` at L9 -- a `PASS` or `FAIL` on it is INVALID. **Flip `complete` only when every MECHANICAL criterion
PASSES by output.**
</proof_of_spec>

**REPORT:** one report to `2.0.0_SA_COO~O` when the order is terminal, naming each criterion's verdict with its
measurement, and naming separately anything a human must still do.

---

## RECORD FACE

<preflight>
comp-schedule: NOT RUN -- this order creates no scheduled producer, no trigger and no pipeline artifact; it writes one principal's POLICY records through a committed operator command and one evidence file. The gate this order feeds (G-C) is a project gate, not a schedule.
comp-iam: DECLARED-NOT-APPLICABLE FOR CHANGES -- this order adds no AWS operation, policy, principal or role. It USES two existing ones: the `opal-gateway-access-admin` operator role (the only writer of POLICY records, `schwab_access_state.tf`) and the reader identity the probe's strong read runs under. Both exist at HEAD and were built by OG-i-1 and OG-i-2.
comp-adversary: the PRD is at v0.9 @8a63c77b51 with BOTH sign-off halves SIGNED and current (prd-signoff status, read at the cut). This order adds criteria against gate text, not against ratified PRD text, and re-cuts nothing.
lane: the <paths> block IS the grant (owned-paths-validate.py worker_grant), plus the seat's own deliverables folder by the tree convention.
seating: 0.7.0_AE_CloudOps~V holds 5 task orders on IRPT_BCKEND whose STATUS WORD reads pending. 2.0.0_SA_COO~B confirmed at 2026-09-22T18:18Z (msg 99579), on a fresh run of surprise-row-gate.py._open_tos_for_project, that all five are TERMINAL BY A VALID PROOF AT HEAD with only the status word stale -- 0 open ids among them. 1.0.0_SA_CTO's no-objection (99573) stands unconditional on that confirmation (99580). The seating override, if the lint takes one, is scoped to the SEATING finding alone and its audit row is read back after the act, because the override is NOT audited by construction (1.0.0_SA_CTO's own correction at 99576: audit_override catches a log-write failure and only WARNs while main still returns 0).
</preflight>

Cut 2026-09-22 by `2.0.0_SA_COO~O` under Andrew-direct ~17:1xZ (*"Yes to Schwab"*, option (A), record
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260922_171xZ_MDPF_SMOKE_CLOSED_AND_YES_TO_SCHWAB_WALKTHROUGH_WINDOW.md`
@`465d591b25`), step (a) of that word: *"0.7.0_AE_CloudOps produces G-C first"*. Addressed to the LANE `~V` and not to the
base serial, because the base has no session and a send to it would read as delivered while nobody read it
(`0.7.0_AE_CloudOps~V` 99562, `1.0.0_SA_CTO` 99564 owning the routing defect in its own earlier message).

⛔ **THE ORDER OF THE REMAINING ACTS IS LOAD-BEARING AND IS STATED HERE SO NO SEAT SHORTENS IT:** this order (G-C
evidence) -> `1.0.0_SA_CTO` records and closes `G-C` -> the never-widen sign-off, BOTH halves, which must MEASURE FRESH
that a principal with no grant is REFUSED -> the switch ON for the walkthrough window only -> a person runs the
controlled walkthrough (`G-D`) -> `2.0.0_SA_COO~O` spawns the grader for `OG-v-4` -> the switch OFF. `OG-v-5` needs
`G-E` and `G-F` beyond all of that. Andrew's word covers this sequence and nothing wider: the five Schwab tools stay NOT
enabled outside the window, and the email-keyed privilege tier (`NFRA_OPLGTW-S61`) is DISCLOSED and accepted for the
window only, not fixed.
