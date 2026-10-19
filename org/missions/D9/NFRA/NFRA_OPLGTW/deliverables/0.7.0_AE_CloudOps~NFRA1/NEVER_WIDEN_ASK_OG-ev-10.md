# NEVER-WIDEN ASK -- `OG-ev-10` STEP 2 (amendment A1) -- the ONE-OBJECT WRITER TEST: a guarded fresh process on the host calls `ratelimit.record_identity_refusal` with a SYNTHETIC principal key under the service's own instance role; the one `gw_ratelimit` object is read back and NEVER deleted

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ev-10.round-44-is-the-audit-refusal-write-failing.md`, AMENDMENT A1 (@df47b978ac; GO msg 35874, on the CTO's ruling msg 35872). STEP 1 (`W/AUDIT_REFUSAL_WRITE.json`, committed): 0 journal 429 lines, 0 writer WARN lines, 0 `gw_ratelimit` rows over 5568 lake objects, counter exposed by no route: `NOT_EXPOSED`. The controlled refusal cannot run: no non-person `/mcp` principal exists (this ask's earlier text, now replaced; the reading stands). Nothing has been written for STEP 2.

## 1. What the test is, and the bounds (these are the bounds the amendment names)

- **ONE lake object only.** A fresh process on the host calls `ratelimit.record_identity_refusal(principal_key, retry, detail)` ONCE, with the synthetic key `OG-ev-10/00000000-0000-4000-8000-00000000e10a` (`key_label` contains `OG-ev-10`; it is not a `<tid>/<oid>` of any real principal), `retry` 60 and `detail` = `{"count": 121, "clients": {"none": 121}}`. The function throttles per key (the first call for a key writes), so the call writes ONE row through `audit.log_ratelimit` -> `audit._emit`: a row `event gw_ratelimit`, `outcome rate_limited`, `scope identity`, the synthetic `principal`, `limit` 120, `window_s` 60.0, `count_in_window` 121, `retry_after_s` 60, `suppressed` 0, `by_client` `{"none": 121}`, `distinct_clients` 1. It carries no email, no token, no body and no real identity. The object's lake key (`audit/dt=<day>/<ts>-<id>.jsonl`) is PRINTED in the record, so any consumer of the lake can exclude it.
- **Under the SERVICE'S OWN INSTANCE ROLE** (so the IAM of the put is tested too): the process runs on the gateway host through SSM (Rule 12, S3 to SSM), where the instance profile is the same one the service uses; `AUDIT_S3_BUCKET` is read from the service's `.env` (a STOP if it is not set). The local audit floor `AUDIT_PATH` is pointed at a scratch file for this process only, so the service's own `audit.jsonl` is not touched.
- **How the put is observed (no code changes anywhere):** `audit._emit` swallows every lake-write error by design (`except Exception: pass`, the floor holds), so the call itself cannot tell success from failure. The process therefore wraps the module's own S3 client in a recording shim for this process only (`audit._s3_client`): the shim records the key and whether `put_object` returned or raised (the exception class name only), and passes the call through unchanged. Then it READS BACK the object by that key with `get_object`, checks it holds exactly one row with `event gw_ratelimit` and the synthetic principal, and prints `written` and `read_back`. The object is **NEVER DELETED** (an audit-lake delete is not ours).
- **Hard guard:** every gateway-code run in a fresh process under the cgroup hard guard `oom_score_adj_1000_cgroup_memmax_1400mb` (`systemd-run --scope -p MemoryMax=1400M`, wall limit 120 s); stop at 75 percent host used. The running service is not touched (its PID and `NRestarts` are read before and after); no `/mcp` request is made; no SSM write; no code, config or environment change; no restart.
- **Records:** `W/AUDIT_REFUSAL_WRITE.json` gains `writer_test` = `{"key_label", "lake_key", "written", "read_back", "instance_role": true, "halves"}` (the amended `ev10.AC1.sh` grades it: `FAILS` if the object was not written or not read back; `WRITES` if both); `controlled_refusal` stays `null`. The proof instance is re-generated and validated.
- **process-wide state this change touches: none, read.** I opened `app/ratelimit.py` (`record_identity_refusal`, lines 218 to 248: it touches only the module's own `_REFUSAL_ROWS` dict and `_audit_failures` counter, in the fresh process) and `app/audit.py` (`log_ratelimit`, `_emit`, `_lake_key`: it appends to the local `AUDIT_PATH` file and puts one S3 object), and `app/config.py` for `AUDIT_PATH` and `AUDIT_S3_BUCKET`. The fresh process is discarded at its end; the service's process memory and files are not reachable from it.

## 2. A finding this ask makes, stated plainly (it bears on the verdict of the whole cell)

`audit._emit` catches EVERY exception from the lake `put_object` and passes (`audit.py` lines 61 to 64: "floor holds; the lake write is best-effort by design"). So `ratelimit.record_identity_refusal`'s own `try/except`, which counts a failure and prints the one stderr line `SCTY_PREMCP ratelimit-audit WARN: refusal row not recorded (<error>)`, can only fire for an error raised BEFORE or AROUND the `_emit` call (audit module unavailable, the formatting, the local file append). **A failed S3 put (an IAM denial, a throttle, a missing bucket) raises nothing the writer can see**, so STEP 1's "0 WARN lines" cannot rule out a lake write that fails. This test is exactly the check that does: it observes the put itself, under the instance role. If it reads `written` true and `read_back` true, the instance role can write the lake and the writer's row reaches it (`WRITES`); if the put fails, the shim's recorded exception class names why (`FAILS`), and the finding is a defect of the best-effort sink, not of the limiter.

## 3. The order of acts (on the GO that names all three halves signed at this ask's sha256)

1. Re-read the host: one gateway process, `NRestarts` 0, `AUDIT_S3_BUCKET` set in `.env` (the value is not printed; only whether it is set and whether it equals the bucket STEP 1 read), host memory under 75 percent.
2. Upload `ev10_writer_host.py` and `ev10_writer_run.py` (committed first; the uploaded bytes must equal the committed blobs, their blob ids go into the report) and run the host process ONCE under the guard.
3. The process prints (counts, status words, the lake key): `written`, `read_back`, `put_error_class` (or none), the row's field names, the key. The runner records `writer_test`, re-reads the lake for the key independently from the runner's side (a second read-back by `get_object` with the runner's own credentials, `head` only if content is not needed), and confirms the lake still holds the object after the process ended.
4. Read the service state after (PID unchanged, `NRestarts` 0); recompute the verdict; run `ev10.AC1` and validate the proof; report.

## 4. Both branches

- **Object written and read back:** `WRITES`; the one synthetic object stays in the lake, excluded by its printed key and its `OG-ev-10` principal.
- **Put refused or read-back empty:** `FAILS`, with the exception class; nothing was written (or one object is there and was not read back, which is also reported with its key); the finding goes to the issuer as a defect of the sink.
- A second attempt is not made: ONE test only. A STOP before the call (the bucket unset, host memory above 75 percent, the service restarted) writes nothing.

## 5. Rollback

None possible and none needed beyond the bound: one small object in the audit lake, labelled, never deleted, keyed by its printed name. No state outside it changes.

## 6. Triggers (any one before the call: STOP, no write; after: report)

The `.env` has no `AUDIT_S3_BUCKET`; host memory above 75 percent; the service PID changing or `NRestarts` above 0 at either read; the guarded process exiting non-zero before the call; more than ONE object appearing under the synthetic principal.

## 7. Gate lines

Files: this ask, `W/ev10_writer_host.py`, `W/ev10_writer_run.py`, the record and the proof. No product file, no test, no release. No account number, person's name, credential or object content (beyond the one synthetic row) appears in any record.

## 8. The three halves (sign ONCE, on this ask's sha256)

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed on this ask's sha256, with the bounds of section 1 (one object, synthetic key, instance role, read back, never deleted) and the finding of section 2 read.

### COO half (`2.0.0_SA_COO~O`)

To be signed on this ask's sha256, with the bounds of section 1 read.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed on this ask's sha256, with the process-wide state line of section 1 and the one object that stays in the audit lake read.
