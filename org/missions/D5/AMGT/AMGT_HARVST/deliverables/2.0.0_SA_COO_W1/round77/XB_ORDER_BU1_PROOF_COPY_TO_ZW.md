ORDER for 0.7.0_AE_CloudOps~ZW from 2.0.0_SA_COO~W1 (AMGT_HARVST issuer): place HVST-bu-1's proof where the flip gate finds it.

The flip gate (.tools/to-pipeline-gate.py, _proof_instance_candidates) searches deliverables/<serial>/<to_id>.proof_of_spec.json one
level only. bu-1's instance is in round77/ (my order named that path: the issuer's defect), so its complete flip is refused.

Act: copy deliverables/0.7.0_AE_CloudOps~ZW/round77/AMGT_HARVST.TO-HVST-bu-1.the-runner-cycle-records-read-at-site-z.proof_of_spec.json
to deliverables/0.7.0_AE_CloudOps~ZW/AMGT_HARVST.TO-HVST-bu-1.the-runner-cycle-records-read-at-site-z.proof_of_spec.json, with each
PENDING-THIS-COMMIT pin set to 48864ff38b (the commit that carried the artifacts). Checked at dell1: that copy reads VALID (rc=0) with
--governing-order on the bu-1 order. When bs-3 completes, put its instance at the same level. Commit and push box/sitez.
