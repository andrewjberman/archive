"""h_check.py <id>: the round-23 (workstream GATEWAY) criteria, run from the repository root. Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL.
Ids: h1.AC1-3 (partition_windows.py), h2.AC1-3 (apply_disposition.py), h3.AC1-3 (index_coverage.py explained remainder), h4.AC1-2 and h5.AC1-2
(disposition files on the REAL census and members), k1..k6.AC1-2 (battery case files on the REAL census). ASCII only; python 3.9.
The contracts are decompositions/NFRA_MCPINDEX_DECOMP.round23-GATEWAY.md section R23.2."""
import copy
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R23 = os.path.normpath(os.path.join(HERE, ".."))
FIX = os.path.join(R23, "fixtures")
R22 = os.path.normpath(os.path.join(R23, "..", "round22"))
CENSUS = os.path.join(R22, "evidence", "GATEWAY_SURFACE_CENSUS_20261019_v2.json")
PKG = os.path.join("workflows", "gateway_battery")
WINDOWS_PY = os.path.join(PKG, "partition_windows.py")
APPLY_PY = os.path.join(PKG, "apply_disposition.py")
COVER_PY = os.path.join(PKG, "index_coverage.py")
TESTS = os.path.join(PKG, "tests")
MEMBERS = os.path.join("workflows", "atom_decomposition", "tool_index", "members.yaml")
PENDING = os.path.join("workflows", "atom_decomposition", "tool_index", "pending_members.yaml")
EMIT = os.path.join("workflows", "atom_decomposition", "emit_catalog_v02.py")
APP = os.path.join("infra", "aws", "ec2", "opal-gateway", "app")
OK, BAD = [], []


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def fx(name):
    return os.path.join(FIX, name)


def run(args, timeout=180):
    if args and args[0].endswith(".py") and not os.path.isfile(args[0]):
        return 98, "", "script absent: %s" % args[0]
    try:
        p = subprocess.run([sys.executable] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        return 99, "", "%s: %s" % (type(exc).__name__, exc)
    return p.returncode, p.stdout.decode("utf-8", "replace").replace("\r", ""), p.stderr.decode("utf-8", "replace").replace("\r", "")


def jload(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def jdump(o, p):
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(o, fh, indent=1)


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


def emit_validator():
    spec = importlib.util.spec_from_file_location("emit_catalog_v02_check", EMIT)
    m = importlib.util.module_from_spec(spec)
    sys.modules["emit_catalog_v02_check"] = m
    spec.loader.exec_module(m)
    return m.validate_claim


# ------------------------------------------------------------------------------------------------ h1: partition windows
def h1_ac1(tmp):
    print("DENOMINATOR: 7 fixture rows over fake listings: dated 3 (two pages; as_of key; a mixed prefix with a bad date and a non-date folder), undated 2, empty 1, error 1")
    out = os.path.join(tmp, "w.json")
    rc, so, se = run([WINDOWS_PY, "--rows", fx("h1_rows.json"), "--fake", fx("h1_fake_listings.json"), "--now", "2026-10-19T16:30:00Z", "--out", out])
    arm("an error row makes rc 1 and the file is still written", rc == 1 and os.path.isfile(out), "rc=%s %s" % (rc, se[-200:]))
    arm("stdout line", line(so, "WINDOWS") == "WINDOWS rows=7 dated=3 undated=2 empty=1 error=1", "got %r" % line(so, "WINDOWS"))
    doc = jload(out) if os.path.isfile(out) else {}
    by = {r.get("entity"): r for r in doc.get("rows", [])}
    arm("header", doc.get("schema") == "partition_windows/1" and doc.get("read_at") == "2026-10-19T16:30:00Z" and doc.get("claim") == "measured", "header=%r" % {k: doc.get(k) for k in ("schema", "read_at", "claim")})
    d = by.get("e_dated", {})
    arm("two pages read: earliest, latest and the partition count", (d.get("kind"), d.get("partition_key"), d.get("earliest"), d.get("latest"), d.get("partitions")) == ("dated", "date", "2026-09-28", "2026-10-08", 4), "got %r" % d)
    a = by.get("e_asof", {})
    arm("an as_of key", (a.get("kind"), a.get("partition_key"), a.get("earliest"), a.get("latest"), a.get("partitions")) == ("dated", "as_of", "2026-10-02", "2026-10-02", 1), "got %r" % a)
    m = by.get("e_mixed", {})
    arm("a non-date folder and a bad date are ignored", (m.get("kind"), m.get("earliest"), m.get("latest"), m.get("partitions")) == ("dated", "2026-10-05", "2026-10-05", 1), "got %r" % m)
    arm("undated (a partition key with no date) and contents-only", by.get("e_undated", {}).get("kind") == "undated" and by.get("e_contents", {}).get("kind") == "undated", "got %r %r" % (by.get("e_undated", {}).get("kind"), by.get("e_contents", {}).get("kind")))
    arm("empty", by.get("e_empty", {}).get("kind") == "empty", "got %r" % by.get("e_empty", {}).get("kind"))
    e = by.get("e_error", {})
    arm("an unlistable prefix reads error with its text, never zero", e.get("kind") == "error" and isinstance(e.get("error"), str) and e["error"].strip(), "got %r" % e)


def h1_ac2(tmp):
    print("DENOMINATOR: determinism over two runs; the client is only ever asked to list; rows input refusals")
    out1, out2 = os.path.join(tmp, "w1.json"), os.path.join(tmp, "w2.json")
    args = [WINDOWS_PY, "--rows", fx("h1_rows.json"), "--fake", fx("h1_fake_listings.json"), "--now", "2026-10-19T16:30:00Z"]
    run(args + ["--out", out1])
    run(args + ["--out", out2])
    arm("two runs give the same bytes", os.path.isfile(out1) and os.path.isfile(out2) and open(out1, "rb").read() == open(out2, "rb").read(), "differs or absent")
    # the measurer lists and never reads, writes or deletes an object: no such call appears in its source
    src = open(WINDOWS_PY, encoding="utf-8").read() if os.path.isfile(WINDOWS_PY) else ""
    forbidden = [t for t in ("get_object", "download_file", "download_fileobj", "put_object", "upload_file", "delete_object", "copy_object", "select_object_content", "get_object_attributes") if t in src]
    arm("the source names no object read, write, copy or delete call", bool(src) and not forbidden, "forbidden tokens: %r" % forbidden)
    bad = {
        "missing rows key": {"nope": []},
        "row without prefix": {"rows": [{"entity": "x", "bucket": "b"}]},
        "row without bucket": {"rows": [{"entity": "x", "prefix": "p/"}]},
        "empty rows": {"rows": []},
    }
    for label, body in bad.items():
        p = os.path.join(tmp, "bad_rows.json")
        jdump(body, p)
        rc, _, _ = run([WINDOWS_PY, "--rows", p, "--fake", fx("h1_fake_listings.json"), "--out", os.path.join(tmp, "bo.json")])
        arm("%s refused (rc 2)" % label, rc == 2, "rc=%s" % rc)
    rc, _, _ = run([WINDOWS_PY, "--rows", os.path.join(tmp, "absent.json"), "--fake", fx("h1_fake_listings.json"), "--out", os.path.join(tmp, "bo.json")])
    arm("an absent rows file is refused (rc 2)", rc == 2, "rc=%s" % rc)


# ------------------------------------------------------------------------------------------------ h2: applier
def apply_run(tmp, tag, members=None, census=None, windows=None, disp=None):
    out = os.path.join(tmp, "members_%s.yaml" % tag)
    rep = os.path.join(tmp, "report_%s.json" % tag)
    args = [APPLY_PY, "--census", census or fx("h2_census.json"), "--members", members or fx("h2_members.yaml"), "--windows", windows or fx("h2_windows.json"),
            "--dispositions", disp or fx("h2_disp.json"), "--out", out, "--report", rep]
    rc, so, se = run(args)
    return rc, so, se, out, rep


def entry_text(text, tool):
    """The block of one entry: from its `- tool: X` line to the next line that starts a new entry, a comment at column 0 or a top-level key."""
    lines = text.split("\n")
    start = None
    for i, ln in enumerate(lines):
        if ln == "- tool: %s" % tool:
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("- tool:") or lines[j].startswith("#") or (lines[j] and not lines[j].startswith((" ", "-"))):
            end = j
            break
    return "\n".join(lines[start:end]).rstrip("\n")


def h2_ac1(tmp):
    import yaml
    print("DENOMINATOR: fixture members 7 entries (b 5, a 1, c 1); census indexes: tA1 1, tA2 2, tC1 1, others 0; windows rowA dated, rowB undated, rowC dated; dispositions 2")
    rc, so, se, out, rep = apply_run(tmp, "g")
    arm("apply rc 0", rc == 0 and os.path.isfile(out), "rc=%s %s" % (rc, se[-300:]))
    arm("stdout line", line(so, "APPLY") == "APPLY auto_a=2 disposed_b=1 disposed_c=1 untouched_b=1", "got %r" % line(so, "APPLY"))
    new = open(out, encoding="utf-8").read() if os.path.isfile(out) else ""
    old = open(fx("h2_members.yaml"), encoding="utf-8").read()
    arm("header comments, the comment between entries and the buckets list are preserved byte for byte",
        all(s in new for s in ("# members fixture -- header comment line 1\n# header comment line 2 (must survive the apply byte for byte)\n", "# comment between entries (must survive)\n", "buckets:\n- tool: tA1\n  bucket: bkt-a\n")), "a comment or the buckets list was lost")
    arm("untouched entries are byte-identical", all(entry_text(new, t) == entry_text(old, t) and entry_text(new, t) is not None for t in ("tB2", "tC1", "tD")), "tB2/tC1/tD changed")
    doc = yaml.safe_load(new) if new else {}
    ents = {e["tool"]: e for e in (doc or {}).get("members", [])}
    arm("the entry order is unchanged", [e["tool"] for e in (doc or {}).get("members", [])] == ["tA1", "tA2", "tA3", "tB1", "tB2", "tC1", "tD"], "order=%r" % [e.get("tool") for e in (doc or {}).get("members", [])])
    validate = emit_validator()
    a1 = ents.get("tA1", {})
    want_fresh = {"claim": "measured", "value": "2026-10-08", "basis": "s3://bkt-a/", "method": "key-date", "read_at": "2026-10-19T16:30:00Z"}
    arm("tA1: indexed b becomes a, index and links from the census, bucket keys kept", (a1.get("member"), a1.get("index"), a1.get("links"), a1.get("bucket"), a1.get("bucket_source")) == ("a", "rowA", ["rowA"], "bkt-a", "app/x.py:10"), "got %r" % a1)
    arm("tA1: freshness is a measured key-date claim from the listing's latest", a1.get("freshness") == want_fresh, "got %r" % a1.get("freshness"))
    d1 = a1.get("history_depth") or {}
    arm("tA1: depth is an inferred partition-listing window", (d1.get("claim"), d1.get("value"), d1.get("method"), d1.get("basis"), d1.get("read_at")) == ("inferred", "2026-09-01..2026-10-08", "partition-listing", "s3://bkt-a/", "2026-10-19T16:30:00Z")
        and isinstance(d1.get("source"), str) and d1["source"].strip(), "got %r" % d1)
    a2 = ents.get("tA2", {})
    arm("tA2: two links, index is the first sorted", (a2.get("member"), a2.get("index"), a2.get("links")) == ("a", "rowA", ["rowA", "rowB"]), "got %r" % a2)
    f2 = a2.get("freshness") or {}
    d2 = a2.get("history_depth") or {}
    els = d2.get("links") or []
    arm("tA2: freshness absent with a reason for a multi-index tool; depth per-link, one element per linked row",
        f2.get("claim") == "absent" and bool(str(f2.get("reason", "")).strip()) and d2.get("claim") == "per-link" and [x.get("row") for x in els] == ["rowA", "rowB"]
        and els[0].get("claim") == "inferred" and els[0].get("value") == "2026-09-01..2026-10-08" and els[1].get("claim") == "absent" and bool(str(els[1].get("reason", "")).strip()), "got %r %r" % (f2, d2))
    arm("tA3: the disposed b keeps its owner, gains the reason, has no index", (ents.get("tA3", {}).get("member"), ents.get("tA3", {}).get("owner"), ents.get("tA3", {}).get("reason"), "index" in ents.get("tA3", {})) == ("b", "PROJ_A", "the dataset it reads has no catalog row yet", False), "got %r" % ents.get("tA3"))
    arm("tB1: the disposed c carries its reason and no owner", (ents.get("tB1", {}).get("member"), ents.get("tB1", {}).get("reason"), "owner" in ents.get("tB1", {})) == ("c", "reads the caller's own mailbox, which is not an Opal dataset", False), "got %r" % ents.get("tB1"))
    errs = validate("tA1 freshness", a1.get("freshness")) + validate("tA1 depth", a1.get("history_depth")) + validate("tA2 freshness", a2.get("freshness")) + validate("tA2 depth", a2.get("history_depth"))
    arm("every composed claim passes the emitter's validate_claim", not errs, "validate_claim refused: %r" % errs)
    rpt = jload(rep) if os.path.isfile(rep) else {}
    arm("report lists each changed tool with its rule", {x.get("tool"): x.get("rule") for x in rpt.get("changes", [])} == {"tA1": "auto_a", "tA2": "auto_a", "tA3": "disposed_b", "tB1": "disposed_c"}, "report=%r" % rpt.get("changes"))


def h2_ac2(tmp):
    print("DENOMINATOR: refusal arms (rc 2, no output file) and determinism")
    base = jload(fx("h2_disp.json"))
    arms = {
        "a tool the census does not serve": [{"tool": "nope", "member": "c", "reason": "a reason that is long enough"}],
        "an a disposition for a tool with no index": [{"tool": "tA3", "member": "a", "reason": "a reason that is long enough"}],
        "a c with no reason": [{"tool": "tB1", "member": "c", "reason": ""}],
        "a b with no owner": [{"tool": "tA3", "member": "b", "reason": "the dataset has no row yet"}],
        "a b with no reason": [{"tool": "tA3", "member": "b", "owner": "PROJ_A"}],
        "the same tool twice": [{"tool": "tB1", "member": "c", "reason": "a reason that is long enough"}, {"tool": "tB1", "member": "c", "reason": "a reason that is long enough"}],
        "a tool that already has an index": [{"tool": "tA1", "member": "c", "reason": "a reason that is long enough"}],
        "an unknown member letter": [{"tool": "tB1", "member": "z", "reason": "a reason that is long enough"}],
    }
    for label, tools in arms.items():
        d = copy.deepcopy(base)
        d["tools"] = tools
        p = os.path.join(tmp, "d_bad.json")
        jdump(d, p)
        rc, so, se, out, rep = apply_run(tmp, "bad", disp=p)
        arm("%s: refused (rc 2) and no output file" % label, rc == 2 and not os.path.isfile(out), "rc=%s out=%s" % (rc, os.path.isfile(out)))
        if os.path.isfile(out):
            os.remove(out)
    badw = os.path.join(tmp, "w_bad.json")
    with open(badw, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("not json")
    rc, so, se, out, rep = apply_run(tmp, "badw", windows=badw)
    arm("an unreadable windows file is refused (rc 2)", rc == 2 and not os.path.isfile(out), "rc=%s" % rc)
    rc1, _, _, o1, _ = apply_run(tmp, "d1")
    rc2, _, _, o2, _ = apply_run(tmp, "d2")
    arm("two runs give the same bytes", os.path.isfile(o1) and os.path.isfile(o2) and open(o1, "rb").read() == open(o2, "rb").read(), "differs")
    # a tool absent from the windows file: its element is absent with a reason, never a guess
    w = jload(fx("h2_windows.json"))
    w["rows"] = [r for r in w["rows"] if r["entity"] != "rowA"]
    pw = os.path.join(tmp, "w_norowA.json")
    jdump(w, pw)
    rc, so, se, out, rep = apply_run(tmp, "norow", windows=pw)
    import yaml
    doc = yaml.safe_load(open(out, encoding="utf-8").read()) if os.path.isfile(out) else {}
    ents = {e["tool"]: e for e in (doc or {}).get("members", [])}
    d1 = (ents.get("tA1", {}).get("history_depth") or {})
    f1 = (ents.get("tA1", {}).get("freshness") or {})
    arm("a linked row with no windows entry reads absent with a reason, for freshness and depth", rc == 0 and d1.get("claim") == "absent" and f1.get("claim") == "absent" and bool(str(d1.get("reason", "")).strip()) and bool(str(f1.get("reason", "")).strip()), "got %r %r" % (f1, d1))


# ------------------------------------------------------------------------------------------------ h3: explained remainder in the gate
def h3_run(tmp, tag, members, catalog, channels=()):
    out = os.path.join(tmp, "c_%s.json" % tag)
    args = [COVER_PY, "--census", os.path.join(R22, "fixtures", "expected_census.json"), "--members", members, "--catalog", catalog, "--out", out]
    for c in channels:
        args += ["--channel", c]
    rc, so, se = run(args)
    return rc, so, se, (jload(out) if os.path.isfile(out) else None)


def h3_ac1(tmp):
    print("DENOMINATOR: fixture census 6 channels, 9 tools, 7 rows under a channel; members: harvest_read is b with owner and reason (explained), send_email is b with an owner and no reason; catalog: gap_row has gap_owner, bad_gap names a ghost tool, gap_blank has an empty gap_owner")
    rc, so, se, doc = h3_run(tmp, "e", fx("h3_members.yaml"), fx("h3_catalog.yaml"))
    arm("exit 1 (refusals remain) and the line carries explained", rc == 1 and line(so, "COVERAGE") == "COVERAGE channels=6 tools=9 rows=7 refusals=3 explained=2", "rc=%s got %r" % (rc, line(so, "COVERAGE")))
    ref = sorted((r["class"], r["subject"]) for r in (doc or {}).get("refusals", []))
    arm("refusals: the b without a reason, the ghost-tool row, the blank gap_owner row", ref == sorted([("tool_member_b", "send_email"), ("row_no_read_tool", "bad_gap"), ("row_no_read_tool", "gap_blank")]), "got %r" % ref)
    exp = sorted((r["class"], r["subject"], r.get("detail")) for r in (doc or {}).get("explained", []))
    arm("explained: the b with owner and reason, the row with a gap_owner (detail = the owner)", exp == sorted([("tool_b_explained", "harvest_read", "AMGT_HARVST"), ("row_explained_gap", "gap_row", "NFRA_OPLGTW")]), "got %r" % exp)
    arm("the denominator block counts explained", (doc or {}).get("denominator", {}).get("explained") == 2, "denominator=%r" % (doc or {}).get("denominator"))
    arm("explained records carry class, channel, subject and detail", all(set(("class", "channel", "subject", "detail")) <= set(r) for r in (doc or {}).get("explained", [])), "shape")
    # green once the three refusals are fixed: an explained remainder alone exits 0
    import yaml
    mem = yaml.safe_load(open(fx("h3_members.yaml"), encoding="utf-8"))
    for e in mem["members"]:
        if e["tool"] == "send_email":
            e["reason"] = "sending is out of scope this round"
    cat = yaml.safe_load(open(fx("h3_catalog.yaml"), encoding="utf-8"))
    cat["harvest_datasets"] = [r for r in cat["harvest_datasets"] if r["entity"] not in ("bad_gap", "gap_blank")]
    pm, pc = os.path.join(tmp, "m.yaml"), os.path.join(tmp, "c.yaml")
    yaml.safe_dump(mem, open(pm, "w", encoding="ascii"))
    yaml.safe_dump(cat, open(pc, "w", encoding="ascii"))
    rc, so, se, doc = h3_run(tmp, "g", pm, pc)
    arm("an explained remainder alone exits 0", rc == 0 and line(so, "COVERAGE") == "COVERAGE channels=6 tools=9 rows=5 refusals=0 explained=3", "rc=%s got %r" % (rc, line(so, "COVERAGE")))


def h3_ac2(tmp):
    print("DENOMINATOR: the round-22 gate arms still hold (g2.AC1 and g2.AC2, updated for the explained field) and the explained field is never a way to hide a refusal")
    for cid in ("g2.AC1", "g2.AC2"):
        p = subprocess.run([sys.executable, os.path.join(R22, "checks", "g_check.py"), cid], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
        out = p.stdout.decode("utf-8", "replace").replace("\r", "")
        arm("round-22 %s still PASSes" % cid, p.returncode == 0 and "RESULT: PASS" in out, out[-300:])
    import yaml
    # a b with an owner and a reason whose reason is blank/whitespace stays a refusal; a row with a non-string gap_owner stays a refusal
    mem = yaml.safe_load(open(fx("h3_members.yaml"), encoding="utf-8"))
    for e in mem["members"]:
        if e["tool"] == "harvest_read":
            e["reason"] = "   "
    cat = yaml.safe_load(open(fx("h3_catalog.yaml"), encoding="utf-8"))
    for r in cat["silver_datasets"]:
        if r["entity"] == "gap_row":
            r["gap_owner"] = 7
    pm, pc = os.path.join(tmp, "m2.yaml"), os.path.join(tmp, "c2.yaml")
    yaml.safe_dump(mem, open(pm, "w", encoding="ascii"))
    yaml.safe_dump(cat, open(pc, "w", encoding="ascii"))
    rc, so, se, doc = h3_run(tmp, "w", pm, pc)
    ref = sorted((r["class"], r["subject"]) for r in (doc or {}).get("refusals", []))
    arm("a blank reason and a non-string gap_owner stay refusals", ("tool_member_b", "harvest_read") in ref and ("row_no_read_tool", "gap_row") in ref, "got %r" % ref)
    # an undeclared-channel tool that is b with an owner and a reason is still an undeclared_tool refusal (not explained away)
    mem3 = yaml.safe_load(open(fx("h3_members.yaml"), encoding="utf-8"))
    for e in mem3["members"]:
        if e["tool"] == "stray_tool":
            e.clear()
            e.update({"tool": "stray_tool", "member": "b", "owner": "SOME_PROJECT", "reason": "has no row"})
    pm3 = os.path.join(tmp, "m3.yaml")
    yaml.safe_dump(mem3, open(pm3, "w", encoding="ascii"))
    rc, so, se, doc = h3_run(tmp, "u", pm3, fx("h3_catalog.yaml"))
    ref = sorted((r["class"], r["subject"]) for r in (doc or {}).get("refusals", []))
    arm("an undeclared-channel tool that is an explained b still refuses as undeclared_tool", ("undeclared_tool", "stray_tool") in ref, "got %r" % ref)


# ------------------------------------------------------------------------------------------------ real-data helpers
def real_scope():
    import yaml
    cen = jload(CENSUS)
    mm = {}
    for path, key in ((MEMBERS, "members"), (PENDING, "pending")):
        if os.path.isfile(path):
            for e in (yaml.safe_load(open(path, encoding="utf-8")) or {}).get(key) or []:
                mm.setdefault(e["tool"], e)
    tools = {t["name"]: t for t in cen["tools"]}
    chan_of = {}
    for c in cen["channels"]:
        for t in c["tools"]:
            chan_of.setdefault(t, c["id"])
    return cen, mm, tools, chan_of


def disposition_check(cid, want_m365):
    cen, mm, tools, chan_of = real_scope()
    scope = sorted(t for t in tools if mm.get(t, {}).get("member") == "b" and not tools[t]["indexes"] and ((chan_of[t] == "m365") == want_m365))
    print("DENOMINATOR: %d tool(s) in scope (member b with no catalog index, %s channel m365); census %s read_at %s" % (len(scope), "in" if want_m365 else "outside", os.path.basename(CENSUS), cen.get("read_at")))
    cand = [p for p in sys.argv[2:]]
    path = cand[0] if cand else None
    arm("a disposition file path was given and exists", bool(path) and os.path.isfile(path), "usage: h_check.py %s <disposition.json>" % cid)
    if not (path and os.path.isfile(path)):
        return None, scope, tools, mm
    return jload(path), scope, tools, mm


def d_ac1(want_m365):
    doc, scope, tools, mm = disposition_check("d", want_m365)
    if doc is None:
        return
    arm("schema and scope fields", doc.get("schema") == "gateway_disposition/1" and isinstance(doc.get("tools"), list), "schema=%r" % doc.get("schema"))
    names = [t.get("tool") for t in doc.get("tools", [])]
    arm("every tool in scope appears exactly once", sorted(names) == scope, "missing=%r extra=%r dup=%r" % (sorted(set(scope) - set(names)), sorted(set(names) - set(scope)), sorted(n for n in set(names) if names.count(n) > 1)))
    arm("every member is b or c (no tool in scope has an index, so none can be a)", all(t.get("member") in ("b", "c") for t in doc.get("tools", [])), "members=%r" % sorted({t.get("member") for t in doc.get("tools", [])}))
    arm("a c carries a reason and no owner; a b carries an owner and a reason",
        all((t.get("member") == "c" and str(t.get("reason", "")).strip() and "owner" not in t) or (t.get("member") == "b" and str(t.get("owner", "")).strip() and str(t.get("reason", "")).strip()) for t in doc.get("tools", [])), "a disposition lacks its fields")


def d_ac2(want_m365):
    doc, scope, tools, mm = disposition_check("d", want_m365)
    if doc is None:
        return
    pat = re.compile(r"\[(app/[A-Za-z0-9_./-]+\.py):(\d+)\]\s*$")
    bad, nonascii, short = [], [], []
    for t in doc.get("tools", []):
        r = str(t.get("reason", ""))
        try:
            r.encode("ascii")
        except UnicodeEncodeError:
            nonascii.append(t.get("tool"))
        m = pat.search(r)
        if len(r) < 40:
            short.append(t.get("tool"))
        if not m:
            bad.append(t.get("tool"))
            continue
        f = os.path.join(APP, m.group(1)[len("app/"):])
        if not os.path.isfile(f) or int(m.group(2)) < 1 or int(m.group(2)) > len(open(f, encoding="utf-8", errors="replace").read().split("\n")):
            bad.append(t.get("tool"))
    arm("every reason is ASCII and at least 40 characters", not nonascii and not short, "nonascii=%r short=%r" % (nonascii, short))
    arm("every reason ends with a source reference [app/<file>.py:<line>] to a real line of the gateway source", not bad, "unreferenced or wrong=%r" % bad)
    lead = {}
    for t in doc.get("tools", []):
        lead.setdefault(re.sub(r"\[.*$", "", str(t.get("reason", ""))).strip(), []).append(t.get("tool"))
    worst = max((len(v) for v in lead.values()), default=0)
    arm("the reasons are about the tool, not one sentence pasted on most of them (no reason text on more than 60 percent of the tools)", worst <= max(2, int(0.6 * max(1, len(doc.get("tools", []))))), "most repeated reason covers %d of %d tools" % (worst, len(doc.get("tools", []))))


def k_scope(channel_ids):
    cen, mm, tools, chan_of = real_scope()
    chans = [c for c in cen["channels"] if c["id"] in channel_ids]
    scope = sorted({t for c in chans for t in c["tools"]})
    return cen, tools, scope


def k_load():
    path = sys.argv[2] if len(sys.argv) > 2 else None
    arm("a cases file path was given and exists", bool(path) and os.path.isfile(path), "usage: h_check.py <id> <cases.json>")
    return jload(path) if path and os.path.isfile(path) else None


def k_ac1(channel_ids, prefix):
    cen, tools, scope = k_scope(channel_ids)
    print("DENOMINATOR: %d tool(s) in scope: channels %s; census %s" % (len(scope), ",".join(channel_ids), os.path.basename(CENSUS)))
    doc = k_load()
    if doc is None:
        return
    cases = doc.get("cases", [])
    arm("schema", doc.get("schema") == "gateway_battery_cases/1" and isinstance(cases, list), "schema=%r" % doc.get("schema"))
    ids = [c.get("case_id") for c in cases]
    arm("case ids are unique and start with %s" % prefix, len(ids) == len(set(ids)) and all(isinstance(i, str) and i.startswith(prefix) for i in ids), "ids=%r" % ids[:6])
    by = {}
    for c in cases:
        by.setdefault(c.get("tool"), []).append(c)
    arm("every tool in scope has at least one case", not (set(scope) - set(by)), "no case for %r" % sorted(set(scope) - set(by)))
    arm("no case names a tool outside the scope", not (set(by) - set(scope)), "outside %r" % sorted(set(by) - set(scope)))
    arm("every case carries its fields (case_id, tool, question, args as an object, expect, source_hint)", all(isinstance(c.get("args"), dict) and c.get("expect") in ("nonempty", "empty", "refused", "preview") and str(c.get("question", "")).strip() and str(c.get("source_hint", "")).strip() for c in cases), "a case lacks a field")


REAL_NO_CLASS = (None, "UNCLASSIFIED")
MUTATING_UNCLASSIFIED = ("opal_data_refresh_upload",)   # the one mutating tool whose class is UNCLASSIFIED (deploy-to-ec2.sh: "ONE MUTATING tool")


def is_sender(t):
    return (t.get("write_class") not in REAL_NO_CLASS) or t.get("name") in MUTATING_UNCLASSIFIED


def src_ref_ok(text):
    m = re.search(r"\[(app/[A-Za-z0-9_./-]+\.py):(\d+)\]\s*$", str(text))
    if not m:
        return False
    f = os.path.join(APP, m.group(1)[len("app/"):])
    return os.path.isfile(f) and 1 <= int(m.group(2)) <= len(open(f, encoding="utf-8", errors="replace").read().split("\n"))


def k_ac2(channel_ids, prefix, src_channels=None):
    cen, tools, scope = k_scope(channel_ids)
    senders = sorted(t for t in scope if is_sender(tools[t]))
    unclassified = sorted(t for t in scope if tools[t].get("write_class") == "UNCLASSIFIED" and t not in senders)
    print("DENOMINATOR: %d tool(s) in scope; senders %d (a real write_class, or opal_data_refresh_upload); %d with write_class UNCLASSIFIED treated as readers on a grounded source reference" % (len(scope), len(senders), len(unclassified)))
    doc = k_load()
    if doc is None:
        return
    cases = doc.get("cases", [])
    by = {}
    for c in cases:
        by.setdefault(c.get("tool"), []).append(c)
    arm("every case of a sender is preview, and a sender has a preview case", all(c.get("expect") == "preview" for t in senders for c in by.get(t, [])) and all(by.get(t) for t in senders), "senders=%r" % senders)
    readers = [t for t in scope if t not in senders]
    arm("every reader has a case that expects an answer (nonempty or empty), not only refusals", all(any(c.get("expect") in ("nonempty", "empty") for c in by.get(t, [])) for t in readers), "readers without: %r" % [t for t in readers if not any(c.get("expect") in ("nonempty", "empty") for c in by.get(t, []))])
    arm("every case of a tool whose write_class is UNCLASSIFIED ends its source_hint with a [app/<file>.py:<line>] reference to the definition that shows it only reads", all(src_ref_ok(c.get("source_hint")) for t in unclassified for c in by.get(t, [])), "a case of %r lacks the reference" % [t for t in unclassified if not all(src_ref_ok(c.get("source_hint")) for c in by.get(t, []))])
    chan_of = {}
    for ch in cen["channels"]:
        for t in ch["tools"]:
            chan_of.setdefault(t, ch["id"])
    need = set(src_channels or ())
    miss = [c.get("case_id") for c in cases if c.get("expect") in ("nonempty", "empty") and chan_of.get(c.get("tool")) in need
            and not (isinstance(c.get("expect_source"), str) and c["expect_source"].strip() and all(ord(ch) < 128 for ch in c["expect_source"]))]
    arm("every reader case that expects an answer, in a channel named below, carries a non-empty ASCII expect_source (%s)" % ", ".join(sorted(need)) if need else "no channel of this cell needs expect_source", not miss, "cases without expect_source: %r" % miss[:6])
    qs = [str(c.get("question", "")).strip() for c in cases]
    arm("questions are ASCII, plain English of at least four words, and unique", all(len(q.split()) >= 4 for q in qs) and len(qs) == len(set(qs)) and all(all(ord(ch) < 128 for ch in q) for q in qs), "a question is short, repeated or not ASCII")
    arm("no case argument holds a credential-shaped value or an email address", not re.search(r"(@[A-Za-z0-9.-]+\.[a-z]{2,}|AKIA[0-9A-Z]{8,}|Bearer\s+\S+|password)", json.dumps(cases)), "an argument looks like an email or a credential")
    arm("a case that needs an earlier answer says so with depends_on, naming an existing case id", all((not c.get("depends_on")) or all(d in {x.get("case_id") for x in cases} for d in c["depends_on"]) for c in cases), "depends_on names a missing case")


# ------------------------------------------------------------------------------------------------ h6 (v2): route recorded, misrouted
BATT_PY = os.path.join(PKG, "tool_battery.py")
ROUTING_PY = os.path.join(PKG, "routing_table.py")


def h6_grade(tmp, tag, results_path, routing_path="__default__"):
    out = os.path.join(tmp, "g_%s.json" % tag)
    args = [BATT_PY, "grade", "--census", os.path.join(R22, "fixtures", "expected_census.json"), "--cases", fx("h6_cases.json"), "--results", results_path,
            "--channel", "opal-data-harvest", "--channel", "opal-data-assets", "--out", out]
    if routing_path == "__default__":
        routing_path = fx("h6_routing.json")
    if routing_path:
        args += ["--routing", routing_path]
    rc, so, se = run(args)
    return rc, so, se, (jload(out) if os.path.isfile(out) else None)


def tool_of(doc, tool):
    for t in (doc or {}).get("tools", []):
        if t.get("tool") == tool:
            return t
    return {}


def case_of(doc, cid):
    for c in (doc or {}).get("cases", []):
        if c.get("case_id") == cid:
            return c
    return {}


def h6_ac1(tmp):
    print("DENOMINATOR: fixture census scoped to opal-data-harvest and opal-data-assets: 4 tools, 4 cases; a routing table with a source set per tool; R1 and R2 results cite their sources, R3 and R4 do not")
    res = jload(fx("h6_results.json"))
    rc, so, se, doc = h6_grade(tmp, "g", fx("h6_results.json"))
    arm("green: PASS=4", rc == 0 and line(so, "GRADE") == "GRADE tools=4 PASS=4 EMPTY-CORRECT=0 REFUSED-CORRECT=0 PREVIEW-ONLY=0 FAIL=0", "rc=%s %r %s" % (rc, line(so, "GRADE"), se[-200:]))
    arm("the record says route: response-cited where the response names a source, code-cited where it does not",
        (case_of(doc, "R1").get("route"), case_of(doc, "R2").get("route"), case_of(doc, "R3").get("route"), case_of(doc, "R4").get("route")) == ("response-cited", "response-cited", "code-cited", "code-cited"),
        "routes=%r" % [case_of(doc, c).get("route") for c in ("R1", "R2", "R3", "R4")])

    def variant(mutate, tag, rmutate=None):
        r = copy.deepcopy(res)
        mutate(r)
        p = os.path.join(tmp, "r_%s.json" % tag)
        jdump(r, p)
        rp = fx("h6_routing.json")
        if rmutate:
            t = jload(rp)
            rmutate(t)
            rp = os.path.join(tmp, "rt_%s.json" % tag)
            jdump(t, rp)
        return h6_grade(tmp, tag, p, rp)

    def get(r, cid):
        return [x for x in r["results"] if x["case_id"] == cid][0]

    def m1(r):
        get(r, "R1")["answer_source"] = ["bloomberg/harvest/silver/article/date=2026-10-05/"]
    rc, so, se, doc = variant(m1, "m1")
    arm("a response that cites a source outside the routed set reads FAIL misrouted", rc == 1 and tool_of(doc, "harvest_list").get("fail_class") == "misrouted", "rc=%s %r" % (rc, tool_of(doc, "harvest_list")))

    def m2(r):
        get(r, "R2")["answer_source"].append("opal-data-bd/silver/fees/")
    rc, so, se, doc = variant(m2, "m2")
    arm("one cited source outside the set is enough to FAIL, even beside a matching one", rc == 1 and tool_of(doc, "harvest_read").get("fail_class") == "misrouted", "rc=%s %r" % (rc, tool_of(doc, "harvest_read")))

    def noop(r):
        pass

    def rm3(t):
        [x for x in t["tools"] if x["tool"] == "schwab_query"][0].update({"verdict": "MISROUTED", "class": "code"})
    rc, so, se, doc = variant(noop, "m3", rm3)
    arm("a code-cited answer needs a ROUTED table row: MISROUTED reads FAIL route_unproven", rc == 1 and tool_of(doc, "schwab_query").get("fail_class") == "route_unproven" and tool_of(doc, "client_get_holdings").get("verdict") == "PASS", "rc=%s %r" % (rc, tool_of(doc, "schwab_query")))

    def rm4(t):
        t["tools"] = [x for x in t["tools"] if x["tool"] != "schwab_query"]
    rc, so, se, doc = variant(noop, "m4", rm4)
    arm("a tool absent from the routing table reads FAIL route_unproven", rc == 1 and tool_of(doc, "schwab_query").get("fail_class") == "route_unproven", "rc=%s %r" % (rc, tool_of(doc, "schwab_query")))
    rc, so, se, doc = variant(m1, "m5", None)
    # same wrong citation, but graded WITHOUT --routing: the round-22 behaviour, route null
    rc2, so2, se2, doc2 = h6_grade(tmp, "m5b", os.path.join(tmp, "r_m1.json"), routing_path=None)
    arm("without --routing the grade is the round-22 grade and the cases carry no route key", rc2 == 0 and "route" not in case_of(doc2, "R1") and line(so2, "GRADE") == "GRADE tools=4 PASS=4 EMPTY-CORRECT=0 REFUSED-CORRECT=0 PREVIEW-ONLY=0 FAIL=0", "rc=%s %r %r" % (rc2, line(so2, "GRADE"), case_of(doc2, "R1").get("route")))


def h6_ac2(tmp):
    print("DENOMINATOR: the planted wrong citation (plant-route) and the round-22 battery arms (g4.AC1 and g4.AC2) still holding")
    out = os.path.join(tmp, "planted.json")
    rc, so, se = run([BATT_PY, "plant-route", "--cases", fx("h6_cases.json"), "--results", fx("h6_results.json"), "--case", "R1", "--out", out])
    arm("plant-route rc 0 and writes the file", rc == 0 and os.path.isfile(out), "rc=%s %s" % (rc, se[-200:]))
    if os.path.isfile(out):
        planted = jload(out)
        orig = jload(fx("h6_results.json"))
        changed = [x["case_id"] for x, y in zip(planted["results"], orig["results"]) if x != y]
        r1 = [x for x in planted["results"] if x["case_id"] == "R1"][0]
        arm("only the named case changes, and its answer_source is now a source outside every routed set", changed == ["R1"] and r1.get("answer_source") == ["planted/wrong/source/"], "changed=%r answer_source=%r" % (changed, r1.get("answer_source")))
        rc, so, se, doc = h6_grade(tmp, "p", out)
        arm("the planted wrong source reads FAIL misrouted", rc == 1 and tool_of(doc, "harvest_list").get("fail_class") == "misrouted", "rc=%s %r" % (rc, tool_of(doc, "harvest_list")))
    rc, so, se = run([BATT_PY, "plant-route", "--cases", fx("h6_cases.json"), "--results", fx("h6_results.json"), "--case", "NOPE", "--out", os.path.join(tmp, "p3.json")])
    arm("plant-route on a case that does not exist is refused (rc 2)", rc == 2, "rc=%s" % rc)
    for cid in ("g4.AC1", "g4.AC2"):
        p = subprocess.run([sys.executable, os.path.join(R22, "checks", "g_check.py"), cid], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
        o = p.stdout.decode("utf-8", "replace").replace("\r", "")
        arm("round-22 %s still PASSes" % cid, p.returncode == 0 and "RESULT: PASS" in o, o[-300:])


# ------------------------------------------------------------------------------------------------ r1: the routing table emitter
def r1_run(tmp, tag, extra=()):
    out = os.path.join(tmp, "rt_%s.json" % tag)
    rc, so, se = run([ROUTING_PY, "--census", fx("r1_census.json"), "--catalog", fx("r1_catalog.yaml"), "--sources", fx("r1_sources.json"), "--out", out] + list(extra))
    return rc, so, se, (jload(out) if os.path.isfile(out) else None)


def r1_ac1(tmp):
    print("DENOMINATOR: fixture census 7 tools (4 channels), catalog 3 rows, source sets for 6 tools (tU1 has none); 8 (tool, row) pairs, one of them a Black Diamond row linked on a Schwab tool")
    rc, so, se, doc = r1_run(tmp, "g")
    arm("exit 1 (defects remain) and the table is written", rc == 1 and doc is not None, "rc=%s %s" % (rc, se[-200:]))
    arm("stdout line", line(so, "ROUTING") == "ROUTING tools=7 pairs=8 routed_pairs=7 misrouted_tools=3 link=1 code=1 display=1 untraced=1", "got %r" % line(so, "ROUTING"))
    by = {t.get("tool"): t for t in (doc or {}).get("tools", [])}
    arm("header and one entry per census tool", (doc or {}).get("schema") == "gateway_routing_table/1" and sorted(by) == ["tB1", "tC1", "tD1", "tM1", "tS1", "tS2", "tU1"], "tools=%r" % sorted(by))
    arm("clean tools read ROUTED", all(by.get(t, {}).get("verdict") == "ROUTED" and by[t].get("class") is None for t in ("tS1", "tB1", "tM1")), "got %r" % {t: (by.get(t, {}).get("verdict"), by.get(t, {}).get("class")) for t in ("tS1", "tB1", "tM1")})
    s2 = by.get("tS2", {})
    pr = {p.get("row"): (p.get("verdict"), p.get("class")) for p in s2.get("pairs", [])}
    arm("Andrew's case: the Black Diamond row linked on a Schwab tool is MISROUTED (link), its Schwab row ROUTED, the tool MISROUTED (link)",
        pr == {"rowS1": ("ROUTED", None), "rowB1": ("MISROUTED", "link")} and (s2.get("verdict"), s2.get("class")) == ("MISROUTED", "link"), "got %r %r" % (pr, (s2.get("verdict"), s2.get("class"))))
    c1 = by.get("tC1", {})
    arm("the intent check: a Schwab tool whose code reads a Black Diamond source is MISROUTED (code) although its link is right", (c1.get("verdict"), c1.get("class")) == ("MISROUTED", "code") and [p.get("verdict") for p in c1.get("pairs", [])] == ["ROUTED"], "got %r" % c1)
    d1 = by.get("tD1", {})
    arm("the display check: a tool listed under a vendor segment its code does not read is MISROUTED (display)", (d1.get("verdict"), d1.get("class")) == ("MISROUTED", "display"), "got %r" % d1)
    u1 = by.get("tU1", {})
    arm("a tool with no source set reads UNTRACED, never ROUTED", u1.get("verdict") == "UNTRACED", "got %r" % u1)
    arm("every ROUTED or MISROUTED tool carries its source set with a cite per member", all(t.get("source_set") and all(s.get("cite") for s in t["source_set"]) for t in by.values() if t.get("verdict") != "UNTRACED"), "a source set or cite is missing")
    cnt = (doc or {}).get("counts", {})
    arm("counts", (cnt.get("tools"), cnt.get("pairs"), cnt.get("routed_pairs"), cnt.get("link"), cnt.get("code"), cnt.get("display"), cnt.get("untraced")) == (7, 8, 7, 1, 1, 1, 1), "got %r" % cnt)


def r1_ac2(tmp):
    print("DENOMINATOR: three planted negatives on the clean tool tS1; each must be detected with its class; determinism; refusals")
    for kind in ("link", "code", "display"):
        out = os.path.join(tmp, "pl_%s.json" % kind)
        rc, so, se = run([ROUTING_PY, "--census", fx("r1_census.json"), "--catalog", fx("r1_catalog.yaml"), "--sources", fx("r1_sources.json"), "--out", out, "--plant", kind, "--tool", "tS1"])
        doc = jload(out) if os.path.isfile(out) else {}
        t = [x for x in doc.get("tools", []) if x.get("tool") == "tS1"]
        arm("planted %s: detected as MISROUTED (%s), rc 0 and the PLANT line" % (kind, kind), rc == 0 and bool(t) and (t[0].get("verdict"), t[0].get("class")) == ("MISROUTED", kind)
            and line(so, "PLANT") == "PLANT kind=%s tool=tS1 verdict=MISROUTED class=%s" % (kind, kind), "rc=%s %r %r" % (rc, line(so, "PLANT"), t[:1]))
    rc1, _, _, d1 = r1_run(tmp, "a")
    rc2, _, _, d2 = r1_run(tmp, "b")
    arm("two runs give the same bytes", open(os.path.join(tmp, "rt_a.json"), "rb").read() == open(os.path.join(tmp, "rt_b.json"), "rb").read() if d1 and d2 else False, "differs or absent")
    rc, so, se = run([ROUTING_PY, "--census", fx("r1_census.json"), "--catalog", fx("r1_catalog.yaml"), "--sources", fx("r1_sources.json"), "--out", os.path.join(tmp, "x.json"), "--plant", "link", "--tool", "nope"])
    arm("a plant on a tool the census does not serve is refused (rc 2)", rc == 2, "rc=%s" % rc)
    bad = os.path.join(tmp, "bad_sources.json")
    jdump({"schema": "gateway_source_sets/1", "tools": [{"tool": "tS1", "vendors": ["schwab"], "sources": [{"kind": "s3", "bucket": "bkt-s", "vendor": "schwab"}]}]}, bad)
    rc, so, se = run([ROUTING_PY, "--census", fx("r1_census.json"), "--catalog", fx("r1_catalog.yaml"), "--sources", bad, "--out", os.path.join(tmp, "y.json")])
    arm("a source with no cite is refused (rc 2)", rc == 2, "rc=%s" % rc)
    rc, so, se = run([ROUTING_PY, "--census", os.path.join(tmp, "absent.json"), "--catalog", fx("r1_catalog.yaml"), "--sources", fx("r1_sources.json"), "--out", os.path.join(tmp, "z.json")])
    arm("an absent census is refused (rc 2)", rc == 2, "rc=%s" % rc)


# ------------------------------------------------------------------------------------------------ s: source-set data cells
SRC_VENDORS_EXTRA = ("opal", "ycharts", "microsoft", "bloomberg", "other")


def s_scope(channel_ids):
    cen, mm, tools, chan_of = real_scope()
    return cen, tools, sorted({t for c in cen["channels"] if c["id"] in channel_ids for t in c["tools"]})


def catalog_vendors():
    import yaml
    cat = yaml.safe_load(open(os.path.join(APP, "refs", "DATA_CATALOG.yaml"), encoding="utf-8"))
    v = set()
    for sec in ("silver_datasets", "portal_datasets", "harvest_datasets"):
        for r in cat.get(sec) or []:
            if isinstance(r, dict) and isinstance(r.get("vendor"), str):
                v.add(r["vendor"])
    return v | set(SRC_VENDORS_EXTRA)


def cite_ok(text):
    m = re.fullmatch(r"(app/[A-Za-z0-9_./-]+\.py):(\d+)", str(text))
    if not m:
        return None
    f = os.path.join(APP, m.group(1)[len("app/"):])
    if not os.path.isfile(f):
        return None
    txt = open(f, encoding="utf-8", errors="replace").read()
    return txt if 1 <= int(m.group(2)) <= len(txt.split("\n")) else None


def s_ac1(channel_ids):
    cen, tools, scope = s_scope(channel_ids)
    print("DENOMINATOR: %d tool(s) in scope: channels %s; census %s" % (len(scope), ",".join(channel_ids), os.path.basename(CENSUS)))
    path = sys.argv[2] if len(sys.argv) > 2 else None
    arm("a source-set file path was given and exists", bool(path) and os.path.isfile(path), "usage: h_check.py <id> <source_sets.json>")
    if not (path and os.path.isfile(path)):
        return
    doc = jload(path)
    arm("schema", doc.get("schema") == "gateway_source_sets/1" and isinstance(doc.get("tools"), list), "schema=%r" % doc.get("schema"))
    names = [t.get("tool") for t in doc.get("tools", [])]
    arm("every tool in scope appears exactly once, and no other", sorted(names) == scope, "missing=%r extra=%r dup=%r" % (sorted(set(scope) - set(names)), sorted(set(names) - set(scope)), sorted(n for n in set(names) if names.count(n) > 1)))
    arm("every tool has at least one source", all(isinstance(t.get("sources"), list) and t["sources"] for t in doc.get("tools", [])), "a tool has no source")


def s_ac2(channel_ids):
    cen, tools, scope = s_scope(channel_ids)
    print("DENOMINATOR: %d tool(s) in scope; the allowed vendors are the catalog's own plus %s" % (len(scope), ", ".join(SRC_VENDORS_EXTRA)))
    path = sys.argv[2] if len(sys.argv) > 2 else None
    arm("a source-set file path was given and exists", bool(path) and os.path.isfile(path), "usage: h_check.py <id> <source_sets.json>")
    if not (path and os.path.isfile(path)):
        return
    doc = jload(path)
    vendors = catalog_vendors()
    need = {"s3": ("bucket", "prefix"), "store": ("store",), "integration": ("integration",), "graph": ("graph",)}
    bad_shape, bad_vendor, bad_cite, bad_ground, bad_union = [], [], [], [], []
    for t in doc.get("tools", []):
        srcs = t.get("sources") or []
        for s in srcs:
            kind = s.get("kind")
            if kind not in need or not all(isinstance(s.get(k), str) and (k == "prefix" or s[k].strip()) for k in need[kind]):
                bad_shape.append(t.get("tool"))
            if s.get("vendor") not in vendors:
                bad_vendor.append((t.get("tool"), s.get("vendor")))
            txt = cite_ok(s.get("cite"))
            if txt is None:
                bad_cite.append(t.get("tool"))
            else:
                key = s.get("bucket") or s.get("store") or s.get("integration") or s.get("graph")
                if not (isinstance(key, str) and key.strip() and (key in txt or key.replace("-", "_") in txt or key.upper().replace("-", "_") in txt)):
                    bad_ground.append((t.get("tool"), key))
        if sorted({s.get("vendor") for s in srcs}) != sorted(t.get("vendors") or []):
            bad_union.append(t.get("tool"))
    arm("every source has the fields of its kind (s3: bucket and prefix; store; integration; graph)", not bad_shape, "tools %r" % sorted(set(bad_shape))[:6])
    arm("every source vendor is in the allowed vocabulary", not bad_vendor, "got %r" % bad_vendor[:6])
    arm("every cite is app/<file>.py:<line> naming a real line of the gateway source", not bad_cite, "tools %r" % sorted(set(bad_cite))[:6])
    arm("the cited file names the source (the bucket, store, integration or graph string appears in it)", not bad_ground, "got %r" % bad_ground[:6])
    arm("a tool's vendors list equals the set of its sources' vendors", not bad_union, "tools %r" % bad_union[:6])


CHECKS = {
    "h1.AC1": h1_ac1, "h1.AC2": h1_ac2, "h1.AC3": lambda t: arm("pytest", pytest_count(os.path.join(TESTS, "test_partition_windows.py"), 6)),
    "h2.AC1": h2_ac1, "h2.AC2": h2_ac2, "h2.AC3": lambda t: arm("pytest", pytest_count(os.path.join(TESTS, "test_apply_disposition.py"), 8)),
    "h3.AC1": h3_ac1, "h3.AC2": h3_ac2, "h3.AC3": lambda t: arm("pytest", pytest_count(os.path.join(TESTS, "test_index_coverage_explained.py"), 4)),
    "h4.AC1": lambda t: d_ac1(False), "h4.AC2": lambda t: d_ac2(False),
    "h5.AC1": lambda t: d_ac1(True), "h5.AC2": lambda t: d_ac2(True),
    "r1.AC1": r1_ac1, "r1.AC2": r1_ac2, "r1.AC3": lambda t: arm("pytest", pytest_count(os.path.join(TESTS, "test_routing_table.py"), 8)),
    "s1.AC1": lambda t: s_ac1(("opal-data-assets", "schwab", "blackdiamond")), "s1.AC2": lambda t: s_ac2(("opal-data-assets", "schwab", "blackdiamond")),
    "s2.AC1": lambda t: s_ac1(("opal-data-etfs",)), "s2.AC2": lambda t: s_ac2(("opal-data-etfs",)),
    "s3.AC1": lambda t: s_ac1(("opal-data-portal-v2", "opal-data-mdpf", "portal_index")), "s3.AC2": lambda t: s_ac2(("opal-data-portal-v2", "opal-data-mdpf", "portal_index")),
    "s4.AC1": lambda t: s_ac1(("opal-data-harvest", "dynamodb")), "s4.AC2": lambda t: s_ac2(("opal-data-harvest", "dynamodb")),
    "s5.AC1": lambda t: s_ac1(("ycharts", "globgrph", "opal_discover", "opal_portal")), "s5.AC2": lambda t: s_ac2(("ycharts", "globgrph", "opal_discover", "opal_portal")),
    "s6.AC1": lambda t: s_ac1(("m365",)), "s6.AC2": lambda t: s_ac2(("m365",)),
    "h6.AC1": h6_ac1, "h6.AC2": h6_ac2, "h6.AC3": lambda t: arm("pytest", pytest_count(os.path.join(TESTS, "test_tool_battery_route.py"), 5)),
    "k1.AC1": lambda t: k_ac1(("opal-data-etfs",), "K1-"), "k1.AC2": lambda t: k_ac2(("opal-data-etfs",), "K1-", ("opal-data-etfs",)),
    "k2.AC1": lambda t: k_ac1(("opal-data-portal-v2", "opal-data-mdpf", "portal_index"), "K2-"), "k2.AC2": lambda t: k_ac2(("opal-data-portal-v2", "opal-data-mdpf", "portal_index"), "K2-", ("opal-data-portal-v2", "opal-data-mdpf", "portal_index")),
    "k3.AC1": lambda t: k_ac1(("opal-data-assets", "schwab", "blackdiamond"), "K3-"), "k3.AC2": lambda t: k_ac2(("opal-data-assets", "schwab", "blackdiamond"), "K3-", ("opal-data-assets", "schwab", "blackdiamond")),
    "k4.AC1": lambda t: k_ac1(("dynamodb", "globgrph", "opal_discover", "opal_portal"), "K4-"), "k4.AC2": lambda t: k_ac2(("dynamodb", "globgrph", "opal_discover", "opal_portal"), "K4-", ("dynamodb",)),
    "k5.AC1": lambda t: k_ac1(("ycharts",), "K5-"), "k5.AC2": lambda t: k_ac2(("ycharts",), "K5-"),
    "k6.AC1": lambda t: k_ac1(("m365",), "K6-"), "k6.AC2": lambda t: k_ac2(("m365",), "K6-"),
}

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in CHECKS:
        print("usage: h_check.py <%s> [file]" % "|".join(sorted(CHECKS)))
        sys.exit(9)
    with tempfile.TemporaryDirectory(prefix="mx_h_") as tmp:
        CHECKS[cid](tmp)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
