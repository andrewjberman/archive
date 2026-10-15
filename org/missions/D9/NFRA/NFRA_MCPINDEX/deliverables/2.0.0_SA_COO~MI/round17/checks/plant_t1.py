"""plant_t1.py -- the ISSUER's cut-time planted arms for t1.AC1 to AC3 (standing battery clause 1). NOT given to the worker, NOT a criterion. Run from the repo root.

Writes a reference derive module and a GOOD catalog (the base with the 44 empty rows tagged by it and marked inferred) and five BAD ones, then runs t1_check with
T1_CATALOG / T1_DERIVE set and compares every exit code with the wanted one."""
import copy
import os
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import t1_check as tc  # noqa: E402

REF = '''import re

STOP = set("a an the of in for to and or is are was were on at by with from as it its this that these those be been what which who how where when why "
           "table data row rows one per each all any not no your you we our can will may must so than then into out up down over under".split())


def _words(text):
    return re.findall(r"[a-z0-9]+", str(text).lower())


def derive_tags(entity, business_meaning, example_questions):
    ent = [w for w in _words(entity) if w not in STOP]
    tags = []
    if len(ent) >= 2:
        tags.append(" ".join(ent[:4]))
    for q in list(example_questions or [])[:2]:
        ws = [w for w in _words(q) if w not in STOP]
        if len(ws) >= 2:
            tags.append(" ".join(ws[:4]))
    ws = [w for w in _words(business_meaning) if w not in STOP]
    for i in range(0, min(len(ws), 12) - 1, 3):
        tags.append(" ".join(ws[i:i + 3]))
    out = []
    for t in tags:
        if t not in out and 2 <= len(t.split()) <= 5:
            out.append(t)
    return out[:5] if len(out) >= 3 else (out + ["catalog row " + (ent[0] if ent else "data"), "opal data catalog", "row description"])[:3]
'''


def main():
    tmp = tempfile.mkdtemp(prefix="plant_t1_")
    ref = os.path.join(tmp, "ref_derive.py")
    open(ref, "w", encoding="ascii").write(REF)
    import importlib.util
    spec = importlib.util.spec_from_file_location("ref_derive", ref)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # the base catalog, loaded through the check's own helper
    cat = tc.base_catalog()

    def all_rows(c):
        return [r for sec in tc.SECTIONS for r in (c.get(sec) or []) if isinstance(r, dict)]

    def tag_empty(c, skip=None, bad_word=None, no_basis=None):
        for r in all_rows(c):
            if r.get("nl_tags"):
                continue
            if skip and r["entity"] == skip:
                continue
            meaning = r.get("business_meaning") or ""
            t = mod.derive_tags(r["entity"], meaning, r.get("example_questions") or [])
            if bad_word and r["entity"] == bad_word:
                t = t[:-1] + ["zzzz outsideword"]
            r["nl_tags"] = t
            if not (no_basis and r["entity"] == no_basis):
                r["nl_tags_basis"] = "inferred"
        return c

    empties = [r["entity"] for r in all_rows(cat) if not r.get("nl_tags")]
    first = empties[0]
    good = tag_empty(copy.deepcopy(cat))
    one_empty = tag_empty(copy.deepcopy(cat), skip=first)
    altered = tag_empty(copy.deepcopy(cat))
    tagged = [r for r in all_rows(altered) if r.get("nl_tags") and r.get("nl_tags_basis") != "inferred"][0]
    tagged["nl_tags"] = list(tagged["nl_tags"]) + ["a tag the contract never gave"]
    outside = tag_empty(copy.deepcopy(cat), bad_word=first)
    nobasis = tag_empty(copy.deepcopy(cat), no_basis=first)

    def dump(c, name):
        p = os.path.join(tmp, name)
        with open(p, "w", encoding="ascii", newline="\n") as fh:
            yaml.safe_dump(c, fh, sort_keys=False, allow_unicode=False)
        return p

    P = {k: dump(v, k + ".yaml") for k, v in (("good", good), ("one_empty", one_empty), ("altered", altered), ("outside", outside), ("nobasis", nobasis))}
    rnd = os.path.join(tmp, "random_derive.py")
    open(rnd, "w", encoding="ascii").write(REF.replace("def derive_tags(entity, business_meaning, example_questions):",
                                                      "import random\n\n\ndef derive_tags(entity, business_meaning, example_questions):\n    random.seed()\n    if random.random() < 2:\n        return _derive_inner(entity, business_meaning, example_questions)[::-1 if random.random() < 0.5 else 1]\n\n\ndef _derive_inner(entity, business_meaning, example_questions):"))
    arms = [("good catalog + reference derive, ac1", "good", ref, "ac1", 0), ("good catalog + reference derive, ac2", "good", ref, "ac2", 0),
            ("good catalog + reference derive, ac3", "good", ref, "ac3", 0),
            ("base catalog (nothing tagged), ac1", None, ref, "ac1", 1), ("base catalog (nothing tagged), ac2", None, ref, "ac2", 1),
            ("one empty row left, ac1", "one_empty", ref, "ac1", 1), ("one empty row left, ac2", "one_empty", ref, "ac2", 1),
            ("a contract-tagged row altered, ac2", "altered", ref, "ac2", 1), ("a derived tag with an outside word, ac3", "outside", ref, "ac3", 1),
            ("an inferred row without the basis mark, ac2", "nobasis", ref, "ac2", 1), ("a non-deterministic derive module, ac3", "good", rnd, "ac3", 1)]
    ok = wrong = 0
    for label, key, dv, ac, want in arms:
        env = dict(os.environ, T1_DERIVE=dv)
        if key:
            env["T1_CATALOG"] = P[key]
        r = subprocess.run([sys.executable, os.path.join(HERE, "t1_check.py"), ac], env=env, capture_output=True, text=True)
        if r.returncode == want:
            ok += 1
            print("ARM ok:    %s -> rc=%d" % (label, r.returncode))
        else:
            wrong += 1
            print("ARM WRONG: %s -> rc=%d want %d" % (label, r.returncode, want))
            print("\n".join(r.stdout.splitlines()[-5:]))
    print("PLANTED ARMS: ok %d, wrong %d" % (ok, wrong))
    return 0 if wrong == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
