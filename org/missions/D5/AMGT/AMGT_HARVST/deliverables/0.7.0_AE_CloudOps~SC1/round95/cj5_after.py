"""HVST-cj-5 after-checks, read only. Run from the round95 folder: python -u cj5_after.py"""
import sys
sys.path.insert(0, r"C:\dev\ajb_workspace\org\missions\D5\AMGT\AMGT_HARVST\deliverables\0.7.0_AE_CloudOps~SC1\round95")
import cj5_run as r  # noqa: E402

client = r.store._default_client()
dp = r.gold.table_prefix(r.dossier.TABLE)
cp = r.gold.table_prefix(r.continuation.TABLE)
nd, nc = len(r.list_rows(client, dp)), len(r.list_rows(client, cp))
print("dossier objects now %d (start 1554, expected 1556: %s)" % (nd, "PASS" if nd == 1556 else "FAIL"))
print("continuation objects now %d (start 446, expected 446: %s)" % (nc, "PASS" if nc == 446 else "FAIL"))
lines = [ln for ln in open(r.MANIFEST, encoding="ascii") if " WROTE dossier name=" in ln]
print("manifest lines: %d (expected 2: %s)" % (len(lines), "PASS" if len(lines) == 2 else "FAIL"))
ok = 0
for name in ("BP/_LN_Equity", "NG/_LN_Equity"):
    part = r.store.entity_partition("security_key", name)
    rows = r.list_rows(client, "%s%s/" % (dp, part))
    picked, dup = r.served_pick(rows)
    mkey = [ln.split(" key=")[1].split(" ")[0] for ln in lines if (" name=%s " % name) in ln]
    eq = bool(mkey) and picked is not None and picked["key"] == mkey[0]
    ok += int(eq)
    raw_rows = r.list_rows(client, "%s%s/" % (dp, name))
    print("PICK name=%s partition=%s objects=%d picked=%s manifest_key=%s pick_equals_manifest=%s objects_under_raw_spelling=%d dup=%s" % (
        name, part, len(rows), picked["key"].rsplit("/", 1)[-1] if picked else None, mkey[0].rsplit("/", 1)[-1] if mkey else None, eq, len(raw_rows), dup))
print("pick_equals_manifest=%d of 2" % ok)
