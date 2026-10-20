#!/usr/bin/env python
"""MP-pd-7: write MP-pd-7_PRE_ACT_RECORD.md (the census, the build comparison, the rollback, this order's path) from the measurement records, just before the ledger is opened. usage: python mp_pd7_preact.py   (repository root)"""
from __future__ import annotations

import hashlib
import io
import json

M = "org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~NFRA1/"
d = json.load(io.open(M + "MP-pd-7_MEASURE.json", encoding="utf-8"))
b = json.load(io.open(M + "MP-pd-7_INVOKE_BEFORE.json", encoding="utf-8"))
ask = hashlib.sha256(open(M + "NEVER_WIDEN_ASK_MP-pd-7.md", "rb").read()).hexdigest()[:12]
nd, rd = d["new_vs_deployed"], d["rollback_vs_deployed"]
txt = """# MP-pd-7 PRE-ACT RECORD (the NEVER-2 ledger's pointer target)

Order: `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-pd-7.person-access-release.md` (AMENDMENT A2), GO `.../deliverables/2.0.0_SA_COO~MP/pd/GO_MP-pd-7.md`. Ask sha256 prefix `%s`, both halves SIGNED at it (CTO @392b19649f, the COO~MP half at HEAD).
Ledger: `nfra-mcportal-pd-release` (legs: package build, apply, deployed-bytes read).

## Census
- Deployed function `mcportal-grant-writer-lambda`: CodeSha256 `%s`, LastModified %s, %d zip members, runtime %s, layer version %s. Its bytes are held: `MP-pd-7_deployed_before_894RI63.zip` (sha256 prefix `%s`, %d bytes), kept 7 days after the close (the CTO half's condition).
- New package: built from the Lambda directory byte-equal to `LAMBDA_COMMIT` `f3774ac1df8` and the live release `%s` (read twice, stable: %s): %d members. Against the deployed zip: %d new, %d differ, %d equal.
- Live release (`EC2_MANIFEST.json` `services.opal-gateway.deployed_commit`) = `LIVE_BASE` `13917ef993`.

## Build comparison
Package built here (`mp_pd7_measure.py`, `new.zip`): members compared after the apply with the zip the function serves (`MP-pd-7_AFTER.json`, `member_md5_equal_to_built`). Import probe (stdlib, boto3, botocore, jwt, cryptography only): imports and answers a no-header event.

## Rollback (proven before the act, as far as it can be: the declared departure of the ask, section 5)
Old handler `%s` on the same live closure: %d members; against the deployed zip %d new, %d differ, %d equal; negative control (the new package differs from the deployed one): %s. Command: `python mp_pd7_act.py rollback` (lays the old `lambda_function.py` in the working tree, uncommitted, plans, applies the saved plan through safe-apply, restores the file). Its time is measured at the act: the build/plan time plus the apply time.

## The before invokes (%s)
`narrow`: %s %s; `set_person_access`: %s %s (each writes one append-only refusal record to the writer's own changes table; the function's existing behaviour).
""" % (ask, d["deployed"]["code_sha256"], d["deployed"]["last_modified"], d["deployed"]["members"], d["deployed"]["runtime"], d["deployed"]["layer_version"], d["deployed"]["zip_sha256_16"], d["deployed"]["code_size"],
       d["live_release_first_read"][:10], d["live_release_stable_and_equals_LIVE_BASE"], d["new_package"]["members"], len(nd["only_in_first"]), len(nd["differ"]), nd["equal"],
       d["rollback_candidate_commit"], d["rollback_package"]["members"], len(rd["only_in_first"]), len(rd["differ"]), rd["equal"], d["negative_control_new_vs_deployed_differs"], b["read_at"],
       b["invokes"]["narrow"]["answer"]["verdict"], b["invokes"]["narrow"]["answer"]["reason"], b["invokes"]["set_person_access"]["answer"]["verdict"], b["invokes"]["set_person_access"]["answer"]["reason"])
io.open(M + "MP-pd-7_PRE_ACT_RECORD.md", "w", encoding="utf-8", newline="\n").write(txt)
print("wrote the pre-act record, %d bytes" % len(txt.encode("utf-8")))
