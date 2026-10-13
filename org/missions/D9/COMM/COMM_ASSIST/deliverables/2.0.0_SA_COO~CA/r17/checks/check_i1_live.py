"""CA-i-1 AC2: the REAL refresh against the real sources stamps ages, carries object_id on draft rows, and leaves answers/ alone.

Prints:  I1-LIVE ok=<True|False> items=<n> aged=<n> object_ids=<n> of <n> answers_untouched=<True|False> readme_answers=<True|False> reason=<text>
Runs the CLI once under the running identity into a temp folder (read-only AWS calls). Passes only if no source is unreadable, every item
carries `age_minutes` and `age_from` keys, at least 80 percent of items have a whole-number age, every drafts item has a non-empty `object_id`,
a file pre-placed under answers/ is byte-identical afterwards, and README.txt names the answers/ folder.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
SOURCES = ("open_calls", "drafts", "eod_today", "sprint_today")


def main():
    why, items, aged, oid_n, oid_of = "", 0, 0, 0, 0
    untouched = readme = False
    try:
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "answers").mkdir()
            keep = Path(d) / "answers" / "keep.txt"
            keep.write_bytes(b"muse answer placeholder\n")
            r = subprocess.run([sys.executable, str(ROOT / "data/transcripts/scripts/muse_reader/refresh.py"), "--root", d],
                               capture_output=True, text=True, timeout=110, cwd=str(ROOT))
            if r.returncode != 0:
                why = "refresh rc=%s %s" % (r.returncode, (r.stderr or "")[:100])
            else:
                for s in SOURCES:
                    doc = json.loads((Path(d) / (s + ".json")).read_text(encoding="utf-8"))
                    if doc["status"] == "unreadable":
                        why = why or "%s unreadable" % s
                    for it in doc.get("items") or []:
                        items += 1
                        if "age_minutes" not in it or "age_from" not in it:
                            why = why or "%s item lacks age keys" % s
                        elif isinstance(it["age_minutes"], int) and it["age_minutes"] >= 0:
                            aged += 1
                        if s == "drafts":
                            oid_of += 1
                            if isinstance(it.get("object_id"), str) and it["object_id"]:
                                oid_n += 1
                untouched = keep.read_bytes() == b"muse answer placeholder\n" and sorted(p.name for p in (Path(d) / "answers").iterdir()) == ["keep.txt"]
                readme = "answers/" in (Path(d) / "README.txt").read_text(encoding="utf-8")
                if not why and items and aged < 0.8 * items:
                    why = "only %d of %d items carry a whole-number age" % (aged, items)
                if not why and oid_n != oid_of:
                    why = "%d of %d draft rows lack object_id" % (oid_of - oid_n, oid_of)
                if not why and not untouched:
                    why = "answers/ changed by the refresh"
                if not why and not readme:
                    why = "README.txt does not name answers/"
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
    print("I1-LIVE ok=%s items=%d aged=%d object_ids=%d of %d answers_untouched=%s readme_answers=%s reason=%s"
          % (not why, items, aged, oid_n, oid_of, untouched, readme, why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
