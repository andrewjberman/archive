"""AMGT-ak-3 (B5) -- READ-ONLY rewrite plan for the STORED CEO-search `basis` sentences.

Scans the pool: every M-1 object (`management/v1/<key>/<as_of>.json`), newest per key, whose
`ceo_public_profile.basis` matches `SERP|contract's search`. The replacement is computed BY CALLING THE
FIXED PRODUCER (`enrich.ceo_public_profile`) with a STUB search (no vendor call) shaped by the case read
from the object's STORED fields: `ir_domain`, `query`, `ceo_name`, `status`, `absence_class`, and the url
counts in the old basis. An object whose case cannot be read from its stored fields, or whose producer
result disagrees with the stored machine fields, is listed under "unreparseable" with its key and reason --
never hand-typed. WRITES NOTHING to the pool: list and get only. One output: m1_ceo_basis_plan.json here.

Run from the worktree root:  PYTHONPATH="$(pwd)" python <this file>"""
import json
import os
import re
import sys

from lib.research.api import scoped_amgt
from lib.research.api.scoped_amgt import pool_reader
from lib.research.management import enrich

MATCH = re.compile(r"SERP|contract's search")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "m1_ceo_basis_plan.json")
COUNT = re.compile(r"(\d+) url\(s\)")
RESOLVED_OLD = re.compile(r"(\d+) url\(s\) returned, (\d+) on the IR domain")
CANNOT_OLD = re.compile(r"^the SERP returned (\d+) url\(s\) and none on (\S+) --")
ZERO_OLD = re.compile(r"^the SERP returned 0 url\(s\) for ")


class _Stub:
    """A stand-in for the search primitive: returns the urls the case implies, or raises. No network."""

    def __init__(self, urls=None, exc=None):
        self.urls, self.exc = urls, exc

    def serp_brightdata(self, query, max_pages=1):
        if self.exc:
            raise self.exc
        return self.urls


def newest_per_key(client, prefix):
    keys = {}
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=pool_reader.POOL_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            parts = obj["Key"][len(prefix):].split("/")
            if len(parts) == 2 and parts[1].endswith(".json"):
                keys.setdefault(parts[0], []).append(obj["Key"])
    return {name: sorted(ks)[-1] for name, ks in keys.items()}


def get(client, key):
    return json.loads(client.get_object(Bucket=pool_reader.POOL_BUCKET, Key=key)["Body"].read().decode("utf-8"))


def case_stub(profile):
    """(ir_domain, stub, case_name) read from the STORED fields, or (None, None, reason)."""
    basis = profile.get("basis") or ""
    ir_domain = profile.get("ir_domain") or None
    query = profile.get("query")
    if query is None:
        if ir_domain is None and basis.startswith("no declared IR domain"):
            return None, None, "no_domain"
        return None, None, "query is null but the case is not the no-domain sentence"
    if not ir_domain:
        return None, None, "query is set but ir_domain is null"
    if basis.startswith("the SERP primitive raised:"):
        return None, None, "the sentence is the CEO-search module's (ceo_search._searched_basis), not ceo_public_profile's"
    if basis.startswith("the SERP primitive raised"):
        return ir_domain, _Stub(exc=RuntimeError("stub")), "search_failed"
    if ZERO_OLD.match(basis):
        return ir_domain, _Stub(urls=[]), "nothing_found"
    cannot = CANNOT_OLD.match(basis)
    if cannot and cannot.group(2).lower() == ir_domain.lower():
        return ir_domain, _Stub(urls=["https://unrelated.invalid/%d" % i for i in range(int(cannot.group(1)))]), "cannot_say"
    resolved = RESOLVED_OLD.search(basis)
    if resolved and basis.startswith("Bright Data SERP zone"):
        n, k = int(resolved.group(1)), int(resolved.group(2))
        if k < 1 or k > n:
            return None, None, "resolved url counts do not read (%d of %d)" % (k, n)
        urls = ["https://%s/p%d" % (ir_domain, i) for i in range(k)] + ["https://unrelated.invalid/%d" % i for i in range(n - k)]
        return ir_domain, _Stub(urls=urls), "resolved"
    return None, None, "the stored basis matches no sentence the producer wrote"


def main():
    client = scoped_amgt._pool_client()
    m1 = newest_per_key(client, scoped_amgt.MANAGEMENT_PREFIX)
    entries, unreparseable, by_case = [], [], {}
    for name, key in sorted(m1.items()):
        doc = get(client, key)
        profile = doc.get("ceo_public_profile")
        basis = profile.get("basis") if isinstance(profile, dict) else None
        if not isinstance(basis, str) or not MATCH.search(basis):
            continue
        security_key = doc.get("security_key") or name
        ir_domain, stub, case = case_stub(profile)
        if stub is None and case != "no_domain":
            unreparseable.append({"security_key": security_key, "store_key": key, "before": basis, "why": case})
            continue
        officers = [{"name": profile.get("ceo_name") or "Name", "role": "Chief Executive Officer"}]
        made = enrich.ceo_public_profile(officers, ir_domain, serp=stub)
        # the producer's machine fields must equal the stored ones, or the case was misread
        stored_status, stored_class = profile.get("status"), profile.get("absence_class")
        same = (made.get("status") == stored_status and made.get("query") == profile.get("query")
                and (stored_class is None or made.get("absence_class") == stored_class or case == "search_failed"))
        after = made.get("basis")
        if not same or not isinstance(after, str) or MATCH.search(after):
            unreparseable.append({"security_key": security_key, "store_key": key, "before": basis,
                                  "why": "producer result disagrees with the stored status/query/absence_class (%s)" % case})
            continue
        by_case[case] = by_case.get(case, 0) + 1
        entries.append({"security_key": security_key, "route": "thesis",
                        "json_path": ".management.ceo_public_profile.basis", "store_key": key,
                        "store_field": "ceo_public_profile.basis", "before": basis, "after": after, "case": case})
    plan = {"denominator": len(m1), "denominator_unit": "M-1 objects scanned (newest per security key)",
            "entries_by_case": by_case, "entries": entries, "unreparseable": unreparseable}
    with open(OUT, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(plan, handle, indent=1, ensure_ascii=True)
        handle.write("\n")
    print("M-1 scanned %d; entries %d %s; unreparseable %d" % (len(m1), len(entries), by_case, len(unreparseable)))
    for u in unreparseable:
        print("  UNREPARSEABLE %s: %s" % (u["security_key"], u["why"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
