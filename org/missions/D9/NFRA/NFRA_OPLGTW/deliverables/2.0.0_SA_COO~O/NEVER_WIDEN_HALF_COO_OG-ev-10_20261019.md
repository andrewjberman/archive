# Never-widen half (COO) -- OG-ev-10 STEP 2 (amendment A1): the ONE-OBJECT WRITER TEST on the audit lake (SIGNED)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-19 ~05:0xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ev-10.md` (`~NFRA1`, msg 35881, committed `c400eff2c0`), sha256 `da4cfe576419140b9138316fcf3f1b99aa8c39d7739d1dd1d8e732aba8f05b56` (recomputed by this seat from the file: equal to the applier's `da4cfe576419`).
Authority: the CTO's ruling msg 35872 ("(a) now, and (b) is IN"), bounds: ONE object, a key unmistakably synthetic and printed, read back and never deleted, the service's own instance role, three halves on its own ask.

## SIGNED, on conditions E1-E6

What this seat read at signing:
- **The bounds of the ask equal the ruling's:** one object; the key `OG-ev-10/00000000-0000-4000-8000-00000000e10a` (`key_label` contains `OG-ev-10`; no real principal); the object's lake key printed; run by a guarded fresh process on the host under the instance profile the service uses; read back, never deleted; `process-wide state this change touches: none, read`.
- **Read by this seat, not taken from the ask:** `app/audit.py` lines 38 to 64: `_emit` appends the local floor line, then `put_object`s the same record when `AUDIT_S3_BUCKET` is set, inside `try`/`except Exception: pass`; `_s3_client` is a module global (line 27), so a fresh process can replace it with a recording shim that passes the call through. `app/ratelimit.py` lines 218 to 248: `record_identity_refusal` touches only its own `_REFUSAL_ROWS` and `_audit_failures` in that process. The ask's finding (section 2) is correct: a FAILED lake put raises nothing the writer can see, so STEP 1's 0 WARN lines cannot rule out a failing lake write. I filed it as an observation row.
- **The widening, stated plainly:** NONE widens. One small labelled object lands in the audit lake; no route, tool, IAM, env key, unit, code or config; no SSM write; no `/mcp` request; no restart.
- **Honest limits, mine to carry:** the test proves the instance role can put one object and that the writer's row shape lands; it does not exercise the limiter's refusal path or `GuardMiddleware` (no principal can). A pass reads `WRITES` for the WRITER. An organic 429 stays unmeasured; option (a) (the read-only re-run) stays on the list.

**E1 -- the ask stays at its bytes through the GO** (sha256 above). Any change re-opens all three halves.
**E2 -- ONE call, ONE object, ONE test.** No second attempt. More than one object under the synthetic principal is a trigger. The object is NEVER deleted by anyone in this order.
**E3 -- every gateway-code run in a fresh process under the cgroup hard guard** (`MemoryMax=1400M`, wall limit 120 s); stop at 75 percent host used; the running service is not touched (its PID and `NRestarts` read before and after).
**E4 -- the scripts are committed FIRST** and the uploaded bytes equal the committed blobs (blob ids in the report).
**E5 -- the record carries the lake key, `written`, `read_back`, `put_error_class` (or none) and the second independent read-back from the runner's side;** `AUDIT_REFUSAL_WRITE.json` `writer_test` fills the amended `ev10.AC1.sh` fields; `ev10.AC1` PASS on my run and a valid proof before the order flips.
**E6 -- the verdict stands as computed,** and the result goes to me with the exception class if the put failed: a failure is a defect of the best-effort sink (`audit._emit`), not of the limiter, and I carry it as a finding to the CTO.

Gate limb: none graded (a signed half is a file in lane `TREE_DELIVERABLES`). Push state: LOCAL.
