"""Read-only trial: run the rivalfunds AI chain for page day 2026-10-15 on gpt-6-astra (no temperature), NOTHING written to S3.

    python astra_trial.py <model> [fund ...]

Prints per fund: the grounding of each item, the number of corrections, the reasons of any FAIL, and the token usage.
The client is the production RestClient with the one difference under test: no `temperature` key in the request.
"""
import datetime as dt
import json
import sys
import time

sys.path[:0] = ["C:/dev/ajb_workspace/data/etfs/scripts", "C:/dev/ajb_workspace"]
import boto3  # noqa: E402
import pandas as pd  # noqa: E402
import requests  # noqa: E402
from rivalfunds import ai_accounts as A  # noqa: E402
from rivalfunds import ai_client, homes, market_context, sinks, universe  # noqa: E402
from rivalfunds.gold_holding_contribution import _newest_by_date, _read, as_of  # noqa: E402
from rivalfunds.publish_page import load_a1  # noqa: E402

MODEL = sys.argv[1]
ONLY = sys.argv[2:]
PAGE_DAY = "2026-10-15"

sec = boto3.client("secretsmanager", region_name="us-east-1").get_secret_value(SecretId="rivalfunds/openai-api-key")["SecretString"]
try:
    d = json.loads(sec)
    KEY = (d.get("api_key") or d.get("key")) if isinstance(d, dict) else sec
except ValueError:
    KEY = sec
USAGE = {"prompt": 0, "completion": 0, "calls": 0}


class TrialClient(ai_client.RestClient):
    def chat(self, messages, model, timeout=None):
        body = {"model": model, "messages": messages, "response_format": {"type": "json_object"}}
        if model.startswith("gpt-5"):
            body["temperature"] = 0.2
        for attempt in (1, 2, 3):
            r = requests.post(ai_client.URL, headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"},
                              json=body, timeout=ai_client.TIMEOUT_S if timeout is None else timeout)
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(5 * attempt)
                continue
            r.raise_for_status()
            j = r.json()
            USAGE["calls"] += 1
            USAGE["prompt"] += j["usage"]["prompt_tokens"]
            USAGE["completion"] += j["usage"]["completion_tokens"]
            return j["choices"][0]["message"]["content"]
        r.raise_for_status()


s = sinks.get_sink("s3")
day = as_of(PAGE_DAY)
lo = (dt.date.fromisoformat(day) - dt.timedelta(days=A.R30_DAYS + A.LOAD_PAD)).isoformat()
g5 = _read(s, _newest_by_date(s, homes.trade_schedule(""), lo, day))
g6 = _read(s, _newest_by_date(s, homes.address("rivalfunds", "etfs", "gold", "flow_reconciliation", "date="), lo, day))
a1, _ = load_a1(s, PAGE_DAY)
hc = pd.DataFrame(a1.get("holding_contribution") or [])
bt = pd.DataFrame(a1.get("buying_trend") or [])
readings = market_context.read_context(day)
client = TrialClient(KEY)
seen = {}
tot = {"PASS": 0, "FAIL": 0, "corr": 0}
t0 = time.time()
for e in universe.entries():
    f, role = str(e["fund_id"]), str(e["role"])
    if role == "index_control" or (ONLY and f not in ONLY):
        continue
    facts = A.fact_pack(f, PAGE_DAY, g5, g6, hc, bt)
    try:
        rows = A.run_chain(f, role, PAGE_DAY, facts, readings, client, "TRIAL", model=MODEL, seen_frames=seen)
    except Exception as ex:  # noqa: BLE001
        print(f, "ERROR", type(ex).__name__, str(ex)[:200])
        continue
    for r in rows:
        m = json.loads(r["input_manifest"])
        tot[r["grounding"]] += 1
        tot["corr"] += m.get("corrections", 0)
        print(f, r["kind"], r["grounding"], "corr", m.get("corrections"), (r["grounding_reason"] or "")[:200])
print("MODEL", MODEL, "TOTAL", tot, "usage", USAGE, "secs", round(time.time() - t0))
