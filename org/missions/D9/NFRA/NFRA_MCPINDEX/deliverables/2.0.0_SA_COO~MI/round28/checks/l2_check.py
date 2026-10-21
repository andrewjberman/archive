"""l2_check.py <id>: the round-28 (workstream GATEWAY) criteria of cell MX-l-2, run from the repository root.
Prints a DENOMINATOR line, one line per arm, then ARMS and RESULT: PASS|FAIL. Ids: l2.AC1 (the verdicts on the real question set:
the ideal control and each single-defect mutant), l2.AC2 (refusals, acceptance rules, the not_served grading, determinism),
l2.AC3 (the unit tests). ASCII only; python 3.9; standard library only.
The contract is decompositions/NFRA_MCPINDEX_DECOMP.round28-GATEWAY.md section R28.3, L2 QUESTION-SET GRADER.
The script directory is workflows/gateway_battery unless the environment names another (L2_PKG_DIR); the issuer uses that to try a reference.
Every input is derived from the REAL question set (round28/evidence/FWD26_QUESTION_SET.json); every mutant is planted from its data."""
import copy
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R28 = os.path.normpath(os.path.join(HERE, ".."))
QSET = os.path.join(R28, "evidence", "FWD26_QUESTION_SET.json")
PKG = os.environ.get("L2_PKG_DIR") or os.path.join("workflows", "gateway_battery")
SCRIPT = os.path.join(PKG, "fwd26_grade.py")
TESTFILE = os.path.join(PKG, "tests", "test_fwd26_grade.py")
OK, BAD = [], []

FORBIDDEN = ("boto3", "urllib", "requests", "socket", "http.client", "import subprocess")
MUTANTS = (("listed", "listed_first"), ("s2", "s2_folder"), ("wrong-folder", "wrong_folder"), ("wrong-table", "wrong_table"), ("missing", "missing_pick"))
OUT_KEYS = ["class", "id", "matched", "size_classes_proposed", "verdict"]
COUNT_KEYS = ["by_class", "fail", "not_served", "pass", "questions"]


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def run(args, timeout=120):
    if args and args[0].endswith(".py") and not os.path.isfile(args[0]):
        return 98, "", "script absent: %s" % args[0]
    try:
        p = subprocess.run([sys.executable] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        return 99, "", "%s: %s" % (type(exc).__name__, exc)
    return p.returncode, p.stdout.decode("utf-8", "replace").replace("\r", ""), p.stderr.decode("utf-8", "replace").replace("\r", "")


def jload(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return json.load(fh)


def jdump(obj, path):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1)


def line(out, prefix):
    for ln in out.splitlines():
        if ln.startswith(prefix):
            return ln.strip()
    return None


def pytest_count(testfile, minimum):
    if not os.path.isfile(testfile):
        print("DENOMINATOR: test file %s absent" % testfile)
        return False
    p = subprocess.run([sys.executable, "-m", "pytest", testfile, "-q", "-p", "no:cacheprovider", "--color=no"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    out = p.stdout.decode("utf-8", "replace").replace("\r", "")
    m = re.search(r"(\d+) passed", out)
    n = int(m.group(1)) if m else 0
    print("DENOMINATOR: pytest rc=%d passed=%d (minimum %d) file=%s" % (p.returncode, n, minimum, testfile))
    return p.returncode == 0 and n >= minimum


def last_seg(prefix):
    parts = [s for s in prefix.split("/") if s]
    return parts[-1] if parts else ""


class Ctx(object):
    """The real question set plus helpers to run the script on it."""

    def __init__(self, tmp):
        self.tmp = tmp
        self.q = jload(QSET)
        self.items = self.q["items"]
        self.ids = [it["id"] for it in self.items]
        self.n = 0

    def path(self, tag):
        self.n += 1
        return os.path.join(self.tmp, "%s_%d.json" % (tag, self.n))

    def ideal(self, mutate="none", questions=None):
        out = self.path("ideal")
        args = [SCRIPT, "ideal", "--questions", questions or QSET, "--out", out]
        if mutate != "none":
            args += ["--mutate", mutate]
        rc, so, se = run(args)
        return rc, so, se, out

    def grade(self, picks, questions=None, extra=None, tag="g"):
        pk = self.path("picks")
        jdump(picks, pk)
        return self.grade_file(pk, questions=questions, extra=extra, tag=tag)

    def grade_file(self, pk, questions=None, extra=None, tag="g"):
        out = self.path(tag)
        args = [SCRIPT, "grade", "--questions", questions or QSET, "--picks", pk, "--out", out] + list(extra or [])
        rc, so, se = run(args)
        doc = None
        if os.path.isfile(out):
            try:
                doc = jload(out)
            except ValueError:
                doc = None
        return rc, so, se, doc, out

    def ideal_picks(self):
        rc, so, se, out = self.ideal()
        return jload(out) if rc == 0 and os.path.isfile(out) else None

    def item(self, doc, qid):
        for it in (doc or {}).get("items", []):
            if isinstance(it, dict) and it.get("id") == qid:
                return it
        return {}


def pick_of(loc, table=None, listed=False, qid=None):
    return {"id": qid, "bucket": loc["bucket"], "prefix": loc["prefix"], "table": table or last_seg(loc["prefix"]), "listed_bucket_first": listed}


def set_pick(picks, qid, new):
    out = copy.deepcopy(picks)
    for i, p in enumerate(out["picks"]):
        if p["id"] == qid:
            out["picks"][i] = dict(new, id=qid)
            return out
    out["picks"].append(dict(new, id=qid))
    return out


def drop_pick(picks, qid):
    out = copy.deepcopy(picks)
    out["picks"] = [p for p in out["picks"] if p["id"] != qid]
    return out


# ------------------------------------------------------------------------------------------------ l2.AC1
def l2_ac1(tmp):
    cx = Ctx(tmp)
    print("DENOMINATOR: the real question set %s (%d questions, %d expected locations); the ideal control, then each of 5 single-defect "
          "mutants planted on the first question only" % (os.path.relpath(QSET), len(cx.items), sum(len(i["expected_locations"]) for i in cx.items)))
    arm("control: the question set is the accepted 12 (4 Schwab, 4 Orion, 4 Cottonwood Black Diamond)",
        len(cx.items) == 12 and [i["id"] for i in cx.items] == ["S1", "S2", "S3", "S4", "O1", "O2", "O3", "O4", "B1", "B2", "B3", "B4"], "ids=%r" % cx.ids)
    rc, so, se, out = cx.ideal()
    picks = jload(out) if rc == 0 and os.path.isfile(out) else None
    arm("ideal: rc 0 and a fwd26_picks/1 file with one pick per question, each the first expected location with its table and no bucket listing",
        picks is not None and picks.get("schema") == "fwd26_picks/1" and [p.get("id") for p in picks.get("picks", [])] == cx.ids and
        all(p.get("bucket") == it["expected_locations"][0]["bucket"] and p.get("prefix") == it["expected_locations"][0]["prefix"] and
            p.get("table") == last_seg(it["expected_locations"][0]["prefix"]) and p.get("listed_bucket_first") is False
            for p, it in zip(picks.get("picks", []), cx.items)), "rc=%s %s" % (rc, se[-160:]))
    rc, so, se, doc, gout = cx.grade_file(out) if picks is not None else (98, "", "no picks", None, "")
    arm("grade of the ideal picks: rc 0 and the stdout line", rc == 0 and line(so, "FWD26") == "FWD26 questions=12 pass=12 fail=0 not_served=0", "rc=%s %r" % (rc, line(so, "FWD26")))
    doc = doc or {}
    its = doc.get("items", [])
    arm("the output file: schema fwd26_grade/1, one item per question in file order, exactly the contract keys",
        doc.get("schema") == "fwd26_grade/1" and [i.get("id") for i in its] == cx.ids and all(sorted(i.keys()) == OUT_KEYS for i in its if isinstance(i, dict)) and len(its) == 12,
        "schema=%r ids=%r" % (doc.get("schema"), [i.get("id") for i in its]))
    arm("every item PASS with a null class and the matched location equal to the first expected location",
        len(its) == 12 and all(i.get("verdict") == "PASS" and i.get("class") is None and i.get("matched") ==
                               {"bucket": it["expected_locations"][0]["bucket"], "prefix": it["expected_locations"][0]["prefix"]}
                               for i, it in zip(its, cx.items)), "got %r" % its[:1])
    arm("each item carries its question's size_classes_proposed through", len(its) == 12 and all(i.get("size_classes_proposed") == it.get("size_classes_proposed") for i, it in zip(its, cx.items)))
    cn = doc.get("counts", {})
    arm("counts: exactly the contract keys, 12 questions, 12 pass, 0 fail, 0 not_served, every per-class count 0",
        sorted(cn.keys()) == COUNT_KEYS and (cn.get("questions"), cn.get("pass"), cn.get("fail"), cn.get("not_served")) == (12, 12, 0, 0) and
        isinstance(cn.get("by_class"), dict) and set(cn["by_class"].values()) == {0} and
        set(cn["by_class"].keys()) == {"missing_pick", "listed_first", "s2_folder", "wrong_folder", "wrong_table", "not_served"}, "got %r" % cn)
    for mode, cls in MUTANTS:
        rc, so, se, mout = cx.ideal(mode)
        mp = jload(mout) if rc == 0 and os.path.isfile(mout) else None
        if mp is None:
            arm("mutant %s: ideal --mutate writes a picks file" % mode, False, "rc=%s %s" % (rc, se[-160:]))
            continue
        rc, so, se, d, _ = cx.grade_file(mout)
        d = d or {}
        di = d.get("items", [])
        first = di[0] if di else {}
        rest_ok = len(di) == 12 and all(i.get("verdict") == "PASS" for i in di[1:])
        arm("mutant %s: rc 1, exactly the first question FAILs with class %s, the other 11 PASS, counts follow" % (mode, cls),
            rc == 1 and first.get("id") == cx.ids[0] and first.get("verdict") == "FAIL" and first.get("class") == cls and rest_ok and
            line(so, "FWD26") == "FWD26 questions=12 pass=11 fail=1 not_served=0" and (d.get("counts", {}).get("by_class") or {}).get(cls) == 1,
            "rc=%s first=%r stdout=%r" % (rc, first, line(so, "FWD26")))


# ------------------------------------------------------------------------------------------------ l2.AC2
def refused(cx, label, rc, se, out):
    arm(label, rc == 2 and se.startswith("REFUSED:") and not os.path.isfile(out), "rc=%s exists=%s stderr=%r" % (rc, os.path.isfile(out), se[:120]))


def l2_ac2(tmp):
    cx = Ctx(tmp)
    needs = list(cx.q.get("needs_candidate_e_served") or [])
    multi = [it for it in cx.items if len(it["expected_locations"]) >= 2]
    alt = [it for it in cx.items if it.get("accept_also")]
    print("DENOMINATOR: the real question set (%d questions); 9 refusals, the any-folder rule on %d question(s) with several expected locations, "
          "the accept_also rule on %d question(s), 6 not_served arms on %s, precedence, trailing slash, determinism, no network library"
          % (len(cx.items), len(multi), len(alt), needs))
    ideal = cx.ideal_picks()
    if ideal is None:
        arm("control: the ideal picks file is written", False, "ideal failed (script absent or broken)")
        return
    rc, so, se, doc, out = cx.grade(ideal)
    arm("control: the ideal picks grade clean (every refusal arm below has this control)", rc == 0 and out != "" and os.path.isfile(out))
    # refusals: each is the ideal file with exactly one defect
    bad = copy.deepcopy(ideal)
    bad["picks"].append(dict(bad["picks"][0], id="ZZ-unknown"))
    rc, so, se, d, out = cx.grade(bad)
    refused(cx, "a pick for an unknown question id exits 2 with REFUSED and writes nothing", rc, se, out)
    dup = copy.deepcopy(ideal)
    dup["picks"].append(copy.deepcopy(dup["picks"][1]))
    rc, so, se, d, out = cx.grade(dup)
    refused(cx, "two picks for one question id exit 2 with REFUSED and write nothing", rc, se, out)
    nb = copy.deepcopy(ideal)
    nb["picks"][0]["listed_bucket_first"] = "no"
    rc, so, se, d, out = cx.grade(nb)
    refused(cx, "a listed_bucket_first that is not a bool exits 2 with REFUSED", rc, se, out)
    nk = copy.deepcopy(ideal)
    del nk["picks"][0]["listed_bucket_first"]
    rc, so, se, d, out = cx.grade(nk)
    refused(cx, "a pick with no listed_bucket_first exits 2 with REFUSED", rc, se, out)
    sc = copy.deepcopy(ideal)
    sc["schema"] = "fwd26_picks/0"
    rc, so, se, d, out = cx.grade(sc)
    refused(cx, "a picks file with another schema exits 2 with REFUSED", rc, se, out)
    qbad = copy.deepcopy(cx.q)
    qbad["schema"] = "fwd26_questions/0"
    qp = cx.path("qbad")
    jdump(qbad, qp)
    pk = cx.path("pk_ok")
    jdump(ideal, pk)
    rc, so, se, d, out = cx.grade_file(pk, questions=qp)
    refused(cx, "a questions file with another schema exits 2 with REFUSED", rc, se, out)
    notjson = cx.path("notjson")
    with open(notjson, "w", encoding="utf-8") as fh:
        fh.write("{not json")
    rc, so, se, d, out = cx.grade_file(notjson)
    refused(cx, "a picks file that is not JSON exits 2 with REFUSED", rc, se, out)
    rc, so, se, d, out = cx.grade_file(pk, extra=["--served-md5", "not-a-md5"])
    refused(cx, "a --served-md5 that is not 32 hex characters exits 2 with REFUSED", rc, se, out)
    rc, so, se = run([SCRIPT])
    arm("no subcommand exits 2", rc == 2, "rc=%s" % rc)
    # acceptance rules, planted from the data
    for it in multi[:1]:
        results = []
        for loc in it["expected_locations"]:
            rc, so, se, d, out = cx.grade(set_pick(ideal, it["id"], pick_of(loc)))
            results.append(rc == 0 and cx.item(d, it["id"]).get("verdict") == "PASS")
        arm("%s: every one of its %d expected locations (each master folder) PASSes" % (it["id"], len(results)), bool(results) and all(results), "got %r" % results)
    for it in alt[:1]:
        a = it["accept_also"][0]
        rc, so, se, d, out = cx.grade(set_pick(ideal, it["id"], pick_of(a)))
        arm("%s: its accept_also folder with its own table PASSes" % it["id"], rc == 0 and cx.item(d, it["id"]).get("verdict") == "PASS", "rc=%s %r" % (rc, cx.item(d, it["id"])))
        rc, so, se, d, out = cx.grade(set_pick(ideal, it["id"], pick_of(a, table=it["expected_table"])))
        arm("%s: its accept_also folder with the other table is wrong_table" % it["id"], rc == 1 and cx.item(d, it["id"]).get("class") == "wrong_table", "rc=%s %r" % (rc, cx.item(d, it["id"])))
    first = cx.items[0]
    loc0 = first["expected_locations"][0]
    nos = dict(pick_of(loc0), prefix=loc0["prefix"].rstrip("/"))
    rc, so, se, d, out = cx.grade(set_pick(ideal, first["id"], nos))
    arm("%s: a prefix without its trailing slash PASSes (one slash is added before the comparison)" % first["id"], rc == 0 and cx.item(d, first["id"]).get("verdict") == "PASS", "rc=%s %r" % (rc, cx.item(d, first["id"])))
    other = cx.items[1]["expected_locations"][0]
    rc, so, se, d, out = cx.grade(set_pick(ideal, first["id"], pick_of(other, listed=True)))
    arm("precedence: a wrong folder named after a bucket listing is listed_first, not wrong_folder", rc == 1 and cx.item(d, first["id"]).get("class") == "listed_first", "%r" % cx.item(d, first["id"]))
    rc, so, se, d, out = cx.grade(set_pick(ideal, first["id"], pick_of(loc0, table=" " + last_seg(loc0["prefix"]) + " ")))
    arm("a table with surrounding spaces is trimmed and PASSes", rc == 0 and cx.item(d, first["id"]).get("verdict") == "PASS", "%r" % cx.item(d, first["id"]))
    # not_served, planted on the question the set names
    if not needs:
        arm("the question set names a question that needs candidate e", False, "needs_candidate_e_served is empty")
    else:
        nid = needs[0]
        md5 = str(cx.q.get("catalog_md5_read"))
        wrong = set_pick(ideal, nid, pick_of(cx.items[0]["expected_locations"][0]))
        rc, so, se, d, out = cx.grade(wrong)
        arm("%s wrong folder, no --served-md5: a plain FAIL wrong_folder" % nid, rc == 1 and cx.item(d, nid).get("verdict") == "FAIL" and cx.item(d, nid).get("class") == "wrong_folder", "%r" % cx.item(d, nid))
        rc, so, se, d, out = cx.grade(wrong, extra=["--served-md5", md5])
        arm("%s wrong folder, --served-md5 equal to the set's catalog md5: still FAIL wrong_folder" % nid, rc == 1 and cx.item(d, nid).get("class") == "wrong_folder" and (d or {}).get("counts", {}).get("not_served") == 0, "%r" % cx.item(d, nid))
        rc, so, se, d, out = cx.grade(wrong, extra=["--served-md5", "f" * 32])
        arm("%s wrong folder, a different --served-md5: NOT_SERVED with class not_served; fail 0, not_served 1; rc 1" % nid,
            rc == 1 and cx.item(d, nid).get("verdict") == "NOT_SERVED" and cx.item(d, nid).get("class") == "not_served" and
            line(so, "FWD26") == "FWD26 questions=12 pass=11 fail=0 not_served=1", "rc=%s %r %r" % (rc, cx.item(d, nid), line(so, "FWD26")))
        rc, so, se, d, out = cx.grade(drop_pick(ideal, nid), extra=["--served-md5", "f" * 32])
        arm("%s missing pick, a different --served-md5: NOT_SERVED" % nid, rc == 1 and cx.item(d, nid).get("verdict") == "NOT_SERVED", "%r" % cx.item(d, nid))
        rc, so, se, d, out = cx.grade(ideal, extra=["--served-md5", "f" * 32])
        arm("%s picked correctly, a different --served-md5: PASS (a correct pick is a pass whatever is served)" % nid, rc == 0 and cx.item(d, nid).get("verdict") == "PASS", "rc=%s %r" % (rc, cx.item(d, nid)))
        plain = [it["id"] for it in cx.items if it["id"] not in needs][0]
        rc, so, se, d, out = cx.grade(set_pick(ideal, plain, pick_of(cx.items[-1]["expected_locations"][0])), extra=["--served-md5", "f" * 32])
        arm("%s (not listed in needs_candidate_e_served) wrong folder with a different --served-md5 stays FAIL" % plain, rc == 1 and cx.item(d, plain).get("verdict") == "FAIL", "%r" % cx.item(d, plain))
    # determinism and no network library
    a = cx.grade(ideal, tag="da")
    b = cx.grade(ideal, tag="db")
    same = os.path.isfile(a[4]) and os.path.isfile(b[4]) and open(a[4], "rb").read() == open(b[4], "rb").read() and a[1] == b[1]
    arm("two grade runs on the same input give the same bytes and the same stdout", bool(same) and a[0] == b[0] == 0, "rc=%s,%s" % (a[0], b[0]))
    i1 = cx.ideal("wrong-table")
    i2 = cx.ideal("wrong-table")
    arm("two ideal runs give the same bytes", os.path.isfile(i1[3]) and os.path.isfile(i2[3]) and open(i1[3], "rb").read() == open(i2[3], "rb").read())
    text = ""
    if os.path.isfile(SCRIPT):
        with open(SCRIPT, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    arm("the script imports no AWS, HTTP or process library and names both subcommands", bool(text) and not any(t in text for t in FORBIDDEN) and "ideal" in text and "grade" in text and "--served-md5" in text,
        "script absent" if not text else "found %r" % [t for t in FORBIDDEN if t in text])


CHECKS = {
    "l2.AC1": l2_ac1,
    "l2.AC2": l2_ac2,
    "l2.AC3": lambda t: arm("pytest", pytest_count(TESTFILE, 8)),
}

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in CHECKS:
        print("usage: l2_check.py <%s>" % "|".join(sorted(CHECKS)))
        sys.exit(9)
    with tempfile.TemporaryDirectory(prefix="mx_l2_") as tmp:
        CHECKS[cid](tmp)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
