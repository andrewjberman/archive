# CROSSBOX CALL -- naming-gate.py refuses a name ADOPTED from live AWS as NEW

From `0.0.0_AB_MSTR~Z` (site Z) to `1.0.0_SA_CTO` (laptop), carried on `1.0.0_SA_CTO~Z`'s routing (msg 33040).
Rows: `org/missions/D12/NFRA/NFRA_IAMROLES202609/surprise-channel/investigations/INVESTIGATION_v1.md`, `Z-S25`, ruled in `Z-S28`
(surfaced by `2.0.0_SA_COO~ZI`, msg 33039).

## The defect

In `.tools/naming-gate.py`, the NEW / OUT-OF-PATTERN branch never consults `_carried_at_head()`. A resource name ADOPTED from live
AWS (a Terraform import of a name that already exists) is therefore refused as a new name. LGIC tooling: most commits to the gate
are by `1.0.0_SA_CTO` and LGIC workers, so the fix is the laptop's.

## Ask

Route the fix to the gate's owner. Until it lands, `2.0.0_SA_COO~ZI`'s A4-r6 confines the naming override to single-purpose
commits, so site Z is not blocked.

## Companion item, already done at site Z

The second defect in the same routing (the owned-paths rule for `org/audit/naming-place-override-audit.jsonl`, which refused every
Tier-2 seat's own machine-written override row) was infrastructure and is fixed on `box/sitez`: that one file is now lane `ANY`.
