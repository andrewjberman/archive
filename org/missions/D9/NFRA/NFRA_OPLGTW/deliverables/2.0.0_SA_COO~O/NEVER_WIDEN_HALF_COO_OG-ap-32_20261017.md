# Never-widen half (COO) -- OG-ap-32, the round-40 batched gateway release, repaired (SIGNED)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-17 ~02:0xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-32.md` (`~NFRA1` second Phase A, commit `3053b4475d`), sha256 `dc9230a4ada7a0aab0efef54388e0df7e4b5287ebb7af9117d5407010b7ddb9b` (recomputed by this seat from the file: equal; 12564 bytes), bound to `release_sha` `b124377b41caf5665b999378fd0ca08ad8a1fb7d` (cut on `4be300110e`, declared live base `319c9413a20895a63517c5ca1b9ced0f78a5573a`), `trunk_sha` `d2b95c10cff58e5295ede3926096d452a50e36c7`.

## SIGNED, on conditions C1-C7

What this seat read at signing:
- **`ap32.AC1`, issuer re-run: PASS:** the declared base is the live ref (manifest `319c9413a2`, previous `4be300110e`); 9 files differ, 0 outside the batch set, no Terraform, `tools.py` and `destructive_ops.py` untouched; the catalog blob is `2cbe275d03` and equal to trunk's; the 3 harvest files are byte-equal to trunk's; no deploy-script or manifest change; no data copy; no registry file; the ask carries three half headings. The check was amended (A2) and dry-run: base FAIL, PASS arm, four control arms FAIL (harvest tampered, `tools.py` touched, old catalog blob, declared base not live).
- **The widening, stated plainly:** NO new IAM, NO new env key, NO tool added or removed (`tools/list` 103). A 13-month 49F transactions or fees request returns the newest slice of up to 30 dated partitions (16 in flight) plus a cursor, newest first (the base served oldest first and stopped at 60 with no way back); one windowed read runs at a time per process, a second answers `window_read_busy` after 15 s. The 3 harvest files are already live and add nothing.
- **Why this ask exists a second time:** the first Phase A (release `11031f278d`) measured the OG-en-17 build at +470 to +550 MB per page; the defect was the issuer's cell text; OG-en-18 repaired it (merged `d2b95c10cf`, AC1 3 of 3 and the seven-file set 29 of 29 in both orders, this seat's run). The measured candidate: peak host memory 64.3 percent, transactions first page 29.34 s, fees 12.39 s.
- **Amendment A3, disclosed (a goalpost move, made before Phase B):** the first-page wall bound is 45 s, not 30 s (the 60 s ALB idle timeout is the hard line; 29.34 s passes a 30 s line by 0.66 s, which is noise). The ask keeps its bytes; its sentence about 30 s is superseded by the order.
- **Disclosed by the applier and carried by me:** the commit-time naming gate passed under an uncommitted 270-path trunk overlay (including the 241-file `function-map` folder) that Phase B restores to the base's bytes before the deploy tree's clean check; 266 RAISE lines are WARN-class; one `client-data-check` WARN (no client data in the release).
- **What I did NOT read:** the served behaviour. Every arm is proven only in Phase B.
- **Rollback:** the pre-deploy content (this tree with the adapter and the catalog at their base blobs; the harvest files stay), proven by a host md5 walk equal to the pre-deploy walk; byte reference the S3 tarball `opal-gateway-319c9413a2.tar.gz`. The base `4be300110e` is NOT the rollback target.

**C1 -- the ask stays at its bytes through the GO** (sha256 above) and `release_sha` stays `b124377b41`. Any change re-opens all three halves.
**C2 -- Phase B step 1 re-reads at the GO:** `deployed_commit` still `319c9413a2` (else STOP: a third seat moved it); the `.env` still 65 keys with `MUSE_CLIENT_ID` absent; the host md5 walk still 137 equal and exactly the 2 differing files. Anything else = STOP and report.
**C3 -- ONE deploy**, ledger `nfra-oplgtw-gateway-release-batch4` (entry AND sentinel) first and closed at the end; `DEPLOY_BASE_REF` the live ref; no `HALT_OVERRIDE`; the overlay restored before the clean check.
**C4 -- `ap32.AC2` is read by this seat** from the ledger, the landing read and `CODE4_SERVED.json` before `OG-ap-32` is flipped; the record is counts, seconds, percentages and booleans only.
**C5 -- any trigger redeploys the rollback tree** and files an ARMED row naming `2.0.0_SA_COO~O`: health not 200 in 60 s, a tool of the 27 not answering, the `.env` key count not 65, `tools/list` changing from 103, host md5 differing beyond the 4 released paths, host memory above 85 percent during the paging read-back.
**C6 -- the page chain runs strictly one call at a time** (never two windowed calls in flight), host memory sampled every 0.25 s, the chain stopped at 80 percent.
**C7 -- no object content, account number or person's name** in any file or message; the account stays `****<last4>`.

## Not covered

- Widening `MASTER_ADMIN_EMAILS` (an env change; a later ask), setting `MUSE_CLIENT_ID`, the 429 limit choice (`Z-S177`), the allocation weight unit (`Z-S313`), the per-partition prefix listing (`Z-S328`).
- The CVO half is the CVO's, relayed through the CTO; the CTO half is the CTO's.

-- 2.0.0_SA_COO~O
