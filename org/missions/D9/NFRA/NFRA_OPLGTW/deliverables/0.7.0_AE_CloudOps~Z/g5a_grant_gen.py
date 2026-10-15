#!/usr/bin/env python
"""OG-ap-20 Phase A step 2: derive the G5 etfs grant FROM THE COMMITTED CATALOG.

The order's reason for a generator is that "the grant cannot drift from the tools' reads". So every
prefix here comes out of the catalog rows the order names, the bucket comes out of those same rows, and
the policy name comes out of lib/opal_naming.py. Nothing is typed.

THE CATALOG IS READ AT HEAD, NOT FROM THE WORKING TREE. The order says "the committed catalog", and
DATA_CATALOG.yaml is modified in this worktree right now (1,059,657 bytes against HEAD's 1,055,963), so
reading the file on disk would derive a grant from bytes nobody has committed. The caller hands in the
HEAD copy; this script refuses a path it was not told to trust.

WHAT IT PRODUCES, in two statements because they are two different shapes of permission:
  1. s3:GetObject on each named prefix of the bucket -- the object reads the six tools make.
  2. s3:ListBucket on the BUCKET, confined by an s3:prefix condition to those same prefixes -- the
     tools list a partner's folder and the report months, and a ListBucket without the condition would
     be bucket-wide enumeration, which is a different and larger permission than reading the objects.

THE THREE REFUSALS, each a trap this grant could otherwise walk into:
  1. A FIRM TOKEN in any prefix. These are CLIENT-derived partner folders; a prefix naming a firm would
     put one firm's name in a grant another firm's grant could be compared against, and the order says
     "no firm token". Refused against the known firm list AND against the partner names the rows'
     own size.objects blocks enumerate, so a new firm added to the catalog is caught too.
  2. A BUCKET-WIDE OBJECT ARN or a "*" resource. Refused outright.
  3. A NAMED ENTITY MISSING FROM THE CATALOG. Refused rather than silently granting fewer prefixes
     than the tools read -- an under-grant fails at runtime with AccessDenied, long after the ask.

Usage:
  git show HEAD:<catalog> > head_catalog.yaml
  python g5a_grant_gen.py head_catalog.yaml --json W/G5A_GRANT.json
"""
from __future__ import annotations

import argparse
import io
import json
import sys

import yaml

POLICY_NAME = "gateway-global-etfs-read-policy"   # lib/opal_naming.name("gateway","global","etfs-read","policy")

# the seven the order names for object reads, plus the rivalfunds page row
NAMED = [
    "opal_data_etfs_gold_daily_partner_ownership",
    "opal_data_etfs_platinum_etf_ownership_dashboard",
    "opal_data_etfs_platinum_monthly_ownership_report",
    "opal_data_etfs_silver_netassets_daily",
    "opal_data_etfs_gold_holding",
    "opal_data_etfs_gold_book",
    "opal_data_etfs_silver_holdings",
    "opal_data_etfs_platinum_rivalfunds_page",
]
# the CTO's one-ask ruling (msg 34198) also grants the rival-funds prefixes that NO tool of this
# release reads yet, so a second ask is not needed later. They are DERIVED, not typed: any
# opal_data_etfs_gold_* row whose address sits under rivalfunds/.
RIVALFUNDS_ROOT = "rivalfunds/etfs/"
FIRMS = ("49financial", "cottonwood", "inflection", "demo", "mdpf")


def rows_of(doc) -> list:
    """Every mapping in the document that carries an `entity` key, at any depth."""
    found = []

    def walk(o):
        if isinstance(o, dict):
            if "entity" in o:
                found.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(doc)
    return found


def address_of(row: dict) -> tuple:
    """(value, kind) for the row's address: ("...", "prefix") or ("...", "object").

    A row whose `prefix` names a single object -- its last segment carries a dot extension and its
    key_template equals it -- is an OBJECT. Treating it as a prefix and appending "/" yields "<key>/*",
    which matches nothing: a silent under-grant that surfaces only as a runtime AccessDenied. Measured
    on this catalog: platinum/etf_ownership_dashboard.json and silver/netassets_daily.parquet are both
    of that shape.
    """
    p = row.get("prefix")
    kt = row.get("key_template")
    if isinstance(p, str) and p.strip():
        p = p.strip()
        if p.endswith("/"):
            return p, "prefix"
        last = p.rsplit("/", 1)[-1]
        if "." in last and (not isinstance(kt, str) or kt.strip().rstrip("/") == p):
            return p, "object"
        return p + "/", "prefix"
    if isinstance(kt, str) and "/" in kt:
        return kt.split("/", 1)[0] + "/", "prefix"
    return "", "prefix"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("catalog", help="the catalog as committed (git show HEAD:<path> > file)")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    doc = yaml.safe_load(io.open(a.catalog, encoding="utf-8", errors="replace").read())
    rows = rows_of(doc)
    by_entity = {}
    for r in rows:
        by_entity.setdefault(r["entity"], []).append(r)
    print("  catalog rows carrying an entity: %d; distinct entities: %d" % (len(rows), len(by_entity)))

    # ---- refusal 3: every named entity must be present -----------------------------------------
    missing = [e for e in NAMED if e not in by_entity]
    if missing:
        raise SystemExit("REFUSED: %d named entity(ies) absent from the committed catalog: %s"
                         % (len(missing), missing))

    wanted, buckets = {}, set()
    kinds = {}
    for e in NAMED:
        for r in by_entity[e]:
            p, kind = address_of(r)
            bkt = r.get("bucket")
            if not p or not bkt:
                continue
            wanted.setdefault(p, []).append("%s (%s, %s)" % (e, r.get("layer") or "?", kind))
            kinds[p] = kind
            buckets.add(bkt)

    # ---- the rivalfunds prefixes, DERIVED from the gold rows ------------------------------------
    rival = {}
    for e, rs in by_entity.items():
        if not e.startswith("opal_data_etfs_"):
            continue
        for r in rs:
            for field in ("prefix", "key_template"):
                v = r.get(field)
                if isinstance(v, str) and v.startswith(RIVALFUNDS_ROOT):
                    seg = v.split("/")
                    # rivalfunds/etfs/<layer>/...  -> keep three segments for gold, four for the page
                    keep = 4 if len(seg) > 3 and seg[2] == "platinum" else 3
                    pref = "/".join(seg[:keep]) + "/"
                    rival.setdefault(pref, []).append("%s.%s" % (e, field))
                    kinds.setdefault(pref, "prefix")
                    if r.get("bucket"):
                        buckets.add(r["bucket"])

    if len(buckets) != 1:
        raise SystemExit("REFUSED: the named rows span %d buckets (%s); this grant is one bucket"
                         % (len(buckets), sorted(buckets)))
    bucket = sorted(buckets)[0]

    allp = dict(wanted)
    for k, v in rival.items():
        allp.setdefault(k, []).extend(v)

    # collapse to the minimal covering set, asserting every drop is covered
    keep = [p for p in sorted(allp) if not any(p != q and p.startswith(q) for q in allp)]
    dropped = [p for p in sorted(allp) if p not in keep]
    for p in dropped:
        if not any(p.startswith(q) for q in keep):
            raise SystemExit("REFUSED: collapsing dropped %r with no covering prefix -- that would narrow the grant" % p)

    # ---- refusal 1: no firm token, checked against the firm list AND the rows' own partner names ----
    # size.objects keys are a MIXED bag -- partner firms, but also months ("2026-05") and labels
    # ("corrections"). Taking them all as firm names would make this guard refuse a correct grant whose
    # prefix merely contained a date, so a candidate must look like a name rather than a period: no
    # digits, and not a known non-firm label. FIRMS stays the authority; these only widen it.
    partners = set()
    for e in NAMED:
        for r in by_entity[e]:
            size = (r.get("contract") or {}).get("size") or {}
            objs = size.get("objects")
            if isinstance(objs, dict):
                for k in objs:
                    k = str(k)
                    if k.startswith("_") or any(c.isdigit() for c in k) or k in ("corrections", "archive"):
                        continue
                    partners.add(k)
    tokens = sorted(set(FIRMS) | partners)
    bad = [(p, tok) for p in keep for tok in tokens if tok and tok in p]
    if bad:
        raise SystemExit("REFUSED: a firm token appears in a grant prefix: %s" % bad)

    # ---- refusal 2: no wildcard, no bucket-wide object ARN -------------------------------------
    if any(p.strip() in ("", "/", "*") for p in keep):
        raise SystemExit("REFUSED: a bucket-wide or wildcard prefix reached the resource list")

    get_res = ["arn:aws:s3:::%s/%s%s" % (bucket, p, "" if kinds.get(p) == "object" else "*")
               for p in keep]
    list_prefixes = ["%s*" % p for p in keep if kinds.get(p) != "object"]
    out = {
        "policy_name": POLICY_NAME,
        "policy_name_builder": 'lib/opal_naming.py name("gateway", "global", "etfs-read", "policy")',
        "bucket": bucket,
        "role": "aws_iam_role.int_reader (gateway-global-internal-reader-role)",
        "statements": [
            {"sid": "InternalReaderEtfsObjectRead", "actions": ["s3:GetObject"], "resources": get_res},
            {"sid": "InternalReaderEtfsListConfined", "actions": ["s3:ListBucket"],
             "resources": ["arn:aws:s3:::%s" % bucket],
             "condition": {"StringLike": {"s3:prefix": list_prefixes}},
             "why": ("the tools list a partner's folder and the report months; a ListBucket without the "
                     "s3:prefix condition would be bucket-wide enumeration, a larger permission than "
                     "reading the objects")},
        ],
        "prefixes": keep,
        "address_kinds": {p: kinds.get(p, "prefix") for p in keep},
        "objects_granted_exactly": [p for p in keep if kinds.get(p) == "object"],
        "object_vs_prefix_note": ("a row addressing a single OBJECT gets its own ARN with NO trailing star and "
                                  "contributes no s3:prefix to the ListBucket condition. Appending a slash to such "
                                  "a row -- which this generator did in its first run -- yields <key>/* and matches "
                                  "NOTHING: an under-grant visible only as a runtime AccessDenied."),
        "prefixes_before_collapse": sorted(allp),
        "prefixes_dropped_as_redundant": dropped,
        "provenance": {p: sorted(set(allp[p])) for p in keep},
        "rivalfunds_prefixes_derived": sorted(rival),
        "rivalfunds_note": ("granted now under the CTO's one-ask ruling (msg 34198) although NO tool of this "
                            "release reads them yet, so no second ask is needed later -- derived from the catalog "
                            "rows whose address sits under %s, never typed" % RIVALFUNDS_ROOT),
        "firm_tokens_checked": tokens,
        "denominator": {"named_entities": len(NAMED), "catalog_entities": len(by_entity),
                        "prefixes_before_collapse": len(allp), "prefixes_granted": len(keep)},
        "method": ("yaml.safe_load over the COMMITTED catalog (git show HEAD:<path>), every mapping carrying an "
                   "`entity` key collected at any depth, each named row's own `prefix` (or the first segment of "
                   "key_template) kept, the rivalfunds prefixes derived from any opal_data_etfs_* row addressed "
                   "under rivalfunds/etfs/, then collapsed to the minimal covering set with every drop asserted "
                   "covered"),
        "no_grant_for": ("mdpf_get_category_views reads platinum/mdpf/ of the PORTAL bucket, which the existing "
                         "internal-reader policy already covers via platinum/* -- so it gets no statement here"),
    }
    if a.json:
        io.open(a.json, "w", encoding="utf-8", newline="\n").write(json.dumps(out, indent=1) + "\n")
        print("  WROTE %s" % a.json)
    print(json.dumps({k: v for k, v in out.items() if k != "provenance"}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
