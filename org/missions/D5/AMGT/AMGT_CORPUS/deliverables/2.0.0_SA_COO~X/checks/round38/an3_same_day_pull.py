"""AMGT_CORPUS round 38 CRPS-an-3 -- the ONE same-day pull, under 1.0.0_SA_CTO~Z's ruling (a), an-2 half AMENDMENT 2 @80b915d9b5.

RUN FROM THE PINNED CHECKOUT, on Python311, exactly like the scheduled task:
  cd C:/Users/Opal Bloomberg/Desktop/opal-pinned/amgt-induction-daily/6f6e4726414e
  OPAL_INDUCTION_FIRE=1 <Python311> <this file> [--probe-only]

Behaviour:
- Imports the PINNED producer (integrations/bloomberg/research/model_block_pull.py at 6f6e472641) and runs its own `cmd_refresh`.
  That gives the same 96 names, fields, health check, batching, call counter, and stage_pull + stage_derive(sa_fallback=False).
- RUN-SCOPED, NEVER A CODE EDIT: for this process only, `_model_block_latest_stamps` returns {}, so the same-day derived-stamp
  skip (Z-S88) sees no name as already current.
- STOP RULE: stage_pull is wrapped. The first exception whose text carries -4001 or 'LIMIT' raises SystemExit(5); the names
  after it are never pulled, and 10-07 restores them.
- --probe-only: open the producer's Bloomberg client, print `health`, and exit. No data call.
"""
import importlib.util
import os
import sys

TOP = os.getcwd()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
for p in (TOP, RES):
    if p not in sys.path:
        sys.path.insert(0, p)
spec = importlib.util.spec_from_file_location("model_block_pull", os.path.join(RES, "model_block_pull.py"))
mbp = importlib.util.module_from_spec(spec)
sys.modules["model_block_pull"] = mbp
spec.loader.exec_module(mbp)

blp = mbp._load_blp_client()
status = blp.health()
print("PROBE health %s" % status, flush=True)
if not status.get("ok"):
    print("PROBE NOT OK -- STOP (10-07 restores)")
    sys.exit(4)
if "--probe-only" in sys.argv:
    sys.exit(0)

_real_pull = mbp.stage_pull


def _guarded_pull(client, s3, security, *a, **kw):
    try:
        return _real_pull(client, s3, security, *a, **kw)
    except Exception as exc:
        text = "%s: %s" % (type(exc).__name__, exc)
        if "-4001" in text or "LIMIT" in text:
            print("STOP -4001/LIMIT at %s: %s" % (security, text[:200]), flush=True)
            raise SystemExit(5)
        raise


mbp.stage_pull = _guarded_pull
mbp._model_block_latest_stamps = lambda s3: {}
rc = mbp.cmd_refresh(dry_run=False)
print("AN3 same-day pull rc %d" % rc, flush=True)
sys.exit(rc)
