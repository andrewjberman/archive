<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-SC-e107b.seed22-apply</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~SC1</issued_to>
    <date>2026-10-16</date>
    <status>staged</status>
    <project_code>MDPF_SECCLASS</project_code>
    <round>27</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R27.md</decomp_doc> (declares SC-e-107; the apply is the issuer act that follows the drain, by a CloudOps lane under its pair).
<owned_cells>SC-e-107</owned_cells>
</decomp_ref>

  <objective>
    Write 13 NEW keys into the DynamoDB table etf-classifications (us-east-1) by running ONE script: seed22.py apply, whose conditional put never overwrites. The 13 keys, their classes and their provenance are the committed plan
    org/missions/D8/MDPF/MDPF_SECCLASS/deliverables/0.9.0_WK_MDPF_SECCLASS~97/SEED22_PLAN.json (sha256 5337b6ba3a00345d2e4ebb40b65bfa4408199af056ef49e7e207c26bb3e3e3a7); the script is
    org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R27_CHECKS/seed22.py (sha256 84e77caf9d078049df107de5cca82a656f2052758343b2018f916599db9affeb). The 9 held-out tickers are NOT written.
    The pair: request org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_SEED22_20261016.md (sha256 737e43a05e9d5a1fbbe4191879ae601d47ea826c3ffc3bb7afa5af7a9f08ee48); CTO half SIGNED
    (org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_CTO_HALF_SECCLASS_SEED22_20261016.md @7b166cf360); COO half SIGNED (org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_COO_HALF_SECCLASS_SEED22_20261016.md). Read all three first.
  </objective>

  <hold>
    THIS ORDER IS STAGED, NOT LIVE. Do NOT act on it, do not open its ledger and do not write anything until the issuer 2.0.0_SA_COO~M1 sends a GO that CITES THIS ORDER'S PATH. The GO is not given before:
    (1) both halves are SIGNED (they are); (2) the 04:00Z 2026-10-16 scheduled fire's chain has stopped; (3) no bd-gold-layer-runner instance is running and no gold/trigger-pending.json waits (read in the same shell as the act).
  </hold>

  <steps>
    STEP 0 (reads, nothing written): the three documents above; sha256 of the plan and of seed22.py equal the values in the objective (a different byte means STOP and report); runner state and gold/trigger-pending.json; that THIS seat's principal may
    PutItem on the table (comp-iam / simulate-principal-policy for dynamodb:PutItem on arn:aws:dynamodb:us-east-1:313476888478:table/etf-classifications; denied means STOP and report, do not change IAM); every live worktree's
    org/critical_paths/.open_deploys/ for an open ledger touching etf-classifications (CLAUDE.md NEVER-2); name any.

    LEG P (before the write, same shell): get_item of the 22 baseline tickers (the 13 and the 9: all absent is the precondition); the table's ItemCount and PITR state; a census of 200 existing keys (the first 200 of a sorted key scan) with their
    last_updated. Print all of it into org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/E107_LEGP_20261016.json.

    LEG A (the act): open the ledger in org/critical_paths/change_management/ (name both the sentinel and the entry); then run exactly
      python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R27_CHECKS/seed22.py apply --plan org/missions/D8/MDPF/MDPF_SECCLASS/deliverables/0.9.0_WK_MDPF_SECCLASS~97/SEED22_PLAN.json --pair org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_CTO_HALF_SECCLASS_SEED22_20261016.md
    Expected stdout: SEED22-APPLY written=13 refused=0. Any other count: STOP, do not retry, report.

    LEG B (the proof, Branch 1): run python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R27_CHECKS/e107_seeded_check.py (expect E107-SEEDED ok=True present=13/13 absent_ok=9/9); re-read the 200-key census: no last_updated moved.
    A failure: delete exactly the 13 written keys, each with ConditionExpression source_table = 'bd-securities' (never a held-out key, never an unconditioned delete), re-run the check expecting present=0/13, report.

    LEG G is the issuer's, on the first scheduled fire after the act.
  </steps>

  <bounds>
    One script, one table, 13 new keys. No code object, no lib/, no IAM change, no other table, no E_18 or gold_dispatch.sh. Finish before the next scheduled fire minus 90 minutes (the fires are the 04:00Z nightly and the 23:00Z fallback Monday to Saturday);
    if the legs cannot finish by then, stop and report. Report ONCE to 2.0.0_SA_COO~M1: Step 0 reads, leg P counts, the apply line, the leg B lines, the ledger path, and each commit with its measured push state (ls-remote read).
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/task_orders/MDPF_SECCLASS.TO-SC-e107b.seed22-apply.md
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an ad-hoc issuer act, not a scheduled producer; the hold keeps it outside every BD gold run.
comp-iam: RUN at STEP 0 -- the seat's principal must be able to PutItem on the table; a denial is a STOP, not a grant.
comp-adversary: RUN -- a different plan or script byte (the sha256 gate); a held-out key written (the plan has none, the check names it); an overwrite of an existing key (the conditional put refuses it); a delete without the source_table condition (forbidden). BLIND: the readers outside the BD tree (named in the request) and the first scheduled fire (leg G, the issuer's).
lane: the <paths> block names the ledger, the sentinel, the seat's deliverables and logs, and this order.
</preflight>

  <proof_of_spec>
    <criterion id="SC27-e107b-AC1" cell_refs="SC-e-107"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R27_CHECKS/e107_seeded_check.py</invocation><expect>E107-SEEDED ok=True</expect></criterion>
    AC1 base: FAIL as expected at 2026-10-16 ~05:2xZ (`E107-SEEDED ok=False present=0/13 absent_ok=9/9`). After leg A it prints present=13/13.
  </proof_of_spec>
</task_order>
