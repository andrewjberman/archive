"""AMGT_CORPUS round 35, CRPS-ak-1 (round-34 analysis ruling 2, row Z-W1-S29) -- every one of the 52 round-34 mnemonics has a
unit family, decided on the values the fires landed. Read-only: it builds unit-map entries IN MEMORY over three landed names
(BA, GOOGL, BP/ LN) through build_unit_map's own build_entries and writes nothing. The issuer's file.

  BUILD arms (FAIL at the base, PASS after):
    b1 none of the 52 is in build_unit_map.unfamilied_mnemonics()
    b2 over the three landed names, no (mnemonic, security) entry of the 52 reads "not in any known field family"
       (in its unit, unit_status or per-security unit_status); the denominator of entries read is printed
  CONTROL arms (PASS at the base and after):
    c1 every one of the 68 base mnemonics stays in the family it is in at the base
    c2 over the same three names, every base mnemonic's per-security unit equals the committed field_map.json's
  -> one 'ARM <id> PASS|FAIL <got>' line per arm, then 'ak1 build <p>/2 control <q>/2'
"""
import importlib.util
import json
import os
import subprocess
import sys

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
for p in (TOP, RES):
    if p not in sys.path:
        sys.path.insert(0, p)
spec = importlib.util.spec_from_file_location("bum_ak1", os.path.join(RES, "build_unit_map.py"))
bum = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bum)
mbp = bum._mbp

NEW = list(mbp.HEADER_FIELDS[18:]) + list(mbp.HIST_FIELDS[39:]) + list(mbp.FORECAST_FIELDS[11:])
BASE = list(mbp.HEADER_FIELDS[:18]) + list(mbp.HIST_FIELDS[:39]) + list(mbp.FORECAST_FIELDS[:11])
NO_FAMILY = "not in any known field family"
FAMILY_SETS = ("TEXT_FIELDS", "PRICE_FIELDS", "PERCENT_FIELDS", "ABSOLUTE_OR_MILLIONS_FIELDS", "PER_SHARE_FIELDS",
               "RATIO_FIELDS", "SHARE_COUNT_ABSOLUTE_FIELDS", "SHARE_COUNT_MILLIONS_FIELDS")
# The base family of each of the 68 base mnemonics is captured beside this file (ak1_base_family.json, at CLOUD dce9d6d507).
SECURITIES = ["BA US Equity", "GOOGL US Equity", "BP/ LN Equity"]

results = []


def arm(aid, ok, got):
    results.append((aid, bool(ok)))
    print("ARM %s %s %s" % (aid, "PASS" if ok else "FAIL", got))


assert len(NEW) == 52 and len(BASE) == 68, (len(NEW), len(BASE))

unfam = sorted(set(bum.unfamilied_mnemonics()) & set(NEW))
arm("b1", not unfam, "new 52 unfamilied %d %s" % (len(unfam), unfam[:6]))


def entry_units(entry, security):
    """(unit text, unit_status text, per-security unit_status text) for one security of one field entry."""
    unit = entry.get("unit")
    u = unit.get(security) if isinstance(unit, dict) else unit
    detail = (entry.get("per_security_detail") or {}).get(security) or {}
    return str(u or ""), str(entry.get("unit_status") or ""), str(detail.get("unit_status") or "")


s3 = mbp._s3()
resolved = {}
for security in SECURITIES:
    sk = bum.security_key(security)
    raw = bum.load_raw_for_key(s3, sk)
    if raw is None:
        continue
    sec, header, hist_rows, raw_stamp = raw
    resolved[sk] = (sec, bum.prepare_header(s3, sec, sk, header, raw_stamp), hist_rows, raw_stamp)
try:
    doc, _ = bum.build_entries(resolved, False)
    built = True
except Exception as exc:  # noqa: BLE001 -- a crash on the landed values is the arm's finding
    doc, built = {"fields": []}, False
    print("BUILD-ENTRIES RAISED %s: %s" % (type(exc).__name__, exc))
by_m = {e.get("mnemonic"): e for e in doc.get("fields", [])}
secs = [v[0] for v in resolved.values()]

read, no_family = 0, []
for m in NEW:
    e = by_m.get(m)
    if not e:
        continue
    for sec in secs:
        u, us, ds = entry_units(e, sec)
        if not (u or ds):
            continue
        read += 1
        if NO_FAMILY in u or NO_FAMILY in ds or (NO_FAMILY in us and sec in us):
            no_family.append((m, sec))
arm("b2", built and len(resolved) == 3 and read > 0 and not no_family,
    "names %d entries_read %d no_family %d %s" % (len(resolved), read, len(no_family), no_family[:4]))

base_family_now = {m: next((name for name in FAMILY_SETS if m in getattr(bum, name, set())), "NONE") for m in BASE}
CAPTURED = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ak1_base_family.json"), encoding="utf-8"))
moved = sorted(m for m in BASE if base_family_now.get(m) != CAPTURED.get(m))
arm("c1", not moved, "base 68 family_moved %d %s" % (len(moved), moved[:6]))

committed = json.load(open(os.path.join(RES, "field_map.json"), encoding="utf-8"))
c_by_m = {e.get("mnemonic"): e for e in committed.get("fields", [])}
diffs, compared = [], 0
for m in BASE:
    e_new, e_old = by_m.get(m), c_by_m.get(m)
    if not e_new or not e_old:
        continue
    for sec in secs:
        u_new, u_old = entry_units(e_new, sec)[0], entry_units(e_old, sec)[0]
        if not u_old:
            continue
        compared += 1
        if u_new != u_old:
            diffs.append((m, sec, u_old, u_new))
arm("c2", built and compared > 0 and not diffs, "base units compared %d moved %d %s" % (compared, len(diffs), diffs[:3]))

b = sum(1 for aid, ok in results if aid.startswith("b") and ok)
c = sum(1 for aid, ok in results if aid.startswith("c") and ok)
print("ak1 build %d/2 control %d/2" % (b, c))
