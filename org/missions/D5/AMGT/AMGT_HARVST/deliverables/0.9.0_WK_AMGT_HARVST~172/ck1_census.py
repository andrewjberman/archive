"""ck1_census.py -- AMGT_HARVST HVST-ck-1 (round 96; CTO round-95 analysis section 3 item 3). READ-ONLY.

The path-component prefixes the gateway builds from a caller's security_key (not a security_key= partition), listed
under the RAW spelling (the key as typed, BP/_LN_Equity) and the CANONICAL spelling (crosswalk.slash_safe_key, the
partition form). For every slash key and every prefix: the objects under each spelling, the same-name pairs, and each
same-name pair's bodies GET whole and compared by SHA-256. No object is renamed, copied, written or deleted. The only
S3 operations reachable from this file are list_objects_v2 and get_object on opal-data-harvest.

Prefixes are READ from the gateway modules (module constants, the KEYED table, harvest_identity._segment, and the
_ledger literal), never typed here. Slash keys are READ from cj1_census.out (SLASHKEY-FOUND lines) and CONFIRMED by a
delimiter listing of every layer that carries a prefix (KEYSCAN).

Budget: 4000 requests and 400 MiB of GET body bytes, enforced in the wrapper; the last line counts both.
Usage, from the worktree root:  python -u <this file>   (writes ck1_census.out beside this file)
"""

import hashlib
import os
import re
import sys
from datetime import timezone

ROOT = os.getcwd()
GW = os.path.join(ROOT, "infra", "aws", "ec2", "opal-gateway")
APP = os.path.join(GW, "app")
sys.path.insert(0, GW)
sys.path.insert(0, ROOT)

from app import harvest_figures as hfig  # noqa: E402
from app import harvest_identity as hid  # noqa: E402
from app import harvest_research as hres  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "ck1_census.out")
CJ1_OUT = os.path.join(ROOT, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                       "0.9.0_WK_AMGT_HARVST~171", "cj1_census.out")
BUCKET = "opal-data-harvest"
BUDGET_REQUESTS = 4000
BUDGET_BYTES = 400 * 1024 * 1024
CONTROL_NAME = "UNH_US_Equity"
SAMPLE_SLASH_KEY = "BP/_LN_Equity"
TOKEN = crosswalk.SLASH_SAFE_TOKEN
# the cj1 rule for a raw nested key: its second segment is a canonical key tail (<CC>_Equity)
KEY_TAIL = re.compile(r"[A-Z]{2}_Equity$")

TOOL_BY_CONST = {
    "P_MANAGEMENT": hres.TOOL_RESEARCH,
    "P_FILINGS": hres.TOOL_FILINGS,
    "P_DRAFTING": hres.TOOL_FILINGS,
    "P_PEERS": hres.TOOL_PEERS,
    "P_SCORES": hres.TOOL_PEERS,
    "P_POSTURE": hres.TOOL_PEERS,
}


class Budget(Exception):
    pass


class RO(object):
    """Read-only S3 access on the harvest bucket. Only list_objects_v2 and get_object exist here."""

    def __init__(self, client):
        self._c = client
        self.requests = 0
        self.bytes = 0

    def _spend(self):
        self.requests += 1
        if self.requests > BUDGET_REQUESTS or self.bytes > BUDGET_BYTES:
            raise Budget()

    def list_page(self, **kw):
        if kw.get("Bucket") != BUCKET:
            raise RuntimeError("census lists %s only; a list named bucket %r" % (BUCKET, kw.get("Bucket")))
        self._spend()
        return self._c.list_objects_v2(**kw)

    def get(self, key):
        self._spend()
        resp = self._c.get_object(Bucket=BUCKET, Key=key)
        data = resp["Body"].read()
        self.bytes += len(data)
        if self.bytes > BUDGET_BYTES:
            raise Budget()
        return data

    def __getattr__(self, name):
        raise RuntimeError("census is read-only: refuses S3 operation %r" % name)


def list_all(ro, prefix, delimiter=None):
    """(common prefixes, objects) under prefix, every page. Objects are the raw list entries (dicts)."""
    cps, objs = [], []
    token = None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": prefix}
        if delimiter:
            kw["Delimiter"] = delimiter
        if token:
            kw["ContinuationToken"] = token
        resp = ro.list_page(**kw)
        cps += [c["Prefix"] for c in resp.get("CommonPrefixes", []) or []]
        objs += list(resp.get("Contents", []) or [])
        if not resp.get("IsTruncated"):
            break
        token = resp.get("NextContinuationToken")
    return sorted(set(cps)), objs


def source_line(fname, needle):
    """(line number, line text) of the first line of app/fname containing needle; (0, '') when absent."""
    with open(os.path.join(APP, fname), "r", encoding="utf-8") as fh:
        for number, line in enumerate(fh, start=1):
            if needle in line:
                return number, line.rstrip("\r\n")
    return 0, ""


def shape_of(template):
    return "object" if template.endswith(".json") else "dir"


def build_sites():
    """Every non-partition prefix or key template built from a caller's spelling, read from the modules."""
    sites = []
    for attr in sorted(a for a in dir(hres) if a.startswith("P_")):
        tpl = getattr(hres, attr)
        if not isinstance(tpl, str) or "%s" not in tpl or "security_key=" in tpl:
            continue
        number, _text = source_line("harvest_research.py", "%s = " % attr)
        sites.append(dict(name=attr, display=tpl, source="harvest_research.py:%d" % number, shape=shape_of(tpl),
                          tool=TOOL_BY_CONST.get(attr, "UNMAPPED"), layer=tpl.split("%s")[0],
                          instantiate=(lambda k, t=tpl: t % k)))
    for attr in sorted(a for a in dir(hfig) if a.endswith("_PREFIX")):
        val = getattr(hfig, attr)
        if not isinstance(val, str) or not val.startswith("derived/"):
            continue
        tpl = val + "%s/"
        number, _text = source_line("harvest_figures.py", "%s + spelled" % attr)
        sites.append(dict(name=attr, display=tpl, source="harvest_figures.py:%d" % number, shape="dir",
                          tool="harvest_get_fundamentals", layer=val,
                          instantiate=(lambda k, t=tpl: t % k)))
    for prefix, tpl, _layer in hid.KEYED:
        if tpl == hid._HIVE:
            continue
        number, _text = source_line("harvest_identity.py", '"%s", ' % prefix)
        if tpl == hid._DIR:
            display, shape = prefix + "%s/", "dir"
        elif tpl == hid._ROOT:
            display, shape = prefix + "<root of key>/", "dir"
        elif tpl == hid._CC:
            display, shape = prefix + "<cc of key>/", "dir"
        else:
            display, shape = prefix + "%s", "object"
        sites.append(dict(name="KEYED:" + prefix, display=display, source="harvest_identity.py:%d" % number,
                          shape=shape, tool=hid.COVERAGE_TOOL, layer=prefix,
                          instantiate=(lambda k, p=prefix, t=tpl: p + hid._segment(t, k, k))))
    number, text = source_line("harvest_identity.py", 'input_ledger.json" % key')
    m = re.search(r'"(packs/%s/input_ledger\.json)"', text)
    if m:
        tpl = m.group(1)
        sites.append(dict(name="_ledger", display=tpl, source="harvest_identity.py:%d" % number, shape="object",
                          tool=hid.COVERAGE_TOOL, layer="packs/",
                          instantiate=(lambda k, t=tpl: t % k)))
    return sites


def distinct_templates(sites, out):
    distinct = []
    for s in sites:
        d = s["display"]
        match = None
        for t in distinct:
            if t["display"] == d or t["display"] == d + ".json":
                match = t
                break
        if match is None:
            entry = dict(s)
            entry["sources"] = [s["source"]]
            entry["tools"] = [s["tool"]]
            entry["names"] = [s["name"]]
            distinct.append(entry)
            tag = "distinct"
        else:
            match["sources"].append(s["source"])
            if s["tool"] not in match["tools"]:
                match["tools"].append(s["tool"])
            match["names"].append(s["name"])
            tag = "dup-of:%s" % match["display"]
        out("PREFIX %s template=%s source=%s shape=%s tool=%s layer=%s %s"
            % (s["name"], d, s["source"], s["shape"], s["tool"], s["layer"], tag))
    return distinct


def keyscan(ro, layer, out):
    """Slash keys found by listing one layer: encoded names and raw nested keys X/<tail>. Returns decoded keys."""
    cps, objs = list_all(ro, layer, "/")
    found = set()
    sub_listings = 0
    other_sub = 0
    encoded = 0
    candidates = []
    for o in objs:
        base = o["Key"][len(layer):]
        base = base[:-5] if base.endswith(".json") else base
        if TOKEN in base:
            encoded += 1
            found.add(base)
    for c in cps:
        d = c[len(layer):].rstrip("/")
        if TOKEN in d:
            encoded += 1
            found.add(d)
            continue
        sub_listings += 1
        scps, sobjs = list_all(ro, c, "/")
        for sc in scps:
            s = sc[len(c):].rstrip("/")
            if KEY_TAIL.search(s):
                candidates.append(d + "/" + s)
            else:
                other_sub += 1
        for so in sobjs:
            s = so["Key"][len(c):]
            s = s[:-5] if s.endswith(".json") else s
            if TOKEN in s:
                encoded += 1
                found.add(d + "/" + s)
            elif KEY_TAIL.search(s):
                candidates.append(d + "/" + s)
            else:
                other_sub += 1
    decoded = set()
    for name in sorted(found):
        try:
            decoded.add(crosswalk.security_key_from_slash_safe(name))
        except Exception as exc:  # recorded, never silently dropped
            out("KEYSCAN-REFUSED layer=%s name=%s: %s" % (layer, name, str(exc)[:100]))
    for cand in sorted(set(candidates)):
        decoded.add(cand)
    out("KEYSCAN layer=%s top_entries=%d top_objects=%d sub_listings=%d raw_nested_candidates=%d encoded_names=%d other_sub=%d"
        % (layer, len(cps) + len(objs), len(objs), sub_listings, len(set(candidates)), encoded, other_sub))
    for cand in sorted(set(candidates)):
        out("KEYSCAN-CANDIDATE layer=%s key=%s" % (layer, cand))
    return decoded


def classify_pair(raw_present, canon_present, raw_digest, canon_digest):
    """The census's one classifier: equal | differ | raw_only | canonical_only | neither."""
    if raw_present and canon_present:
        return "equal" if raw_digest == canon_digest else "differ"
    if raw_present:
        return "raw_only"
    if canon_present:
        return "canonical_only"
    return "neither"


def utc(ts):
    return ts.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def inst_objects(ro, template, spelled):
    """{name: (object key, size, LastModified)} under one spelling of a key, and the prefix string listed."""
    prefix = template["instantiate"](spelled)
    if template["shape"] == "object":
        _cps, objs = list_all(ro, prefix)
        hits = [o for o in objs if o["Key"] == prefix]
        if not hits:
            return {}, prefix
        o = hits[0]
        return {"(object)": (o["Key"], o.get("Size", 0), o["LastModified"])}, prefix
    _cps, objs = list_all(ro, prefix)
    result = {}
    for o in objs:
        if o["Key"] == prefix:
            continue
        result[o["Key"][len(prefix):]] = (o["Key"], o.get("Size", 0), o["LastModified"])
    return result, prefix


def main():
    fh = open(OUT_PATH, "w", encoding="utf-8", newline="\n")

    def out(text):
        safe = text.encode("ascii", "backslashreplace").decode("ascii")
        print(safe, flush=True)
        fh.write(safe + "\n")
        fh.flush()

    ro = RO(store._default_client())
    out("CENSUS-HEADER HVST-ck-1 path-component prefix census under both slash-key spellings (round 96, CTO round-95 "
        "analysis section 3 item 3); READ-ONLY list and get on bucket %s only" % BUCKET)
    out("CENSUS-HEADER budget_requests=%d budget_bytes=%d; a list page is one request; bytes counts GET body bytes only"
        % (BUDGET_REQUESTS, BUDGET_BYTES))
    out("CENSUS-HEADER raw = the key as typed; canonical = crosswalk.slash_safe_key(key); prefixes read from app/harvest_research.py, harvest_figures.py, harvest_identity.py")
    out("SELF-CHECK slash_safe_key(%s)=%s" % (SAMPLE_SLASH_KEY, crosswalk.slash_safe_key(SAMPLE_SLASH_KEY)))
    try:
        sites = build_sites()
        templates = distinct_templates(sites, out)
        out("PREFIX-COUNT sites=%d distinct=%d" % (len(sites), len(templates)))

        cj1 = []
        with open(CJ1_OUT, "r", encoding="utf-8") as cfh:
            for line in cfh:
                if line.startswith("SLASHKEY-FOUND "):
                    cj1.append(line[len("SLASHKEY-FOUND "):].strip())
        cj1 = sorted(set(cj1))
        out("CJ1-SLASHKEYS n=%d keys=%s" % (len(cj1), ",".join(cj1)))

        found = set()
        layers = sorted(set(t["layer"] for t in templates))
        for layer in layers:
            found |= keyscan(ro, layer, out)
        listed_slash = sorted(k for k in found if "/" in k)
        out("KEYSCAN-SLASH-SET layers=%d found=%d cj1=%d match=%s found_keys=%s"
            % (len(layers), len(listed_slash), len(cj1), "yes" if listed_slash == cj1 else "no",
               ",".join(listed_slash)))
        keys = sorted(set(cj1) | set(listed_slash))
        out("KEY-SET slash_keys=%d keys=%s" % (len(keys), ",".join(keys)))

        # the matrix: every key x every distinct prefix, both spellings
        totals = dict(raw=0, canon=0, same=0, differ=0, cells=0)
        matrix = {}
        for t in templates:
            matrix[t["display"]] = dict(raw=0, canon=0, same=0, equal=0, differ=0, raw_only=0, canon_only=0)
        for key in keys:
            canon = crosswalk.slash_safe_key(key)
            for t in templates:
                raw_map, raw_prefix = inst_objects(ro, t, key)
                can_map, can_prefix = inst_objects(ro, t, canon)
                names = sorted(set(raw_map) | set(can_map))
                labels = {}
                for name in names:
                    rp = name in raw_map
                    cp = name in can_map
                    rd = cd = None
                    if rp and cp:
                        rd = hashlib.sha256(ro.get(raw_map[name][0])).hexdigest()
                        cd = hashlib.sha256(ro.get(can_map[name][0])).hexdigest()
                    label = classify_pair(rp, cp, rd, cd)
                    labels[name] = label
                    if label in ("equal", "differ"):
                        rk, rsz, rlm = raw_map[name]
                        ck, csz, clm = can_map[name]
                        out("PAIR %s %s %s raw_sha256=%s canonical_sha256=%s equal=%s raw_bytes=%d canonical_bytes=%d "
                            "raw_last_modified=%s canonical_last_modified=%s"
                            % (key, t["display"], name, rd[:12], cd[:12], "yes" if label == "equal" else "no",
                               rsz, csz, utc(rlm), utc(clm)))
                n_same = sum(1 for v in labels.values() if v in ("equal", "differ"))
                n_eq = sum(1 for v in labels.values() if v == "equal")
                n_dif = sum(1 for v in labels.values() if v == "differ")
                n_ro = sum(1 for v in labels.values() if v == "raw_only")
                n_co = sum(1 for v in labels.values() if v == "canonical_only")
                out("CELL %s %s raw_objects=%d canonical_objects=%d same_name=%d same_name_equal=%d "
                    "same_name_differ=%d raw_only=%d canonical_only=%d raw_prefix=%s canonical_prefix=%s"
                    % (key, t["display"], len(raw_map), len(can_map), n_same, n_eq, n_dif, n_ro, n_co,
                       raw_prefix, can_prefix))
                m = matrix[t["display"]]
                m["raw"] += len(raw_map)
                m["canon"] += len(can_map)
                m["same"] += n_same
                m["equal"] += n_eq
                m["differ"] += n_dif
                m["raw_only"] += n_ro
                m["canon_only"] += n_co
                totals["raw"] += len(raw_map)
                totals["canon"] += len(can_map)
                totals["same"] += n_same
                totals["differ"] += n_dif
                totals["cells"] += 1
        for t in templates:
            m = matrix[t["display"]]
            out("MATRIX %s raw_objects=%d canonical_objects=%d same_name=%d same_name_equal=%d same_name_differ=%d "
                "raw_only=%d canonical_only=%d tools=%s" % (t["display"], m["raw"], m["canon"], m["same"], m["equal"],
                                                           m["differ"], m["raw_only"], m["canon_only"],
                                                           ",".join(t["tools"])))

        # controls
        unh_raw = CONTROL_NAME
        unh_canon = crosswalk.slash_safe_key(CONTROL_NAME)
        pos_same = all(t["instantiate"](unh_raw) == t["instantiate"](unh_canon) for t in templates)
        out("CONTROL-POSITIVE %s raw_equals_canonical=%s" % (CONTROL_NAME, "yes" if pos_same else "no"))
        results = [classify_pair(True, True, "a" * 8, "a" * 8), classify_pair(True, True, "a" * 8, "b" * 8),
                   classify_pair(True, False, None, None), classify_pair(False, True, None, None)]
        out("CONTROL-NEGATIVE synthetic equal=%s differ=%s raw_only=%s canonical_only=%s"
            % (results[0], results[1], results[2], results[3]))

        out("CENSUS-PATHKEY slash_keys=%d prefixes=%d cells=%d raw_objects=%d canonical_objects=%d same_name=%d "
            "same_name_differ=%d gets=%d bytes=%d"
            % (len(keys), len(templates), totals["cells"], totals["raw"], totals["canon"], totals["same"],
               totals["differ"], ro.requests, ro.bytes))
    except Budget:
        out("BUDGET-EXCEEDED gets=%d bytes=%d -- census stopped at the budget; no CENSUS-PATHKEY line"
            % (ro.requests, ro.bytes))
        fh.close()
        return 2
    fh.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
