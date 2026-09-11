"""check_e2e.py -- AMGT-s-2 AC3: ONE end-to-end exercise of the built seam, for ONE uncovered
ticker (F2/G-24: this order's only new security).

Sequence, all against the REAL deployed cloud side and this box's real Bloomberg session:
  1. `aws lambda invoke` on the deployed `opal-research-pull-enqueue` function with a direct-invoke
     payload `{"ticker": "<TICKER>"}` -- the same code path an authenticated
     `POST /api/private/research/pull` would run (SEAM_DESIGN.md section 1; a direct invoke
     substitutes for a real browser session because no page/JWT exists yet -- C-DESIGN-SPEC-FIRST).
     This writes packs/<security_key>/status.json state=REQUESTED and sends one SQS message.
  2. Launch `integrations/bloomberg/research/pull_consumer.py --once` as a background process --
     it drains that one message, checks bloomberg_health(), and runs the real pull.
  3. Poll status.json (S3 GetObject) every 3s, capped at 40 polls (~120s, this order's stated
     BOUNDS cap), recording every DISTINCT state observed in order.
  4. On a terminal state (LANDED/FAILED) or the cap: stop, report the observed transition
     sequence, elapsed seconds, and (on LANDED) the raw object count under raw/bloomberg/<key>/.

Prints exactly one line of the shape this order's AC3 names:
    E2E: ticker <key> status REQUESTED->FETCHING->LANDED in <n> s; raw objects 2; status.json LANDED
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import boto3

TICKER = "NVDA US Equity"  # the ONE uncovered ticker named in SEAM_DESIGN.md section 7 -- not
# one of Adam's 89-name research coverage universe (universe.json, deliverables/~3/), not one of
# AMGT-s-1's 3 covered-name test securities (SAP GY Equity, BA US Equity, BABA US Equity).
BUCKET = "opal-data-research"
FUNCTION_NAME = "opal-research-pull-enqueue"
POLL_INTERVAL_S = 3
MAX_POLLS = 40  # ~120s cap -- BOUNDS: never an unbounded wait

_HERE = Path(__file__).resolve().parent
# _HERE = .../AMGT_RESAPP/deliverables/<worker>; parents[0]=deliverables, [1]=AMGT_RESAPP,
# [2]=AMGT, [3]=D5, [4]=missions, [5]=org, [6]=workspace root.
_WORKSPACE = _HERE.parents[6]
_CONSUMER = _WORKSPACE / "integrations" / "bloomberg" / "research" / "pull_consumer.py"


def security_key(ticker: str) -> str:
    return ticker.replace(" ", "_")


def read_status(s3, sec_key: str) -> dict | None:
    try:
        obj = s3.get_object(Bucket=BUCKET, Key=f"packs/{sec_key}/status.json")
        return json.loads(obj["Body"].read())
    except Exception:
        return None


def count_raw_objects(s3, sec_key: str, stamp: str) -> int:
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=f"raw/bloomberg/{sec_key}/{stamp}/")
    return len(resp.get("Contents", []))


def main() -> int:
    sec_key = security_key(TICKER)
    lam = boto3.client("lambda")
    s3 = boto3.client("s3")

    t0 = time.time()

    invoke_resp = lam.invoke(
        FunctionName=FUNCTION_NAME,
        InvocationType="RequestResponse",
        Payload=json.dumps({"ticker": TICKER}).encode("utf-8"),
    )
    payload = json.loads(invoke_resp["Payload"].read())
    print(f"ENQUEUE: {payload}")
    if invoke_resp.get("FunctionError"):
        print(f"E2E: ticker {sec_key} status ENQUEUE_FAILED in 0 s; raw objects 0; status.json ABSENT")
        return 1

    consumer_proc = subprocess.Popen(
        [sys.executable, str(_CONSUMER), "--once"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    seen_states: list[str] = []
    final_status: dict | None = None
    for _ in range(MAX_POLLS):
        status = read_status(s3, sec_key)
        if status is not None:
            st = status.get("state")
            if not seen_states or seen_states[-1] != st:
                seen_states.append(st)
            if st in ("LANDED", "FAILED"):
                final_status = status
                break
        time.sleep(POLL_INTERVAL_S)

    try:
        consumer_proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        consumer_proc.kill()
    consumer_out = consumer_proc.stdout.read() if consumer_proc.stdout else ""
    print("CONSUMER OUTPUT:")
    print(consumer_out)

    elapsed = round(time.time() - t0, 1)
    transitions = "->".join(seen_states) if seen_states else "NO_STATUS_OBSERVED"

    if final_status is None:
        print(f"E2E: ticker {sec_key} status {transitions} in {elapsed} s; raw objects 0; status.json TIMEOUT")
        return 1

    final_state = final_status.get("state")
    raw_count = 0
    if final_state == "LANDED":
        raw_count = count_raw_objects(s3, sec_key, final_status.get("raw_stamp", ""))

    print(f"E2E: ticker {sec_key} status {transitions} in {elapsed} s; raw objects {raw_count}; status.json {final_state}")
    return 0 if final_state == "LANDED" and raw_count == 2 else 1


if __name__ == "__main__":
    sys.exit(main())
