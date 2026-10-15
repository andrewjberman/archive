"""CA-k-3 (round 19): the batch repair cell -- stale test assertions and two cosmetic reader texts, NO behaviour change.

Prints:  L3-BATCH ok=<True|False> arms=<k> of <n>      then one line per failed arm:  FAIL <arm>: <reason>
Run from the ROOT OF THE CHECKOUT UNDER TEST by relative path. Everything is read from `git rev-parse --show-toplevel` of the
current directory (never from this file's own location), so a worker's worktree is what is graded, not the trunk.
Arms:
  mail_cases       test_inbound_mail.py prints ok=True with every case passing (the four party-registry cases pass)
  mail_draft_arms  test_inbound_mail_draft.py prints ok=True with every arm passing (the stale text-tail assertion)
  natural_alone    pytest test_teams_chat_natural.py ALONE from the repo root collects and passes (no bare sibling import)
  natural_in_set   pytest test_teams_chat_tenant.py + test_teams_chat_natural.py in one run passes (the repair breaks nothing)
  help_sources     refresh.py --help names every source in refresh.SOURCES and does not say "four"
  scan_log_truth   reading mentions / mail_log through refresh.py logs the source actually read, never "READ drafts"
  refresh_same     refresh.py writes byte-identical folders to its text at the base (merge-base with the trunk) on a fixed stub
  no_product_change nothing under data/, infra/ or .tools/ changed against the base except the four allowed files
The base is `git merge-base HEAD <trunk>` (trunk = L3_TRUNK, default box/laptop, then CLOUD); in the trunk checkout itself the base is
HEAD, so refresh_same and no_product_change pass trivially there and bite in a worker's worktree. L3_BASE overrides the base.
"""
import contextlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile

REFRESH = "data/transcripts/scripts/muse_reader/refresh.py"
TESTS = "data/transcripts/scripts/tests/"
ALLOWED = {TESTS + "test_inbound_mail.py", TESTS + "test_inbound_mail_draft.py", TESTS + "test_teams_chat_natural.py", REFRESH}
WATCHED = ("data/", "infra/", ".tools/")
NOW = "2026-10-14T20:00:00Z"


def sh(args, cwd, timeout=240):
    r = subprocess.run(args, cwd=cwd, capture_output=True, timeout=timeout)
    return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")


def toplevel():
    rc, out, err = sh(["git", "rev-parse", "--show-toplevel"], os.getcwd())
    if rc != 0:
        raise SystemExit("L3-BATCH ok=False arms=0 of 8\nFAIL setup: not inside a git checkout (%s)" % err.strip()[:120])
    return out.strip()


def base_ref(root):
    if os.environ.get("L3_BASE"):
        return os.environ["L3_BASE"]
    for trunk in (os.environ.get("L3_TRUNK") or "box/laptop", "CLOUD"):
        rc, out, _ = sh(["git", "merge-base", "HEAD", trunk], root)
        if rc == 0 and out.strip():
            return out.strip()
    return "HEAD"


def last_line(text, prefix):
    for line in reversed(text.splitlines()):
        if line.startswith(prefix):
            return line
    return ""


def arm_mail_cases(root, base):
    rc, out, _ = sh([sys.executable, TESTS + "test_inbound_mail.py"], root)
    line = last_line(out, "INBOUND-MAIL-TEST")
    m = re.search(r"ok=True cases=(\d+)/(\d+)", line)
    if m and m.group(1) == m.group(2) and int(m.group(2)) >= 15:
        return None
    return "test_inbound_mail.py printed: %s" % (line or out.strip()[-160:])


def arm_mail_draft(root, base):
    rc, out, _ = sh([sys.executable, TESTS + "test_inbound_mail_draft.py"], root)
    line = last_line(out, "MAIL-DRAFT")
    m = re.search(r"ok=True arms=(\d+)/(\d+)", line)
    if m and m.group(1) == m.group(2) and int(m.group(2)) >= 12:
        return None
    return "test_inbound_mail_draft.py printed: %s (failed: %s)" % (
        line or out.strip()[-160:], ",".join(ln.split()[1].rstrip(":") for ln in out.splitlines() if ln.startswith("FAIL ")))


def pytest_run(root, files):
    rc, out, err = sh([sys.executable, "-m", "pytest"] + files + ["-q", "--color=no", "-p", "no:cacheprovider"], root, 300)
    tail = (out.strip().splitlines() or [""])[-1]
    passed = re.search(r"(\d+) passed", tail)
    bad = re.search(r"(\d+) (failed|error)", tail) or "error" in tail
    return rc == 0 and passed and not bad, tail[:140]


def arm_natural_alone(root, base):
    ok, tail = pytest_run(root, [TESTS + "test_teams_chat_natural.py"])
    return None if ok else "pytest alone from the repo root: %s" % tail


def arm_natural_in_set(root, base):
    ok, tail = pytest_run(root, [TESTS + "test_teams_chat_tenant.py", TESTS + "test_teams_chat_natural.py"])
    return None if ok else "pytest tenant + natural in one run: %s" % tail


def load_module(name, path, source=None):
    path = str(path)
    if source is None:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    import types
    mod = types.ModuleType(name)
    mod.__file__ = path
    exec(compile(source, path, "exec"), mod.__dict__)  # noqa: S102 -- the base's own text, read with git show
    return mod


STUB_ROWS = [
    ("19:chat-one", {"title": "Pat Invented", "pending": {"tag": "C101", "kind": "chat", "version": 2, "seq": 4, "status": "texted",
                                                          "texted_at": "2026-10-14T19:30:00Z", "draft": "Sounds good", "chat_title": "Pat Invented"}}),
    ("mail:owner", {"kind": "mail", "mail_log": [
        {"seq": 3, "tag": "M201", "considered_at": "2026-10-14T19:40:00Z", "from": "Pat Invented", "domain": "example-fund.test",
         "firm": "invented-firm", "subject": "export"}]}),
    ("19:chat-two@thread.v2", {"mentions": [
        {"id": "t|c|m1", "team": "Team", "channel": "General", "from": "Sam Invented", "snippet": "please look",
         "mentioned_at": "2026-10-14T19:50:00Z", "seen_at": "2026-10-14T19:50:30Z"}]}),
]


def stub_aws(args):
    if "scan" in args:
        items = [{"pk": {"S": pk}, "sk": {"S": "state"}, "data": {"S": json.dumps(st)}} for pk, st in STUB_ROWS]
        return json.dumps({"Items": items, "ScannedCount": len(items)})
    return ""     # get-item of an absent eod row prints nothing


def run_refresh(mod):
    """(files of the folder as bytes, stdout) for one fixed stubbed refresh run of `mod`."""
    import datetime
    mod.aws_json = stub_aws
    now_dt = datetime.datetime(2026, 10, 14, 20, 0, 0, tzinfo=datetime.timezone.utc)
    readers = mod.make_readers(now_dt)
    readers["open_calls"] = lambda: [{"call": "stub"}]
    readers["sprint_today"] = lambda: [{"key": "stub", "size": 1, "last_modified": "2026-10-14T19:00:00Z"}]
    with tempfile.TemporaryDirectory(prefix="l3_refresh_") as td, contextlib.redirect_stdout(io.StringIO()) as out:
        mod.refresh(td, readers, NOW)
        files = {n: open(os.path.join(td, n), "rb").read() for n in sorted(os.listdir(td))}
    return files, out.getvalue()


def arm_help(root, base):
    mod = load_module("l3_refresh_help", os.path.join(root, REFRESH))
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            mod.main(["--help"])
        except SystemExit:
            pass
    text = buf.getvalue()
    missing = [s for s in mod.SOURCES if s not in text]
    if re.search(r"\bfour\b", text, re.I):
        return "the help text still says 'four': %s" % " ".join(text.split())[-160:]
    if missing:
        return "the help text does not name %s" % ",".join(missing)
    return None


def arm_scan_log(root, base):
    mod = load_module("l3_refresh_log", os.path.join(root, REFRESH))
    mod.aws_json = stub_aws
    import datetime
    readers = mod.make_readers(datetime.datetime(2026, 10, 14, 20, 0, 0, tzinfo=datetime.timezone.utc))
    for name in ("mentions", "mail_log"):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            readers[name]()
        lines = out.getvalue().splitlines()
        if any(ln.startswith("READ drafts") for ln in lines):
            return "reading %s logged a 'READ drafts' line: %s" % (name, lines[0][:100])
        if not any(("READ " + name) in ln or name in ln for ln in lines):
            return "reading %s logged no line naming %s: %s" % (name, name, lines[:2])
    with contextlib.redirect_stdout(io.StringIO()) as out:
        readers["drafts"]()
    if not any(ln.startswith("READ drafts") for ln in out.getvalue().splitlines()):
        return "reading drafts no longer logs a 'READ drafts' line"
    return None


def arm_refresh_same(root, base):
    rc, src, err = sh(["git", "show", "%s:%s" % (base, REFRESH)], root)
    if rc != 0:
        return "git show %s:%s failed: %s" % (base, REFRESH, err.strip()[:100])
    before = load_module("l3_refresh_base", os.path.join(root, REFRESH), source=src.replace("\r\n", "\n"))
    after = load_module("l3_refresh_cur", os.path.join(root, REFRESH))
    f0, _ = run_refresh(before)
    f1, _ = run_refresh(after)
    diff = sorted(n for n in set(f0) | set(f1) if f0.get(n) != f1.get(n))
    return None if not diff and len(f0) >= 8 else "folder differs from the base's in %s (files=%d)" % (",".join(diff) or "(none)", len(f0))


def arm_no_product_change(root, base):
    rc, out, err = sh(["git", "diff", "--name-only", base], root)       # the base against the working tree: committed + uncommitted
    if rc != 0:
        return "git diff failed: %s" % err.strip()[:100]
    changed = {p.strip() for p in out.splitlines() if p.strip()}     # tracked paths only: a worker commits what it adds
    stray = sorted(p for p in changed if p.startswith(WATCHED) and p not in ALLOWED and "__pycache__" not in p)
    return None if not stray else "files changed outside the four allowed: %s" % ", ".join(stray[:6])


ARMS = [("mail_cases", arm_mail_cases), ("mail_draft_arms", arm_mail_draft), ("natural_alone", arm_natural_alone),
        ("natural_in_set", arm_natural_in_set), ("help_sources", arm_help), ("scan_log_truth", arm_scan_log),
        ("refresh_same", arm_refresh_same), ("no_product_change", arm_no_product_change)]


def main():
    root = toplevel()
    base = base_ref(root)
    fails = []
    for name, fn in ARMS:
        try:
            why = fn(root, base)
        except Exception as exc:  # noqa: BLE001 -- an arm that cannot run is a failed arm, never a pass
            why = "%s: %s" % (type(exc).__name__, str(exc)[:160])
        if why:
            fails.append((name, why))
    print("L3-BATCH ok=%s arms=%d of %d" % (not fails, len(ARMS) - len(fails), len(ARMS)))
    for name, why in fails:
        print("FAIL %s: %s" % (name, why))
    return 0


if __name__ == "__main__":
    sys.exit(main())
