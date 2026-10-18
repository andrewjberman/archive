# scratch helper (not a deliverable): re-runs ONLY the negative control of the census with the SAME walker and scan
# function as ck4_writers.py, on a token generated at run time (never typed in any file).
import importlib.util
import os
import secrets

WT = "C:/dev/wk-harvst-173"
SCRIPT = os.path.join(WT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~173/ck4_writers.py")
OUT = os.path.join(os.path.dirname(SCRIPT), "ck4_writers.out")

spec = importlib.util.spec_from_file_location("ck4_writers", SCRIPT)
ck4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ck4)

token = "ZZ_NO_SUCH_" + secrets.token_hex(8) + "_ZZ/v1/"
assert len(token) == len("ZZ_NO_SUCH_") + 16 + len("_ZZ/v1/"), token

denom, excluded, skipped_big, lit_hits, name_uses, defs_all = ck4.scan([token], False, set())
hits = lit_hits.get(token, [])
lines = [
    "CONTROL-NEGATIVE-2 token=%s occurrences=%d" % (token, len(hits)),
    "CONTROL-NEGATIVE-NOTE the first-run control above counted 2 hits, both the text of the task order, which named its literal",
]
with open(OUT, "a", encoding="utf-8", newline="\n") as fh:
    for ln in lines:
        fh.write(ln + "\n")
for ln in lines:
    print(ln)
print("files_scanned=%d skipped_over_2MiB=%d" % (sum(denom.values()), skipped_big))
for rel, ln, ext, txt in hits:
    print("HIT %s:%d ext=%s" % (rel, ln, ext))
