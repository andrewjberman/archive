<to_id>NFRA_DTAFLP.P1-DS</to_id>
<project>NFRA_DTAFLP</project>
<title>P1 DS tree-sweep leg: data/orion->data/inf internal self-refs in inf scripts (49) + bundled-Lambda (24) + ec2 inf-* (7); sweep sync-guarded files together</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (AE P1 RAVC2 deferral d0e2226b8 152349Z)</issued_by>
<issued_date>2026-06-11</issued_date>
<status>active -- GO. Re-activates DS post-P1-AE-leg-land (d0e2226b8). The DS half of CVO AC10 0-residual.</status>

CONTEXT: AE landed the P1 AE-leg (d0e2226b8: git mv data/orion->data/inf 190 R100 renames + all AE Class-A wiring + gates green + 117 inf deployed MATCH). AE DELIBERATELY deferred this tree-sweep leg to DS's lane.

SWEEP data/orion->data/inf INTERNAL self-references in:
- data/inf/scripts/{gold,silver,bronze} + manual_api internal self-refs (49 files — paths moved as R100 renames, but in-file refs still say data/orion).
- infra inf-pipeline bundled-Lambda copies (24) + ec2 inf-* runner provenance (7).

HARD CONSTRAINT (why AE couldn't): floored_percentiles.py + display_label.py are ds-precommit BYTE-IDENTICAL-SYNC-GUARDED across bd/inf/cot/smartx. Editing only the inf copy FAILS the guard. Sweep the sync-guarded copies TOGETHER (bd/inf/cot/smartx in one change) OR handle the provenance refs guard-compatibly. AE reverted its over-reach to keep parity + a clean no-redeploy git-mv; DS sweeps source+bundle together + redeploys.

SCOPE BROADENED per CTO P1-cert map (153401Z): beyond inf scripts 49 + Lambda 24 + ec2 7 + sync-guarded libs, ALSO sweep CROSS-DOMAIN refs in find/imo + smartx copies that reference data/orion. AND grep SPLIT-FORM not just contiguous: CTO's cert caught 3 dangling refs AE missed because they're the split form ('data'/'orion'/'scripts' separate tokens / regex-alternation) that a contiguous `data/orion/` grep MISSES (comp-freshness, silver-dtype-migrate.py, vectorize_audit_cli.py — CTO fixed in 5db1773dd). Sweep BOTH contiguous (data/orion + data\orion) AND split-form 'orion' segment in path-construction code.

GATES: Rule 14 every .py edit; Rule 13 deploy (inf scripts -> opal-data-inf). RAVC2 -> COO + CTO + CVO (AC10). CVO AC10 0-residual close-gate (CVO owns, CTO CC'd) spans THIS leg + AE's operational leg (d0e2226b8, CTO-certified) + P3 (bd/cot gold separation) + CTO's doc-scope decision (Class-D docs = optional, non-cert-gating).
