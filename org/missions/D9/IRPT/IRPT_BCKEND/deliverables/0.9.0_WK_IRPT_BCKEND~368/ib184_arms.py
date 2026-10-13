"""IRPT_BCKEND IB-pr-518 (worker 0.9.0_WK_IRPT_BCKEND~367): the four offline arms, SYNTHETIC, in memory.

Usage:
  python -I ib184_arms.py child <zip> <scratch_dir>     (one zip per process; prints one JSON line on stdout)
  python -I ib184_arms.py parent <built.zip> <live.zip> <scratch_dir> <out.json>

The child imports comparison_catalogue and maintained_sources FROM THE ZIP (sys.path = the zip and its lib/),
calls build_catalogue and _admitted_comparison, and never invokes a Lambda, never calls AWS, never calls a vendor.
Client data: none; firm identifiers stay inside the child's stdout, which the parent reads and does not write.
The parent writes the verdict record only.
"""
import copy
import json
import os
import subprocess
import sys
import zipfile

NEW_KEY = "opal_ultra_short_term"
EXPECTED_ORDER = ["Opal Ultra Short-Term", "Opal Short-Term", "Opal Intermediate-Term", "Opal Long-Term", "Opal Ultra Long-Term"]
EXISTING_KEYS = ["opal_long_term", "opal_short_term", "opal_intermediate_term", "opal_ultra_long_term"]


def child(zip_path, scratch):
    # opal_naming reads infra/logic/registry/*.json by real path, which a zip cannot serve; the zip's bytes are
    # extracted (outside the worktree, never uploaded) and imported from that directory. No AWS, no invoke.
    os.makedirs(scratch, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(scratch)
    sys.path.insert(0, scratch)
    sys.path.insert(0, os.path.join(scratch, "lib"))
    tpl = os.path.join(scratch, "templates.json")
    import comparison_catalogue as cc
    import maintained_sources as ms
    firms = sorted(ms._comparison_firms())
    tenant = firms[0]
    cat = cc.build_catalogue(tenant=tenant, templates_path=tpl)
    served_model = [e["label"] for e in cat["entries"] if e.get("name_source") == cc.NAME_SOURCE_MODEL]
    with open(tpl, encoding="utf-8") as fh:
        doc = json.load(fh)
    entries = doc["comparison_catalog"]["entries"]
    keys_order = [e["key"] for e in entries]
    admit = {}
    for i, firm in enumerate(firms):
        row = {}
        for e in entries:
            if e["key"] not in ms._COMPARISON_POLICY_SHA256:
                row[e["key"]] = "NO_POLICY"
                continue
            try:
                ms._admitted_comparison(copy.deepcopy(e), {"firm_id": firm}, {"principal_class": "FIRM_ADVISOR"})
                row[e["key"]] = "ADMITTED"
            except ms.MaintainedSourceUnauthorized:
                row[e["key"]] = "REFUSED"
        admit[str(i)] = row
    new = [e for e in entries if e["key"] == NEW_KEY]
    altered = "NOT_RUN"
    if len(new) == 1:
        bad = copy.deepcopy(new[0])
        # the entry's name is candidate.name (the field _comparison_policy hashes); a top-level "name" does not exist
        bad["candidate"]["name"] = "Altered " + str(bad["candidate"].get("name", ""))
        try:
            ms._admitted_comparison(bad, {"firm_id": firms[0]}, {"principal_class": "FIRM_ADVISOR"})
            altered = "ADMITTED"
        except ms.MaintainedSourceUnauthorized:
            altered = "REFUSED"
        # the altered copy must be the NAME change only: prove the copy differs from the entry it was made from
        altered_differs = json.dumps(bad, sort_keys=True) != json.dumps(new[0], sort_keys=True)
    else:
        altered_differs = False
    out = {
        "firm_count": len(firms),
        "served_model_labels": served_model,
        "entry_keys_in_order": keys_order,
        "key_label": [[e["key"], e["label"]] for e in entries],
        "admit": admit,
        "altered": altered,
        "altered_differs_from_source": altered_differs,
        "new_entry_count": len(new),
    }
    print(json.dumps(out))


def run_child(zip_path, scratch):
    r = subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "child", zip_path, scratch],
                       capture_output=True, env={k: v for k, v in os.environ.items() if not k.startswith("AWS_")})
    if r.returncode != 0:
        raise SystemExit("child failed rc=%d: %s" % (r.returncode, r.stderr.decode("utf-8", "replace")[-600:]))
    return json.loads(r.stdout.decode("utf-8").strip().splitlines()[-1])


def parent(built, live, scratch, out):
    b = run_child(built, os.path.join(scratch, "built"))
    live_rec = run_child(live, os.path.join(scratch, "live"))
    # (a) five models in canonical order: the served model labels read exactly the expected five, in order
    five = "five_in_order" if b["served_model_labels"] == EXPECTED_ORDER else "not_in_order"
    # (b) the four existing entries: key and label equal the live zip's, same relative order
    bkl = {k: lab for k, lab in b["key_label"]}
    lkl = {k: lab for k, lab in live_rec["key_label"]}
    existing_kl_equal = all(k in bkl and k in lkl and bkl[k] == lkl[k] for k in EXISTING_KEYS)
    rel_b = [k for k in b["entry_keys_in_order"] if k in EXISTING_KEYS]
    rel_l = [k for k in live_rec["entry_keys_in_order"] if k in EXISTING_KEYS]
    existing_order_equal = rel_b == rel_l
    existing = "unchanged" if (existing_kl_equal and existing_order_equal) else "changed"
    # (c) admitted for each permitted firm, principal class FIRM_ADVISOR, all five entries
    total = sum(len(row) for row in b["admit"].values())
    yes = sum(1 for row in b["admit"].values() for v in row.values() if v == "ADMITTED")
    all_five_per_firm = all(
        all(row.get(k) == "ADMITTED" for k in EXPECTED_KEYS) for row in b["admit"].values())
    admitted = "admitted" if (b["firm_count"] == 3 and all_five_per_firm) else "not_admitted"
    # (d) altered copy of the new entry refused
    altered = "refused" if (b["altered"] == "REFUSED" and b["altered_differs_from_source"] and b["new_entry_count"] == 1) else "not_refused"
    verdicts = {"five_models_canonical_order": five, "existing_four_entries": existing,
                "admitted_three_firms": admitted, "altered_copy": altered}
    rec = {"verdicts": verdicts, "firm_count": b["firm_count"], "admit_pairs_admitted": yes, "admit_pairs_total": total,
           "built_served_model_count": len(b["served_model_labels"]), "live_served_model_count": len(live_rec["served_model_labels"]),
           "measured": {"existing_four_key_label_equal": existing_kl_equal, "existing_four_order_equal": existing_order_equal,
                        "existing_four_order_built": rel_b, "existing_four_order_live": rel_l,
                        "altered_child": b["altered"], "altered_differs": b["altered_differs_from_source"]}}
    print(json.dumps(rec))
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, indent=2)
        fh.write("\n")


EXPECTED_KEYS = [NEW_KEY] + EXISTING_KEYS


if __name__ == "__main__":
    if sys.argv[1] == "child":
        child(sys.argv[2], sys.argv[3])
    else:
        parent(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
