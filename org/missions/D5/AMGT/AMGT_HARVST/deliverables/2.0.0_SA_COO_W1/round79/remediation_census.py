"""AMGT_HARVST round 79 -- census of open remediation rows across every REMEDIATION_v*.md (latest version per row id).

Read-only. Run from the repo root: `python <this file>`.
"""
import glob
import json
import re

DIR = "org/missions/D5/AMGT/AMGT_HARVST/surprise-channel/remediations/"


def version(path):
    return int(re.search(r"_v(\d+)", path).group(1))


def main():
    files = sorted(glob.glob(DIR + "REMEDIATION_v*.md"), key=version)
    latest = {}
    for path in files:
        text = open(path, encoding="utf-8").read()
        for block in re.finditer(r"```json\s*(\[.*?\])\s*```", text, re.S):
            try:
                rows = json.loads(block.group(1))
            except ValueError:
                print("PARSE-FAIL", path)
                continue
            for row in rows:
                if isinstance(row, dict) and row.get("id"):
                    latest[row["id"]] = (version(path), row)
    print("files %d, row ids %d" % (len(files), len(latest)))
    open_rows = [(v, r) for v, r in latest.values()
                 if not r.get("closed") and (r.get("remediation") or {}).get("state", "OPEN") != "CLOSED"]
    print("open %d" % len(open_rows))
    for v, row in sorted(open_rows, key=lambda item: item[0]):
        rem = row.get("remediation") or {}
        print("v%-3d %-28s %-8s owner=%s round=%s" % (v, row["id"], row.get("hazard_standing"),
                                                     rem.get("owner") or row.get("owner"),
                                                     rem.get("round") or row.get("round")))


if __name__ == "__main__":
    main()
