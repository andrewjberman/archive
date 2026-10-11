"""MDPF_CANON round 4, cell CN-d-2 -- the X2 basis counts a count_as_of entry as a CARRY and lists each with its age
(CTO ADDENDUM 1 @187b53dbe6, AC1 re-cut; the fold does not change).

One command, four arms; prints `ROUND 4 CARRIES: k of 4 arms` and exits 0 only on all four.
Root for the worker's files = $R4_ROOT, else `git rev-parse --show-toplevel`. Served objects are read-only gets at 2026-10-08.

  B1 the basis file exists at deliverables/0.9.0_WK_MDPF_CANON~11/X2_GLOBAL_BASIS.md
  B2 (control, true at base) over the four served aggregate-aua-timeseries objects, every global by_model entry with a
     nonzero count at the as-of is held by at least one firm scope (same key, nonzero count) or wears count_as_of
  B3 the file lists EVERY entry that wears count_as_of with a nonzero count at the as-of: a line holding the key, its
     count_as_of date and an integer age equal to the trading days in (count_as_of, as-of], and the word CARRY
  B4 the ledger's X2 row still reads GRANTED and cites the new basis path (the status is Andrew's; only the citation moves)
"""
import json
import os
import re
import subprocess
import sys

AS_OF = "2026-10-08"
BUCKET = "opal-data-assets"
SCOPES = ("global", "49financial", "inflection", "cottonwood")
BASIS_REL = "org/missions/D8/MDPF/MDPF_CANON/deliverables/0.9.0_WK_MDPF_CANON~11/X2_GLOBAL_BASIS.md"
LEDGER_REL = "infra/logic/06_CONFORMANCE_LEDGER.md"


def _git_root() -> str:
    return subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()


def _served(scope: str) -> dict:
    import boto3
    key = f"portal/gold/mdpf/{scope}/aggregate-aua-timeseries/{AS_OF}.json"
    body = boto3.client("s3", region_name="us-east-1").get_object(Bucket=BUCKET, Key=key)["Body"].read()
    return json.loads(body)


def _count_at(doc: dict, key: str):
    e = (doc.get("by_model") or {}).get(key)
    if not e:
        return None
    try:
        i = doc["dates"].index(AS_OF)
    except ValueError:
        return None
    cc = e.get("account_count") or []
    return cc[i] if i < len(cc) else None


def main() -> int:
    wroot = os.environ.get("R4_ROOT") or _git_root()
    repo = _git_root()
    arms = []

    # B1
    basis_path = os.path.join(wroot, *BASIS_REL.split("/"))
    text = ""
    ok = os.path.isfile(basis_path)
    if ok:
        text = open(basis_path, encoding="utf-8").read()
    print("  B1 %s: %s" % ("PASS" if ok else "FAIL", BASIS_REL if ok else "file absent: " + BASIS_REL))
    arms.append(ok)

    # served reads (needed by B2 and B3)
    served = {}
    err = None
    try:
        for sc in SCOPES:
            served[sc] = _served(sc)
    except BaseException as exc:                              # noqa: BLE001
        err = f"{type(exc).__name__}: {str(exc)[:160]}"

    carries = []          # (key, count_as_of)
    if err is None:
        g = served["global"]
        unheld = []
        for key, e in (g.get("by_model") or {}).items():
            c = _count_at(g, key)
            if not c:                                         # None or 0: no count to account for
                continue
            wears = bool((e or {}).get("count_as_of"))
            held = any((_count_at(served[sc], key) or 0) > 0 for sc in SCOPES if sc != "global")
            if wears:
                carries.append((key, str(e["count_as_of"])[:10]))
            if not held and not wears:
                unheld.append(key)
        ok = not unheld
        print("  B2 %s: nonzero-count global entries neither held by a firm nor wearing count_as_of: %s; carries read: %d" % (
            "PASS" if ok else "FAIL", unheld if unheld else "none", len(carries)))
        arms.append(ok)
    else:
        print(f"  B2 FAIL: served read failed: {err}")
        arms.append(False)

    # B3
    ok = False
    if err is None and text:
        if repo not in sys.path:
            sys.path.insert(0, repo)
        try:
            from lib.trading_calendar import trading_days_between
            import datetime as dt
            missing = []
            lines = text.splitlines()
            for key, cao in carries:
                age = len(trading_days_between(dt.date.fromisoformat(cao) + dt.timedelta(days=1),
                                               dt.date.fromisoformat(AS_OF)))
                hit = any(key in ln and cao in ln and re.search(r"(?<![\d-])%d(?![\d-])" % age, ln)
                          for ln in lines)
                if not hit:
                    missing.append(f"{key}({cao}, age {age})")
            has_word = re.search(r"\bcarr(y|ies)\b", text, re.I) is not None
            ok = bool(carries) and not missing and has_word
            print("  B3 %s: carries %d, unlisted %s, word CARRY %s" % (
                "PASS" if ok else "FAIL", len(carries), missing if missing else "none", "present" if has_word else "absent"))
        except BaseException as exc:                          # noqa: BLE001
            print(f"  B3 FAIL: {type(exc).__name__}: {str(exc)[:160]}")
    else:
        print("  B3 FAIL: no basis file or no served read")
    arms.append(ok)

    # B4
    ok = False
    lp = os.path.join(wroot, *LEDGER_REL.split("/"))
    if os.path.isfile(lp):
        for ln in open(lp, encoding="utf-8").read().splitlines():
            if ln.startswith("| X2 |"):
                ok = "GRANTED" in ln and "0.9.0_WK_MDPF_CANON~11/X2_GLOBAL_BASIS.md" in ln
                break
    print("  B4 %s: ledger X2 row %s" % ("PASS" if ok else "FAIL",
                                       "GRANTED and cites the new basis" if ok else "does not read GRANTED with the new basis path"))
    arms.append(ok)

    k = sum(1 for a in arms if a)
    print(f"ROUND 4 CARRIES: {k} of {len(arms)} arms")
    return 0 if k == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
