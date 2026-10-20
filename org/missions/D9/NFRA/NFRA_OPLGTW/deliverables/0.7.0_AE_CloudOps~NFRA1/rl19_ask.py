#!/usr/bin/env python
"""OG-rl-19 Phase A: write W/NEVER_WIDEN_ASK_OG-rl-19.md from the records. usage: python rl19_ask.py   (repository root, after rl19_phasea.py)"""
from __future__ import annotations

import io
import json
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
G = "infra/aws/ec2/opal-gateway/"
rel = json.load(io.open(W + "rl19_release.json", encoding="utf-8"))
pa = json.load(io.open(W + "PHASE_A_OG-rl-19.json", encoding="utf-8"))["body"]
t, tp, pr = pa["tests"], pa["terraform_plan"], pa["probes"]
TREE = "C:/tmp/og-rel-r3c"


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True, cwd=TREE).stdout.decode().strip()


files = [("app/integrations/schwab/catalog.py", "WHOLE from trunk (OG-sk-2): the firm form helpers and the dual read in `Catalog.read_marker` and `Catalog.list_dates`"),
         ("app/integrations/schwab/integration.py", "**HYBRID, not trunk's blob**: the BASE blob plus the one OG-sk-2 hunk (a function-local import and one changed condition); trunk's blob carries OG-rt-1's eight hunks (batch17's, which waits)"),
         ("deploy/NFRA_OPLGTW_CONTRACT.json", "WHOLE from trunk (OG-sk-2): the additive `firm_form` key; every old-form field byte-equal; absent key = today's behaviour"),
         ("tests/test_og_sk2.py", "WHOLE from trunk (OG-sk-2): new, source only, ships nowhere that runs")]
rows = []
for p, why in files:
    stat = git("diff", "--numstat", rel["base_sha"], rel["release_sha"], "--", G + p).split()
    rows.append("| `%s` | +%s -%s | blob `%s` | %s |" % (p, stat[0], stat[1], git("rev-parse", "%s:%s%s" % (rel["release_sha"], G, p))[:12], why))
ask = """# NEVER-WIDEN ASK -- `OG-rl-19` -- release R3c, the Schwab 0840 DUAL READ: master `08403355` moves to the firm folder `schwab/49financial/`; the reader IAM first (two in-place role-policy updates, the FIRST GRANT on `opal-data-49financial`), the gate read, then four code files

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-19.round-47-release-r3c-the-schwab-0840-dual-read-and-its-reader-iam.md` (GO for Phase A: the issuer's ferry 20261020T230500Z; method `OG-rl-17`'s for the code, `OG-ls-1`'s for the IAM). Source: Andrew-direct ~17:0xZ (master `08403355` moves to `schwab/49financial/`), the CTO's rulings of 2026-10-20 20:18Z, 22:02Z and 22:08Z ("the edit is a DUAL READ: new path first, then the old path ... as its own small release under its own signed pair"), and the laptop's binding order 110051.
**Phase A deploys and applies NOTHING in any form** and writes no SSM parameter and no store item. Both the release and the plan below are LOCAL: the release is on branch `rel-nfra-oplgtw-r3c` in `C:/tmp/og-rel-r3c` (not pushed).
**The release signed:** `release_sha` `%(rel)s`, cut on `base_sha` `%(base)s` = batch16's release, PREDICTED (`OG-rl-17`, window 2026-10-21 06:00Z-06:45Z; the host reads `%(live)s` now, `live_ref_host`); from `trunk_sha` `%(trunk)s` (the `OG-sk-3` drain, which holds the `OG-sk-2` drain `bed56db150e`). `6575999df5` (dell1's harvest release) is an ancestor of the base; dell1's four harvest files are byte-equal. **Phase B RE-READS the host marker; it must still equal `base_sha`, else the release is re-cut.**
Records: `W/rl19_release.json`, `W/PHASE_A_OG-rl-19.json`, `W/rl19_pa/{host_leg,oldform_compare,tests}.json`, `W/RL19_PLAN.txt`, `W/rl19_host.py`, `W/rl19_sk2_probe.py`, `W/rl19_tests.py`, `W/rl19_phasea.py`, `W/rl19_ask.py`.

## 1. The diff, by file (EXACTLY FOUR files over the base)

| file under `infra/aws/ec2/opal-gateway/` | lines | release blob | cell and reading |
|---|---|---|---|
%(rows)s

Barred and absent (the check counts them at 0): the deploy script, the unit, every other `deploy/` file, `EC2_MANIFEST.json`, every `.tf` in the release tree, `app/data_entitlement.py`, `app/account_ref.py`, `OG-rt-1`'s other files. The organisation-standards copy of the contract (`org/standards/NFRA_OPLGTW_CONTRACT.json`) lands in the LANDING (Phase C), not in this tree.
**The IAM, applied separately (not part of the tree):** `infra/aws/terraform/opal-gateway/schwab_reader_iam.tf` at trunk `a4c6ecfd30` (`OG-sk-3`), blob `26d5685504`, the two resources `aws_iam_role_policy.schwab_data_read_policy` and `aws_iam_role_policy.schwab_catalog_read_policy`, applied with `-target` for exactly those two through `safe-apply`. The plan (`W/RL19_PLAN.txt`, scrubbed of the account number, `-lock=false`, no `-out`, nothing applied) reads **`Plan: %(add)d to add, %(chg)d to change, %(dst)d to destroy.`**, both in place: %(targets)s. The root may carry other drift; it is not mine to apply and the targeted plan shows none of it.

## 2. The widening, stated plainly

1. **The first grant on opal-data-49financial.** Two role policies change in place:
   - the DATA role (`gateway-schwab-read-role`) gains `s3:GetObject` and `s3:GetObjectVersion` on FOUR silver files BY NAME in the EXISTING bucket `opal-data-assets`: `schwab/49financial/silver/<table>/date=*/08403355.parquet` for `dim_position`, `dim_balance`, `dim_asset`, `dim_transaction`; its Deny statements are widened to match (the new prefixes are added to the allowed forms);
   - the CATALOG role (`gateway-schwab-catalog-read-role`) gains `s3:GetObject` and `s3:GetObjectVersion` on ONE state object name in the NEW bucket `opal-data-49financial`: `schwab/49financial/state/complete/date=*/08403355.complete.json`, and a prefix-conditioned `s3:ListBucket` there (`s3:prefix` like `schwab/49financial/state/complete/*`); a new Deny refuses any other listing of that bucket, and `DenyListingOtherBuckets` now excludes the two buckets by `NotResource`.
   - No write action, no bucket-wide or folder-wide read, no other master's file, no other principal. The OLD grants stay byte for byte: the old form is the fallback.
   - **The listing note, for the signers:** a prefix-conditioned list reveals KEY NAMES under that prefix, so when another master lands in the firm folder its key names become listable to the catalog role (its CONTENTS stay unreadable: the GetObject is by file name `08403355` only). The bucket's own policy is a separate Deny that the laptop's R3a exemption lifts for this one role and prefix.
2. **The dual read, in code.** For master `08403355` only: the catalog reads the NEW location first (`opal-data-49financial`, the firm form), then the OLD (`schwab/08403355/`), and **falls back on ABSENT only**: on `NoSuchKey` or an empty listing. **`AccessDenied` (or any other error) on the new location is a hard dependency error and does NOT fall back.** A file of another master in the firm folder is ignored by NAME (the master is taken from the FILE NAME; a planted `08242234.parquet` or `08242234.complete.json` is refused or ignored). An old-form master (`08242234`, `08335338`) never calls the state bucket. **Before the cutover nothing changes for any principal** (the new location is empty, so every read falls through to the old); after the cutover the same reads continue from the new location.
3. **R3a.** The laptop applies the bucket exemption on `opal-data-49financial` (its order `TO-BF-r2`, lane `0.7.0_AE_CloudOps~NFRA2`) and confirms THROUGH `0.0.0_AB_MSTR~Z`, who writes the confirmation file into this seat's inbox. **R3a must be verified live before this release: no confirmation file, no apply.**
No new tool, no `tools/list` change (103), no env key (65 stays), no stored grant touched, no write to any bucket.

## 3. Phase A measurements (every host run in a FRESH process under the cgroup hard guard `%(guard)s`; the running service untouched: PID `%(pid)s` before and after, `NRestarts` %(nr)s; the scratch copies removed)

- **(a) The probes.** The python of `sk2.AC1` run VERBATIM (one line changed: the pinned base contract is read from a file, the host holds no git objects) on the candidate stage on the host: **%(ok)d of %(lines)d** labelled lines read `ok`.
- **(b) Old-form reads unchanged.** In one fresh process per stage with a fake S3 client: the live tree's `_read_marker` and `list_dates` against the candidate's `read_marker` and `list_dates` for `08242234` and `08335338`: the answers and the calls made are equal and the state bucket is never called: **%(old)s**. (The live tree has no `marker_locations`; the candidate's answers `[old location]` only for both masters.)
- **(c) The plan.** As section 1.
- **Tests, release tree (both orders equal).** Named set (%(nf)d files: `test_og_sk2` and the Schwab and catalog tests): %(np)d passed, %(nlit)d failed in each order, the SAME failures as at the base (%(nsame)d of %(nlit)d); **new reds against the base: %(nred)d**. Window set (%(wf)d existing `test_og_*` files green at the base): %(wp)d passed, %(wfail)d failed in both orders. With trunk's standards copy overlaid (uncommitted, restored to the base's bytes after: %(restored)s).
- **Full suite, per test id** against the base's tree (the batch16 release tree, the same sparse cone and invocation): release %(rf)d failed, base %(bf)d failed; **only in the release: `test_og_sk2_contract_firm_form_parses_and_copies_are_byte_equal`**, which compares the deploy copy with the standards copy and passes once the standards copy lands (it does with the overlay); only at the base: none. The remaining failures are the live ref's own.

## 4. The order of acts (Phase B), recorded in `W/R3C_SERVED.json` `order`

Window 2026-10-21, **after batch16's ledger is CLOSED and not before 07:00Z** (the CTO's slot 07:00Z-11:30Z); abort line `/health` 200 within 60 s of the restart. Announce to `0.0.0_AB_MSTR~Z`. Ledger `nfra-oplgtw-gateway-release-r3c` (the Terraform leg is a leg of the SAME entry), entry AND sentinel first; re-read the live ref on the host (must equal `base_sha`; else STOP and re-cut).
1. **R3a is confirmed:** the confirmation file is read BEFORE any apply (its name goes in `order.r3a_confirmation_ref`).
2. **Terraform apply** of the two policies through `safe-apply` with `-target` for exactly those two; the plan re-read at the apply must read add 0, change 2, destroy 0 (any other count STOPS). `comp-iam` for both roles before and after, statement ids and counts recorded.
3. **THE GATE READ**, as `gateway-schwab-catalog-read-role` (the gateway's assume path, in a hard-guarded fresh process): ONE `GetObject` of `schwab/49financial/state/complete/date=2026-10-20/08403355.complete.json` and ONE `ListBucket` with prefix `schwab/49financial/state/complete/` on `opal-data-49financial`. They must answer **NoSuchKey** and **an empty list**. **`AccessDenied` is NOT a pass: STOP, do not deploy the code**, keep the applied policies (they are inert), report with the exact error code.
4. **Only then the code deploy** (as `OG-rl-17` step 5, `DEPLOY_BASE_REF` the live ref read on the host), then the unarmed served read, the dual-read measurement (dates and newest date before and after, not lower), a 15-minute read-back, the host clock and failed units read BEFORE the ledger closes, the landing.

## 5. Both branches

- **The gate read passes (NoSuchKey, empty list):** deploy the code. **The gate read answers `AccessDenied` (or any key):** do NOT deploy; the policies stay (inert: nothing reads the new location yet); I report the exact code; the laptop's exemption is the next question.
- **After the deploy:** an old-form master reads exactly as before; `08403355` reads the old location until the cutover puts data in the new one, then the new location; a failure on the new location other than ABSENT surfaces as a dependency error to the caller (no silent fallback).

## 6. Rollback

Redeploy the live ref's tree (the wrapper's pre-deploy tarball; `DEPLOY_BASE_REF` the live ref), and re-apply the previous bodies of the two policies by reverting `schwab_reader_iam.tf` to the base and `safe-apply` with the same two targets. The code-only rollback restores the single-location read; the policies are inert without the code, so the order may be code first, IAM second.

## 7. Triggers (any one: roll back as section 6)

`/health` not 200 in 60 s; a tool of the 27 not answering; the `.env` key count not 65; `tools/list` changing from 103; md5 beyond the four files; host memory above 85 percent; `NRestarts` above 0; the marker not equal to the release; **the gate read answering `AccessDenied` or any key**; **the dual-read read-back showing fewer dates or an older newest date than before the deploy**; any `audit-lake WARN` line during the read-back; the plan at the apply showing anything but add 0, change 2, destroy 0.

## 8. Gate lines

process-wide state this change touches: %(pw)s

I read: `catalog.py`'s diff whole, `integration.py`'s diff whole, the contract diff, `schwab_reader_iam.tf`'s diff and the plan, `sk2.AC1` whole, and the base and trunk lineage of each file. No SSM write, no store write, no bucket write, no env key, no deploy-script or unit edit. No account number, person's name, credential or object content appears here (the plan record is scrubbed of the account number).

## 9. The three halves (sign ONCE, on `release_sha` `%(rel)s` and this ask's sha256)

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed on `release_sha` and this ask's sha256, with the widening (section 2: the first grant, the listing note, the ABSENT-only fallback), the hybrid `integration.py` (section 1) and R3a (section 2, point 3) read.

### COO half (`2.0.0_SA_COO~O`)

To be signed on `release_sha` and this ask's sha256, with the Phase A measurements (section 3), the order of acts and window (section 4) and the triggers (section 7) read.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed on `release_sha` and this ask's sha256, with the process-wide state line (the verdict 35844; section 8), the widening (section 2) and the suite difference named (section 3) read.
""" % {
    "rel": rel["release_sha"], "base": rel["base_sha"], "trunk": rel["trunk_sha"], "live": rel["live_ref_host"][:10], "rows": "\n".join(rows),
    "add": tp["add"], "chg": tp["change"], "dst": tp["destroy"], "targets": ", ".join("`%s`" % x for x in tp["targets"]),
    "guard": pr["guard"], "pid": pa["host_probe_service"]["pid_before"], "nr": pa["host_probe_service"]["nrestarts_after"], "ok": pr["sk2_ac1_ok"], "lines": pr["sk2_ac1_lines"], "old": pa["old_form_unchanged"],
    "nf": t["named_files"], "np": t["named_passed"], "nlit": t["named_failed_literal"], "nsame": t["named_reds_same_at_base"], "nred": t["named_failed"], "wf": t["window_files"], "wp": t["window_set_passed"], "wfail": t["window_set_failed"],
    "restored": t["standards_copy_restored_to_live_ref_bytes"], "rf": t["full_suite"]["release_failed"], "bf": t["full_suite"]["base_failed"], "pw": pa["process_wide_state"]}
io.open(W + "NEVER_WIDEN_ASK_OG-rl-19.md", "w", encoding="utf-8", newline="\n").write(ask)
print("wrote the ask, %d bytes" % len(ask.encode("utf-8")))
