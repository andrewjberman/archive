"""HVST-z-3 AC3 -- census over lib/ of dotted-string patch targets, with a resolution verdict per occurrence.

Pattern (multi-line safe, single or double quotes): patch("lib.  patch.dict("lib.  monkeypatch.setattr("lib.
Also printed: every OTHER dotted-string patch/setattr target under lib/ (any prefix), so "0 that miss" is read
against the whole population and not only the `lib.` prefix.  A POSITIVE CONTROL runs the same census over the
five files as they stood at the cut (2c3e657865, before this cell's edit): it must read 8, or the census is blind.
In-process; no network, no S3, no vendor call.
"""
import importlib
import os
import re
import subprocess
import sys

ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
os.chdir(ROOT)
sys.path.insert(0, ROOT)
CUT = "2c3e657865"
LIB_PAT = re.compile(r"""(?P<call>\bpatch\.dict|\bpatch|\bmonkeypatch\.setattr)\(\s*[rbf]?(?P<q>["'])(?P<target>lib\.[\w\.]+)(?P=q)""")
ANY_PAT = re.compile(r"""(?P<call>\bpatch\.dict|\bpatch|\bmonkeypatch\.setattr|\bsetattr)\(\s*[rbf]?(?P<q>["'])(?P<target>[A-Za-z_][\w]*\.[\w\.]+)(?P=q)""")
TOUCHED = ["lib/research/posture/tests/test_posture.py", "lib/research/api/tests/test_scoped_amgt.py",
           "lib/opal_data_harvest/test_retrieval_provenance.py", "lib/opal_data_harvest/test_verification.py",
           "lib/opal_data_harvest/test_worker.py"]


def census(texts, pat):
    hits = []
    for path, text in texts:
        for m in pat.finditer(text):
            hits.append((path, text.count("\n", 0, m.start()) + 1, m.group("call"), m.group("target")))
    return hits


def read_lib():
    out = []
    for d, _, fs in os.walk("lib"):
        for f in fs:
            if f.endswith(".py"):
                p = os.path.join(d, f).replace("\\", "/")
                out.append((p, open(p, encoding="utf-8", errors="replace").read()))
    return out


def resolve(target):
    """Import the longest module prefix, walk the rest by getattr; return (module, owner_object) or an error."""
    parts = target.split(".")
    for i in range(len(parts) - 1, 0, -1):
        try:
            mod = importlib.import_module(".".join(parts[:i]))
        except ImportError:
            continue
        obj = mod
        for p in parts[i:-1]:
            obj = getattr(obj, p)
        return mod, obj
    raise ImportError(target)


def main():
    texts = read_lib()
    print("SCANNED: %d .py files under lib/ (denominator)" % len(texts))
    hits = census(texts, LIB_PAT)
    print("\nCENSUS  patch(\"lib.  patch.dict(\"lib.  monkeypatch.setattr(\"lib.  -> %d occurrence(s)" % len(hits))
    for path, line, call, target in hits:
        print("  %s:%d  %s(%r)" % (path, line, call, target))
    misses = 0
    for path, line, call, target in hits:
        try:
            mod, owner = resolve(target)
            print("  VERDICT %s:%d resolves to %s (module %s); same-object-as-code-under-test UNPROVEN by this census -> counted MISS" % (path, line, id(owner), mod.__name__))
        except ImportError:
            print("  VERDICT %s:%d does not import -> MISS" % (path, line))
        misses += 1
    print("  occurrences that MISS: %d of %d" % (misses, len(hits)))

    print("\nRELATED POPULATION -- every dotted-string patch/setattr target of ANY prefix under lib/ (so 0 is read against the whole):")
    other = [h for h in census(texts, ANY_PAT) if not h[3].startswith("lib.")]
    for path, line, call, target in other:
        top = target.split(".")[0]
        mod, owner = resolve(target)
        copies = [k for k, v in list(sys.modules.items()) if getattr(v, "__name__", None) == top and k != top]
        print("  %s:%d  %s(%r) -> owner module %r; copies of module %r under another sys.modules key: %d ; VERDICT: %s"
              % (path, line, call, target, mod.__name__, top, len(copies),
                 "RESOLVES to the one module object every importer of %r gets (third-party, single canonical name)" % top if not copies else "SPLIT"))
    print("  related occurrences: %d (none with a lib. prefix; none can split -- a third-party package has one import name)" % len(other))

    print("\nPOSITIVE CONTROL -- the same census over the five touched files AS AT THE CUT %s (before this cell's edit):" % CUT)
    old = []
    for p in TOUCHED:
        old.append((p, subprocess.check_output(["git", "show", "%s:%s" % (CUT, p)]).decode("utf-8")))
    ctl = census(old, LIB_PAT)
    for path, line, call, target in ctl:
        print("  %s:%d  %s(%r)" % (path, line, call, target))
    print("  control reads %d (expected 8: posture 4, scoped_amgt 1, retrieval_provenance 1, verification 1, worker 1)" % len(ctl))
    now = census([(p, t) for p, t in texts if p in TOUCHED], LIB_PAT)
    print("  the same five files NOW read %d" % len(now))

    print("\nAC3 SUMMARY: scanned %d files; %d dotted-string 'lib.' patch targets remain under lib/; %d MISS; control instrument reads %d/8"
          % (len(texts), len(hits), misses, len(ctl)))
    sys.exit(0 if (misses == 0 and len(ctl) == 8) else 1)


if __name__ == "__main__":
    main()
