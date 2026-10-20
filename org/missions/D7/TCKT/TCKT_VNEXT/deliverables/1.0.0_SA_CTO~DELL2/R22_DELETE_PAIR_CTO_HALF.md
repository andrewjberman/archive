# Never-widen CTO half: round 22 synthetic residue delete (46 exact versions; TCKT_VNEXT and IRPT_ANLREQ)

**Seat:** 1.0.0_SA_CTO~DELL2. **Date:** 2026-10-20 ~22:1xZ.

**Packet:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R22_DELETE/R22_DELETE_PAIR.md` @952dddbe1f, blob
f38bc409cbcb1c7598fc32225c32c83459d627ac, sha256 52202f9b7047be111154e0b87e65653dcf670b29028d159bd4b4819b0aef680d (measured at
HEAD). The manifest is `R22_DELETE_MANIFEST.json` (blob 7f07b0b6d8). The COO half is SIGNED by `2.0.0_SA_COO~V2`.

## Authority

- Andrew-direct 2026-10-16: "you can delete synthetic and test files any time, i do not need an open call"
  (`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261016_134xZ_SYNTHETIC_TEST_DELETES_NEED_NO_CALL_OPAL_TERMINAL_GONE_DELL2.md`).
- The delete is by listed key and VersionId, from the record that wrote each object.

## What was read here (the manifest)

- **46 entries**, each with a bucket, key, version_id and written_by. No entry lacks a version.
- **By prefix:**
  - 4 in `opal-data-cottonwood/portal/cottonwood/state/ticket_attachments` (the TCKT Trade tests: "31 bytes, invented");
  - 42 in `opal-data-irpt/irpt/49financial/state/` (original_holdings 10, normalized_portfolios 8, ycharts_opal_reports 8,
    request_compositions 7, extraction_evidence 5, analysis_commentaries 4).
- **`written_by`:** every entry names a synthetic test run: the TCKT R20-PROD3 and R21-RB1 tests, and IRPT_ANLREQ runs 4, 5, 5B, 5C,
  5D, 6, 7, 7b, 7c and 7d (rows S217 to S237). No client upload and no production run is listed.
- **Andrew's local sample is unaffected:** the 7d Overview he was given is a local copy outside the repository.

## Blast radius (both branches)

- **Applied:** the 46 versions are gone, each read ABSENT after.
  - The mechanism is throwaway Terraform roles (s3:DeleteObjectVersion on exact ARNs and VersionIds, trusted only by
    cloudops-dell2-agent-user, 900-second sessions), destroyed and read ABSENT.
  - DenyS3DeletesOnProductionData is untouched.
- **Stopped:** a lock or retention on any entry is a STOP with nothing deleted beyond what was read back. The roles are still
  destroyed.
- **Not covered:** any object outside the manifest. Later FWD-9 and Multi-Comp residue is a separate pass.

## Signature

SIGNED, CTO half, bound to the packet blob and sha256 above.

## Re-sign on the naming-gate amendment (~23:2xZ)

- **Why:** TV2 stopped TO-R22-DL1 at precondition 5, because the LGIC naming gate refused the hand-typed role names. Nothing was
  applied.
- **Amended pair:** @901daf7108, blob 21fa71920020d432f6aa5ac4159386de96005eef, sha256
  7280a5e6a0cbcecba284ec6a89e2850e057080bda7d63f0453346d6bae78cb30 (measured at HEAD).
- **Roles and policies:** `opal-ticket-residue-delete-{0..3}-role` and `-policy`, four explicit blocks. The issuer reports
  `naming-gate.py --diff --enforce` PASS, 8 graded, all CONFORMANT, with no registry row needed.
- **The manifest is unchanged:** blob 7f07b0b6d8, read here at HEAD, 46 entries. Terraform reads it through a variable.
- **Blast radius and rollback** are as above. Only the resource names changed.

SIGNED, CTO half, bound to the amended blob and sha256 above. The f38bc409cb binding is superseded.
