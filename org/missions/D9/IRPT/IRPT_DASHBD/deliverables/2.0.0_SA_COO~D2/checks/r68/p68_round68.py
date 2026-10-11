"""IRPT_DASHBD round 68 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ROUND-68 ANALYSIS @0005d9fd9a, section 4, items 1 to 6.

Cells: DB-b-124 the present state of the nine rows compiled before today; DB-b-125 the thresholds file (claims, tracked at the
handler's path, hash against the served copy); DB-b-126 R45 presented again on current bytes; DB-b-127 the Cottonwood adapter's two
stale statements and the account-id read; DB-b-128 the income reason reworded for the method; DB-b-129 the 244 UNEXPLAINED segments.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB68-1-AC1  ~99/ROW_STATE.json: rows covers exactly the nine row ids; each {state CLOSED_BY_EVIDENCE / STILL_OPEN / NOT_ESTABLISHED,
              evidence [{file (exists), line (int) or commit (hex)}], how READ or RUN}; a NOT_ESTABLISHED carries its reason;
              armed lists the two ARMED rows with disarmed (bool) and what would disarm.
  DB68-2-AC1  ~100/THRESHOLDS_FILE.json: handler_paths (the paths the handler reads, with file and line); tracked_at (one of them,
              an existing tracked-path file); claims has the five threshold keys, each measured/inferred/held/absent with a reason;
              served_copy {address, read (bool), sha256 or denial}; tracked_sha256 equals the file's; equal_to_served is true, false
              or "NOT_ESTABLISHED" with a reason; s3_writes == 0; tests {passed > 0, failed == 0}.
  DB68-3-AC1  ~101/NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH_3.md exists; ~101/R45_REFRESH3.json: packet {path, sha256 (the file's)};
              members lists the release's files, each {file, pin (hex), sha256}; sources_json {pin, declares_method_version_for_49f true};
              kit {method_version_equal_rows, rows, equal (bool)}; manifest_fields {method_version, valuation_source, fee_treatment,
              price_basis}, none of them the literal "absent" unless stated with a reason; s3_writes == 0.
  DB68-4-AC1  ~102/COTTONWOOD_ADAPTER.json: stale_statements has two entries {where, before, after}; row3_sentences {read (int > 0),
              false_for_cottonwood (list), each with a disposition}; account_id {measured (bool), gold_form, directory_form, joins
              (true / false / "NOT_ESTABLISHED"), how, counts_only true}; tests {passed > 0, failed == 0}.
  DB68-5-AC1  ~103/INCOME_REASON.json: reason_before and reason_after differ; reason_after names no single channel (channels_named == []);
              rule24 {mece, same_grain, intent_coherence, state_coherence} each with a finding; reader_named {file, line}; packet
              {path (exists), sha256 (the file's), object_address}; tests {passed > 0, failed == 0}; s3_writes == 0.
  DB68-6-AC1  ~104/UNEXPLAINED_244.json: denominator == 244; classes non-empty [{cause, count, rule, example_segment_ref}], counts
              sum with remainder to 244; remainder {count, why}; method {source, how}; no figure of any client (client_figures == 0).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~"
HEX = re.compile(r"^[0-9a-f]{7,64}$")
NINE = ["IRPT_DASHBD-D2-W86-S1", "IRPT_DASHBD-D2-W86-S2", "IRPT_DASHBD-D2-W87-S1", "IRPT_DASHBD-D2-W85-S1", "IRPT_DASHBD-D2-W88-S1",
        "IRPT_DASHBD-D2-W88-S3", "IRPT_DASHBD-D2-W89-S1", "IRPT_DASHBD-D2-W96-S2", "IRPT_DASHBD-D2-W96-S3"]
CLAIMS = ("measured", "inferred", "held", "absent")
KEYS = ("tolerance", "large_flow_share", "plausibility_band_low", "plausibility_band_high", "comparability_max_excluded_weight")
POST = {"mece", "same_grain", "intent_coherence", "state_coherence"}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB68"))
        sys.exit(1)

    def text(v):
        return str(v or "").strip()

    def load(n, name):
        p = root / (D + "%d/%s" % (n, name))
        if not p.is_file():
            fail("no record %s" % name)
        return json.loads(p.read_bytes().decode("utf-8"))

    def sha(rel):
        p = root / text(rel)
        return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None

    def tests_ok(t):
        return isinstance((t or {}).get("passed"), int) and t["passed"] > 0 and t.get("failed") == 0

    if cid == "DB68-1-AC1":
        r = load(99, "ROW_STATE.json")
        rows = r.get("rows") or []
        if sorted(text(x.get("id")) for x in rows) != sorted(NINE):
            fail("rows do not cover exactly the nine ids (%d given)" % len(rows))
        for x in rows:
            if x.get("state") not in ("CLOSED_BY_EVIDENCE", "STILL_OPEN", "NOT_ESTABLISHED") or x.get("how") not in ("READ", "RUN"):
                fail("%s state %r how %r" % (x.get("id"), x.get("state"), x.get("how")))
            if x["state"] == "NOT_ESTABLISHED":
                if not text(x.get("reason")):
                    fail("%s is NOT_ESTABLISHED without a reason" % x.get("id"))
                continue
            ev = x.get("evidence") or []
            if not ev:
                fail("%s carries no evidence" % x.get("id"))
            for e in ev:
                ok_file = text(e.get("file")) and (root / text(e.get("file"))).is_file() and isinstance(e.get("line"), int)
                if not ok_file and not HEX.match(text(e.get("commit"))):
                    fail("%s evidence %r names neither a file with a line nor a commit" % (x.get("id"), e))
        armed = {text(a.get("id")): a for a in (r.get("armed") or [])}
        for i in ("IRPT_DASHBD-D2-W88-S1", "IRPT_DASHBD-D2-W88-S3"):
            a = armed.get(i) or {}
            if not isinstance(a.get("disarmed"), bool) or not text(a.get("what_disarms")):
                fail("armed row %s lacks disarmed or what_disarms" % i)
        n = {}
        for x in rows:
            n[x["state"]] = n.get(x["state"], 0) + 1
        print("OK: nine rows read at their present state %r; the two ARMED rows carry their disarm" % n)
    elif cid == "DB68-2-AC1":
        r = load(100, "THRESHOLDS_FILE.json")
        hp = r.get("handler_paths") or []
        ta = text(r.get("tracked_at"))
        if not hp or ta not in [text(x.get("path")) for x in hp] or not (root / ta).is_file():
            fail("tracked_at %r is not an existing file at one of the handler's paths" % ta)
        cl = r.get("claims") or {}
        for k in KEYS:
            c = cl.get(k) or {}
            if c.get("claim") not in CLAIMS or not text(c.get("reason")):
                fail("threshold %s lacks a claim of %r with a reason" % (k, CLAIMS))
        if r.get("tracked_sha256") != sha(ta):
            fail("tracked_sha256 is not the file's")
        sc = r.get("served_copy") or {}
        if not text(sc.get("address")) or not isinstance(sc.get("read"), bool) or not (text(sc.get("sha256")) or text(sc.get("denial"))):
            fail("served_copy %r" % sc)
        eq = r.get("equal_to_served")
        if eq not in (True, False, "NOT_ESTABLISHED") or (eq is not True and not text(r.get("equal_reason"))):
            fail("equal_to_served %r without its reason" % eq)
        if r.get("s3_writes") != 0 or not tests_ok(r.get("tests")):
            fail("s3_writes %r or tests %r" % (r.get("s3_writes"), r.get("tests")))
        print("OK: the thresholds file is tracked at %s with five claims; equal to the served copy: %s; no S3 write" % (ta, eq))
    elif cid == "DB68-3-AC1":
        r = load(101, "R45_REFRESH3.json")
        pk = r.get("packet") or {}
        if not text(pk.get("path")).endswith("NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH_3.md") or sha(pk.get("path")) is None or pk.get("sha256") != sha(pk.get("path")):
            fail("packet %r" % pk.get("path"))
        ms = r.get("members") or []
        if not ms or any(not text(m.get("file")) or not HEX.match(text(m.get("pin"))) or not HEX.match(text(m.get("sha256"))) for m in ms):
            fail("members must each carry file, pin and sha256")
        sj = r.get("sources_json") or {}
        if not HEX.match(text(sj.get("pin"))) or sj.get("declares_method_version_for_49f") is not True:
            fail("sources_json %r" % sj)
        k = r.get("kit") or {}
        if not isinstance(k.get("rows"), int) or not isinstance(k.get("method_version_equal_rows"), int) or not isinstance(k.get("equal"), bool):
            fail("kit %r" % k)
        mf = r.get("manifest_fields") or {}
        for f in ("method_version", "valuation_source", "fee_treatment", "price_basis"):
            if f not in mf or (mf[f] == "absent" and not text((r.get("manifest_absent_reasons") or {}).get(f))):
                fail("manifest field %s missing, or absent without a reason" % f)
        if r.get("s3_writes") != 0:
            fail("s3_writes %r" % r.get("s3_writes"))
        print("OK: R45 presented on %d member(s) at their pins; sources.json declares method_version for 49F; kit equal: %s (%d of %d rows)"
              % (len(ms), k["equal"], k["method_version_equal_rows"], k["rows"]))
    elif cid == "DB68-4-AC1":
        r = load(102, "COTTONWOOD_ADAPTER.json")
        st = r.get("stale_statements") or []
        if len(st) != 2 or any(not text(s.get("where")) or not text(s.get("before")) or not text(s.get("after")) or s["before"] == s["after"] for s in st):
            fail("stale_statements wants two entries, each with where, before and a different after")
        rs = r.get("row3_sentences") or {}
        if not isinstance(rs.get("read"), int) or rs["read"] <= 0 or not isinstance(rs.get("false_for_cottonwood"), list) \
                or any(not text(s.get("sentence")) or not text(s.get("disposition")) for s in rs["false_for_cottonwood"]):
            fail("row3_sentences %r" % {k: rs.get(k) for k in ("read",)})
        a = r.get("account_id") or {}
        if not isinstance(a.get("measured"), bool) or a.get("joins") not in (True, False, "NOT_ESTABLISHED") or not text(a.get("how")) or a.get("counts_only") is not True:
            fail("account_id %r" % a)
        if a["measured"] and (not text(a.get("gold_form")) or not text(a.get("directory_form"))):
            fail("a measured account_id read names both forms")
        if not tests_ok(r.get("tests")):
            fail("tests %r" % r.get("tests"))
        print("OK: two stale statements corrected; %d row-3 sentence(s) read, %d false for Cottonwood; the account ids join: %s"
              % (rs["read"], len(rs["false_for_cottonwood"]), a["joins"]))
    elif cid == "DB68-5-AC1":
        r = load(103, "INCOME_REASON.json")
        if not text(r.get("reason_before")) or not text(r.get("reason_after")) or r["reason_before"] == r["reason_after"] or r.get("channels_named") != []:
            fail("reason_before / reason_after / channels_named")
        ps = r.get("rule24") or {}
        if set(ps) != POST or any(not text(ps[k].get("finding")) for k in ps):
            fail("rule24 %r" % sorted(ps))
        rn = r.get("reader_named") or {}
        if not text(rn.get("file")) or not isinstance(rn.get("line"), int):
            fail("reader_named %r" % rn)
        pk = r.get("packet") or {}
        if sha(pk.get("path")) is None or pk.get("sha256") != sha(pk.get("path")) or not text(pk.get("object_address")):
            fail("packet %r" % pk.get("path"))
        if r.get("s3_writes") != 0 or not tests_ok(r.get("tests")):
            fail("s3_writes %r or tests %r" % (r.get("s3_writes"), r.get("tests")))
        print("OK: the income reason is worded for the method; its reader is named; the packet is bound; no S3 write")
    elif cid == "DB68-6-AC1":
        r = load(104, "UNEXPLAINED_244.json")
        cs = r.get("classes") or []
        rem = r.get("remainder") or {}
        if r.get("denominator") != 244 or not cs or any(not text(c.get("cause")) or not isinstance(c.get("count"), int) or not text(c.get("rule")) for c in cs):
            fail("denominator %r or classes malformed" % r.get("denominator"))
        if not isinstance(rem.get("count"), int) or sum(c["count"] for c in cs) + rem["count"] != 244 or (rem["count"] and not text(rem.get("why"))):
            fail("the classes and the remainder do not sum to 244, or the remainder has no reason")
        m = r.get("method") or {}
        if not text(m.get("source")) or not text(m.get("how")) or r.get("client_figures") != 0:
            fail("method or client_figures")
        print("OK: 244 segments: %d class(es) holding %d, remainder %d" % (len(cs), sum(c["count"] for c in cs), rem["count"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
