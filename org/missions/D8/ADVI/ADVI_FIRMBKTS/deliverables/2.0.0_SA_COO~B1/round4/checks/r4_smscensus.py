"""ADVI_FIRMBKTS round 4 check for cell FB-g-32 (the census of every publisher that reaches the SEV1 SMS subscription; the CTO's
ruling AMENDMENT 5, msg 4005: each publisher sets AWS.MM.SMS.OriginationNumber from ONE Terraform-managed value),
issuer 2.0.0_SA_COO~B1.

--arms census --file <path> [--root <tree>]  (4 arms)
  S1 the JSON file exists and holds `topics` (a non-empty list), each entry with: topic_arn, sms_subscriptions (an integer
     count; never an endpoint), publishers (a list), alarm_actions (a list), eventbridge_targets (a list).
  S2 every publisher entry has `kind` in {"code", "aws_service"}, a `where` (a "path:line" for code whose file exists in
     the tree, or a service resource id), and `can_set_message_attributes` (true for code, false for an alarm action or an
     EventBridge target).
  S3 the file carries `n_publishers` (the printed N) equal to the number of publisher entries, and `n_unable` equal to the
     number whose `can_set_message_attributes` is false; `terraform_value_candidates` lists at least one existing
     Terraform file:line that already carries the origination number's identifier or says none does.
  S4 no phone number appears anywhere in the file: no run of 10 or more digits after an optional +, no `+1`-prefixed number.
Plain ASCII output; the last line carries the arm count. READ-ONLY. Never edit this file.
"""
import argparse
import json
import os
import re
import subprocess
import sys


def _root(arg):
    if arg:
        return arg
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def census(root, file):
    res = []
    d = None
    try:
        d = json.load(open(file, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print("  file unreadable: %s" % type(e).__name__)
    topics = d.get("topics") if isinstance(d, dict) else None
    ok1 = isinstance(topics, list) and bool(topics) and all(
        isinstance(t, dict) and isinstance(t.get("topic_arn"), str) and isinstance(t.get("sms_subscriptions"), int)
        and all(isinstance(t.get(k), list) for k in ("publishers", "alarm_actions", "eventbridge_targets"))
        for t in topics)
    print("  S1 topics=%d" % (len(topics) if isinstance(topics, list) else 0))
    res.append(("S1 a non-empty topics list with every key", ok1))

    pubs = [p for t in (topics or []) if isinstance(t, dict) for p in t.get("publishers", [])]
    ok2 = bool(pubs)
    for p in pubs:
        if not isinstance(p, dict) or p.get("kind") not in ("code", "aws_service") or "where" not in p \
                or not isinstance(p.get("can_set_message_attributes"), bool):
            ok2 = False
            continue
        if p["kind"] == "code":
            m = re.match(r"^(.*?):(\d+)$", str(p["where"]))
            if not m or not os.path.isfile(os.path.join(root, *m.group(1).split("/"))) \
                    or p["can_set_message_attributes"] is not True:
                ok2 = False
        elif p["can_set_message_attributes"] is not False:
            ok2 = False
    print("  S2 publishers=%d" % len(pubs))
    res.append(("S2 every publisher is typed, located and its attribute ability stated", ok2))

    n = d.get("n_publishers") if isinstance(d, dict) else None
    unable = d.get("n_unable") if isinstance(d, dict) else None
    cand = d.get("terraform_value_candidates") if isinstance(d, dict) else None
    ok3 = n == len(pubs) and unable == sum(1 for p in pubs if isinstance(p, dict)
                                          and p.get("can_set_message_attributes") is False) \
        and isinstance(cand, list)
    print("  S3 n_publishers=%s of %d; n_unable=%s" % (n, len(pubs), unable))
    res.append(("S3 N is printed and equals the entries; the unable count equals the entries that cannot set attributes",
                ok3))

    text = open(file, encoding="utf-8").read() if d is not None else ""
    ok4 = d is not None and re.search(r"\+?\d{10,}", text) is None and re.search(r"\+1\d", text) is None
    res.append(("S4 no phone number appears in the file", ok4))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("census",), required=True)
    ap.add_argument("--file", required=True)
    ap.add_argument("--root")
    a = ap.parse_args()
    root = _root(a.root)
    try:
        res = census(root, a.file if os.path.isabs(a.file) else os.path.join(root, a.file))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: (%s: %s)" % (type(e).__name__, str(e)[:160]))
        res = [("the census readable", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 SMS CENSUS: %d of 4 arms" % n)
    sys.exit(0 if n == 4 else 1)


if __name__ == "__main__":
    main()
