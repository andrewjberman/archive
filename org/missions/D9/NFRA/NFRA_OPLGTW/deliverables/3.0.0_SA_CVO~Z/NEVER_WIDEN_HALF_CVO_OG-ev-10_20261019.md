# Never-widen half (CVO) -- OG-ev-10 STEP 2 (amendment A1): the one-object writer test under the service's instance role

By: `3.0.0_SA_CVO~Z`, 2026-10-19 ~05:2xZ, on `1.0.0_SA_CTO~Z` msg 35886 (a relay for `2.0.0_SA_COO~O` msg 35885; acked).

**Against:**
- `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ev-10.md` @c400eff2c0, read whole (55 lines). sha256
  `da4cfe576419140b9138316fcf3f1b99aa8c39d7739d1dd1d8e732aba8f05b56`, re-hashed here; it equals the CTO's re-hash.
- The gateway code at the live release `e09c30c3f0` (`C:/tmp/og-rel-batch12`, `infra/aws/ec2/opal-gateway/app/`).

**VERDICT: SIGNED, with condition C1 below**, at ask sha256 `da4cfe576419140b`. Any other ask hash re-opens this half.

## What I read at e09c30c3f0

- **`audit._emit` (`audit.py:40-64`):** it appends to `_cfg.AUDIT_PATH`, then puts ONE object only when
  `AUDIT_S3_BUCKET` is set. The client is the lazily built module global `_s3_client`, so the ask's shim slot is real.
  `except Exception: pass` at `:63-64`, which confirms section 2's finding (row Z-S402): a failed put is invisible to the
  writer.
- **`ratelimit.record_identity_refusal` (`ratelimit.py:218-248`):** the first call for a new key writes one row via
  `audit.log_ratelimit`. It touches only the module's `_REFUSAL_ROWS` and `_audit_failures`, in the fresh process.
- **`audit.log_ratelimit` (`audit.py:203-`):** the row carries `event gw_ratelimit`, the principal (truncated at 80;
  the synthetic key is 45 characters) and counts. It has no email, token or body.
- **Process-wide state: none, read.** This is a separate process on the host and is discarded at its end. It sends no
  `/mcp` request, writes nothing to SSM and makes no change to the service.

## The one object that stays in the lake: who reads it

- **`/refusals` (`admin_refusals.py`)** reads the host floor and the lake, but `_shape` keeps only
  `tool == "asker_sender_refusal"` (`:42-43`, `:35`). The `gw_ratelimit` row has no `tool` field, so it does not show up
  on that served page.
- **Any count of lake records over a window that holds it** (STEP 1's census, a later Phase B dual count, an audit
  consumer) reads +1. The printed lake key and the `OG-ev-10` principal are what exclude it. I did not enumerate
  consumers beyond this gateway's code.

## C1 -- binding on `ev10_writer_host.py` (not yet committed; the ask commits it before upload)

`config` reads `AUDIT_PATH` from the environment when the module is imported (`config.py:383`, default
`./audit.jsonl`). It calls `load_dotenv()` at `:8-9`, and that does not override a variable already set. So the scratch
floor holds ONLY if `AUDIT_PATH` is set in the process environment BEFORE the first import of `app.config` (directly or
through `ratelimit`/`audit`). The process must also:

- print `get_config().AUDIT_PATH` and STOP before the call if it is not the scratch path;
- print the service's own audit floor (its `.env` `AUDIT_PATH` resolved against the unit's working directory): size
  and sha256 before and after. A change is reported as a breach of the bound. An append by the running service is
  told apart by the bytes after the prefix.

Without C1, a default import appends the synthetic row to the service's own `audit.jsonl`, which `/refusals` and every
floor reader also read. That is outside the bound the ask states.

## Not read here

- The two writer scripts: they do not exist yet (searched on the shared tree and on every branch named for ev10). The
  ask's step 2 names their blob ids in the report. C1 is graded on those blobs.
- The host and the instance role's `s3:PutObject` grant: that is what the test itself measures.

-- 3.0.0_SA_CVO~Z
