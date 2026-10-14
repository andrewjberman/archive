#!/usr/bin/env python3
"""MDPF_CANON round 7 -- issuer checks for cell CN-k-1 (the two repairs: rows D1-S23 and D1-S24).

One subcommand per criterion; every arm prints one `ARM <name>: PASS|FAIL <detail>` line, then
`ROUND 7 CN-K-1 <NAME>: k of n arms`; exit 0 only when every arm passes. ASCII only. Terminates well under 120 s.
Read-only against AWS (S3 list/get only); every git repository it builds is a temp directory.

  tool   6 arms, the equality tool (.tools/mdpf-code-equality.py): a CRLF working file whose git blob equals the S3 object
         reads EQUAL by blob; a true difference stays DIFFER; a path with no index entry falls back to the working tree;
         the result carries each name's basis and the CR count; the same fact on the REAL S3 object of
         mdpf_model_registry.json; and the CLI controls (bronze_homes.json still DIFFER, three stable names still EQUAL).
         Every arm builds its own temp git repository, so the result does not depend on the checkout's line endings.
  card   5 arms, round7/checks/portfolios_card.py: `after` with no --date reads the newest account-distribution key; its
         FIRST line names the date and the exact key of each type; a newer distribution key than the date read is a WARN
         line; an explicit date is still honoured (control); and the same on the real objects.

  --tool <path>  --card <path>   the files under test (defaults: .tools/mdpf-code-equality.py and
                                 round7/checks/portfolios_card.py). The issuer's dry-run passes the scratch reference copies.
"""
import argparse
import contextlib
import datetime
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or os.getcwd()
DEFAULT_TOOL = os.path.join(ROOT, ".tools", "mdpf-code-equality.py")
DEFAULT_CARD = os.path.join(ROOT, "org", "missions", "D8", "MDPF", "MDPF_CANON", "deliverables", "2.0.0_SA_COO~D1",
                            "round7", "checks", "portfolios_card.py")
REGISTRY = "data/mdpf/scripts/gold/mdpf_model_registry.json"
STABLE = ["data/mdpf/scripts/gold/mdpf_revamp_model_crosswalk.py", "data/mdpf/scripts/gold/mdpf_calendar_binding.py",
          "data/mdpf/scripts/gold/taxsma_membership.py"]
BRONZE_HOMES = "data/mdpf/config/bronze_homes.json"
BUCKET = "opal-data-mdpf"


def md5(b):
    return hashlib.md5(b).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def clean_env():
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, "-c", "core.autocrlf=false", "-c", "user.name=t", "-c", "user.email=t@t"] + list(args),
                          capture_output=True, env=clean_env())


def make_repo(td, files):
    """A temp git repository holding `files` ({rel: bytes}) committed as given (no newline translation)."""
    git(td, "init", "-q")
    for rel, body in files.items():
        full = os.path.join(td, *rel.split("/"))
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as fh:
            fh.write(body)
        git(td, "add", rel)
    r = git(td, "commit", "-q", "-m", "x")
    if r.returncode != 0:
        raise RuntimeError("temp repo commit failed: %s" % r.stderr.decode("ascii", "replace")[:120])


def to_crlf(td, rel):
    full = os.path.join(td, *rel.split("/"))
    with open(full, "rb") as fh:
        body = fh.read()
    with open(full, "wb") as fh:
        fh.write(body.replace(b"\n", b"\r\n"))


class FakeS3Tool:
    def __init__(self, objs):
        self.objs = objs

    def get_paginator(self, _name):
        return self

    def paginate(self, Bucket, Prefix):
        yield {"Contents": [{"Key": k, "ETag": '"%s"' % v} for k, v in sorted(self.objs.items()) if k.startswith(Prefix)]}


def run_cli(tool, args):
    return subprocess.run([sys.executable, tool] + args, capture_output=True, text=True, cwd=ROOT, timeout=100)


# ---------------------------------------------------------------- tool

def arms_tool(tool):
    arms = []
    res = None
    try:
        mod = load(tool, "eq_under_test")
        with tempfile.TemporaryDirectory() as td:
            lf_a, lf_b = b"x\ny\n", b"p\n"
            make_repo(td, {"data/x/a.txt": lf_a, "data/x/b.txt": lf_b})
            to_crlf(td, "data/x/a.txt")
            with open(os.path.join(td, "data", "x", "c.txt"), "wb") as fh:  # untracked: no index entry
                fh.write(b"c\r\nc\r\n")
            mod.ROOT = td
            objs = {"p/a.txt": md5(lf_a), "p/b.txt": md5(b"q\n"), "p/c.txt": md5(b"c\r\nc\r\n")}
            res = mod.compare_tree(os.path.join(td, "data", "x"), "b", "p/", FakeS3Tool(objs))
    except Exception as exc:  # noqa: BLE001
        arms.append(("T-SETUP", False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))
    if res is not None:
        arms.append(("T1-BLOB-EQUAL", "a.txt" in res.get("equal", []) and "a.txt" not in res.get("differ", []),
                     "equal=%s differ=%s (CRLF working file, LF blob equal to S3)" % (res.get("equal"), res.get("differ"))))
        arms.append(("T2-TRUE-DIFFER", "b.txt" in res.get("differ", []) and "b.txt" not in res.get("equal", []),
                     "differ=%s" % res.get("differ")))
        arms.append(("T3-NO-INDEX-FALLBACK", "c.txt" in res.get("equal", []),
                     "equal=%s (untracked path read from the working tree)" % res.get("equal")))
        basis, cr = res.get("basis") or {}, res.get("worktree_cr") or {}
        ok4 = basis.get("a.txt") == "blob" and basis.get("c.txt") == "worktree" and cr.get("a.txt") == 2 and "c.txt" not in cr
        arms.append(("T4-BASIS-AND-CR", ok4, "basis=%s worktree_cr=%s" % (basis or "absent", cr or "absent")))
    # T5 the real S3 object of the registry file, in a temp repo whose working copy is CRLF
    try:
        mod = load(tool, "eq_under_test_real")
        import boto3
        s3 = boto3.client("s3", region_name="us-east-1")
        head = subprocess.run(["git", "show", "HEAD:" + REGISTRY], capture_output=True, cwd=ROOT, env=clean_env())
        etag = s3.head_object(Bucket=BUCKET, Key="code/scripts/gold/mdpf_model_registry.json")["ETag"].strip('"')
        if head.returncode != 0 or md5(head.stdout) != etag:
            arms.append(("T5-REAL-S3-BLOB", False, "premise changed: HEAD blob md5 %s vs S3 ETag %s" % (md5(head.stdout)[:10], etag[:10])))
        else:
            with tempfile.TemporaryDirectory() as td:
                make_repo(td, {REGISTRY: head.stdout})
                to_crlf(td, REGISTRY)
                mod.ROOT = td
                r = mod.compare_tree(os.path.join(td, *REGISTRY.split("/")[:-1]), BUCKET, "code/scripts/gold/", s3)
            name = REGISTRY.split("/")[-1]
            arms.append(("T5-REAL-S3-BLOB", name in r.get("equal", []),
                         "%s equal=%s differ=%s (CRLF copy, blob md5 %s = S3)" % (name, name in r.get("equal", []), name in r.get("differ", []), etag[:10])))
    except Exception as exc:  # noqa: BLE001
        arms.append(("T5-REAL-S3-BLOB", False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))
    # T6 CLI controls on the real trees
    try:
        r1 = run_cli(tool, ["--files", BRONZE_HOMES])
        r2 = run_cli(tool, ["--files"] + STABLE)
        ok = (r1.returncode == 1 and "NAMED NOT_EQUAL DIFFER" in r1.stdout and r2.returncode == 0
              and "named_not_equal 0" in r2.stdout)
        arms.append(("T6-CLI-CONTROLS", ok, "bronze_homes rc=%s (want 1, DIFFER); three stable names rc=%s (want 0, named_not_equal 0)"
                     % (r1.returncode, r2.returncode)))
    except Exception as exc:  # noqa: BLE001
        arms.append(("T6-CLI-CONTROLS", False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))
    return arms


# ---------------------------------------------------------------- card

class FakeS3Card:
    def __init__(self, objs):
        self.objs = objs  # {key: dict}

    def get_paginator(self, _name):
        return self

    def paginate(self, Bucket, Prefix):
        lm = datetime.datetime(2026, 10, 14, 13, 31, 0)
        yield {"Contents": [{"Key": k, "LastModified": lm} for k in sorted(self.objs) if k.startswith(Prefix)]}

    def get_object(self, Bucket, Key):
        return {"Body": io.BytesIO(json.dumps(self.objs[Key]).encode("ascii"))}


def fake_card_objects():
    base = "portal/gold/mdpf/global/"
    am = {"total": {"aum": 100.0, "account_count": 5},
          "by_model": [{"model_name": "Short Term", "aum": 100.0, "account_count": 3, "q0": {}, "q1": {}, "q2": {}, "q3": {}}]}
    ts = {"dates": ["2026-10-12", "2026-10-13"], "by_model": {"Short Term": {"model_value": [1.0, 2.0], "cohort_class": "model"}}}
    objs = {}
    for d in ("2026-10-12", "2026-10-13"):
        objs[base + "aum-metrics/%s.json" % d] = am
        objs[base + "aggregate-aua-timeseries/%s.json" % d] = ts
    objs[base + "account-distribution/2026-10-13.json"] = {"total": {"account_count": 8422}, "by_model": {}}
    objs[base + "account-distribution/2026-10-14.json"] = {"total": {"account_count": 8430}, "by_model": {}}
    return objs


def card_run(mod, client, argv):
    """Run the card's main(argv) with the given client; returns (stdout lines, exit code or 'exit N')."""
    buf = io.StringIO()
    code = None
    mod.s3 = lambda: client
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            try:
                code = mod.main(argv)
            except TypeError:  # a main() that takes no argv list reads sys.argv
                saved, sys.argv = sys.argv, ["portfolios_card.py"] + list(argv)
                try:
                    code = mod.main()
                finally:
                    sys.argv = saved
    except SystemExit as exc:
        code = "exit %s" % (exc.code,)
    except Exception as exc:  # noqa: BLE001 -- e.g. main() that takes no argv list
        code = "%s: %s" % (type(exc).__name__, str(exc)[:80])
    return buf.getvalue().splitlines(), code


def arms_card(card):
    arms = []
    try:
        mod = load(card, "card_under_test")
        client = FakeS3Card(fake_card_objects())
    except Exception as exc:  # noqa: BLE001
        return [("C-SETUP", False, "%s: %s" % (type(exc).__name__, str(exc)[:160]))]
    dist = "account-distribution/2026-10-14.json"
    out, code = card_run(mod, client, ["after", "--before-date", "2026-10-13"])
    first = out[0] if out else ""
    arms.append(("C1-DEFAULT-DATE", code == 0 and "date=2026-10-14" in first and dist in first, "code=%s first=%r" % (code, first[:150])))
    out, code = card_run(mod, client, ["after", "--date", "2026-10-14", "--before-date", "2026-10-13"])
    first = out[0] if out else ""
    want = [dist, "aum-metrics/2026-10-13.json", "aggregate-aua-timeseries/2026-10-13.json"]
    arms.append(("C2-FIRST-LINE-KEYS", code == 0 and first.startswith("PORTFOLIOS-CARD READ") and all(w in first for w in want),
                 "code=%s first=%r" % (code, first[:150])))
    out, code = card_run(mod, client, ["after", "--date", "2026-10-13", "--before-date", "2026-10-13"])
    warn = [ln for ln in out if ln.startswith("WARN:") and "2026-10-14.json" in ln]
    arms.append(("C3-NEWER-KEY-WARN", code == 0 and len(warn) == 1 and "date=2026-10-13" in (out[0] if out else ""),
                 "code=%s warn_lines=%d first=%r" % (code, len(warn), (out[0] if out else "")[:100])))
    text = "\n".join(out)
    arms.append(("C4-EXPLICIT-HONOURED", code == 0 and "Total Holdings headline: 8422" in text,
                 "explicit --date 2026-10-13 reads the 2026-10-13 distribution (total 8422), code=%s: %s" % (code, "Total Holdings headline: 8422" in text)))
    # C5 the real objects: the default date is the newest real account-distribution key
    try:
        import boto3
        c = boto3.client("s3", region_name="us-east-1")
        keys = []
        for pg in c.get_paginator("list_objects_v2").paginate(Bucket="opal-data-assets", Prefix="portal/gold/mdpf/global/account-distribution/"):
            keys += [o["Key"] for o in pg.get("Contents", []) if o["Key"].endswith(".json")]
        newest = sorted(keys)[-1].split("/")[-1][:-5]
        mod2 = load(card, "card_under_test_real")
        out, code = card_run(mod2, c, ["after", "--before-date", "2026-10-13"])
        first = out[0] if out else ""
        arms.append(("C5-REAL-DEFAULT", code == 0 and ("date=%s" % newest) in first and ("account-distribution/%s.json" % newest) in first,
                     "newest real distribution key %s; code=%s first=%r" % (newest, code, first[:150])))
    except Exception as exc:  # noqa: BLE001
        arms.append(("C5-REAL-DEFAULT", False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))
    return arms


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("tool", "card"))
    ap.add_argument("--tool", default=DEFAULT_TOOL)
    ap.add_argument("--card", default=DEFAULT_CARD)
    a = ap.parse_args(argv)
    arms = arms_tool(a.tool) if a.cmd == "tool" else arms_card(a.card)
    for name, ok, detail in arms:
        print("ARM %s: %s %s" % (name, "PASS" if ok else "FAIL", detail))
    n_ok = sum(1 for _n, ok, _d in arms if ok)
    print("ROUND 7 CN-K-1 %s: %d of %d arms" % (a.cmd.upper(), n_ok, len(arms)))
    return 0 if n_ok == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
