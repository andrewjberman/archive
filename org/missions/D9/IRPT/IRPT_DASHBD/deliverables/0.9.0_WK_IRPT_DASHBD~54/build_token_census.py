"""TO-DB-b-77: parse raw `comp-find -i --corpus all --all '<word-boundary regex>'` outputs into TOKEN_CENSUS.json.
Usage: python build_token_census.py <raw_dir> <out.json>   (raw_dir holds N.txt, one per token, and tokens.json = [{n, token, regex, why}])
hits = comp-find's own DENOMINATOR hit count minus the hits in this worker's own files (.scratch/ and its deliverables folder),
which exist only because the census ran; both numbers are recorded. files_scanned = comp-find's own scan denominator."""
import json
import re
import sys
from pathlib import Path

raw = Path(sys.argv[1])
toks = json.loads((raw / "tokens.json").read_text(encoding="utf-8"))
OWN = (".scratch/", "0.9.0_WK_IRPT_DASHBD~54/")
rows = []
for t in toks:
    txt = (raw / ("%d.txt" % t["n"])).read_text(encoding="utf-8", errors="replace")
    m = re.search(r"DENOMINATOR:\s*(\d+) hit\(s\) across (\d+) file\(s\) scanned in scope \[corpus=([a-z]+)\]", txt)
    if not m:
        raise SystemExit("REFUSED: no DENOMINATOR line in %s.txt" % t["n"])
    total, scanned, corpus = int(m.group(1)), int(m.group(2)), m.group(3)
    lines = re.findall(r"^\s{4}(\S+?):(\d+):", txt, re.M)
    if len(lines) != total:
        raise SystemExit("REFUSED: token %d lists %d hit lines, DENOMINATOR says %d (page cut?)" % (t["n"], len(lines), total))
    own = sum(1 for p, _ in lines if any(o in p.replace("\\", "/") for o in OWN))
    files = sorted({p for p, _ in lines if not any(o in p.replace("\\", "/") for o in OWN)})
    rows.append({"token": t["token"], "regex": t["regex"], "why": t["why"], "hits": total - own, "hits_reported_total": total,
                 "own_files_excluded": own, "files_with_hits": len(files), "files_scanned": scanned, "corpus": corpus,
                 "flags": "comp-find -i --corpus all --all"})
Path(sys.argv[2]).write_text(json.dumps({"record_version": "1.0", "task_order": "IRPT_DASHBD.TO-DB-b-77",
                                         "method": "word-boundary regex, case-insensitive, whole corpus (--corpus all), every hit listed (--all)",
                                         "census": rows}, indent=1) + "\n", encoding="utf-8")
print("OK: %d tokens" % len(rows))
