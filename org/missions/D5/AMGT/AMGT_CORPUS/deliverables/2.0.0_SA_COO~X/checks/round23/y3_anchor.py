"""AMGT_CORPUS round 23, CRPS-y-3 -- the same-currency anchor on the real raw: TSM (TWD fundamentals, USD market cap; the store
holds no TWD line and no FX field at the cut) and the control SAP GY (EUR both sides). Read-only (S3 raw reads). The issuer's file.

  -> 'y3 tsm anchor <field|none> searched N reason_set True|False fx_invented False|True control_sap anchor <field|none>'
"""
import importlib.util
import os
import subprocess

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bum = load("bum_y3", os.path.join(RES, "build_unit_map.py"))
ua = load("ua_y3", os.path.join(RES, "unit_anchor.py"))
s3 = bum._mbp._s3()


def read(security):
    r = bum.load_raw_for_key(s3, bum.security_key(security))
    sec, header, _hist, stamp = r
    return sec, bum.prepare_header(s3, sec, bum.security_key(security), header, stamp)


sec, hdr = read("TSM US Equity")
t = ua.same_currency_anchor(s3, sec, hdr)
csec, chdr = read("SAP GY Equity")
c = ua.same_currency_anchor(s3, csec, chdr)
ta = (t.get("anchor") or {}).get("field") or "none"
ca = (c.get("anchor") or {}).get("field") or "none"
invented = bool(t.get("anchor")) and str((t.get("anchor") or {}).get("source_key") or "") == ""
print("y3 tsm anchor %s searched %d reason_set %s fx_invented %s control_sap anchor %s" % (
    ta, len(t.get("searched") or []), bool(str(t.get("reason") or "").strip()), invented, ca))
