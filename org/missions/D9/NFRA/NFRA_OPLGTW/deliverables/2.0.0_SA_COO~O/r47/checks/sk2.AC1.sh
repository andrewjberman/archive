#!/usr/bin/env bash
# OPLGTW OG-sk-2 AC1 (round 47; the Schwab 0840 move to schwab/49financial/, the CTO's DUAL READ ruling 20:18Z): the Schwab catalog reads the NEW form first and the OLD form second for master 08403355 only, fenced by FILE NAME.
# One fresh process, MOCK_GRAPH=1, no network (a fake S3 client behind fake role objects). The API this cell fixes (names are the contract of this check):
#  contract (both copies, additive key; absent key = today's behaviour byte for byte):
#     "firm_form": {"masters": {"08403355": "49financial"}, "state_bucket": "opal-data-49financial",
#                   "silver_prefixes": ["schwab/49financial/silver/<t>/" for t in dim_position, dim_balance, dim_asset, dim_transaction],
#                   "completion_prefix": "schwab/49financial/state/complete/", "backfill_status_prefix": "schwab/49financial/state/backfill_status/"}
#  catalog.py: firm_form_masters(contract) -> dict master->firm ({} when the key is absent); state_bucket(contract) -> str|None;
#     marker_locations(contract, master, date) -> [(bucket, key), ...] NEW FIRST then OLD (only OLD for an old-form master);
#     parse_silver_key(key) accepts the new form schwab/49financial/silver/<table>/date=<d>/<master>.parquet and returns (master FROM THE FILE NAME, table, date, filename); a firm-folder key whose file name is not <8 digits>.parquet returns None;
#     Catalog.read_marker(master, date, policy_check) -> (marker|None, version|None, (bucket, key)|None): tries the new location, falls back to the old ONLY when the new one is ABSENT (NoSuchKey); any other error on the new location raises the module's dependency error (no fallback on an error);
#     Catalog.list_dates(master, policy_check): the UNION of dates under the new completion prefix (keys whose file name is <master>.complete.json only) and the old prefix, newest first.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
G=infra/aws/ec2/opal-gateway
res=$(MOCK_GRAPH=1 python3 -I - "$(native "$G")" <<'PYEOF'
import json, os, subprocess, sys, types, warnings
warnings.simplefilter("ignore")
G = sys.argv[1]
sys.path.insert(0, G)
os.environ["MOCK_GRAPH"] = "1"
from botocore.exceptions import ClientError
from app.integrations.schwab import catalog as C, aws_roles
ok = True


def say(label, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print("%s: %s%s" % (label, "ok" if cond else "NOT OK", (" (%s)" % extra) if extra else ""))


def attempt(f, *a, **k):
    try:
        return f(*a, **k)
    except Exception as e:
        return "raised %s: %s" % (type(e).__name__, str(e)[:90])


BASE_PIN = "5daeeef445dc32fd80c4da23b7345b991985d7aa"
base_raw = json.loads(subprocess.run(["git", "show", BASE_PIN], capture_output=True).stdout.decode("utf-8"))
new_raw = json.load(open(os.path.join(G, "deploy", "NFRA_OPLGTW_CONTRACT.json"), encoding="utf-8"))
std_path = os.path.join("org", "standards", "NFRA_OPLGTW_CONTRACT.json")
std_raw = json.load(open(std_path, encoding="utf-8")) if os.path.exists(std_path) else None
base_c = C.parse_contract(base_raw, "base")
cont = attempt(C.parse_contract, new_raw, "new")
if isinstance(cont, str):
    say("the new contract parses", False, cont)
    print("NO")
    sys.exit(0)
ff = new_raw.get("firm_form") or {}
say("contract firm_form keys: masters 08403355 -> 49financial, state_bucket opal-data-49financial, 4 silver prefixes, completion_prefix, backfill_status_prefix",
    ff.get("masters") == {"08403355": "49financial"} and ff.get("state_bucket") == "opal-data-49financial" and len(ff.get("silver_prefixes") or []) == 4
    and ff.get("completion_prefix") == "schwab/49financial/state/complete/" and ff.get("backfill_status_prefix") == "schwab/49financial/state/backfill_status/"
    and all(p.startswith("schwab/49financial/silver/") and p.endswith("/") for p in ff.get("silver_prefixes") or []))
same_old = all(getattr(cont, f) == getattr(base_c, f) for f in ("bucket", "masters", "datasets", "data_prefixes", "completion_prefixes", "completion_prefix_by_master", "reader_role", "catalog_role"))
say("every OLD-form field of the parsed contract equals the pinned base contract's (the old form is the fallback, unchanged)", same_old)
say("the deploy copy and the standards copy are identical (parsed)", std_raw is None or std_raw == new_raw)
say("firm_form_masters and state_bucket accessors", attempt(lambda: C.firm_form_masters(cont)) == {"08403355": "49financial"} and attempt(lambda: C.state_bucket(cont)) == "opal-data-49financial"
    and attempt(lambda: C.firm_form_masters(base_c)) == {} and attempt(lambda: C.state_bucket(base_c)) is None)
nk = "schwab/49financial/silver/dim_position/date=2026-10-20/08403355.parquet"
ok_parse = (C.parse_silver_key(nk) == ("08403355", "dim_position", "2026-10-20", "08403355.parquet")
            and C.parse_silver_key("schwab/08403355/silver/dim_position/date=2026-10-20/data.parquet") == ("08403355", "dim_position", "2026-10-20", "data.parquet")
            and C.parse_silver_key("schwab/49financial/silver/dim_position/date=2026-10-20/data.parquet") is None
            and C.parse_silver_key("schwab/49financial/silver/dim_position/date=2026-10-20/08242234.parquet")[0] == "08242234")
say("parse_silver_key: new form takes the master from the FILE NAME; old form unchanged; a firm-folder data.parquet is refused", ok_parse)
closure = {"master": "08403355", "date": "2026-10-20", "tables": {"dim_position": {"object": {"key": nk}}}, "objects": []}
bad = {"master": "08403355", "date": "2026-10-20", "tables": {"dim_position": {"object": {"key": "schwab/49financial/silver/dim_position/date=2026-10-20/08242234.parquet"}}}, "objects": []}
old = {"master": "08403355", "date": "2026-10-20", "tables": {"dim_position": {"object": {"key": "schwab/08403355/silver/dim_position/date=2026-10-20/data.parquet"}}}, "objects": []}
marker = {"master": "08403355", "date": "2026-10-20"}
f_new = [x["class"] for x in attempt(C.membership_findings, marker, closure, "08403355", "2026-10-20", cont)] if isinstance(attempt(C.membership_findings, marker, closure, "08403355", "2026-10-20", cont), list) else ["ERR"]
f_bad = [x["class"] for x in attempt(C.membership_findings, marker, bad, "08403355", "2026-10-20", cont)] if isinstance(attempt(C.membership_findings, marker, bad, "08403355", "2026-10-20", cont), list) else ["ERR"]
f_old = [x["class"] for x in attempt(C.membership_findings, marker, old, "08403355", "2026-10-20", cont)] if isinstance(attempt(C.membership_findings, marker, old, "08403355", "2026-10-20", cont), list) else ["ERR"]
say("membership: the new-form 08403355 key and the old-form key pass; a PLANTED 08242234 file in the firm folder is refused (F_REJECTED_MASTER)", f_new == [] and f_old == [] and C.F_REJECTED_MASTER in f_bad, "new %s old %s planted %s" % (f_new, f_old, f_bad))
hs = attempt(C.head_set, {"tables": {"dim_position": {"object": {"key": nk}}}, "objects": [{"table": "dim_position", "key": "schwab/49financial/silver/dim_position/date=2026-10-20/08242234.parquet"}, {"table": "dim_position", "key": "schwab/08403355/silver/dim_position/date=2026-10-20/data.parquet"}]}, cont)
hkeys = sorted(r["key"] for r in hs) if isinstance(hs, list) else hs
say("head_set keeps the new-form and old-form 08403355 keys and DROPS the planted 08242234 file in the firm folder", hkeys == sorted([nk, "schwab/08403355/silver/dim_position/date=2026-10-20/data.parquet"]), str(hkeys)[:200])
loc = attempt(lambda: C.marker_locations(cont, "08403355", "2026-10-20"))
loc_old = attempt(lambda: C.marker_locations(cont, "08335338", "2026-10-20"))
say("marker_locations: 08403355 new first (state bucket) then old; 08335338 old only",
    loc == [("opal-data-49financial", "schwab/49financial/state/complete/date=2026-10-20/08403355.complete.json"), ("opal-data-assets", "schwab/08403355/meta/complete/date=2026-10-20.json")]
    and loc_old == [("opal-data-assets", "schwab/08335338/meta/complete/date=2026-10-20.json")], str(loc)[:200])


class NoKey(ClientError):
    def __init__(self):
        super().__init__({"Error": {"Code": "NoSuchKey", "Message": "x"}}, "GetObject")


class Denied(ClientError):
    def __init__(self):
        super().__init__({"Error": {"Code": "AccessDenied", "Message": "x"}}, "GetObject")


class FakeS3:
    def __init__(self, objs, denied=()):
        self.objs, self.denied, self.calls = objs, set(denied), []

    def get_object(self, Bucket, Key, **kw):
        self.calls.append(("get", Bucket, Key))
        if (Bucket, Key) in self.denied:
            raise Denied()
        if (Bucket, Key) not in self.objs:
            raise NoKey()
        body = self.objs[(Bucket, Key)]
        return {"Body": types.SimpleNamespace(read=lambda n=None, b=body: b), "VersionId": "v1"}

    def list_objects_v2(self, Bucket, Prefix, MaxKeys=1000, ContinuationToken=None, **kw):
        self.calls.append(("list", Bucket, Prefix))
        return {"Contents": [{"Key": k} for (b, k) in sorted(self.objs) if b == Bucket and k.startswith(Prefix)], "IsTruncated": False}


def catalog_with(fake):
    def role(kind):
        return types.SimpleNamespace(config=types.SimpleNamespace(kind=kind), session=lambda pc: types.SimpleNamespace(client=lambda n: fake))
    return C.Catalog(contract=cont, catalog_role=role(aws_roles.CATALOG), data_role=role(aws_roles.READER), store=object())


mj = json.dumps({"master": "08403355", "date": "2026-10-20", "closure": {"x": 1}}).encode()
NB, OB = "opal-data-49financial", "opal-data-assets"
NEWK = "schwab/49financial/state/complete/date=2026-10-20/08403355.complete.json"
OLDK = "schwab/08403355/meta/complete/date=2026-10-20.json"
f1 = FakeS3({(OB, OLDK): mj})
r1 = attempt(lambda: catalog_with(f1).read_marker("08403355", "2026-10-20", lambda *a, **k: None))
say("read_marker: the new location is ABSENT -> the old location is read (location reported old)", isinstance(r1, tuple) and r1[0] == {"master": "08403355", "date": "2026-10-20", "closure": {"x": 1}} and r1[2] == (OB, OLDK) and f1.calls[0] == ("get", NB, NEWK), str(r1)[:160])
f2 = FakeS3({(NB, NEWK): mj, (OB, OLDK): b"{}"})
r2 = attempt(lambda: catalog_with(f2).read_marker("08403355", "2026-10-20", lambda *a, **k: None))
say("read_marker: both present -> the NEW one wins and the old one is not read", isinstance(r2, tuple) and r2[2] == (NB, NEWK) and not any(c[2] == OLDK for c in f2.calls), str(r2)[:120])
f3 = FakeS3({(OB, OLDK): mj}, denied={(NB, NEWK)})
r3 = attempt(lambda: catalog_with(f3).read_marker("08403355", "2026-10-20", lambda *a, **k: None))
say("read_marker: an ERROR (AccessDenied) on the new location raises the dependency error and does NOT fall back to the old", isinstance(r3, str) and r3.startswith("raised _Dependency") and any(c[2] == NEWK for c in f3.calls) and not any(c[2] == OLDK for c in f3.calls), str(r3)[:120])
f4 = FakeS3({(OB, "schwab/08335338/meta/complete/date=2026-10-20.json"): mj})
r4 = attempt(lambda: catalog_with(f4).read_marker("08335338", "2026-10-20", lambda *a, **k: None))
say("read_marker for an old-form master touches the old location only (no state-bucket call)", isinstance(r4, tuple) and not any(c[1] == NB for c in f4.calls), str(f4.calls)[:120])
lst = {(NB, "schwab/49financial/state/complete/date=2026-10-21/08403355.complete.json"): b"{}", (NB, "schwab/49financial/state/complete/date=2026-10-20/08403355.complete.json"): b"{}",
       (NB, "schwab/49financial/state/complete/date=2026-10-22/08242234.complete.json"): b"{}", (OB, "schwab/08403355/meta/complete/date=2026-10-19.json"): b"{}",
       (OB, "schwab/08403355/meta/complete/date=2026-10-20.json"): b"{}"}
d1 = attempt(lambda: catalog_with(FakeS3(lst)).list_dates("08403355", lambda *a, **k: None))
d2 = attempt(lambda: catalog_with(FakeS3(lst)).list_dates("08335338", lambda *a, **k: None))
say("list_dates: the union of new and old dates, newest first, the PLANTED 08242234 file under the new prefix ignored; an old-form master lists the old prefix only",
    d1 == ["2026-10-21", "2026-10-20", "2026-10-19"] and d2 == [], "08403355 %s, 08335338 %s" % (d1, d2))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
