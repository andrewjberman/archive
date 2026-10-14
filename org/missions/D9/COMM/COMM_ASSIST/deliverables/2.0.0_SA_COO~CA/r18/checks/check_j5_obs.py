"""CA-j-5 observation read: what the assistant's handler has COUNTED since the ingress mark went live in record mode. Numbers only; no message content is printed.

Scans the state table (teams-global-chat-assist-table, the sk "state" rows) for objects whose state carries the mark counters and sums them:
  marks_ok   = marks in `marks_seen` (events whose mark verified and was new)   -- the legitimate-text count
  unmarked   = sum of `unmarked_seen`                                           -- events the handler would REFUSE in enforce mode
  reasons    = counts of the recorded refusal reasons (no-mark, bad-mark, stale-mark, replayed-mark)
Prints:  OBS scanned=<n> state_rows=<n> with_counters=<n> marks_ok=<n> unmarked=<n> reasons=<json> first_refusal=<iso|none> last_refusal=<iso|none>
         VERDICT: NO-EVIDENCE (no marked text yet) | CLEAN (marks_ok >= MIN and unmarked == 0) | DIRTY (unmarked > 0: read the reasons) | THIN (marks_ok < MIN, unmarked == 0)
Env: OBS_MIN (default 3) is the number of marked texts the observation window needs before CLEAN. Read-only: one paginated scan; ScannedCount is the denominator.
"""
import json
import os
import subprocess
import sys

TABLE = "teams-global-chat-assist-table"
MIN = int(os.environ.get("OBS_MIN", "3"))


def main():
    exe = "aws.cmd" if os.name == "nt" else "aws"
    args = [exe, "dynamodb", "scan", "--table-name", TABLE, "--projection-expression", "pk, sk, #d",
            "--filter-expression", "sk = :s AND (contains(#d, :a) OR contains(#d, :b))",
            "--expression-attribute-names", json.dumps({"#d": "data"}),
            "--expression-attribute-values", json.dumps({":s": {"S": "state"}, ":a": {"S": "marks_seen"}, ":b": {"S": "unmarked_seen"}}),
            "--output", "json"]
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", timeout=300)
    if r.returncode != 0:
        print("OBS ERROR: %s" % ((r.stderr or "").strip().splitlines() or ["rc=%d" % r.returncode])[-1])
        print("VERDICT: ERROR")
        return 1
    doc = json.loads(r.stdout)
    marks_ok = unmarked = with_counters = 0
    reasons, ats = {}, []
    for item in doc.get("Items", []):
        try:
            st = json.loads(item["data"]["S"])
        except Exception:  # noqa: BLE001 -- a row that does not parse is counted as not carrying counters
            continue
        seen, refusals, n = st.get("marks_seen") or [], st.get("mark_refusals") or [], int(st.get("unmarked_seen") or 0)
        if not (seen or refusals or n):
            continue
        with_counters += 1
        marks_ok += len(seen)
        unmarked += n
        for x in refusals:
            reasons[x.get("reason")] = reasons.get(x.get("reason"), 0) + 1
            if x.get("at"):
                ats.append(x["at"])
    ats.sort()
    print("OBS scanned=%s state_rows=%s with_counters=%d marks_ok=%d unmarked=%d reasons=%s first_refusal=%s last_refusal=%s"
          % (doc.get("ScannedCount"), doc.get("Count"), with_counters, marks_ok, unmarked, json.dumps(reasons, sort_keys=True),
             ats[0] if ats else "none", ats[-1] if ats else "none"))
    if marks_ok == 0 and unmarked == 0:
        print("VERDICT: NO-EVIDENCE")
    elif unmarked > 0:
        print("VERDICT: DIRTY")
    elif marks_ok < MIN:
        print("VERDICT: THIN")
    else:
        print("VERDICT: CLEAN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
