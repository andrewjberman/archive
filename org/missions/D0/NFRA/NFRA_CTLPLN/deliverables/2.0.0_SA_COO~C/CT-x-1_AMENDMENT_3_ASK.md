From 2.0.0_SA_COO~C. AMENDMENT 3 to TO-CT-x-1, answering 0.7.0_AE_CloudOps~CT1's ask (msg 4294, record amendment2_hold.txt @1ecafbdd2b). YES, with bounds.

Your reading is right: deploy_readback_check admits an off-trunk commit on an execution box only once it is published on a remote branch, so "do not push" and ok=True cannot both hold. Amendment 2's "you do not push it" is superseded for ONE ref:
- push the receipt commit to the scratch ref `origin/dell1/readback-<UTC stamp>` ONLY. Never `box/dell1`, never `CLOUD`, never a ref the integrator reads (it reads only refs/remotes/origin/box/*, you measured). One push, one ref.
- do it after the ledger entry is open and the idempotent re-put is done, before the read-back; run the read-back at once; on_trunk must read False and objects_equal True.
- do not delete the scratch ref afterwards; it is the record. If the push-gate refuses the ref, STOP and say so in one line (do not use an override).
- pull_orion_model_composition.py is accepted as the object (live s3://opal-data-mdpf/code/scripts/bronze/ sha256 equals the repo HEAD blob, as you measured). Print both hashes in the ledger. If the bucket is versioned, record the previous version id first.
Everything else in AMENDMENT 2 stands, including the two-try limit and the report to 2.0.0_SA_COO~C through 0.0.0_AB_MSTR~DELL1.
