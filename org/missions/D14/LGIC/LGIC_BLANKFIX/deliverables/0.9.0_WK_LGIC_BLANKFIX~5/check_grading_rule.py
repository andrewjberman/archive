"""BE5-AC2: the worked-case file carries the fourth verdict's case and the ratified cadence rules,
and the library's suite (which loads cases from that file) still passes whole.

Run from the worktree root. ASCII only. Last line printed exactly once.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([".."] * 7)))
RULE = os.path.join(ROOT, "org", "missions", "D14", "LGIC", "LGIC_NAMING", "deliverables", "GRADING_RULE.md")
SCHEMA = os.path.join(ROOT, "org", "standards", "NAMING_SCHEMA.json")


def worked_case(text):
    hits = []
    for line in text.splitlines():
        s = line.strip().rstrip(",")
        if s.startswith("{") and '"pandas-pyarrow-layer"' in s and '"LAMBDA_LAYER"' in s:
            try:
                hits.append(json.loads(s))
            except ValueError:
                pass
    return len(hits) == 1 and hits[0].get("verdict") == "NO-SYSTEM-ASKED" \
        and hits[0].get("canonical_form") == "pandas-pyarrow-layer"


def cadence_ok(text, schema):
    rx = re.compile(schema["cadence"]["interval_form"]["token_regex"])
    i = text.find("**V6 CADENCES**")
    j = text.find("**V7 TIERS**")
    if i < 0 or j < i:
        return False
    sec = text[i:j]
    flat = " ".join(sec.split())
    ticks = re.findall(r"`([^`]+)`", sec)
    has_five = "five or more days" in flat
    mins = [t for t in ticks if re.fullmatch(r"\d+min", t) and rx.match(t)]
    hours = [t for t in ticks if re.fullmatch(r"\d+h", t) and rx.match(t)]
    has_event = "{function}-on-{event}" in sec
    no_weekday = "never named" in flat
    return has_five and bool(mins) and bool(hours) and has_event and no_weekday


def main():
    text = open(RULE, "rb").read().decode("utf-8")
    schema = json.load(open(SCHEMA, "rb"))
    wc = worked_case(text)
    cad = cadence_ok(text, schema)
    p = subprocess.run(
        [sys.executable, "-m", "pytest", "lib/tests/test_opal_naming.py", "-q", "-p", "no:cacheprovider", "--color=no"],
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.decode("utf-8", "replace")
    failed = re.search(r"(\d+) failed", out)
    passed = re.search(r"(\d+) passed", out)
    nf = int(failed.group(1)) if failed else 0
    np_ = int(passed.group(1)) if passed else 0
    suite_ok = p.returncode == 0 and nf == 0 and np_ > 0
    ok = wc and cad and suite_ok
    print("GRADING-RULE ok=%s worked_case=%s cadence=%s suite_failed=%d suite_passed=%d" % (ok, wc, cad, nf, np_))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
