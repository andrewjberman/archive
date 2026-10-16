"""c26_check.py -- grades MX-c-26 (the 49F live opal-data-bd tables: four NEW catalog rows, the eight frozen-copy rows back in their own bucket, the `address` field), from the repo root.

  python c26_check.py ac1   the four NEW live rows (unrealized, transactions, allocations, fees): entry file blackdiamond_live_<t>.yaml with prefix silver/<t>/, table <t>, layer silver,
                            `address` blackdiamond/49f-live/silver/<t>/, read_tool the mapped client tool, not retired, no gap_owner, and not the legacy open item "do not build a tool on this prefix" (a live row MAY point at the frozen copy, as the face requires); freshness.latest_partition EQUAL
                            to the newest YYYY-MM-DD.parquet the aws CLI lists under s3://opal-data-bd/silver/<t>/ now, claim measured, trading_days_behind_t1 equal to the trading calendar's;
                            the issuer's group map round19/live_bd_group_map.json maps the four to bucket opal-data-bd, vendor blackdiamond, firm 49financial
  python c26_check.py ac2   the eight FROZEN-copy rows (49financial_<t>_silver_legacy for allocations, assets, fees, prices, realized, transactions_enriched, transactions, unrealized): prefix is
                            blackdiamond/49financial/silver_legacy/<t>/ and a non-empty listing exists there in opal-data-assets (aws CLI), the group map round18/assets_group_map.json
                            says bucket opal-data-assets for all nine legacy rows, each still has read_tool null, gap_owner NFRA_OPLGTW and its `FROZEN copy` open item
  python c26_check.py ac7   (A7, CTO msg 35145) the four `address` strings are HELD whole at HEAD by legacy_addresses.json (read through naming-gate.py's own `_catalog_registry_held(repo)`),
                            that file differs from its state at d1092a10f6 by exactly the four appended rows, catalog_fork_keys.json is byte-equal to that state, and the placed catalog
                            blob is unchanged (b81c48aa3c)
  python c26_check.py ac3   the field: `address` is an accepted optional TABLE-row field in the emitter and the validator and is carried to the emitted row by the row builder; exactly four
                            entries carry it, each unique; tests/test_address_field.py (new, at least 5 tests) with tests/test_c_group.py and tests/test_silver_table_grain.py pass;
                            validate_catalog_v02.py prints no FAIL line

The tree is the worktree (or C26_ROOT). Exit 0 PASS, 1 FAIL, 9 no run.
"""
import json
import os
import re
import subprocess
import sys

import yaml

ROOT = os.environ.get("C26_ROOT") or "."
ENT = os.path.join(ROOT, "workflows", "atom_decomposition", "catalog_entries")
AD = os.path.join(ROOT, "workflows", "atom_decomposition")
MAPDIR = os.path.join(ROOT, "org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables", "2.0.0_SA_COO~MI")
LIVE_MAP = os.path.join(MAPDIR, "round19", "live_bd_group_map.json")
ASSETS_MAP = os.path.join(MAPDIR, "round18", "assets_group_map.json")
AWS = os.path.join(ROOT, ".tools", "aws.cmd") if os.path.exists(os.path.join(ROOT, ".tools", "aws.cmd")) else os.path.join(ROOT, ".tools", "aws")
TOOLS = {"unrealized": "client_get_holdings", "transactions": "client_get_transactions", "allocations": "client_get_allocation", "fees": "client_get_fees"}
LEGACY = ("allocations", "assets", "fees", "prices", "realized", "transactions_enriched", "transactions", "unrealized")
DATEFILE = re.compile(r"(\d{4}-\d{2}-\d{2})\.parquet\s*$")


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok  " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def entry(name):
    p = os.path.join(ENT, name + ".yaml")
    if not os.path.exists(p):
        return None
    return yaml.safe_load(open(p, encoding="utf-8"))


def s3ls(bucket, prefix):
    r = subprocess.run([AWS, "s3", "ls", "s3://%s/%s" % (bucket, prefix)], capture_output=True, text=True, timeout=120)
    if r.returncode not in (0, 1):
        print("ERROR: aws s3 ls s3://%s/%s rc %d: %s" % (bucket, prefix, r.returncode, r.stderr[-200:]))
        sys.exit(9)
    return [ln for ln in (r.stdout or "").replace("\r", "").splitlines() if ln.strip()]


def ac1():
    sys.path.insert(0, ROOT)
    from lib import trading_calendar as tc
    gm = (json.load(open(LIVE_MAP, encoding="utf-8")).get("rows") or {}) if os.path.exists(LIVE_MAP) else {}
    res, found = [], 0
    for t, tool in TOOLS.items():
        ent = "blackdiamond_live_" + t
        e = entry(ent)
        if e is None:
            res.append(("%s: entry file present" % ent, False))
            continue
        found += 1
        fr = ((e.get("contract") or {}).get("freshness")) or {}
        live = sorted(m.group(1) for m in (DATEFILE.search(ln) for ln in s3ls("opal-data-bd", "silver/%s/" % t)) if m)
        newest = live[-1] if live else None
        behind = None
        if newest:
            behind = tc.trading_days_behind(newest, tc.expected_last_trading_day(__import__("datetime").datetime.utcnow()))
        ok = (e.get("prefix") == "silver/%s/" % t and e.get("table") == t and e.get("layer") == "silver"
              and e.get("address") == "blackdiamond/49f-live/silver/%s/" % t and e.get("read_tool") == tool
              and e.get("retired") is False and not e.get("gap_owner")
              and not any("do not build a tool on this prefix" in str(x) for x in (e.get("open_items") or [])))
        res.append(("%s: prefix, table, layer, address, read_tool %s, not retired, no gap_owner, no copy-over of the legacy do-not-build item" % (ent, tool), ok))
        fok = (newest is not None and str(fr.get("latest_partition"))[:10] == newest and fr.get("claim") == "measured"
               and fr.get("trading_days_behind_t1") == behind)
        res.append(("%s: freshness latest_partition %s equals the live newest %s, behind %s equals %s, claim measured"
                    % (ent, fr.get("latest_partition"), newest, fr.get("trading_days_behind_t1"), behind), fok))
        m = gm.get(ent) or {}
        res.append(("%s: live group map bucket opal-data-bd, vendor blackdiamond, firm 49financial" % ent,
                    m.get("bucket") == "opal-data-bd" and m.get("vendor") == "blackdiamond" and m.get("firm") == "49financial"))
    # the emitter's own path: each new entry built into a row by the emitter's row builder, then the live group map applied with the emitter's own rule
    # (a map firm that differs from the row's firm is a CONFLICT and the row is left without a bucket: the 2026-10-16 trial emit crashed there)
    sys.path.insert(0, AD)
    import emit_catalog_v02 as em
    rows, ents = [], {}
    for t in TOOLS:
        e = entry("blackdiamond_live_" + t)
        if e is not None:
            ents["blackdiamond_live_" + t] = e
            rows.append(em.silver_catalog_row("blackdiamond_live_" + t, e))
    spec, gerrs = em.load_group_maps([LIVE_MAP]) if os.path.exists(LIVE_MAP) else ({}, ["live map absent"])
    applied, unused, conflicts = em.apply_group_map({"silver_datasets": rows, "portal_datasets": [], "harvest_datasets": []}, spec)
    good = [r for r in rows if r.get("bucket") == "opal-data-bd" and r.get("vendor") == "blackdiamond" and r.get("firm") == "49financial"
            and r.get("address") == "blackdiamond/49f-live/silver/%s/" % r["entity"].rsplit("_", 1)[-1] and r.get("read_tool")]
    print("DENOMINATOR emitter path: rows built %d; group map applied %d of %d; conflicts %d; map errors %d; rows complete %d"
          % (len(rows), applied, len(spec), len(conflicts), len(gerrs), len(good)))
    res.append(("the emitter builds the four rows and the live group map applies with no conflict (bucket, vendor, firm, address, read_tool on each)",
                len(rows) == 4 and applied == 4 and not conflicts and not gerrs and len(good) == 4))
    print("DENOMINATOR live rows present %d of %d; live group map entries %d" % (found, len(TOOLS), len(gm)))
    return report(res)


def ac2():
    gm = json.load(open(ASSETS_MAP, encoding="utf-8"))["rows"]
    res, nonempty = [], 0
    for t in LEGACY:
        ent = "opal_data_assets_silver_49financial_%s_silver_legacy" % t
        e = entry(ent)
        if e is None:
            res.append(("%s: entry present" % ent, False))
            continue
        pre = "blackdiamond/49financial/silver_legacy/%s/" % t
        n = len(s3ls("opal-data-assets", pre))
        nonempty += 1 if n else 0
        res.append(("%s: prefix is the frozen copy's %s (listing %d lines), read_tool null, gap_owner NFRA_OPLGTW, FROZEN open item kept" % (ent, pre, n),
                    e.get("prefix") == pre and n > 0 and e.get("read_tool") is None and e.get("gap_owner") == "NFRA_OPLGTW"
                    and any("FROZEN" in str(x) for x in (e.get("open_items") or []))))
    # the emitter's own path: the entries as the LOADER returns them (joined to the fork registry, which restores bucket and key_template), built into
    # rows, then the assets group map applied with the emitter's rule (a map bucket that differs from the row's valid S3 bucket is a CONFLICT, 2026-10-16 trial emit)
    sys.path.insert(0, AD)
    import emit_catalog_v02 as em
    ents, eerrs = em.load_catalog_entries()
    lrows = [em.silver_catalog_row(n, ents[n]) for n in ("opal_data_assets_silver_49financial_%s_silver_legacy" % t for t in LEGACY) if n in ents]
    spec, gerrs = em.load_group_maps([ASSETS_MAP])
    applied, unused, conflicts = em.apply_group_map({"silver_datasets": lrows, "portal_datasets": [], "harvest_datasets": []}, spec)
    kt_ok = sum(1 for r, t in zip(lrows, LEGACY) if str(r.get("key_template") or "").startswith("blackdiamond/49financial/silver_legacy/%s/" % t))
    b_ok = sum(1 for r in lrows if r.get("bucket") == "opal-data-assets")
    print("DENOMINATOR emitter path: legacy rows built %d; conflicts %d (%s); bucket opal-data-assets %d; key_template at the frozen prefix %d; entry errors %d"
          % (len(lrows), len(conflicts), "; ".join(c.split(":")[0][-40:] for c in conflicts[:2]), b_ok, kt_ok, len(eerrs)))
    res.append(("the eight legacy rows, as the loader returns them, take the assets group map with no conflict, bucket opal-data-assets, key_template at the frozen copy's prefix",
                len(lrows) == 8 and not conflicts and b_ok == 8 and kt_ok == 8 and not eerrs))
    legacy_all = [k for k in gm if k.startswith("opal_data_assets_silver_49financial_") and k.endswith("_silver_legacy")]
    bad = [k for k in legacy_all if gm[k].get("bucket") != "opal-data-assets"]
    print("DENOMINATOR legacy entries %d; frozen prefixes non-empty %d; group-map legacy rows %d, not in opal-data-assets %d" % (len(LEGACY), nonempty, len(legacy_all), len(bad)))
    res.append(("the base group map holds nine legacy rows, all in opal-data-assets", len(legacy_all) == 9 and not bad))
    return report(res)


def ac3():
    em = open(os.path.join(AD, "emit_catalog_v02.py"), encoding="utf-8").read()
    gen = open(os.path.join(AD, "gen_silver_rows.py"), encoding="utf-8").read()
    carried = '"address"' in em and ('"address"' in gen or "address" in em.split("def _clean_table_row", 1)[-1][:6000])
    carriers = {}
    for f in sorted(os.listdir(ENT)):
        if f.endswith(".yaml"):
            d = yaml.safe_load(open(os.path.join(ENT, f), encoding="utf-8")) or {}
            if isinstance(d, dict) and "address" in d:
                carriers[f[:-5]] = d["address"]
    uniq = len(set(carriers.values())) == len(carriers)
    print("DENOMINATOR entries carrying address %d (%s)" % (len(carriers), ", ".join(sorted(carriers))))
    res = [("the emitter names `address` as an optional table field", carried), ("exactly four entries carry it, each address unique", len(carriers) == 4 and uniq)]
    t = os.path.join(AD, "tests", "test_address_field.py")
    n_new = 0
    if os.path.exists(t):
        co = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--co", "tests/test_address_field.py"], cwd=AD, capture_output=True, text=True, timeout=120)
        n_new = sum(1 for ln in (co.stdout or "").splitlines() if "::" in ln)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--no-header", "tests/test_address_field.py", "tests/test_c_group.py",
                        "tests/test_silver_table_grain.py"], cwd=AD, capture_output=True, text=True, timeout=250) if os.path.exists(t) else None
    tail = [ln for ln in ((r.stdout if r else "") or "").replace("\x1b", "").splitlines() if "passed" in ln or "failed" in ln][-1:]
    print("pytest rc=%s: %s; new tests collected %d" % (r.returncode if r else "n/a", tail[0].strip() if tail else "-", n_new))
    res.append(("the new test file holds at least 5 tests and the three files pass", r is not None and r.returncode == 0 and n_new >= 5))
    v = subprocess.run([sys.executable, "validate_catalog_v02.py"], cwd=AD, capture_output=True, text=True, timeout=250)
    bad = [ln for ln in (v.stdout or "").replace("\r", "").splitlines() if ln.strip().startswith(("FAIL", "ERROR"))]
    res.append(("validate_catalog_v02.py: rc 0 and no FAIL line (%d)" % len(bad), v.returncode == 0 and not bad))
    return report(res)


def ac7():
    import importlib.util
    spec = importlib.util.spec_from_file_location("naming_gate", os.path.join(ROOT, ".tools", "naming-gate.py"))
    ng = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ng)
    held = ng._catalog_registry_held(repo=os.path.abspath(ROOT))
    want = ["blackdiamond/49f-live/silver/%s/" % t for t in TOOLS]
    got = {w: held.get(w, "") for w in want}
    print("DENOMINATOR addresses %d; held at HEAD by legacy_addresses.json %d" % (len(want), sum(1 for v in got.values() if v.endswith("legacy_addresses.json"))))
    res = [("the four address strings are held whole in legacy_addresses.json at HEAD", all(v.endswith("legacy_addresses.json") for v in got.values()))]

    def git_show(ref, path):
        r = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (ref, path)], capture_output=True)
        if r.returncode != 0:
            print("ERROR: git show %s:%s rc %d" % (ref, path, r.returncode))
            sys.exit(9)
        return r.stdout
    legacy, fork = "infra/logic/registry/legacy_addresses.json", "infra/logic/registry/catalog_fork_keys.json"
    old, new = json.loads(git_show("d1092a10f6", legacy)), json.loads(git_show("HEAD", legacy))
    orows, nrows = old["legacy_addresses"], new["legacy_addresses"]
    appended = nrows[len(orows):]
    keys = [r.get("key") for r in appended]
    ok_rows = (len(appended) == 4 and nrows[:len(orows)] == orows and keys == ["gateway-client-bdlive-%s-logical" % t for t in TOOLS]
               and [r.get("template") for r in appended] == want and all(r.get("bucket") == "opal-data-bd" and r.get("shape") == "prefix" for r in appended))
    print("DENOMINATOR legacy rows: d1092a10f6 %d, HEAD %d; appended keys %s" % (len(orows), len(nrows), keys))
    res.append(("legacy_addresses.json differs from its d1092a10f6 state by exactly the four appended rows (keys, templates, bucket, shape)", ok_rows))
    res.append(("catalog_fork_keys.json is byte-equal to its d1092a10f6 state", git_show("d1092a10f6", fork) == git_show("HEAD", fork)))
    blob = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD:infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml"], capture_output=True, text=True).stdout.strip()
    res.append(("the placed catalog blob is unchanged (%s)" % blob[:10], blob == "b81c48aa3c6c0ce3e79628e55cc5e8501f73dcf3"))
    return report(res)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("ac1", "ac2", "ac3", "ac7"):
        print(__doc__)
        return 9
    return {"ac1": ac1, "ac2": ac2, "ac3": ac3, "ac7": ac7}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
