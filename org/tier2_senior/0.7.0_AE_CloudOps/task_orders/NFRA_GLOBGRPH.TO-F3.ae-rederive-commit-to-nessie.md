<to_id>NFRA_GLOBGRPH.TO-F3</to_id>
<project>NFRA_GLOBGRPH</project>
<title>TO-F3 — Ad-hoc derive gains --commit-to-nessie opt-in (re-derive IS a Nessie version by construction)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (CTO decompose handoff 232252Z)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>complete</status>
<priority>P2 — after TO-F1; independent of the TO-F2 gate</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_GLOBGRPH_PRD.md §2b (v0.4 5208e0193) — ruling F3</ref>
</references>

<scope>
Ad-hoc full derive (`infra/aws/globgrph/derive_runner.py` path) gains a `--commit-to-nessie` flag via the importable `derive_runner.commit_to_iceberg` path, so an ad-hoc re-derive lands as a Nessie commit by construction instead of only the tarball side-channel. The tarball side-channel remains as time-travel archive — no longer the only landing. Closes CVO verdict leg 3 (ad-hoc derives never reach Nessie). F5 doctrine echo: a re-derive is still graph-maintenance, not verification — read-your-own-writes checks stay on served-artifact / live AWS.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Read infra/aws/globgrph/derive_runner.py — confirm commit_to_iceberg importable path + current tarball publish flow; grep ad-hoc derive callers (.tools/, buildspec.yml, org/modules/)</run>
      <expect>One clean injection point for the flag; caller inventory known.</expect>
      <if_mismatch>STOP. Surface structural surprises to COO before writing.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/ds-commit-gate.sh on touched .py; flag-off regression check (default behavior unchanged without --commit-to-nessie)</run>
      <expect>Gate exits 0; default path byte-identical behavior.</expect>
      <if_mismatch>Fix before commit; the flag is opt-in by ruling — default-on is a scope violation.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>One ad-hoc derive with --commit-to-nessie; then canonical rebuild (or kuzu_nessie_load) and query</run>
      <expect>The re-derive is visible as a Nessie commit; the next canonical rebuild serves it (= acceptance).</expect>
      <if_mismatch>Surface to COO; do not RAVC2-close without the end-to-end demonstration.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- Shares infra/aws/globgrph/ with TO-F1/TO-F2 + AE~B Item-2b work — same-directory coordination per TO-F1 block; derive_runner.py specifically may be touched by AE~B's 2b path. MCP AE~B before commit if both in flight.
</cross_domain_coordination>

<acceptance_criteria>
- A re-derive run with --commit-to-nessie is visible as a Nessie commit AND the next canonical rebuild serves it.
- Default (flag absent) behavior unchanged.
- Session log Compiler Tools section reproduces every `<run>` + observed output + pass/fail vs `<expect>`. Missing rows = REWORK.
- RAVC2 evidence to COO: commit hash + Nessie commit id + post-rebuild query output.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Platform tooling only; no silver/bronze converters, no S3 data-prefix writes.</no_reprocess_needed></data_reprocess_scope>
