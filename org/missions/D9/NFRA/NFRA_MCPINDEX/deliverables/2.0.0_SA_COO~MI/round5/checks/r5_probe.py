"""r5_probe.py -- NFRA_MCPINDEX round-5 check helper (2.0.0_SA_COO~MI). Read-only; no network call.

usage (from the WORKSPACE root):
  python r5_probe.py s15            dim_transaction is declared on all 6 surfaces beside the three dim_* tables
  python r5_probe.py q3route        (run with cwd = the gateway dir) discover's mac.01 match names an MCP tool, not the route
  python r5_probe.py t13            a blackdiamond integration is registered and a catalog row names one of its tools
Prints one line per surface and a denominator; exit 0 only when every surface holds.
"""
import json
import re
import sys
from pathlib import Path

GW = Path("infra/aws/ec2/opal-gateway")
TF = Path("infra/aws/terraform/opal-gateway/schwab_reader_iam.tf")
DS = "dim_transaction"
MASTERS = ("08242234", "08335338")


def _read(p):
    return Path(p).read_text(encoding="utf-8")


def s15():
    res = []
    d = json.loads(_read(GW / "app/integrations/schwab/datasets.json"))
    ds = d.get("datasets")
    names = set(ds) if isinstance(ds, dict) else {str(x.get("name", x.get("dataset", ""))) for x in (ds or []) if isinstance(x, dict)}
    res.append(("datasets.json datasets", DS in names))
    q = _read(GW / "app/integrations/schwab/query.py")
    schemas = q.split("DATASET_SCHEMAS", 1)[-1].split("SCHEMA_SOURCE", 1)[0]
    res.append(("query.py DATASET_SCHEMAS", '"%s"' % DS in schemas))
    grains = q.split("DATASET_GRAINS", 1)[-1][:2000]
    res.append(("query.py DATASET_GRAINS", '"%s"' % DS in grains))
    de = re.search(r"^DATASETS\s*=\s*\(([^)]*)\)", _read(GW / "app/data_entitlement.py"), re.M)
    res.append(("data_entitlement.py DATASETS", bool(de) and '"%s"' % DS in de.group(1)))
    au = re.search(r"^_DATASETS\s*=\s*frozenset\(\{([^}]*)\}\)", _read(GW / "app/schwab_audit.py"), re.M)
    res.append(("schwab_audit.py _DATASETS", bool(au) and '"%s"' % DS in au.group(1)))
    tf = re.search(r"schwab_data_prefixes\s*=\s*\[([^\]]*)\]", _read(TF), re.S)
    both = bool(tf) and all('"schwab/%s/silver/%s/"' % (m, DS) in tf.group(1) for m in MASTERS)
    res.append(("schwab_reader_iam.tf schwab_data_prefixes, both masters", both))
    for name, ok in res:
        print("%s %s" % ("OK:" if ok else "MISSING:", name))
    n = sum(1 for _, ok in res if ok)
    print("dim_transaction declared on %d of %d surfaces" % (n, len(res)))
    return 0 if n == len(res) else 1


def q3route():
    sys.path.insert(0, str(Path.cwd()))
    from app.graphql_plumbing import catalog_gate
    from app.integrations.opal_discover import integration as od
    ans = od.discover("macro data", catalog_gate.OPAL_INTERNAL)
    hit = [m for m in (ans.get("matches") or []) if str(m.get("property", {}).get("entity", "")).startswith("mac.01")]
    if not hit:
        print("no mac.01 match among %d matches" % len(ans.get("matches") or []))
        return 1
    nt = hit[0].get("next_tool") or {}
    name, kind = nt.get("name"), nt.get("kind")
    defs = 0
    for p in Path("app/integrations").rglob("*.py"):
        if re.search(r"^\s*(async\s+)?def\s+%s\s*\(" % re.escape(str(name)), p.read_text(encoding="utf-8"), re.M):
            defs += 1
    print("mac.01 next_tool=%s kind=%s; defined as a function in app/integrations: %d file(s)" % (name, kind, defs))
    return 0 if (kind == "mcp_tool" and name and name != "query_v0" and defs >= 1) else 1


def t13():
    import yaml
    reg = _read(GW / "app/integrations/registry.py")
    registered = bool(re.search(r"[\"']blackdiamond[\"']", reg))
    root = GW / "app/integrations/blackdiamond"
    defs = set()
    if root.is_dir():
        for p in root.rglob("*.py"):
            defs |= set(re.findall(r"^\s*(?:async\s+)?def\s+([a-z][a-z0-9_]*)\s*\(", p.read_text(encoding="utf-8"), re.M))
    cat = yaml.safe_load(_read(GW / "app/refs/DATA_CATALOG.yaml"))
    rows = []

    def walk(o):
        if isinstance(o, dict):
            if "read_tool" in o:
                rows.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(cat)
    bd_rows = [r for r in rows if str(r.get("read_tool")) in defs and str(r.get("read_tool")).startswith("blackdiamond_")]
    print("registry names blackdiamond=%s; functions under %s: %d; catalog rows with read_tool: %d; "
          "of them naming a blackdiamond_* blackdiamond function: %d" % (registered, root.as_posix(), len(defs), len(rows), len(bd_rows)))
    return 0 if (registered and bd_rows) else 1


if __name__ == "__main__":
    fn = {"s15": s15, "q3route": q3route, "t13": t13}.get(sys.argv[1] if len(sys.argv) > 1 else "")
    if fn is None:
        print(__doc__)
        sys.exit(2)
    sys.exit(fn())
