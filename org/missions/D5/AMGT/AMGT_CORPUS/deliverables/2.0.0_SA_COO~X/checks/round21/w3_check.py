"""AMGT_CORPUS round 21, CRPS-w-3 -- the cross-field unit discriminator through build_unit_map's own function, over the nine
facts the round-20 addendum names plus a MEASURED control (SAP GY Equity CURR_ENTP_VAL, MILLIONS in the committed map).
Read-only (S3 raw reads); the issuer's file.

  -> one 'FACT <security> | <mnemonic> | <RESOLVED unit | UNRESOLVED> | <evidence or reason>' per fact, then
     'w3 facts A of 9 answered resolved R unresolved U resolved_with_evidence E unresolved_with_reason N control
      SAP_GY_CURR_ENTP_VAL <unit> agrees <True|False>'
"""
import importlib.util
import os
import subprocess

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
spec = importlib.util.spec_from_file_location("bum_w3", os.path.join(TOP, "integrations", "bloomberg", "research", "build_unit_map.py"))
bum = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bum)

FACTS = [("6501 JP Equity", "SALES_REV_TURN"), ("8316 JP Equity", "SALES_REV_TURN"),
         ("6501 JP Equity", "CURR_ENTP_VAL"), ("9433 JP Equity", "CURR_ENTP_VAL"), ("8035 JP Equity", "CURR_ENTP_VAL"),
         ("8766 JP Equity", "CURR_ENTP_VAL"), ("TSM US Equity", "CURR_ENTP_VAL"),
         ("8316 JP Equity", "NET_DEBT"), ("6501 JP Equity", "BEST_SALES")]
CONTROL = ("SAP GY Equity", "CURR_ENTP_VAL")

out = bum.discriminate_facts(FACTS + [CONTROL])
by = {(r.get("security"), r.get("mnemonic")): r for r in out}
answered = resolved = unresolved = with_ev = with_reason = 0
for f in FACTS:
    r = by.get(f)
    if not r or r.get("state") not in ("RESOLVED", "UNRESOLVED"):
        print("FACT %s | %s | MISSING |" % f)
        continue
    answered += 1
    if r["state"] == "RESOLVED":
        resolved += 1
        with_ev += bool(str(r.get("unit") or "").strip() and str(r.get("evidence") or "").strip())
        print("FACT %s | %s | RESOLVED %s | %s" % (f[0], f[1], r.get("unit"), r.get("evidence")))
    else:
        unresolved += 1
        with_reason += bool(str(r.get("reason") or "").strip())
        print("FACT %s | %s | UNRESOLVED | %s" % (f[0], f[1], r.get("reason")))
c = by.get(CONTROL) or {}
cu = c.get("unit") if c.get("state") == "RESOLVED" else "UNRESOLVED"
print("w3 facts %d of 9 answered resolved %d unresolved %d resolved_with_evidence %d unresolved_with_reason %d control "
      "SAP_GY_CURR_ENTP_VAL %s agrees %s" % (answered, resolved, unresolved, with_ev, with_reason, cu, cu == "MILLIONS"))
