"""OG-tm-1 Phase A probe: build_closure for master 08403355 on a synthetic day, with and without slm.

Run from the repo root:  python org/.../probes/tm1_closure_probe.py
Reads the vendored package in infra/aws/lambda/opal-assets/opal-assets-silver-schwab/ (read only; no AWS call).
"""
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, "infra/aws/lambda/opal-assets/opal-assets-silver-schwab")

import conversion_manifest as cm  # noqa: E402
import set_identity_guard as g  # noqa: E402

TYPES13 = "acc rld rly rps rty sec tcfx tnn trn uln ult upn upt".split()


def inventory(master, types, date="20261007"):
    bronze, silver = {}, {}
    for t in types:
        bronze[t] = ["schwab/%s/bronze/%s/%s/%s.CRS%s.%s.zip" % (master, t, date, master, date, t.upper())]
        for fact in g.expected_tables(t):
            for tab in [fact] + list(g._dims_for_table(fact)):
                silver.setdefault(tab, []).append(
                    {"key": cm.canonical_object_key(master, tab, "2026-10-07"),
                     "version_id": "v1", "size": 10, "etag": "e", "rows": 5})
    return {"bronze": bronze, "silver": silver, "errors": []}


def main():
    assert cm._registry_masters_tie()
    cases = (("08403355", TYPES13), ("08335338", TYPES13 + ["slm"]), ("08403355", TYPES13 + ["slm"]))
    for master, types in cases:
        c = cm.build_closure("r1", "event", master, "2026-10-07", inventory(master, types), [])
        na = [(x["kind"], x["subject"], x["reason"]) for x in c["non_applicable"] if "slm" in x["subject"]]
        print(master, "slm_in_bronze=", "slm" in types, "status=", c["status"], "findings=", c["findings"],
              "slm_na=", na)


if __name__ == "__main__":
    main()
