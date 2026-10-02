# NFRA_OPLGTW task order -- `OG-r-4` -- FWD-7 re-measure: on-host capacity at contract scale against the SERVED release, read-only

<!-- ===================== WORKER FACE -- this is the WHOLE of the worker's context ===================== -->

<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md</decomp_doc>
<owned_cells>OG-r-4</owned_cells>
</decomp_ref>
<issued_to>0.9.0_WK_NFRA_OPLGTW~16</issued_to>
<issued_by>2.0.0_SA_COO~O</issued_by>
<placeholders>NONE</placeholders>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- one measurement run; no cron, alarm, monitor or cadence.
comp-iam: DECLARED-NOT-APPLICABLE -- SSM and S3 reads with existing access; nothing written to the state store.
comp-adversary: DECLARED-NOT-APPLICABLE -- the instrument and caps are OG-x-4's, unchanged.
EGRESS CLASS, declared: NONE beyond Opal's own AWS.
</preflight>

## 1. THE CELL -- `OG-r-4` (decomposition addendum R3-T.5, item 5)

FWD-7 is NOT_REALIZED on round 1's INSUFFICIENT verdict. OG-x-4 re-measured SUFFICIENT
(`deliverables/0.9.0_WK_NFRA_OPLGTW~11/CAPACITY_X4.json`) but against release `63264dfb22`; live is now
`3a7d6a7dc85fe3c54a4b63b27b59055abc9adca7` (its `app/integrations/schwab/` differs: `aws_roles.py`, `datasets.json`
+dim_transaction, `integration.py`, `query.py`). Re-run the SAME instrument against the served release.

1. Confirm the host engine first: md5 of every `app/integrations/schwab/*` file on the host equals `3a7d6a7dc8`'s bytes.
   A mismatch STOPS.
2. Off-hours only (before 11:00Z or after 21:00Z). Copy CLOUD's `infra/aws/ec2/opal-gateway/tests/acceptance/onhost_bench.py`
   to the host scratch dir and run `--scale full` with `/opt/opal-gateway/.venv`'s python, exactly as OG-x-4 did
   (synthetic principals, nothing written to the state store, job caps from the contract), then remove the copy.
3. Assemble `deliverables/0.9.0_WK_NFRA_OPLGTW~16/CAPACITY_R4.json` in OG-x-4's shape (`ac2`, `ac4`, `ac5`, `admission`,
   `deadlines`, `export`, `ctx`, `verdict`, `started_utc`, `finished_utc`) plus two top-level keys: `served_release`
   (the full sha the md5 check confirmed) and `engine_md5_equal` (true/false). The ac4 regression window is a
   post-`3a7d6a7dc8` window.

## 2. BOUNDS

Read-only on the host except the bench copy in a scratch dir, removed after. No deploy, no restart, no `.env` read
beyond key names. Never push, merge, rebase, stash, `checkout --` or `clean`; never override a gate.

## 3. SURFACES

<paths>
org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~16/
org/missions/D9/NFRA/NFRA_OPLGTW/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

Rows: id `NFRA_OPLGTW-Z-W16-S<k>`, fabric `site-z`, disarm_owner `2.0.0_SA_COO~O`.

## 4. PROOF OF SPEC (literal; run from your worktree root after your commit)

<proof_of_spec>
  <criterion id="AC1" cell_refs="OG-r-4"><invocation>XF_CAPACITY=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~16/CAPACITY_R4.json bash org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/round2/checks/xf.AC1.sh; echo "exit=$?"</invocation><expect>(?s)RESULT: PASS.*exit=0</expect></criterion>
  <criterion id="AC2" cell_refs="OG-r-4"><invocation>XF_CAPACITY=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~16/CAPACITY_R4.json bash org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/round2/checks/xf.AC2.sh; echo "exit=$?"</invocation><expect>(?s)RESULT: PASS.*exit=0</expect></criterion>
  <criterion id="AC3" cell_refs="OG-r-4"><invocation>bash org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r13/checks/r4.AC3.sh; echo "exit=$?"</invocation><expect>(?s)served_release equals deployed_commit: True.*RESULT: PASS.*exit=0</expect></criterion>
</proof_of_spec>

- `AC1`: export peak RSS flat across 25k/125k/250k rows at 11 columns.
- `AC2`: the maximal query stays under 80% of the job cap.
- `AC3`: the record was measured against the served release, on the host install, writing nothing.

A FAIL on AC1 or AC2 is a real result: report it, do not re-run until it passes.

## 5. WHEN YOU ARE DONE

Instance at `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~16/NFRA_OPLGTW.TO-OG-r-4.capacity-remeasure-live.proof_of_spec.json`,
validated with `python .tools/proof-of-spec-check.py <instance>`; if all PASS, append a `complete` status tag after the
order's last status line in the same commit. Report once: verdict, peaks, the literal AC output.

<!-- ===================== RECORD FACE ===================== -->

**ISSUER NOTES:**
- Round label 13 (addendum R3-T.5, item 5). xf.AC1/AC2 take `XF_CAPACITY` (their test-only override, here the record
  path). Pre-cut: `r4.AC3` FAIL (record absent).

<status>pending</status>
<round>13</round>
<slot>~16</slot>
<fabric>site-z</fabric>
<risk>SERVED</risk>
<worker_class>worker</worker_class>
