"""TO-DB-b-117: field-by-field comparison of every captured manifest / status record, live-pinned handler against HEAD's.

Usage: python <this file> <capture_live.json> <capture_new.json> <out.json>

Inputs are the raw captures of manifest_capture.py (outside the repo; they carry account ids). Output is the repo-safe record:
for each manifest, each field with live / new / verdict (EQUAL, ADDED, CHANGED, REMOVED). A value is written verbatim only when it is a
scalar string, bool, int or None, or a small container of the same with no 6-digit run in a key or string; anything account-keyed,
float-valued (a client figure) or large is written as {"sha256", "n"} of its canonical JSON, so equal means byte-equal.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

DIGITS = re.compile(r"\d{6,}")
ABSENT = "<key not in the manifest>"


def canon(v):
    return json.dumps(v, sort_keys=True, separators=(",", ":"))


def leaves(v):
    if isinstance(v, dict):
        for k, x in v.items():
            yield k
            yield from leaves(x)
    elif isinstance(v, list):
        for x in v:
            yield from leaves(x)
    else:
        yield v


def show(v):
    if v == ABSENT:
        return v
    if v is None or isinstance(v, (bool, int)):
        return v
    if isinstance(v, str):
        if len(v) <= 700 and not re.search(r"\d{9,}", v):
            return v
        return {"sha256": hashlib.sha256(v.encode()).hexdigest(), "n": len(v)}
    ok = len(canon(v)) <= 700
    for x in leaves(v):
        if isinstance(x, float) or (isinstance(x, str) and re.search(r"\d{9,}", x)):
            ok = False
    if ok:
        return v
    return {"sha256": hashlib.sha256(canon(v).encode()).hexdigest(), "n": len(v) if hasattr(v, "__len__") else 1}


def label(key, body):
    try:
        m = json.loads(body)
    except Exception:
        return key
    if "table" in m:
        return "%s manifest" % m["table"]
    if "statements" in m:
        return "lots_not_computed.json status record"
    return key


def table_keys(cap):
    """{label: (key, parsed body)} for the run's puts and the forced status record."""
    out = {}
    for k, body in cap["run_bodies"].items():
        out[label(k, body)] = (k, json.loads(body))
    for k, body in cap["status_forced"].items():
        out[label(k, body) + " (forced refusal shape)"] = (k, json.loads(body))
    return out


def strip_key(k):
    """The key with the bucket and firm path left whole except nothing is an account id: keep the last 3 path parts."""
    return "/".join(k.split("/")[-3:])


def main(live_p, new_p, out_p):
    live = json.loads(Path(live_p).read_text(encoding="utf-8"))
    new = json.loads(Path(new_p).read_text(encoding="utf-8"))
    tl, tn = table_keys(live), table_keys(new)
    names = sorted(set(tl) | set(tn))
    manifests = []
    for name in names:
        if name not in tl or name not in tn:
            manifests.append({"manifest": name, "fields": [{"field": "<whole object>", "live": "present" if name in tl else "absent",
                                                            "new": "present" if name in tn else "absent",
                                                            "verdict": "REMOVED" if name in tl else "ADDED"}]})
            continue
        (kl, ml), (kn, mn) = tl[name], tn[name]
        fields = [{"field": "<object key (last 3 path parts)>", "live": strip_key(kl), "new": strip_key(kn),
                   "verdict": "EQUAL" if kl == kn else "CHANGED"}]
        fields.append({"field": "<full bucket/key equal>", "live": kl == kn, "new": kl == kn, "verdict": "EQUAL"})
        fields.append({"field": "<key count>", "live": len(ml), "new": len(mn), "verdict": "EQUAL" if len(ml) == len(mn) else "CHANGED"})
        for f in sorted(set(ml) | set(mn)):
            lv = ml.get(f, ABSENT)
            nv = mn.get(f, ABSENT)
            if f not in ml:
                verdict = "ADDED"
            elif f not in mn:
                verdict = "REMOVED"
            else:
                verdict = "EQUAL" if canon(lv) == canon(nv) else "CHANGED"
            fields.append({"field": f, "live": show(lv), "new": show(nv), "verdict": verdict})
        manifests.append({"manifest": name, "key_tail": {"live": strip_key(kl), "new": strip_key(kn)}, "fields": fields})
    rec = {"capture": {"live": {"kit": live["kit"], "run_put_count": live["run_put_count"], "stream_calls": len(live["stream_calls"]),
                                "run_keys": [strip_key(k) for k in live["run_keys"]]},
                       "new": {"kit": new["kit"], "run_put_count": new["run_put_count"], "stream_calls": len(new["stream_calls"]),
                               "run_keys": [strip_key(k) for k in new["run_keys"]]}},
           "manifests": manifests}
    Path(out_p).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    for m in manifests:
        c = {}
        for f in m["fields"]:
            c[f["verdict"]] = c.get(f["verdict"], 0) + 1
        print(m["manifest"], c)
        for f in m["fields"]:
            if f["verdict"] != "EQUAL":
                print("   ", f["verdict"], f["field"], "live=", str(f["live"])[:140], "new=", str(f["new"])[:140])


if __name__ == "__main__":
    main(*sys.argv[1:4])
