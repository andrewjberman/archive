"""IRPT_DASHBD round 37 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-36 ADDENDUM 5 (on ADJUDICATION_v21 @37daf4f637), PRD v0.9.

Cells: DB-b-73 the realized-lot key + a population re-size on the kit; DB-b-74 the R37 release packet with EVERY bundle member pinned
at HEAD bytes (rows W47-S4, S5); DB-b-75 the Orion custody-master registry row for Inflection; DB-b-76 Inflection's like-for-like
compounded GROSS tie-out with fees as their own figures, sliced (Andrew @669ab7d677); DB-b-77 the rule-24 amendment proposal for the two
Orion flow classes (row W49-S3).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB37-1-AC1  ~50/LOTS_KEY_E1.json repeat_census {day "2026-10-07", pairs int > 0, differing_columns non-empty list}; new_key a list that
              contains the old key (firm, account_id, business_date, lot_id, quantity) plus at least one more column; the HEAD contract
              org/standards/IRPT_DASHBD_ACCOUNT_LOT_REALIZED_CONTRACT.json primary_key equals new_key.
  DB37-1-AC2  the record's kit_runs: days 2026-10-06 and 2026-10-07, each {accounts >= 7000, refusals == 0, lots_rows > 0, peak_mb number,
              total_s number}; runtime.pandas == "2.2.3".
  DB37-1-AC3  the record's tests {passed > 0, failed == 0, new_test "<file>::<function>"} with that function defined in that file at HEAD.
  DB37-2-AC1  ~51/NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE_R37.md: a pins table, one row per member of the source-map entry
              irpt-49f-reporting-gold-lambda staged_from at HEAD (`| `<repo_path>` | `<pin>` | `<sha256>` |`), every row's sha256 equal to
              both `git show <pin>:<path>` and HEAD's bytes, and every staged_from member covered.
  DB37-2-AC2  the packet prints, beside the sizing, each kit_runs day's peak_mb and total_s from ~50's record and "refusals: 0".
  DB37-2-AC3  the packet carries "Rollback, per key", "Writers of the property", "BRANCH A", "BRANCH B", and both halves read UNSIGNED.
  DB37-3-AC1  infra/logic/registry/scopes.json carries a MASTER row with firm "inflection" and vendor "orion", and the inflection FIRM row's
              masters list names it.
  DB37-3-AC2  ~52/ORION_MASTER_ROW.json names that key, and lib/opal_naming.lookup(<key>) returns firm "inflection" (imported from root).
  DB37-3-AC3  the record's landing {prefix non-empty, objects int > 0, read_at non-empty}: where that master's data lands, read by listing.
  DB37-4-AC1  ~53/INF_GROSS_FEE_TIEOUT.json comparison_basis "gross", comparison_source non-empty, accounts int >= 1, denominator int > 0,
              within int in [0, denominator], tolerance_pp == 0.35.
  DB37-4-AC2  fee_source non-empty; fee_slices carries the six keys supervised, unsupervised, supervision_total, billed, unbilled,
              billing_total, each a number or a string starting "ABSENT:".
  DB37-4-AC3  misses: length denominator - within, every class in the declared classes, none UNCLASSED; flagged_classes: a non-empty
              list of {class, count int} (the two W49-S3 classes, mapped by the ratified taxonomy and flagged).
  DB37-5-AC1  ~54/ORION_TAXONOMY_AMENDMENT_PROPOSAL.md carries the four postulate headings: MECE, SAME GRAIN, INTENT COHERENCE,
              STATE COHERENCE.
  DB37-5-AC2  ~54/TOKEN_CENSUS.json census: a non-empty list of {token, hits int, files_scanned int > 0}.
  DB37-5-AC3  ~54/MEASURED_EFFECT.json {denominator int > 0, within_ratified int, within_proposed int, both in [0, denominator]}.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~"
OLD_KEY = ["firm", "account_id", "business_date", "lot_id", "quantity"]
PIN_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]{7,40})`\s*\|\s*`([0-9a-f]{64})`\s*\|\s*$", re.M)
SLICES = ["supervised", "unsupervised", "supervision_total", "billed", "unbilled", "billing_total"]
POSTULATES = ["MECE", "SAME GRAIN", "INTENT COHERENCE", "STATE COHERENCE"]


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB37"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    def text(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return p.read_bytes().decode("utf-8")

    def classed(r):
        n, w, cl, ms = r.get("denominator"), r.get("within"), r.get("classes"), r.get("misses")
        if not isinstance(n, int) or not isinstance(w, int) or not isinstance(cl, list) or not cl or not isinstance(ms, list):
            fail("denominator %r / within %r / classes %r / misses %s" % (n, w, cl, type(ms).__name__))
        if len(ms) != n - w:
            fail("%d misses listed, %d expected" % (len(ms), n - w))
        bad = [x for x in ms if not isinstance(x, dict) or x.get("class") not in cl or x.get("class") == "UNCLASSED"]
        if bad:
            fail("%d miss(es) unclassed: %r" % (len(bad), bad[:3]))
        return len(ms)

    if cid == "DB37-1-AC1":
        r = load(D + "50/LOTS_KEY_E1.json")
        c = r.get("repeat_census") or {}
        if c.get("day") != "2026-10-07" or not isinstance(c.get("pairs"), int) or c["pairs"] <= 0 \
                or not isinstance(c.get("differing_columns"), list) or not c["differing_columns"]:
            fail("repeat_census %r" % c)
        nk = r.get("new_key")
        if not isinstance(nk, list) or not set(OLD_KEY) <= set(nk) or len(nk) <= len(OLD_KEY):
            fail("new_key %r must extend %r" % (nk, OLD_KEY))
        ck = load("org/standards/IRPT_DASHBD_ACCOUNT_LOT_REALIZED_CONTRACT.json").get("primary_key")
        if ck != nk:
            fail("contract primary_key %r != new_key %r" % (ck, nk))
        print("OK: %d repeat pair(s) on 2026-10-07 differ in %r; key extended to %r (contract equal)" % (c["pairs"], c["differing_columns"], nk))
    elif cid == "DB37-1-AC2":
        r = load(D + "50/LOTS_KEY_E1.json")
        if (r.get("runtime") or {}).get("pandas") != "2.2.3":
            fail("runtime %r is not the pandas 2.2.3 kit" % r.get("runtime"))
        kr = r.get("kit_runs") or {}
        for day in ("2026-10-06", "2026-10-07"):
            x = kr.get(day) or {}
            if not isinstance(x.get("accounts"), int) or x["accounts"] < 7000 or x.get("refusals") != 0 \
                    or not isinstance(x.get("lots_rows"), int) or x["lots_rows"] <= 0 or not num(x.get("peak_mb")) or not num(x.get("total_s")):
                fail("kit_runs[%s] %r" % (day, x))
        print("OK: kit runs " + "; ".join("%s %d accts, lots_rows %d, %s MB, %s s, refusals 0" % (d, kr[d]["accounts"], kr[d]["lots_rows"], kr[d]["peak_mb"], kr[d]["total_s"]) for d in ("2026-10-06", "2026-10-07")))
    elif cid == "DB37-1-AC3":
        t = load(D + "50/LOTS_KEY_E1.json").get("tests") or {}
        if not isinstance(t.get("passed"), int) or t["passed"] <= 0 or t.get("failed") != 0:
            fail("tests %r" % t)
        m = re.fullmatch(r"([^:]+\.py)::(\w+)", str(t.get("new_test") or ""))
        if not m or not re.search(r"^def %s\(" % re.escape(m.group(2)), text(m.group(1)), re.M):
            fail("new_test %r is not a function defined in that file" % t.get("new_test"))
        print("OK: tests %d passed, 0 failed; new test %s" % (t["passed"], t["new_test"]))
    elif cid in ("DB37-2-AC1", "DB37-2-AC2", "DB37-2-AC3"):
        pk = text(D + "51/NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE_R37.md")
        if cid == "DB37-2-AC1":
            sm = load("infra/aws/lambda/ci/lambda-source-map.json")
            members = {m["repo_path"] for m in ((sm.get("functions") or {}).get("irpt-49f-reporting-gold-lambda") or {}).get("staged_from", [])}
            rows = PIN_ROW.findall(pk)
            if not members or not rows:
                fail("%d staged_from member(s), %d pin row(s)" % (len(members), len(rows)))
            bad = []
            for path, pin, sha in rows:
                head = root / path
                at_pin = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (pin, path)], capture_output=True)
                if not head.is_file() or at_pin.returncode != 0 or hashlib.sha256(head.read_bytes()).hexdigest() != sha \
                        or hashlib.sha256(at_pin.stdout).hexdigest() != sha:
                    bad.append(path)
            missing = sorted(members - {p for p, _, _ in rows})
            if bad or missing:
                fail("pin rows not equal to HEAD and pin bytes: %r; staged_from members with no row: %r" % (bad[:5], missing[:5]))
            print("OK: %d pin rows, every one equal at HEAD and at its pin; %d staged_from member(s) covered" % (len(rows), len(members)))
        elif cid == "DB37-2-AC2":
            kr = load(D + "50/LOTS_KEY_E1.json").get("kit_runs") or {}
            for day in ("2026-10-06", "2026-10-07"):
                x = kr.get(day) or {}
                for v in (x.get("peak_mb"), x.get("total_s")):
                    if not num(v) or str(v) not in pk:
                        fail("the packet does not print %s's %r" % (day, v))
            if not re.search(r"refusals:\s*0\b", pk):
                fail("no 'refusals: 0' line")
            print("OK: packet prints both kit days' peak and time, and refusals: 0")
        else:
            for s in ("Rollback, per key", "Writers of the property", "BRANCH A", "BRANCH B"):
                if s not in pk:
                    fail("section %r missing" % s)
            if len(re.findall(r"^## (CTO|COO) half.*\n+UNSIGNED", pk, re.M)) != 2:
                fail("both halves must read UNSIGNED")
            print("OK: sections present, both halves UNSIGNED")
    elif cid in ("DB37-3-AC1", "DB37-3-AC2", "DB37-3-AC3"):
        sc = {x["key"]: x for x in load("infra/logic/registry/scopes.json")["scopes"]}
        r = load(D + "52/ORION_MASTER_ROW.json")
        key = r.get("key")
        row = sc.get(key) or {}
        if cid == "DB37-3-AC1":
            if row.get("class") != "MASTER" or row.get("firm") != "inflection" or row.get("vendor") != "orion":
                fail("row %r for key %r" % ({k: row.get(k) for k in ("class", "firm", "vendor")}, key))
            if key not in (sc.get("inflection") or {}).get("masters", []):
                fail("inflection's masters %r do not name %r" % ((sc.get("inflection") or {}).get("masters"), key))
            print("OK: MASTER %s -> inflection / orion, named in inflection.masters" % key)
        elif cid == "DB37-3-AC2":
            sys.path.insert(0, str(root))
            try:
                from lib.opal_naming import lookup
                got = lookup(key)
            except Exception as e:  # the builder's own refusal is the evidence
                fail("lookup(%r) raised %r" % (key, e))
            firm = got.get("firm") if isinstance(got, dict) else getattr(got, "firm", None)
            if firm != "inflection":
                fail("lookup(%r) firm %r" % (key, firm))
            print("OK: lookup(%r) -> firm inflection" % key)
        else:
            ld = r.get("landing") or {}
            if not str(ld.get("prefix") or "").strip() or not isinstance(ld.get("objects"), int) or ld["objects"] <= 0 or not ld.get("read_at"):
                fail("landing %r" % ld)
            print("OK: %s lands under %s (%d objects, read %s)" % (key, ld["prefix"], ld["objects"], ld["read_at"]))
    elif cid in ("DB37-4-AC1", "DB37-4-AC2", "DB37-4-AC3"):
        r = load(D + "53/INF_GROSS_FEE_TIEOUT.json")
        if cid == "DB37-4-AC1":
            a, n, w = r.get("accounts"), r.get("denominator"), r.get("within")
            if r.get("comparison_basis") != "gross" or not str(r.get("comparison_source") or "").strip() or not isinstance(a, int) or a < 1 \
                    or not isinstance(n, int) or n <= 0 or not isinstance(w, int) or not 0 <= w <= n or r.get("tolerance_pp") != 0.35:
                fail("basis %r, source %r, accounts %r, denominator %r, within %r, tolerance %r" % (
                    r.get("comparison_basis"), r.get("comparison_source"), a, n, w, r.get("tolerance_pp")))
            print("OK: gross vs %s: %d of %d within 0.35 pp over %d account(s)" % (r["comparison_source"], w, n, a))
        elif cid == "DB37-4-AC2":
            fs = r.get("fee_slices")
            if not str(r.get("fee_source") or "").strip() or not isinstance(fs, dict):
                fail("fee_source %r / fee_slices %r" % (r.get("fee_source"), fs))
            bad = [k for k in SLICES if not (num(fs.get(k)) or str(fs.get(k) or "").startswith("ABSENT:"))]
            if bad:
                fail("fee slices not a number or 'ABSENT: <reason>': %r" % bad)
            print("OK: fee source %s; slices %s" % (r["fee_source"], ", ".join("%s=%s" % (k, fs[k] if num(fs[k]) else "ABSENT") for k in SLICES)))
        else:
            k = classed(r)
            fc = r.get("flagged_classes")
            if not isinstance(fc, list) or not fc or any(not isinstance(x, dict) or not x.get("class") or not isinstance(x.get("count"), int) for x in fc):
                fail("flagged_classes %r" % fc)
            print("OK: %d misses classed; flagged %r" % (k, [(x["class"], x["count"]) for x in fc]))
    elif cid == "DB37-5-AC1":
        t = text(D + "54/ORION_TAXONOMY_AMENDMENT_PROPOSAL.md")
        miss = [p for p in POSTULATES if not re.search(r"^#+ .*%s" % re.escape(p), t, re.M | re.I)]
        if miss:
            fail("postulate heading(s) missing: %r" % miss)
        print("OK: the four postulate headings are present")
    elif cid == "DB37-5-AC2":
        c = load(D + "54/TOKEN_CENSUS.json").get("census")
        if not isinstance(c, list) or not c or any(not isinstance(x, dict) or not x.get("token") or not isinstance(x.get("hits"), int)
                                                    or not isinstance(x.get("files_scanned"), int) or x["files_scanned"] <= 0 for x in c):
            fail("census %r" % (c if not isinstance(c, list) else c[:3]))
        print("OK: %d token(s) censused, e.g. %r" % (len(c), [(x["token"], x["hits"], x["files_scanned"]) for x in c[:3]]))
    elif cid == "DB37-5-AC3":
        m = load(D + "54/MEASURED_EFFECT.json")
        n, a, b = m.get("denominator"), m.get("within_ratified"), m.get("within_proposed")
        if not isinstance(n, int) or n <= 0 or not isinstance(a, int) or not isinstance(b, int) or not 0 <= a <= n or not 0 <= b <= n:
            fail("measured effect %r" % m)
        print("OK: within %d (ratified) vs %d (proposed) of %d" % (a, b, n))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
