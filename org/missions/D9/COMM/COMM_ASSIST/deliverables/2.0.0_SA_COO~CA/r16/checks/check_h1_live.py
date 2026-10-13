"""CA-h-1 AC2: the real sources, read once under the running identity. A source MAY be absent (no object yet today);
it may NOT be unreadable. Prints H1-LIVE ok=<bool> unreadable=<n> of <N>."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _h1_cli  # noqa: E402

td, rc, tail = _h1_cli.run()
if td is None:
    print("H1-LIVE ok=False unreadable=NA of 0 reason=%s" % tail)
    sys.exit(0)
names = ["open_calls", "drafts", "eod_today", "sprint_today"]
st = {}
for n in names:
    p = pathlib.Path(td.name) / (n + ".json")
    st[n] = json.loads(p.read_text(encoding="utf-8")).get("status") if p.is_file() else "NOFILE"
bad = [n for n, s in st.items() if s not in ("ok", "absent")]
ok = rc == 0 and not bad
print("H1-LIVE ok=%s unreadable=%d of %d rc=%s statuses=%s" % (ok, len(bad), len(names), rc, json.dumps(st, sort_keys=True)))
if not ok:
    print("tail: " + tail.replace("\n", " | "))
