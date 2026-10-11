"""IRPT_YCDGEN round 11 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python r11_checks.py a11        the journey record: 26 rows by subtraction from the slug, value sets, real refs, 8 hops
    python r11_checks.py a11md      the readable record names every row and says what it could not establish
    python r11_checks.py e11        GENERATE_MAX_RECEIVES is 5 and the dead-letter record tests pass
    python r11_checks.py e11suite   the ycharts/generate tests: 0 failed, at least 503 passed

Prints one RESULT line: R11-<MODE>-OK or R11-<MODE>-FAIL <reason>; rc 0 only on OK. ASCII only.
"""
import json
import os
import re
import subprocess
import sys

P = "org/missions/D9/IRPT/IRPT_YCDGEN/"
OUT = P + "deliverables/0.9.0_WK_IRPT_YCDGEN~14/"
SLUG = P + "surprise-channel/remediations/REMEDIATION_v9.md"
GEN = "infra/aws/lambda/investor-reporting/ycharts/generate"
ID = re.compile(r"IRPT_YCDGEN-[A-Z0-9]+(?:-[A-Z0-9]+)*")


def slug_ids():
    return sorted(set(ID.findall(open(SLUG, encoding="utf-8").read())))


def main_checkout():
    out = subprocess.run(["git", "worktree", "list", "--porcelain"], capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.startswith("worktree "):
            return line[len("worktree "):].strip()
    return "."


def ref_ok(ref, main):
    if not isinstance(ref, dict) or not isinstance(ref.get("path"), str) or type(ref.get("line")) is not int:
        return False
    path = ref["path"].replace("\\", "/")
    if path.startswith("/") or ".." in path.split("/") or ":" in path:
        return False
    for base in (".", main):
        full = os.path.join(base, path)
        if os.path.isfile(full):
            with open(full, encoding="utf-8", errors="replace") as fh:
                return 1 <= ref["line"] <= sum(1 for _ in fh)
    return False


def pytest_line(target):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", target],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    lines = [ln for ln in (out.stdout + out.stderr).splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    return out.returncode, line, int(m.group(1)) if m else 0


def main(mode):
    if mode == "a11":
        want = slug_ids()
        try:
            doc = json.load(open(OUT + "JOURNEY_READ_YCD-a-11.json", encoding="utf-8"))
        except Exception as exc:
            print("R11-A11-FAIL %s: %s" % (type(exc).__name__, str(exc)[:160]))
            return 1
        main = main_checkout()
        rows = doc.get("rows") if isinstance(doc.get("rows"), list) else []
        hops = doc.get("hops") if isinstance(doc.get("hops"), list) else []
        ids = [r.get("id") for r in rows if isinstance(r, dict)]
        missing = sorted(set(want) - set(ids))
        extra = sorted(set(ids) - set(want))
        dup = sorted({i for i in ids if ids.count(i) > 1})
        bad = []
        for r in rows:
            if not isinstance(r, dict):
                bad.append("a row is not an object")
                continue
            i = r.get("id")
            ev = r.get("evidence") if isinstance(r.get("evidence"), list) else []
            if r.get("state") not in ("OPEN", "MET"):
                bad.append("%s state" % i)
            if r.get("on_path") not in ("YES", "NO", "NOT_DETERMINED"):
                bad.append("%s on_path" % i)
            if type(r.get("needs_live_read")) is not bool:
                bad.append("%s needs_live_read" % i)
            if not isinstance(r.get("note"), str) or not r["note"].strip():
                bad.append("%s note" % i)
            if r.get("state") == "MET" and (not ev or r.get("needs_live_read")):
                bad.append("%s MET without evidence, or MET beside needs_live_read" % i)
            if any(not ref_ok(e, main) for e in ev):
                bad.append("%s a ref is not a real file and line" % i)
        hop_bad = [str(h.get("n")) for h in hops if not isinstance(h, dict) or not h.get("name") or not h.get("finding")
                   or not isinstance(h.get("refs"), list) or not h["refs"] or any(not ref_ok(e, main) for e in h["refs"])]
        head_ok = all(isinstance(doc.get(k), str) and re.fullmatch(r"[0-9a-f]{40}", doc[k]) for k in ("head", "portal_head"))
        print("slug ids %d | rows %d | missing %d | extra %d | duplicate %d | hops %d" % (
            len(want), len(rows), len(missing), len(extra), len(dup), len(hops)))
        print("MET %d | OPEN %d | on path YES %d | needs a live read %d" % (
            sum(1 for r in rows if isinstance(r, dict) and r.get("state") == "MET"),
            sum(1 for r in rows if isinstance(r, dict) and r.get("state") == "OPEN"),
            sum(1 for r in rows if isinstance(r, dict) and r.get("on_path") == "YES"),
            sum(1 for r in rows if isinstance(r, dict) and r.get("needs_live_read") is True)))
        problems = (["missing " + ",".join(missing)] if missing else []) + (["extra " + ",".join(extra)] if extra else []) \
            + (["duplicate " + ",".join(dup)] if dup else []) + bad[:6] \
            + (["hops fewer than 8"] if len(hops) < 8 else []) + (["hop " + ",".join(hop_bad)] if hop_bad else []) \
            + ([] if head_ok else ["head or portal_head is not a 40-hex commit"])
        if problems:
            print("R11-A11-FAIL %s" % "; ".join(problems)[:600])
            return 1
        print("R11-A11-OK rows=%d hops=%d" % (len(rows), len(hops)))
        return 0
    if mode == "a11md":
        want = slug_ids()
        try:
            text = open(OUT + "JOURNEY_READ_YCD-a-11.md", encoding="utf-8").read()
        except Exception as exc:
            print("R11-A11MD-FAIL %s: %s" % (type(exc).__name__, str(exc)[:160]))
            return 1
        named = set(ID.findall(text))
        missing = sorted(set(want) - named)
        print("slug ids %d | named in the record %d | missing %d" % (len(want), len(set(want) & named), len(missing)))
        if missing or "What this read could not establish" not in text or any(ord(c) > 127 for c in text):
            print("R11-A11MD-FAIL %s" % ("missing " + ",".join(missing) if missing else "heading absent or non-ASCII text"))
            return 1
        print("R11-A11MD-OK named=%d" % len(want))
        return 0
    if mode == "e11":
        sys.path.insert(0, GEN)
        for rel in ("ycharts/extract", "ycharts/session", "reports", "_scope", "_ids", "_keys", "_authz", "intake", "ops"):
            sys.path.insert(0, "infra/aws/lambda/investor-reporting/" + rel)
        try:
            import resident_worker
            limit = getattr(resident_worker, "GENERATE_MAX_RECEIVES", None)
        except Exception as exc:
            print("R11-E11-FAIL import %s: %s" % (type(exc).__name__, str(exc)[:160]))
            return 1
        rc, line, passed = pytest_line(GEN + "/tests/test_dead_letter_record.py")
        print("GENERATE_MAX_RECEIVES = %r | %s" % (limit, line))
        if limit != 5 or type(limit) is not int or rc != 0 or "failed" in line or "error" in line or passed < 6:
            print("R11-E11-FAIL limit=%r rc=%d passed=%d (need limit 5, 0 failed, at least 6 passed)" % (limit, rc, passed))
            return 1
        print("R11-E11-OK limit=5 passed=%d" % passed)
        return 0
    if mode == "e11suite":
        rc, line, passed = pytest_line(GEN + "/tests")
        print(line)
        if rc != 0 or "failed" in line or "error" in line or passed < 503:
            print("R11-E11SUITE-FAIL rc=%d passed=%d (need >= 503, 0 failed, 0 errors)" % (rc, passed))
            return 1
        print("R11-E11SUITE-OK passed=%d" % passed)
        return 0
    raise SystemExit(__doc__)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
