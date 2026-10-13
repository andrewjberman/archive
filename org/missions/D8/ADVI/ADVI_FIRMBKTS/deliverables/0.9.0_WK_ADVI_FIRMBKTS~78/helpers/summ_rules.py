import json
import os
import re

D = "C:/dev/wk-firmbkts-78-data"
rules = json.load(open(os.path.join(D, "rules.json"), encoding="utf-8"))["Rules"]
names = [line.strip() for line in open(os.path.join(D, "rule_names.lf.txt"), encoding="utf-8") if line.strip()]
by_name = {r["Name"]: r for r in rules}
pat = re.compile(r"opal-data-cot|cottonwood|gold|opal-data-bd|cot-|/cot/|cot/|\bcot\b|-cot-", re.I)

hits = []
tgt_total = 0
for i, name in enumerate(names, 1):
    tg = json.load(open(os.path.join(D, "tg", "%d.json" % i), encoding="utf-8"))["Targets"]
    tgt_total += len(tg)
    r = by_name.get(name, {})
    pattern = r.get("EventPattern") or ""
    blob_t = " ".join("%s %s %s" % (t.get("Arn", ""), t.get("Input", "") or "", json.dumps(t.get("InputTransformer", "")) if t.get("InputTransformer") else "") for t in tg)
    flags = []
    if pat.search(pattern):
        flags.append("PATTERN")
    if pat.search(blob_t):
        flags.append("TARGET-OR-INPUT")
    if pat.search(name):
        flags.append("NAME")
    if flags:
        hits.append((name, r.get("State"), r.get("ScheduleExpression", ""), flags, tg, pattern))

print("RULES scanned=%d targets_total=%d names_matched=%d" % (len(names), tgt_total, len(hits)))
for name, st, sched, flags, tg, pattern in hits:
    print("== %s state=%s sched=%s flags=%s" % (name, st, sched, ",".join(flags)))
    if pattern:
        print("   pattern=" + pattern[:400])
    for t in tg:
        inp = (t.get("Input") or "")
        it = t.get("InputTransformer")
        print("   target id=%s arn=%s input=%s transformer=%s" % (t.get("Id"), t.get("Arn"), inp[:300], json.dumps(it)[:300] if it else "-"))
