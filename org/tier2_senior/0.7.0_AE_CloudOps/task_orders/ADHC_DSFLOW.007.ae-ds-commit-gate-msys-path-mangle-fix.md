<task_order>
  <metadata>
    <id>ADHC_DSFLOW.007</id>
    <slug>ae-ds-commit-gate-msys-path-mangle-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-18 (authored backlog as .005) / 2026-05-19 (dispatched GO + renumbered .005 -> .007 to avoid collision with already-shipped .005 ae-safe-deploy-gate-extension and .006 ae-orion-gold-dispatch-sentinel-logging from 2026-05-11)</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <completion>COMPLETE 2026-05-20 (AE 0.7.0, commit 74c2cffee). Root cause: MSYS_NO_PATHCONV=1 (CLAUDE.md/MEMORY-mandated for every Terraform/AWS-CLI session) leaves the gate's POSIX /c/... helper-script paths unconverted to python.exe; Windows resolves the leading slash as current-drive-absolute -> C:\c\Users\... -> can't-open-file -> AST scanner + silver enforcement skipped while the gate hard-blocked (fail-closed-wrong). Fix: SCRIPT_DIR_WIN via guarded `pwd -W` mixed form for the 3 helper invocations. AC1/AC2/AC3 met; 4-case Windows-Git-Bash matrix PASS. RAVC2 sent COO + CC CTO.</completion>
    <dispatch_unblock_condition>GO 2026-05-19 (2.0.0_SA_COO): dispatched in the 3-TO sequence behind SXIN_DAY1ZG.001 (rider-2 priority, deadline 2026-06-01) and ahead of ADVI_INFALM.001 (defense-in-depth alarm). CTO-recommended sequencing held -- this fix has higher latent-risk (silently breaks the Rule-14 gate on the primary dev host) than the alarm item.</dispatch_unblock_condition>
    <project_code>ADHC_DSFLOW</project_code>
    <priority>P2 -- structural-enforcement integrity. NOT a live data-correctness fault (AE 0.7.0 ran the 3 ds-commit-gate checks directly for MDPF -- py_compile OK, ds-precommit-check.py exit 0, ruff --target-version py39 clean -- so no bad code shipped under the broken wrapper). BUT this is the dangerous class: ds-commit-gate.sh is CLAUDE.md Rule 14, mandated for EVERY .py edit; on Windows Git Bash it silently fails (mangled invocation path), so a future agent that trusts the gate gets a silent no-op / fail-open-or-closed. Higher latent-risk than ADVI_INFALM.001 (it undermines a workspace-wide structural gate) -- COO recommends prioritizing this above the alarm item when dispatched.</priority>
    <sla>0.5d wall -- a script-dir-derivation fix in the .tools/ds-commit-gate.sh wrapper (likely an MSYS_NO_PATHCONV=1 guard or a realpath/$(dirname "$0")-based resolution), plus a Windows-Git-Bash invocation test.</sla>
  </metadata>

  <references>
    <origin>AE 0.7.0 RAVC1 to COO 20260518T233202Z, item 2 of 2 CTO-directed backlog items. CTO routed it to COO for backlog triage citing the MDPF_ASSETS RAVC1 2026-05-18 as origin.</origin>
    <owner_project>ADHC_DSFLOW -- "DS Gold-Script Commit->Deploy Flow Hardening". .001 shipped the ds-commit-gate.sh wrapper + stdlib-only AST scanner (commits b6e0c154 + 7b7381ac); .002 added CLAUDE.md Rules 13+14; .004 added ruff target-version=py39 + the `from __future__ import annotations` mandate. This TO is the .005 follow-on hardening the .001 wrapper's cross-platform invocation integrity.</owner_project>
    <symptom>On Windows Git Bash the wrapper invokes .tools/ds-precommit-check.py via an MSYS-mangled path (observed: `C:\c\Users\AndrewBerman\Desktop\ajb_workspace\.tools\ds-precommit-check.py` -> python "can't open file"). The check then silently no-ops / fails -- the gate does not run the AST undefined-name scanner + silver coerce_silver_ids() enforcement it is supposed to. Same MSYS path-mangle class the build-and-upload.sh zip/upload steps already dodge via PowerShell, and the documented `export MSYS_NO_PATHCONV=1` Terraform/AWS-CLI pattern.</symptom>
    <constraint>Rule 16 -- this is a local-runtime bash script under .tools/; it MUST work with the Git Bash 3.6.7-fb42d713 default-install utility set (no pgrep/pkill/flock/pidof/setsid/wget; realpath IS present). Any new utility need takes a `command -v`-guarded fallback.</constraint>
  </references>

  <context>
    ds-commit-gate.sh is the Rule-14 pre-commit structural gate every DS agent must run before `git add`/`git commit` on any .py edit (three checks: python -m py_compile, .tools/ds-precommit-check.py AST scanner + silver coerce_silver_ids() enforcement, ruff --target-version py39). On the primary development host (Windows Git Bash) the wrapper's derivation of the ds-precommit-check.py path is MSYS-mangled, so that middle check silently does not execute. The gate appears to pass (or hard-blocks for the wrong reason) without doing its job -- exactly the silent structural-enforcement-integrity failure ADHC_DSFLOW exists to prevent. Non-blocking for MDPF only because AE 0.7.0 ran the three checks by hand; it is unsafe to rely on that going forward.
  </context>

  <scope>
    <step>Phase 1 -- reproduce the MSYS path-mangle on Windows Git Bash; identify the exact script-dir / ds-precommit-check.py path-derivation line in .tools/ds-commit-gate.sh that mangles. Fix it robustly -- a scoped `MSYS_NO_PATHCONV=1` around the python invocation, and/or a `$(cd "$(dirname "$0")" && pwd)`-style or realpath-based self-relative resolution that survives MSYS. Do NOT set MSYS_NO_PATHCONV globally (per CLAUDE.md / MEMORY -- it breaks other tools); scope it to the offending invocation only. Keep the fix Rule-16-clean (Git Bash 3.6.7 default utilities; realpath is available; guard anything else).</step>
    <step>Phase 2 -- verify on Windows Git Bash that ds-commit-gate.sh now actually runs all three checks: (a) a clean .py file -> exit 0 with ds-precommit-check.py demonstrably executed (not skipped); (b) a deliberately-broken reproducer (undefined name, mirroring the .001 081223b5 canary) -> exit 1 from ds-precommit-check.py, proving the gate is no longer silently no-opping. Capture both transcripts. Confirm no regression on a non-MSYS path (the wrapper must still work where it already did).</step>
    <step>Phase 3 -- commit via .tools/safe-commit.sh with the agent --author; this is local-runtime tooling (no Terraform / no pipeline deploy). RAVC2 to COO + CC CTO (CTO endorsed the follow-on). Record the root cause, the exact fix, and both Phase-2 transcripts. Note in the ADHC_DSFLOW project record that the .001 wrapper is now cross-platform-integrity-hardened.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Root cause identified (the specific path-derivation line) and fixed in .tools/ds-commit-gate.sh; MSYS_NO_PATHCONV (if used) is scoped to the offending invocation, never global; Rule-16-clean (Git Bash 3.6.7 default utilities only, guarded fallbacks for any non-default).</ac>
    <ac id="AC2">Windows-Git-Bash verified: clean .py -> exit 0 with ds-precommit-check.py demonstrably run (not skipped); broken reproducer -> exit 1 from the AST scanner. Both transcripts captured. No regression on non-MSYS invocation.</ac>
    <ac id="AC3">No emoji; committed via safe-commit.sh with agent --author (local tooling -- no Terraform/deploy step); session log with reasoning + transcripts; RAVC2 to COO + CC CTO. ADHC_DSFLOW project record updated to reflect .005 hardening.</ac>
  </acceptance_criteria>

  <deliverables>
    - The cross-platform-integrity fix to .tools/ds-commit-gate.sh.
    - Phase-2 Windows-Git-Bash verification transcripts (pass + fail-reproducer).
    - Session log + RAVC2 to COO + CC CTO; ADHC_DSFLOW.json .005 registration.
  </deliverables>
</task_order>
