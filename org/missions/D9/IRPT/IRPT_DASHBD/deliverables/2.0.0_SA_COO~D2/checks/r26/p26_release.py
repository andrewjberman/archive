"""IRPT_DASHBD round 26 (workstream B, issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-25 analysis @3543da2f4d: E1 prepares the
release of the activity and lot tables (W20-S1, W20-S3, W22-S3 folded in); E2 reads whether a served input can carry a repeated index
label (W22-S5). No apply, no S3 write.

Usage: python <this file> <repo_root> <criterion_id>
  DB26-1-AC1  the three contracts under org/standards/ name every column the producer's SCHEMAS carry and no other (0 unnamed either
              way); each carries a non-empty `primary_key` whose members are its columns (W20-S3); both lot contracts carry
              `enums.basis_source` with WASH_SALE_EXCLUDED_BASIS among its members (W22-S3). Base: FAIL.
  DB26-1-AC2  the release packet prints every new address exactly as lib/opal_naming.py returns it (recomputed here through the
              producer's builder_output for the declared firm), and the producer carries no custodian table name as a literal
              (fact_rld / fact_uln / fact_ult / fact_trn): they come from sources.json, which carries them (W20-S1). Base: FAIL.
  DB26-1-AC3  the release packet names the root infra/aws/terraform/investor-reporting/reporting-gold, a TARGETED plan
              (`terraform plan` with `-target=`), the expected plan counts, both branches (`## BRANCH A` and `## BRANCH B`), the
              rollback per key, and the unapplied account_class_daily release it carries. Base: FAIL.
  DB26-2-AC1  REPEATED_INDEX_E2.json: partitions_read > 0 over the served producer's sources, frames_read > 0,
              repeated_label_frames (int) and verdict CAN | CANNOT agreeing with it; on CAN, a test whose name contains
              "repeated_index" in tests/test_account_return_daily_none.py passes. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

G = "data/assets/scripts/gold/irpt_reporting/"
PRODUCER = G + "account_activity_lots.py"
SOURCES = G + "sources.json"
NONE_TESTS = G + "tests/test_account_return_daily_none.py"
STD = "org/standards/IRPT_DASHBD_%s_CONTRACT.json"
CONTRACTS = {"account_activity_daily": "ACCOUNT_ACTIVITY_DAILY", "account_lot_realized": "ACCOUNT_LOT_REALIZED",
             "account_lot_unrealized_daily": "ACCOUNT_LOT_UNREALIZED_DAILY"}
LOTS = ("account_lot_realized", "account_lot_unrealized_daily")
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
PACKET = D + "0.9.0_WK_IRPT_DASHBD~23/NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE.md"
REPEAT = D + "0.9.0_WK_IRPT_DASHBD~24/REPEATED_INDEX_E2.json"
ROOT_TF = "infra/aws/terraform/investor-reporting/reporting-gold"
CUSTODIAN_TABLES = ("fact_rld", "fact_uln", "fact_ult", "fact_trn")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB26"))
        sys.exit(1)

    def text(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return p.read_bytes().decode("utf-8")

    def producer():
        sys.path.insert(0, str(root / G))
        spec = importlib.util.spec_from_file_location("aal_check", str(root / PRODUCER))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m

    if cid == "DB26-1-AC1":
        m = producer()
        for t, c in CONTRACTS.items():
            doc = json.loads(text(STD % c))
            named = {col["name"] for col in doc.get("columns") or []}
            built = {f.name for f in m.SCHEMAS[t]}
            if named != built:
                fail("%s: unnamed in contract %s; in contract, not built %s" % (t, sorted(built - named), sorted(named - built)))
            pk = doc.get("primary_key") or []
            if not pk or [k for k in pk if k not in built]:
                fail("%s: primary_key %r empty or names a non-column" % (t, pk))
            if t in LOTS:
                members = (doc.get("enums") or {}).get("basis_source")
                vals = members if isinstance(members, list) else list((members or {}).keys()) if isinstance(members, dict) else []
                if "WASH_SALE_EXCLUDED_BASIS" not in vals:
                    fail("%s: enums.basis_source %r lacks WASH_SALE_EXCLUDED_BASIS" % (t, members))
            print("  %-30s %d columns named, 0 unnamed; key %s" % (t, len(built), pk))
        print("OK: 3 contracts name every built column and key; basis_source carried on both lot contracts")
    elif cid == "DB26-1-AC2":
        m = producer()
        pkt = text(PACKET)
        doc = m.ard.load_declaration()
        firm = m.ard.firm_scope(m.ard.source_entry(doc, m.ard.declared_sources(doc)[0]))
        rows = m.builder_output(firm, "2000-01-01")
        want = [r["output"].rsplit("/date=", 1)[0] for r in rows]
        miss = [a for a in want if a not in pkt]
        if miss:
            fail("packet does not print builder addresses %s" % miss)
        src = text(PRODUCER)
        lit = sorted(t for t in CUSTODIAN_TABLES if re.search(r"[\"']%s[\"']" % t, src))
        if lit:
            fail("producer still types custodian table names %s" % lit)
        decl = text(SOURCES)
        absent = [t for t in CUSTODIAN_TABLES if t not in decl]
        if absent:
            fail("sources.json does not carry %s" % absent)
        print("OK: %d builder addresses printed in the packet (firm %s); 0 custodian table literals in the producer" % (len(want), firm))
    elif cid == "DB26-1-AC3":
        pkt = text(PACKET)
        need = {"root": ROOT_TF in pkt,
                "targeted plan": bool(re.search(r"terraform plan[^\n]*-target=", pkt)),
                "plan counts": bool(re.search(r"\d+ to add, \d+ to change, \d+ to destroy", pkt)),
                "branch A": "## BRANCH A" in pkt, "branch B": "## BRANCH B" in pkt,
                "rollback": "rollback" in pkt.lower(),
                "class release carried": "account_class_daily" in pkt}
        miss = [k for k, v in need.items() if not v]
        if miss:
            fail("packet lacks %s" % miss)
        print("OK: packet names the root, a targeted plan with counts, both branches, the rollback and the class release it carries")
    elif cid == "DB26-2-AC1":
        rec = json.loads(text(REPEAT))
        n, f, r, v = rec.get("partitions_read"), rec.get("frames_read"), rec.get("repeated_label_frames"), rec.get("verdict")
        if not isinstance(n, int) or n <= 0 or not isinstance(f, int) or f <= 0 or not isinstance(r, int):
            fail("partitions_read %r, frames_read %r, repeated_label_frames %r" % (n, f, r))
        if v not in ("CAN", "CANNOT") or (v == "CAN") != (r > 0):
            fail("verdict %r disagrees with %d repeated-label frames" % (v, r))
        if v == "CAN":
            t = text(NONE_TESTS)
            if not re.search(r"^def test_\w*repeated_index\w*\(", t, re.M):
                fail("verdict CAN and no repeated_index test")
            rr = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(root / NONE_TESTS), "-k",
                                 "repeated_index"], cwd=str(root), capture_output=True, text=True, timeout=110)
            out = re.sub(r"\x1b\[[0-9;]*m", "", (rr.stdout or "") + (rr.stderr or ""))
            if rr.returncode or not re.search(r"\d+ passed", out):
                fail("repeated_index test: %s" % out[-300:])
        print("OK: %d partitions, %d frames read; %d with a repeated label; verdict %s" % (n, f, r, v))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
