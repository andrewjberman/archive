"""V8-AC8 re-record: the seeder's OWN merge_item over the thirteen, per ticker.
READ-ONLY: scans the live table, calls merge_item(), writes nothing."""
import io
import importlib.util
from pathlib import Path
from datetime import datetime, timezone
import boto3

ROOT = Path(".").resolve()
SEEDER = ROOT / "infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-classifications.py"
spec = importlib.util.spec_from_file_location("seeder_under_test", str(SEEDER))
seeder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(seeder)

THIRTEEN = [
    ("DBC",  "commodities",  "Commodities"),
    ("GLD",  "commodities",  "Metals"),
    ("GSG",  "commodities",  "Commodities"),
    ("IAU",  "commodities",  "Metals"),
    ("SLV",  "commodities",  "Metals"),
    ("USO",  "commodities",  "Oil"),
    ("PDBC", "commodities",  "Commodities"),
    ("VXX",  "structured",   "Hedge"),
    ("VIXY", "structured",   "Hedge"),
    ("UVXY", "structured",   "Hedge"),
    ("QBER", "structured",   "Hedge"),
    ("JEPI", "structured",   "Options Income"),
    ("VNQ",  "alternatives", "Real Estate"),
]
GRADED = ("asset_class", "sub_asset_class", "management_style")

ddb = boto3.resource("dynamodb", region_name="us-east-1")
table = ddb.Table(seeder.TABLE_NAME)
resp = table.scan()
rows = list(resp.get("Items", []))
pages = 1
lek = resp.get("LastEvaluatedKey")
while lek:
    resp = table.scan(ExclusiveStartKey=lek)
    pages = pages + 1
    rows.extend(resp.get("Items", []))
    lek = resp.get("LastEvaluatedKey")
live = {r["ticker"]: r for r in rows}

out = []
def p(s=""):
    out.append(s)
    print(s)

ts = datetime.now(timezone.utc).isoformat()
p("V8-AC8 RE-RECORD -- the seeder's OWN merge_item() over the THIRTEEN, per ticker")
p("read at %s by 0.9.0_WK_POSN_ASTTAX~19 (READ-ONLY: scan + merge_item, no write API called)" % ts)
p("seeder under test: %s" % SEEDER.as_posix())
p("table: %s -- rows scanned %d over %d page(s)" % (seeder.TABLE_NAME, len(rows), pages))
p("module union: %d ticker(s)" % len(set(list(seeder.ETF_CLASSIFICATIONS.keys())
                                         + list(seeder.ETF_SUB_ASSET_CLASS.keys())
                                         + list(seeder.ETF_MANAGEMENT_STYLE.keys())
                                         + list(seeder.ETF_SECTOR_MAPPING.keys())
                                         + list(seeder.ETF_NAME_OVERRIDES.keys()))))
p("")
p("PER TICKER -- 13 tickers x 3 graded fields = 39 fields; a CONFLICT is merge_item's own")
p("(the module and the table both know the field and DISAGREE).")
p("%-6s %-17s %-24s %-24s %-9s %s" % ("ticker", "field", "table serves", "module asserts", "conflict", "== TARGET per THE CELL"))
fields_checked = 0
conf_thirteen = 0
target_ok = 0
for tkr, tgt_ac, tgt_sac in THIRTEEN:
    existing = live.get(tkr)
    item, preserved, conflicts = seeder.merge_item(tkr, existing, ts)
    cf = {(c[1]) for c in conflicts}
    mod = seeder.module_values(tkr)
    for field in GRADED:
        fields_checked += 1
        tv = (existing or {}).get(field)
        mv = mod[field]
        isconf = field in cf
        if isconf:
            conf_thirteen += 1
        tgt = tgt_ac if field == "asset_class" else (tgt_sac if field == "sub_asset_class" else "(mgmt, per THE CELL)")
        if field == "asset_class":
            ok = "YES" if str(tv) == tgt_ac else "NO"
            target_ok += 1 if ok == "YES" else 0
        elif field == "sub_asset_class":
            ok = "YES" if str(tv) == tgt_sac else "NO"
            target_ok += 1 if ok == "YES" else 0
        else:
            ok = "n/a"
        p("%-6s %-17s %-24s %-24s %-9s %s" % (tkr, field, repr(tv), repr(mv),
                                              "CONFLICT" if isconf else "-",
                                              ("%s %s" % (ok, tgt)) if ok != "n/a" else "n/a"))
    p("%-6s merge_item -> conflicts=%d preserved=%s" % (tkr, len(conflicts), preserved))
p("")
p("THE THIRTEEN: conflicting fields %d of %d (13 tickers x 3 graded fields)" % (conf_thirteen, fields_checked))
p("THE THIRTEEN: table value == TARGET per level on %d of 26 (13 x asset_class + 13 x sub_asset_class)" % target_ok)
p("")
p("CONFLICT CENSUS OVER THE WHOLE MODULE UNION (the denominator the script itself uses)")
union = sorted(set(list(seeder.ETF_CLASSIFICATIONS.keys())
                   + list(seeder.ETF_SUB_ASSET_CLASS.keys())
                   + list(seeder.ETF_MANAGEMENT_STYLE.keys())
                   + list(seeder.ETF_SECTOR_MAPPING.keys())
                   + list(seeder.ETF_NAME_OVERRIDES.keys())))
all_conf = []
for tkr in union:
    _, _, conflicts = seeder.merge_item(tkr, live.get(tkr), ts)
    all_conf.extend(conflicts)
p("conflicting field(s): %d on %d ticker(s) of %d in the union" %
  (len(all_conf), len({c[0] for c in all_conf}), len(union)))
for c in all_conf:
    inset = "IN THE THIRTEEN" if c[0] in {t[0] for t in THIRTEEN} else "OUTSIDE THE THIRTEEN"
    p("  CONFLICT -- %s %s table=%s module=%s  [%s]" % (c[0], c[1], repr(c[2]), repr(c[3]), inset))
p("")
p("CONSEQUENCE FOR THE FACE'S INVOCATION: seed_table() returns 3 at the conflict branch")
p("BEFORE the batch_writer block (source lines 236-241 -- 'NOTHING WAS WRITTEN'), so the")
p("bare invocation is provably write-free while any conflict stands.")
io.open(".scratch/ac8_thirteen.txt", "w", encoding="ascii", newline="\n").write("\n".join(out) + "\n")
