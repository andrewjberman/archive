"""A BUNDLE SMOKE built from the PINNED blobs of a source-map entry (issuer 2.0.0_SA_COO~F2, round 137; the lesson of the 49 Financial apply's STOP at Act 3).

The Lambda artifact packages each `staged_from` member as `git show <pin>:<repo_path>` at its `packaged_as` path, plus the entry's `source_dir` files. This tool lays that
exact content out in a fresh temporary directory (a stand-in for /var/task; pandas and pyarrow come from the interpreter, the stand-in for the native layer) and runs a
short program against it from ANOTHER directory under `python -I`. A stale pin, a missing member or a missing attribute fails HERE, not at the applier's dry run.

Usage: python <this file> <repo_root> <entry_name> <code-file>      prints the program's output and "SMOKE PASS" or "SMOKE FAIL" last
       python <this file> --selftest
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SOURCE_MAP = "infra/aws/lambda/ci/lambda-source-map.json"


def build_dir(root, entry_name, dest):
    """Write the entry's pinned members and its source_dir handler into dest; return the list of packaged paths."""
    doc = json.loads(Path(root, SOURCE_MAP).read_text(encoding="utf-8"))
    entry = doc["functions"][entry_name]
    written = []
    for s in entry.get("staged_from", []):
        r = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (s["pin"], s["repo_path"])], capture_output=True, timeout=120)
        if r.returncode != 0:
            raise SystemExit("the pinned blob of %s at %s cannot be read" % (s["repo_path"], s["pin"][:10]))
        t = Path(dest, s["packaged_as"])
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_bytes(r.stdout)
        written.append(s["packaged_as"])
    src_dir = Path(root, entry["source_dir"])
    for name in entry.get("files", []):
        if name in written:
            continue
        f = src_dir / name
        if f.is_file():
            t = Path(dest, name)
            t.parent.mkdir(parents=True, exist_ok=True)
            t.write_bytes(f.read_bytes())
            written.append(name)
    return written


def smoke(root, entry_name, code):
    with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as other:
        bundle = Path(td, "var_task")
        bundle.mkdir()
        written = build_dir(root, entry_name, bundle)
        prog = "import sys\nsys.path.insert(0, %r)\n%s\n" % (str(bundle), code)
        r = subprocess.run([sys.executable, "-I", "-c", prog], capture_output=True, text=True, timeout=300, cwd=other)
        return r.returncode, (r.stdout or "") + (r.stderr or ""), written


def selftest():
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "infra/aws/lambda/ci").mkdir(parents=True)
        (Path(td) / "infra/aws/lambda/ci/lambda-source-map.json").write_text(json.dumps({"functions": {"e": {"source_dir": "src", "files": ["handler.py"], "staged_from": []}}}), encoding="utf-8")
        (Path(td) / "src").mkdir()
        (Path(td) / "src/handler.py").write_text("X = 1\n", encoding="utf-8")
        rc, out, written = smoke(td, "e", "import handler\nprint(handler.X)")
        ok = rc == 0 and out.strip() == "1" and written == ["handler.py"]
        rc2, out2, _w = smoke(td, "e", "import handler\nprint(handler.Y)")
    print("selftest %s" % ("PASS (2 arms)" if ok and rc2 != 0 and "AttributeError" in out2 else "FAIL"))
    return 0 if ok and rc2 != 0 else 1


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 4:
        print(__doc__)
        return 2
    root, entry, codefile = argv[1], argv[2], argv[3]
    rc, out, written = smoke(root, entry, Path(codefile).read_text(encoding="utf-8"))
    print(out.rstrip())
    print("members laid out: %d" % len(written))
    print("SMOKE %s" % ("PASS" if rc == 0 else "FAIL"))
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
