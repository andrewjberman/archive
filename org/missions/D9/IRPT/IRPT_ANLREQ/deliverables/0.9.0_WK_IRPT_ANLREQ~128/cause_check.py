"""AR318-y-AC1: print CAUSE-NAMED only when the record names the FIRST step that fails for D1 and passes for D6
and for the CONTROL, re-derived here from the step table of r40/COMPOSITION_CAUSE.json.

Value rule (checked on every leaf): a sha256 hex, an integer, a boolean, null, a status word, a field or check
name, or a repository path. The PROSE keys below carry sentences; they are exempt from the value rule and
scanned instead for any identifier of a person, an input id or an address.
Exit 0 with CAUSE-NAMED ..., exit 1 with CAUSE-NOT-NAMED <why>.
"""
import json
import re
import sys
from pathlib import Path

RECORD = Path(__file__).resolve().parent / "r40" / "COMPOSITION_CAUSE.json"
REPO = Path(__file__).resolve().parents[7]
PROSE_KEYS = {"method", "claim", "difference_in_words", "not_read"}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_.]*$")
PATH = re.compile(r"^[A-Za-z0-9_./~-]+$")
STATUS = {"PASS", "FAIL", "OK"}
LEAK = re.compile(r"portfolio_|@|[0-9a-f]{40,}")


def leaves(node, key=None):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from leaves(v, k)
    elif isinstance(node, list):
        for v in node:
            yield from leaves(v, key)
    else:
        yield key, node


def refuse(why):
    print("CAUSE-NOT-NAMED " + why)
    sys.exit(1)


def main():
    rec = json.loads(RECORD.read_text(encoding="utf-8"))
    for key, val in leaves(rec):
        if key in PROSE_KEYS:
            if isinstance(val, str) and LEAK.search(val):
                refuse("prose key %s carries an identifier" % key)
            continue
        if isinstance(val, bool) or val is None or isinstance(val, int):
            continue
        if isinstance(val, str) and (HEX64.match(val) or NAME.match(val) or PATH.match(val) or val in STATUS):
            continue
        refuse("value under key %s is not a hash, count, status, field name or check name" % key)

    rows = sorted(rec["steps"], key=lambda r: r["step"])
    d1_fail = [r["step"] for r in rows if r["D1"] == "FAIL"]
    if not d1_fail:
        refuse("the table has no failing step for D1")
    first = min(d1_fail)
    row = next(r for r in rows if r["step"] == first)
    if row["D6"] != "PASS" or row["CONTROL"] != "PASS":
        refuse("the first failing step for D1 does not pass for D6 and the CONTROL")
    cause = rec["cause"]
    if cause["step"] != first or cause["step_name"] != row["name"]:
        refuse("the cause step %s is not the first failing step %s" % (cause["step"], first))
    if rec["D1_detail"]["field_path"] != cause["field_path"]:
        refuse("the cause field path disagrees with the D1 detail of the table")
    if any(v != "PASS" for v in rec["negative_control"]["steps"].values()):
        refuse("the negative control (D1 without the named field) does not pass all five steps")
    path = REPO / cause["file"]
    if not path.is_file():
        refuse("the cited file is absent")
    lines = path.read_text(encoding="utf-8").splitlines()
    if not 1 <= cause["line"] <= len(lines) or '"else"' not in lines[cause["line"] - 1]:
        refuse("the cited line does not carry the else branch of the owner definition")
    print("CAUSE-NAMED step=%d file=%s line=%d" % (first, cause["file"], cause["line"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
