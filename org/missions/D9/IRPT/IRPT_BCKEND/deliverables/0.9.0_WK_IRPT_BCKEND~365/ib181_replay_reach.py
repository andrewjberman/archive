"""IB-pr-515 worker 0.9.0_WK_IRPT_BCKEND~365: replay arms on the BUILT and CURRENT-LIVE handler.py, and REACH per firm.

Derived from ib171_4_replay_reach.py (IB-pr-499, worker ~349). Two differences: the REACH counts are read from
LOCAL copies of the landed directory objects that the worker fetched with `.tools/aws s3api get-object` into
scratch (GET only), so no boto3 client is built here; and the output is the counts only.

Usage: python ib181_replay_reach.py <built.zip> <live.zip> <gold_dir> <lib_dir> <scratch_dir> <out.json>

The handler source is read from each zip IN MEMORY and executed as a module; nothing is written to disk.
The four arms run over a SYNTHETIC directory (opaque ids and made-up masks, the shapes of
directory/tests/test_tail_account_entry.py, re-stated here). search() and resolve() are pure: no Lambda is
invoked and no network call is made on that path.
"""
import copy
import hashlib
import json
import sys
import types
import zipfile

FIRM = "firm_tail"
_ACTIVE = {"indicator": "ACTIVE", "effective_date": None}
_GRANTED = {"entitled": "GRANTED", "reason": None}
_REVISION = {
    "directory_revision": "tail/synthetic/1.0",
    "source_revision": "tail/synthetic",
    "source_completion_date": "2026-10-01",
    "as_of_business_date": "2026-10-01",
}
_COHORT = {
    "fee_taking_status": "UNKNOWN",
    "advisory_status": "UNKNOWN",
    "vendor_account_supervised": "UNKNOWN",
    "hierarchy_path": [],
    "authoritative": False,
    "capability_facts": [],
}


def _entry(client, rel, accounts, masks, name, kind, with_masks=True):
    ids = {"firm_id": FIRM, "client_id": client, "account_ids": list(accounts)}
    if rel is not None:
        ids["relationship_id"] = rel
    e = {
        "ids": ids,
        "display_name": name,
        "masked_discriminator": masks[0],
        "permitted_scope": {"scope_kind": kind, "scope_ids": [rel or accounts[0]]},
        "permitted_capabilities": ["DIRECTORY_READ"],
        "termination": dict(_ACTIVE),
        "access": dict(_GRANTED),
        "revision": dict(_REVISION),
        "cohort": copy.deepcopy(_COHORT),
    }
    if with_masks:
        e["account_masks"] = [{"account_id": a, "masked_discriminator": m}
                              for a, m in zip(accounts, masks)]
    return e


REL_A = _entry("c_alpha", "r_alpha", ["a_head", "a_two", "a_three"],
               ["****1111 / IRA", "****2222 / JOINT", "****3333 / TRUST"],
               "Alpha Household", "RELATIONSHIP")
REL_B = _entry("c_gamma", "r_gamma", ["b_one", "b_two"],
               ["****9999 / IRA", "****2222 / IRA"],
               "Gamma Holdings", "RELATIONSHIP")
SOLO = _entry("c_solo", None, ["z_one"], ["****7777 / IRA"], "Solo Entry", "ACCOUNT",
              with_masks=False)
DIRECTORY = {"entries": [REL_A, REL_B, SOLO]}


def _scope(accounts):
    return {
        "principal_class": "STAFF",
        "permitted_account_set": list(accounts),
        "verified_request_firm_id": FIRM,
        "entitlement_revision": "e-tail",
        "viewer_policy": {"policy_revision": "p-tail"},
    }


SCOPE = _scope(["a_head", "a_two", "a_three", "b_one", "b_two", "z_one"])

# (arm, query). The four arms of the order, in its order.
ARMS = [
    ("tail_of_non_head_account", "3333"),
    ("shared_tail", "2222"),
    ("name_query", "Alpha Household"),
    ("entry_without_masks", "7777"),
]


def load_handler(zip_path, name):
    src = zipfile.ZipFile(zip_path).read("handler.py")
    mod = types.ModuleType(name)
    exec(compile(src, name + "::handler.py", "exec"), mod.__dict__)
    return mod


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def classify(hd, q):
    """The verdict of one search, read from the shape of its results (no string is matched on)."""
    r = hd.search(DIRECTORY, SCOPE, q)
    res = r["results"]
    kinds = [x["scope_kind"] for x in res]
    pre_existing = hd._entry_key(SOLO)
    single = True
    for x in res:
        got = hd.resolve(DIRECTORY, SCOPE, {"entry_id": x["entry_id"]})
        if not (got.get("ok") and len(got.get("account_ids", [])) == 1):
            single = False
    if r["count"] == 0:
        verdict = "no_match"
    elif all(k == "RELATIONSHIP" for k in kinds):
        verdict = "relationship_entry"
    elif r["count"] == 1 and kinds == ["ACCOUNT"] and res[0]["entry_id"] == pre_existing:
        verdict = "unchanged"
    elif r["count"] == 2 and kinds == ["ACCOUNT", "ACCOUNT"] and res[0]["entry_id"] != res[1]["entry_id"]:
        verdict = "two_account_entries"
    elif r["count"] == 1 and kinds == ["ACCOUNT"]:
        verdict = "account_entry"
    else:
        verdict = "other:" + ",".join(kinds)
    return verdict, r["count"], kinds, single


def reach_from_local(doc):
    """Counts for one firm's landed directory document, read as holdings_snapshot._directory_account_ids reads it."""
    entries = doc.get("entries", []) or []
    n_masked = 0
    accounts = set()
    addressable = set()
    for e in entries:
        member = set((e.get("ids") or {}).get("account_ids", []) or [])
        accounts |= member
        masks = e.get("account_masks") or []
        if masks:
            n_masked += 1
            mask_accounts = {m.get("account_id") for m in masks}
            addressable |= (member & mask_accounts)
        else:
            addressable |= member
    return {"entries": len(entries), "entries_with_masks": n_masked, "accounts": len(accounts),
            "accounts_tail_addressable_after": len(addressable)}


def main():
    built_zip, live_zip, gold, lib, scratch, out_path = sys.argv[1:7]
    sys.path.insert(0, gold)
    sys.path.insert(0, lib)
    import holdings_snapshot as hs  # noqa: E402  (bucket map and the directory prefixes only)

    built = load_handler(built_zip, "hd_built")
    live = load_handler(live_zip, "hd_live")

    arms, contrast, single_ok = [], [], {}
    for arm, q in ARMS:
        bv, bc, bk, bsingle = classify(built, q)
        lv, lc, lk, _ = classify(live, q)
        arms.append({"arm": arm, "verdict": bv})
        contrast.append({"arm": arm, "live_verdict": lv})
        single_ok[arm] = bsingle
        print("ARM %s built=%s (count=%d kinds=%s single_account_resolve=%s) live=%s (count=%d kinds=%s)"
              % (arm, bv, bc, ",".join(bk), bsingle, lv, lc, ",".join(lk)))

    rel = built.search(DIRECTORY, SCOPE, "Alpha Household")
    rel_eid = rel["results"][0]["entry_id"] if rel["results"] else None
    rel_got = built.resolve(DIRECTORY, SCOPE, {"entry_id": rel_eid}) if rel_eid else {}
    rel_ok = bool(rel_got.get("ok")) and rel_got.get("account_ids") == sorted(["a_head", "a_two", "a_three"])
    print("RELATIONSHIP_REACHES_ALL_ACCOUNTS=%s" % rel_ok)

    reach, landed_map, not_est = {}, {}, []
    for firm in ("49financial", "cottonwood", "inflection"):
        bucket = hs.firm_bucket_map().get(firm, "")
        ptr_path = "%s/%s_latest.json" % (scratch, firm)
        doc_path = "%s/%s_directory.json" % (scratch, firm)
        with open(ptr_path, encoding="utf-8") as f:
            ptr = json.load(f)
        with open(doc_path, encoding="utf-8") as f:
            doc = json.load(f)
        if hs.PROD_PREFIX.replace("holdings", "directory") != "investor-reporting/directory":
            not_est.append("%s: PROD directory prefix differs from the one read" % firm)
        counts = reach_from_local(doc)
        reach[firm] = counts
        landed_map[firm] = "PROD" if ptr.get("key") else "ABSENT"
        print("REACH %s bucket=%s landed=%s %s" % (firm, bucket, landed_map[firm], json.dumps(counts, sort_keys=True)))

    out = {
        "function": "irpt-directory-search",
        "built_sha256": sha256_file(built_zip),
        "live_sha256": sha256_file(live_zip),
        "arms": arms,
        "live_contrast": contrast,
        "relationship_reaches_all_accounts": rel_ok,
        "reach": reach,
        "landed_prefix_class": landed_map,
        "not_established": not_est + [
            "reach counts are over the WHOLE landed directory, not per viewer; the permitted-set filter is not applied",
            "the synthetic arms exercise search() and resolve() only; no Lambda invocation, no entitlement resolver",
        ],
        "functions_invoked": 0,
        "sign_ins_made": 0,
        "aws_writes_made": 0,
        "accounts_written": 0,
        "figures_written": 0,
        "vendor_requests_sent": 0,
    }
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=2, sort_keys=False)
        f.write("\n")
    print("WROTE %s" % out_path)


if __name__ == "__main__":
    main()
