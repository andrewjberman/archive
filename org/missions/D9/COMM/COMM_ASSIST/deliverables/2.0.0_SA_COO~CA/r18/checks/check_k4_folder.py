"""CA-j-15 AC1 (run ON dell2, from the repository root of its checkout): the muse reader folder now carries the two new sources, mentions.json and mail_log.json, and is clean.

Prints:  K4-FOLDER ok=<True|False> arms=<n> of 6 failed=<names|none> sources=<n> mentions=<status|missing> mail_log=<status|missing> run_age_min=<n|none> files=<n> reason=<text>
Usage: python check_k4_folder.py [folder]   (default: %USERPROFILE%\\muse-reader)
Reads the folder's files only. Arms: index (INDEX.json lists exactly six sources incl. mentions and mail_log), files (both files exist, are valid envelopes, status ok or absent: an `unreadable` is a FAIL, and
an absent source has null items), fresh (INDEX run_at is within 20 minutes of now: the job ran the new code), shape (an ok source's items have exactly the contracted keys), readme (README.txt names both files),
clean (no address, key or token shaped string in ANY file of the folder: FWD-11). The contracted keys: mentions = id, team, channel, from, snippet, mentioned_at, seen_at, age_minutes, age_from; mail_log =
seq, tag, considered_at, from, domain, firm, subject, object_id, age_minutes, age_from.
"""
import datetime
import json
import re
import sys
from pathlib import Path

MENT = {"id", "team", "channel", "from", "snippet", "mentioned_at", "seen_at", "age_minutes", "age_from"}
MAIL = {"seq", "tag", "considered_at", "from", "domain", "firm", "subject", "object_id", "age_minutes", "age_from"}
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+")
SECRETS = (re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"), re.compile(r"-----BEGIN [A-Z ]*(?:KEY|CERTIFICATE)"), re.compile(r"(?i)bearer\s+[a-z0-9._~+/=-]{20,}"),
           re.compile(r"\beyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{10,}"), re.compile(r"(?i)(?:secret|token|password|passwd|api[_-]?key)[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9/+_=.-]{8,}"))
ARMS = ("index", "files", "fresh", "shape", "readme", "clean")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "muse-reader"
    got, why, docs, nfiles = {}, "", {}, 0
    n_sources, run_age = 0, None
    try:
        idx = load(folder / "INDEX.json")
        srcs = idx.get("sources") or {}
        n_sources = len(srcs)
        got["index"] = n_sources == 6 and "mentions" in srcs and "mail_log" in srcs
        ok_files = True
        for name in ("mentions", "mail_log"):
            p = folder / (name + ".json")
            if not p.is_file():
                ok_files = False
                continue
            d = load(p)
            docs[name] = d
            if d.get("source") != name or d.get("status") not in ("ok", "absent") or (d.get("status") == "absent" and d.get("items") is not None) \
                    or (d.get("status") == "ok" and not isinstance(d.get("items"), list)):
                ok_files = False
        got["files"] = ok_files
        run_at = datetime.datetime.strptime(idx.get("run_at"), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
        run_age = int((datetime.datetime.now(datetime.timezone.utc) - run_at).total_seconds() // 60)
        got["fresh"] = 0 <= run_age <= 20
        shape = True
        for name, keys in (("mentions", MENT), ("mail_log", MAIL)):
            d = docs.get(name)
            if d and d.get("status") == "ok":
                shape &= all(isinstance(i, dict) and set(i) == keys for i in d["items"])
        got["shape"] = bool(docs) and shape
        readme = (folder / "README.txt").read_text(encoding="utf-8")
        got["readme"] = "mentions.json" in readme and "mail_log.json" in readme
        hits = 0
        for f in folder.rglob("*"):
            if f.is_file():
                nfiles += 1
                text = f.read_text(encoding="utf-8", errors="replace")
                hits += len([m for m in EMAIL.findall(text) if "withheld" not in m]) + sum(len(rx.findall(text)) for rx in SECRETS)
        got["clean"] = hits == 0
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
    failed = [a for a in ARMS if not got.get(a)]
    print("K4-FOLDER ok=%s arms=%d of %d failed=%s sources=%d mentions=%s mail_log=%s run_age_min=%s files=%d reason=%s"
          % (not why and not failed, len(ARMS) - len(failed), len(ARMS), ",".join(failed) or "none", n_sources,
             (docs.get("mentions") or {}).get("status", "missing"), (docs.get("mail_log") or {}).get("status", "missing"),
             run_age if run_age is not None else "none", nfiles, why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
