"""RIV-wg-1's real run -- the AI leg on live inputs, LOCAL writes only, then the opening census of the Direction Verdicts.

    python ai_real_run_local.py <code root> <page day> <out dir> [--funds A,B,...]

Runs `ai_accounts.run_day` from <code root> (a worktree or the merged tree) through an overlay sink: reads live S3, writes
only under <out dir>/layer. It makes real model calls (RIVALFUNDS_AI_ENABLE=1 and RIVALFUNDS_OPENAI_SECRET are set by this
script for this process only, as in the daily Lambda). Prints each fund's verdict opening and the census: PASS when no
four-word opening leads more than a quarter of the verdicts (the page-level rule of verdict_openers_check.py). Exit 0 PASS,
1 FAIL, 2 no verdict.
"""
import collections
import io
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
DAY, OUT = sys.argv[2], pathlib.Path(sys.argv[3]).resolve()
FUNDS = sys.argv[sys.argv.index("--funds") + 1].split(",") if "--funds" in sys.argv else None
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))
os.environ.setdefault("RIVALFUNDS_AI_ENABLE", "1")
os.environ.setdefault("RIVALFUNDS_OPENAI_SECRET", "rivalfunds/openai-api-key")
import pandas as pd  # noqa: E402
from rivalfunds import ai_accounts, sinks  # noqa: E402


class OverlaySink:
    kind = "overlay"

    def __init__(self, local_root):
        self.live, self.local = sinks.S3Sink(), sinks.LocalSink(str(local_root))

    def get(self, uri):
        return self.local.get(uri) if self.local.exists(uri) else self.live.get(uri)

    def exists(self, uri):
        return self.local.exists(uri) or self.live.exists(uri)

    def list(self, prefix_uri):
        return sorted(set(self.live.list(prefix_uri)) | set(self.local.list(prefix_uri)))

    def put(self, uri, data, content_type=None):
        return self.local.put(uri, data, content_type)


OUT.mkdir(parents=True, exist_ok=True)
overlay = OverlaySink(OUT / "layer")
sinks.get_sink = lambda spec=None, *a, **k: overlay  # every read and write of the run goes through the overlay
res = ai_accounts.run_day(DAY, sink_spec="overlay", funds=FUNDS)
(OUT / "ai_real_run_local.json").write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
print(json.dumps({k: res[k] for k in ("status", "outputs", "run_id", "as_of")}, default=str))
if not res.get("outputs"):
    print("NO-MEASUREMENT: the run wrote no rows")
    sys.exit(2)
df = pd.read_parquet(io.BytesIO(overlay.get(res["outputs"][0])))
dv = df[df["kind"] == "direction_verdict"]
openers = []
for _, r in dv.iterrows():
    op = " ".join(re.sub(r"\d{4}-\d{2}-\d{2}", "<date>", str(r["text"])).split()[:4]).lower()  # dates differ per fund; the lead does not
    openers.append(op)
    print(f"{r['fund_id']:6} {r['grounding']:4} | {' '.join(str(r['text']).split()[:14])}")
if not openers:
    print("NO-MEASUREMENT: 0 Direction Verdicts")
    sys.exit(2)
top, n = collections.Counter(openers).most_common(1)[0]
ok = n <= len(openers) / 4
print(f"verdicts: {len(openers)}; most shared opening: '{top}' x{n}; limit {len(openers) / 4:.2f}")
print("OPENERS RESULT: " + ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
