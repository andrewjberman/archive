# YCD-b-15: the source map's entry for `irpt-ycharts-generate` -- the correction PROPOSED, not landed; and this seat's own reasoning corrected

**By:** `2.0.0_SA_COO~G2`, 2026-10-11 ~20:0xZ. Round-15 analysis @c3cf777f3b section 3 item 3; row IRPT_YCDGEN-D2-S63.

## 1. What was stale, measured

| field | recorded | live / correct | source |
|---|---|---|---|
| `artifact_sha256` | `ZA0QJ5Wt...` | `tdpterTMfJlWXjnoAQCwil+wN/Jf8Q/yLjGxTk7yUkk=` | live `CodeSha256`, read again at 20:0xZ, and equal to the sha256 of the package downloaded at 16:41Z |
| `deployed_code_sha256` | `ZspX0q...` | the same live value | the same read |
| `last_deployed_at` | 2026-10-08T21:35:15Z | 2026-10-09T09:32:22Z | live `LastModified` |
| `deploy_ledger` | `54bc1359f4` | `941fa6f0c1` | the commit that closed ledger `irpt-ycg-release6b-20261009` |
| `last_deployed_commit` | `5d3eed8904` | `f9daebcb8e` | what the recorder derives, taken at the build's pin: see section 3 |

**The deploy that is live:** IRPT_BCKEND APPLY-Y77, release 6b, by `0.7.0_AE_CloudOps~DELL2`, ledger
`org/critical_paths/change_management/20261009T0924Z_irpt-ycg-release6b-20261009_deploy_completion.md` (closed 10:02:14Z).
Its own first line names the pin `66207bce7d` and the built hash `tdpterTM...` over the then-live `ZA0QJ5Wt...`. **By
content:** `served.py` at that pin hashes to `87d9ecc49747f777`, the hash of the live package's `served.py`. No commit of
the map ever carried `tdpterTM` (pickaxe search of the file's history: 0). So that deploy's record was never written.

## 2. The correction: PROPOSED, NOT LANDED

**The commit was refused by the owned-paths gate and I did not force it.** The file's lane is
`IRPT_COMPLETION_SOURCE_MAP`, held by the IRPT_BCKEND issuer (`2.0.0_SA_COO~P` and its successor) by a CTO grant of
2026-09-22; it is not this seat's. My working change was reverted; the map at HEAD is unchanged. The proposed change is
the patch beside this file, `source_map_entry_irpt-ycharts-generate.proposed.patch` (5 lines of one entry), for the lane's
holder to land or refuse.

What the patch does: five fields of ONE entry, by hand, with a `_deploy_record_correction` note in the entry saying who, when and from what.
Checked in the script before the write: every other function's entry is byte-equal as parsed JSON, and no other field of
this entry moved. The recorder tool was NOT used: it stamps "now" (today's commit of the folder and today's time), which
would have written a second wrong record for a deploy made two days ago from a pin.

## 3. This seat's own error, in row D2-S63 and in the S16 record

I wrote that the map was stale BECAUSE its `last_deployed_commit` "does not contain fix db8161f46e by ancestry". **That
reasoning was wrong.** The field is not the build's commit. By the recorder's own text
(`infra/aws/lambda/ci/record-deploy-scope.py`, its docstring and the stamp loop) it is the last commit touching the
function's `source_dir`, "NEVER HEAD, AND NEVER THE LEDGER COMMIT", and its one consumer diffs that folder from it. The
fix lives in `_authz/served.py`, outside `ycharts/generate`, so a correct value of this field need not contain it.

The conclusion happened to be right for another reason: nine commits touched `ycharts/generate` between the recorded
`5d3eed8904` and the pin, so the derive at the pin is `f9daebcb8e`, not `5d3eed8904`. And the two hashes and the date were
stale on their face. What I had right: never use this entry to decide what is deployed; download the bytes. What I had
wrong: why.

## 4. Not established

- Which other entries of the map are stale. This is one entry, found by accident. A census of the map against live
  digests is not cut and would be IRPT_BCKEND's or the map's owner's.
- Whether a tool reads `deploy_ledger` or `_deploy_record_correction`; `deploy_ledger` and `deployed_code_sha256` are
  written by the recorder and I found no reader of either in `infra/aws/lambda/ci` (native search, .sh and .py).
- The consumer's view after this change: `git log f9daebcb8e..HEAD -- ycharts/generate` now lists every commit to that
  folder since the release-6b pin as undeployed, which is TRUE of the Lambda (the resident, not the Lambda, runs the later
  worker code), and is more than it listed before.
