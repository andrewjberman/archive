"""IRPT_DASHBD round 60 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling msg 4036 on row IRPT_DASHBD-D2-W89-S1.

Cell: DB-b-116 one measurement: does METHOD_ROWS row 3 (and the dim_return_method row it writes) describe the Cottonwood rows -- its income
treatment read from the adapter against row 3's text, field by field -- and does a dim row 3 partition exist at the builder address.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB60-1-AC1  ~91/ROW3_VS_COTTONWOOD.json: fields is a non-empty list of {field, row3_states, cottonwood_does, verdict in TRUE / FALSE /
              NOT_STATED, evidence [{file, line}] resolving to files at HEAD}, and it includes the income basis; verdict is ROW3_TRUE or
              ROW3_FALSE, and ROW3_TRUE only when no field reads FALSE; dim_partition {address, exists (bool), read: {call, result}} with
              the address ending method_version=3 and a positive_control {address, exists: true}.
"""
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB60"))
        sys.exit(1)

    if cid != "DB60-1-AC1":
        fail("unknown criterion %r" % cid)
    p = root / (D + "91/ROW3_VS_COTTONWOOD.json")
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    fs = r.get("fields") or []
    if not fs:
        fail("fields empty")
    for f in fs:
        if f.get("verdict") not in ("TRUE", "FALSE", "NOT_STATED"):
            fail("field %r verdict %r" % (f.get("field"), f.get("verdict")))
        if not str(f.get("row3_states") or "").strip() or not str(f.get("cottonwood_does") or "").strip():
            fail("field %r lacks row3_states or cottonwood_does" % f.get("field"))
        ev = f.get("evidence") or []
        if not ev:
            fail("field %r has no evidence" % f.get("field"))
        for e in ev:
            if not (root / str(e.get("file") or "")).is_file() or not isinstance(e.get("line"), int):
                fail("field %r evidence %r does not name a file and line" % (f.get("field"), e))
    if not any("income" in str(f.get("field") or "").lower() for f in fs):
        fail("no income field among %r" % [f.get("field") for f in fs])
    v = r.get("verdict")
    if v not in ("ROW3_TRUE", "ROW3_FALSE"):
        fail("verdict %r" % v)
    n_false = sum(1 for f in fs if f["verdict"] == "FALSE")
    if v == "ROW3_TRUE" and n_false:
        fail("verdict ROW3_TRUE with %d FALSE field(s)" % n_false)
    if v == "ROW3_FALSE" and not n_false:
        fail("verdict ROW3_FALSE with no FALSE field")
    dp = r.get("dim_partition") or {}
    if not str(dp.get("address") or "").rstrip("/").endswith("method_version=3") or not isinstance(dp.get("exists"), bool):
        fail("dim_partition %r" % dp)
    rd = dp.get("read") or {}
    if not rd.get("call") or "result" not in rd:
        fail("dim_partition.read %r" % rd)
    pc = r.get("positive_control") or {}
    if not pc.get("address") or pc.get("exists") is not True:
        fail("positive_control %r" % pc)
    print("OK: %d field(s) read, %d FALSE, verdict %s, dim row 3 partition exists=%s" % (len(fs), n_false, v, dp["exists"]))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
