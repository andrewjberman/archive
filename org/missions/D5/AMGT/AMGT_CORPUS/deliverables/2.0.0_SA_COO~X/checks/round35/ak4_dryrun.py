"""AMGT_CORPUS round 35, CRPS-ak-4 -- the serializing dry run of the unit-map rebuild for the 52 round-34 mnemonics, over EVERY
name with raw landed. In memory only: build_unit_map's own population resolver, loader and build_entries (remeasure=False, the
additive merge), compared against the committed field_map.json. Nothing is written. The issuer's file.

Prints:
  population <N> raw_landed <R>
  new52: per mnemonic MEASURED / UNRESOLVED / absent over the R names, and the top UNRESOLVED reasons
  base: entries compared, base per-security units moved (expected 0), base securities added
  totals: new52 entries MEASURED / UNRESOLVED; fields in the would-be map; securities covered
"""
import collections
import importlib.util
import json
import os
import subprocess
import sys
from types import SimpleNamespace

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
for p in (TOP, RES):
    if p not in sys.path:
        sys.path.insert(0, p)
spec = importlib.util.spec_from_file_location("bum_ak4", os.path.join(RES, "build_unit_map.py"))
bum = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bum)
mbp = bum._mbp

NEW = list(mbp.HEADER_FIELDS[18:]) + list(mbp.HIST_FIELDS[39:]) + list(mbp.FORECAST_FIELDS[11:])
BASE = sorted(set(mbp.HEADER_FIELDS[:18]) | set(mbp.HIST_FIELDS[:39]) | set(mbp.FORECAST_FIELDS[:11]))
assert len(NEW) == 52


def entry_unit(entry, security):
    unit = entry.get("unit")
    u = unit.get(security) if isinstance(unit, dict) else unit
    detail = (entry.get("per_security_detail") or {}).get(security) or {}
    return str(u or ""), str(detail.get("unit_status") or entry.get("unit_status") or "")


s3 = mbp._s3()
sec_keys = bum.resolve_population(SimpleNamespace(securities=None, population="crosswalk"), s3)
resolved = {}
for sk in sec_keys:
    raw = bum.load_raw_for_key(s3, sk)
    if raw is None:
        continue
    security, header, hist_rows, raw_stamp = raw
    resolved[sk] = (security, bum.prepare_header(s3, security, sk, header, raw_stamp), hist_rows, raw_stamp)
print("population %d raw_landed %d" % (len(sec_keys), len(resolved)))

doc, summaries = bum.build_entries(resolved, False)
by_m = {e["mnemonic"]: e for e in doc.get("fields", [])}
secs = [v[0] for v in resolved.values()]

tot_meas = tot_unres = 0
reasons_all = collections.Counter()
for m in NEW:
    e = by_m.get(m) or {}
    meas = unres = absent = 0
    reasons = collections.Counter()
    for sec in secs:
        u, st = entry_unit(e, sec)
        if not u and not st:
            absent += 1
        elif st.startswith("UNRESOLVED") or u.startswith("UNRESOLVED"):
            unres += 1
            r = (st or u).split(":", 1)[-1].strip()[:70]
            reasons[r] += 1
            reasons_all[r] += 1
        else:
            meas += 1
    tot_meas += meas
    tot_unres += unres
    top = "; ".join("%s x%d" % (r, n) for r, n in reasons.most_common(2))
    print("   %-34s measured %3d unresolved %3d absent %3d %s" % (m, meas, unres, absent, top))

committed = json.load(open(os.path.join(RES, "field_map.json"), encoding="utf-8"))
c_by_m = {e["mnemonic"]: e for e in committed.get("fields", [])}
compared = moved = 0
moved_samples = []
for m in BASE:
    e_new, e_old = by_m.get(m), c_by_m.get(m)
    if not e_new or not e_old:
        continue
    for sec in secs:
        u_old = entry_unit(e_old, sec)[0]
        if not u_old:
            continue
        compared += 1
        u_new = entry_unit(e_new, sec)[0]
        if u_new != u_old:
            moved += 1
            moved_samples.append((m, sec, u_old[:30], u_new[:30]))
print("base entries_compared %d units_moved %d %s" % (compared, moved, moved_samples[:4]))
print("totals new52 measured %d unresolved %d | would-be map fields %d (committed %d) securities %d (committed %d)"
      % (tot_meas, tot_unres, len(doc.get("fields", [])), len(committed.get("fields", [])),
         len(doc.get("securities") or []), len(committed.get("securities") or [])))
print("top unresolved reasons:", reasons_all.most_common(5))
