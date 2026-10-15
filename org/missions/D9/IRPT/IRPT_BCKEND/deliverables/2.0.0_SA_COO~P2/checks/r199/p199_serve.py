"""IRPT_BCKEND round 199 (workstream ~P) -- the serve-path design check IB199-3 (IB-pr-551), imported by p199_cells.py.

  IB199-3  IB-pr-551  hops 2-4 of the filled-report serve path as ONE never-widen pair: the design record and the packet, both halves UNSIGNED (READ ONLY)
    AC1  hops 2 (platinum publisher), 3 (the /report route) and 4 (the export source kind) each name the files to change, each file site read at HEAD, nothing existing today
    AC2  the input contract (the builder's document, contract 0.5.1), the scope rule, the blast radius, the rollback per key, the first exercise on 49 Financial
    AC3  the packet exists with its phrases and both halves UNSIGNED, the build slices are LOCAL cells with files, notes, counters 0, no long digit run
"""
import json
import re

import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.9.0_WK_IRPT_BCKEND~395/IB199-3_serve_path_design.json"
PKT = D + "0.9.0_WK_IRPT_BCKEND~395/SERVE_PATH_PAIR_PACKET_V1.md"
ROUTE = "/api/scoped/investor-reporting/reporting/client/{client_id}/report"
CONTRACT = "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
CLAIMS = ("measured", "inferred", "absent")
fail, load, is_int, counters, no_long_digits, git_show = P6.fail, P6.load, P6.is_int, P6.counters, P6.no_long_digits, P6.git_show


def site_ok(f, what):
    m = isinstance(f, dict) and f.get("path")
    if not m or not is_int(f.get("line")) or not isinstance(f.get("identifier"), str) or not f["identifier"]:
        fail("%s: each file needs path, line and the identifier on that line" % what)
    src = git_show("HEAD", f["path"])
    if src is None:
        fail("%s: %s does not exist at HEAD" % (what, f["path"]))
    lines = src.decode("utf-8", "replace").splitlines()
    if f["line"] < 1 or f["line"] > len(lines) or f["identifier"] not in lines[f["line"] - 1]:
        fail("%s: %s:%s does not hold %r" % (what, f["path"], f["line"], f["identifier"]))


def c1():
    r = load(REC)
    if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("base_commit", ""))):
        fail("base_commit must be a 40-hex commit")
    hops = r.get("hops")
    if not isinstance(hops, dict) or sorted(hops) != ["2", "3", "4"]:
        fail("hops must hold exactly 2, 3 and 4")
    for k, h in hops.items():
        if h.get("exists_today") is not False or h.get("risk") not in ("SERVED", "WORLD"):
            fail("hop %s: nothing exists today and the risk is SERVED or WORLD" % k)
        if not isinstance(h.get("what"), str) or len(h["what"]) < 40:
            fail("hop %s: state what changes" % k)
        files = h.get("files")
        if not isinstance(files, list) or not files:
            fail("hop %s: name the files to change" % k)
        for f in files:
            site_ok(f, "hop %s" % k)
    h2, h3, h4 = hops["2"], hops["3"], hops["4"]
    if "opal_naming" not in json.dumps(h2) or not isinstance(h2.get("address_builder_output"), str) or "client=" not in h2["address_builder_output"]:
        fail("hop 2: the new object's address is the naming builder's output for client=<id> (never typed by hand), and a registry row need is stated")
    if not isinstance(h2.get("registry_row_needed"), bool):
        fail("hop 2: registry_row_needed must be true or false")
    if h3.get("path_template") != ROUTE:
        fail("hop 3: the route is %s" % ROUTE)
    if not isinstance(h4.get("source_kind"), str) or len(h4["source_kind"]) < 4:
        fail("hop 4: name the export source kind")
    print("OK: hops 2 to 4 with file sites read at HEAD")


def c2():
    r = load(REC)
    ic = r.get("input_contract") or {}
    d = ic.get("document_shape") or {}
    if d.get("contract") != CONTRACT or d.get("version") != "0.5.1" or d.get("key") != "document" or d.get("sha256_prefix") != "0b515243b310":
        fail("input_contract.document_shape must name %s 0.5.1, key document, sha256 prefix 0b515243b310" % CONTRACT)
    if ic.get("claim") not in CLAIMS or not isinstance(ic.get("source"), str) or len(ic["source"]) < 40:
        fail("input_contract needs the source of the document (who writes it and where it lands) and a claim")
    if not isinstance(r.get("scope_rule"), str) or "every account" not in r["scope_rule"].lower():
        fail("scope_rule must state that the viewer's scope covers EVERY account the document names")
    b = r.get("blast_radius") or {}
    if not isinstance(b.get("writes"), list) or not b["writes"] or not isinstance(b.get("reads"), list) or b.get("new_iam") not in (True, False):
        fail("blast_radius needs writes, reads and new_iam")
    for k in ("served_values_changed", "existing_routes_changed"):
        if b.get(k) is not False:
            fail("blast_radius.%s must read false: a new route and object change no existing served value" % k)
    if not isinstance(r.get("rollback_per_key"), str) or len(r["rollback_per_key"]) < 40:
        fail("rollback_per_key must be stated per key")
    fe = r.get("first_exercise") or {}
    if fe.get("firm") != "49financial" or fe.get("order") != "first":
        fail("the first exercise is 49 Financial first")
    print("OK: input contract, scope rule, blast radius, rollback, first exercise")


def c3():
    r = load(REC)
    f = P6.ROOT / PKT
    if not f.is_file():
        fail("no packet at %s" % PKT)
    t = f.read_text(encoding="utf-8")
    low = t.lower()
    if len(t) < 6000:
        fail("the packet must be at least 6,000 characters")
    for need in ("never-widen", "hop 2", "hop 3", "hop 4", "blast radius", "rollback", "49 financial", "stop rule", "coo half", "cto half", "opal_naming"):
        if need not in low:
            fail("the packet does not carry %r" % need)
    if len(re.findall(r"unsigned", low)) < 2:
        fail("both halves must read UNSIGNED")
    sl = r.get("build_slices")
    if not isinstance(sl, list) or len(sl) < 2:
        fail("build_slices needs at least two proposed LOCAL cells")
    for s in sl:
        if s.get("risk") != "LOCAL" or not isinstance(s.get("cell"), str) or not isinstance(s.get("files"), list) or not s["files"]:
            fail("each build slice is a LOCAL cell with the files it writes")
    counters(r)
    no_long_digits(json.dumps(r))
    no_long_digits(t)
    print("OK: the packet, both halves unsigned, the build slices, counters 0")


CHECKS = {"IB199-3-AC1": c1, "IB199-3-AC2": c2, "IB199-3-AC3": c3}
