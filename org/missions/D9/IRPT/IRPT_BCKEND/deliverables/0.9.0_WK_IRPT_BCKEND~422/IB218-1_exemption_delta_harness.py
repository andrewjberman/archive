#!/usr/bin/env python3
"""IB-pr-580 (TO IRPT_BCKEND.TO-IB-pr-580) -- the served DELTA of the absent_at_source exemption, measured ALONE, per firm.

READ-ONLY dry run of the HEAD code over the live pinned inputs. It mirrors run_firm up to the publish gate and never calls
land, never passes upload, never calls write_refusal_record, never publishes, never invokes a function and never writes an
object. Every S3 call is a read (get_object through the module's own readers, list and head through the same readers).

For each firm the candidate is built ONCE. The WITHOUT arm gates a plain copy of it with no evidence provider. The WITH arm
gates a deep copy of it with the provider run_firm builds, and applies the visible listing exactly where run_firm does (only
on a PUBLISHED gate that exempted an account). The exemption alone is the node-by-node difference between the two arms. The
second fire serves the WITH arm's account-id set and gates the WITHOUT candidate again with the provider.

The firm ids are taken from BUILDERS (the builders are selected by function identity, never by a typed firm name).
Prints counts, dates, outcome and condition names only. Writes the record JSON named by argv[2].

    python IB218-1_exemption_delta_harness.py <repo_root> <record_out.json>
"""
import copy
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path


def main():
    repo = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    sys.path.insert(0, str(repo / "data" / "assets" / "scripts" / "gold" / "investor_reporting"))
    import boto3
    import holdings_snapshot as hs
    import holdings_49f

    base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(repo)).decode("ascii").strip()
    read_date = dt.datetime.now(dt.timezone.utc).date().isoformat()
    s3 = boto3.client("s3", region_name="us-east-1")
    today_business = hs.select_business_date()
    wanted = (holdings_49f.build_49f_meshed, hs.build_cot)
    firm_ids = [k for k, b in hs.BUILDERS.items() if b in wanted]
    print("OK: business date selected %s; firm keys in scope %d of %d builders" % (today_business, len(firm_ids), len(hs.BUILDERS)))

    firms_out = {}
    for firm_id in firm_ids:
        builder = hs.BUILDERS[firm_id]
        bucket = hs.firm_bucket_map().get(firm_id, "")

        def closed(firm_id=firm_id, bucket=bucket):
            return hs.closed_account_ids(s3, bucket, firm_id)

        def marks(firm_id=firm_id, bucket=bucket):
            return hs.directory_marks_no_closures(s3, bucket, firm_id)

        # Mirror run_firm up to the gate, WITHOUT writing.
        publisher = hs.HoldingsPublication(s3, firm_id, qa=False)
        expected = publisher.begin()
        inputs = hs.VersionedInputs(s3)
        snapshot = hs.build_snapshot(firm_id, inputs, today_business)
        served = hs.served_publication(publisher, expected)
        candidate_day = (snapshot.get("clocks") or {}).get("business_date")
        served_day = served.get("business_date") if served else None
        print("OK: %s builder=%s candidate_day=%s served_day=%s" % (firm_id, builder.__name__, candidate_day, served_day))
        served_ids = set(served.get("account_ids") or ()) if served else set()

        # ARM WITHOUT: no evidence provider.
        cand_wo = copy.deepcopy(snapshot)
        gate_wo = hs.evaluate_publish_gate(cand_wo, served, closed, marks)
        wo_names = [c["condition"] for c in gate_wo["conditions"]]
        wo_nodes = len(cand_wo["nodes"])
        wo_accounts = sum(1 for n in cand_wo["nodes"] if n.get("node_kind") == "ACCOUNT")
        print("OK: %s WITHOUT outcome=%s conditions=%s nodes=%d accounts=%d"
              % (firm_id, gate_wo["outcome"], wo_names, wo_nodes, wo_accounts))

        # ARM WITH: deep copy of the same candidate, the provider exactly as run_firm builds it.
        cand_with = copy.deepcopy(snapshot)
        captured = []
        provider = hs._absent_provider(captured, firm_id, inputs, cand_with, served)
        gate_with = hs.evaluate_publish_gate(cand_with, served, closed, marks, absent_at_source_evidence=provider)
        listed = (gate_with.get("listed") or {}).get("account_lost_absent_at_source") or {}
        exempt_dates = listed.get("dates") or {}
        exempt_ids = set(exempt_dates)
        listing_applied = gate_with["outcome"] == "PUBLISHED" and bool(exempt_ids)
        if listing_applied:
            hs._absent_scope_listing(cand_with, gate_with, captured)
        evidence = next((e for e in reversed(captured) if e), None) or {}
        wi_names = [c["condition"] for c in gate_with["conditions"]]
        wi_nodes = len(cand_with["nodes"])
        wi_accounts = sum(1 for n in cand_with["nodes"] if n.get("node_kind") == "ACCOUNT")
        print("OK: %s WITH outcome=%s conditions=%s nodes=%d accounts=%d exempted=%d listing_applied=%s"
              % (firm_id, gate_with["outcome"], wi_names, wi_nodes, wi_accounts, len(exempt_ids), listing_applied))

        # THE EXEMPTION ALONE: node by node, by node_id.
        by_id_wo = {}
        for n in cand_wo["nodes"]:
            by_id_wo.setdefault(n["node_id"], n)
        dup_wo = len(cand_wo["nodes"]) - len(by_id_wo)
        by_id_wi = {}
        for n in cand_with["nodes"]:
            by_id_wi.setdefault(n["node_id"], n)
        dup_wi = len(cand_with["nodes"]) - len(by_id_wi)
        added = [n for nid, n in by_id_wi.items() if nid not in by_id_wo]
        removed = [nid for nid in by_id_wo if nid not in by_id_wi]
        changed = 0
        for nid, n in by_id_wi.items():
            if nid in by_id_wo and json.dumps(n, sort_keys=True, default=str) != json.dumps(by_id_wo[nid], sort_keys=True, default=str):
                changed += 1
        accounts_added = sum(1 for n in added if n.get("node_kind") == "ACCOUNT")
        amount_added = round(sum(float((n.get("amount") or {}).get("value", 0.0) or 0.0) for n in added), 2)
        scope_wo = set((cand_wo.get("scope") or {}).get("account_ids") or [])
        scope_wi = set((cand_with.get("scope") or {}).get("account_ids") or [])
        print("OK: %s exemption_alone nodes_added=%d accounts_added=%d amount_added_usd=%s other_nodes_changed=%d removed=%d duplicate_ids=%d/%d"
              % (firm_id, len(added), accounts_added, amount_added, changed, len(removed), dup_wo, dup_wi))

        # THE SECOND FIRE. Primary served set: the served publication's own account ids PLUS the WITH arm's account ids (the
        # listed ids included). Literal served set: the WITH arm's account ids alone (recorded as second_fire_literal).
        def second_fire(served_ids):
            served2 = dict(served) if served else {"business_date": candidate_day, "placed_keys": set(), "unplaced_keys": set()}
            served2["account_ids"] = set(served_ids)
            cand_wo2 = copy.deepcopy(snapshot)
            captured2 = []
            provider2 = hs._absent_provider(captured2, firm_id, inputs, cand_wo2, served2)
            gate2 = hs.evaluate_publish_gate(cand_wo2, served2, closed, marks, absent_at_source_evidence=provider2)
            exempt2 = set(((gate2.get("listed") or {}).get("account_lost_absent_at_source") or {}).get("dates") or {})
            names2 = [c["condition"] for c in gate2["conditions"]]
            return {"exempt_again": bool(exempt_ids) and exempt_ids <= exempt2,
                    "outcome_account_lost": "account_lost" in names2, "outcome": gate2["outcome"], "conditions": names2}

        primary2 = second_fire(served_ids | scope_wi | exempt_ids)
        literal2 = second_fire(scope_wi | exempt_ids if listing_applied else scope_wi)
        print("OK: %s second_fire outcome=%s conditions=%s exempt_again=%s outcome_account_lost=%s | literal outcome=%s conditions=%s"
              % (firm_id, primary2["outcome"], primary2["conditions"], primary2["exempt_again"], primary2["outcome_account_lost"],
                 literal2["outcome"], literal2["conditions"]))

        # What the listing WOULD add when the gate refused and so the listing did not apply (information only; not the exemption
        # alone, which is measured above on the arm exactly as run_firm applies it).
        would = None
        if exempt_ids and not listing_applied:
            cand_would = copy.deepcopy(cand_with)
            gate_would = copy.deepcopy(gate_with)
            hs._absent_scope_listing(cand_would, gate_would, captured)
            would = {"node_count": len(cand_would["nodes"]),
                     "account_count": sum(1 for n in cand_would["nodes"] if n.get("node_kind") == "ACCOUNT")}
            print("OK: %s listing_if_applied nodes=%d accounts=%d (information only)" % (firm_id, would["node_count"], would["account_count"]))

        wi_block = {"outcome": gate_with["outcome"], "conditions": wi_names, "node_count": wi_nodes, "account_count": wi_accounts,
                    "exempted_accounts": len(exempt_ids),
                    "first_absent_day": evidence.get("first_absent_day") if exempt_ids else None,
                    "since_bound_reached": bool(evidence.get("since_bound_reached")) if exempt_ids else False,
                    "listing_applied": bool(listing_applied), "listing_if_applied": would}
        firms_out[firm_id] = {
            "candidate_day": candidate_day, "served_day": served_day, "builder": builder.__name__,
            "without": {"outcome": gate_wo["outcome"], "conditions": wo_names, "node_count": wo_nodes, "account_count": wo_accounts,
                        "listed_not_refused": int(((gate_wo.get("listed") or {}).get("account_lost_not_refused") or {}).get("count", 0))},
            "with": wi_block,
            "exemption_alone": {"nodes_added": len(added), "accounts_added": accounts_added,
                                "amount_added_usd": amount_added, "other_nodes_changed": changed,
                                "nodes_removed": len(removed), "scope_account_ids_added": len(scope_wi - scope_wo)},
            "second_fire": {"exempt_again": primary2["exempt_again"], "outcome_account_lost": primary2["outcome_account_lost"],
                            "outcome": primary2["outcome"], "conditions": primary2["conditions"]},
            "second_fire_literal": {"exempt_again": literal2["exempt_again"], "outcome_account_lost": literal2["outcome_account_lost"],
                                    "outcome": literal2["outcome"], "conditions": literal2["conditions"]},
        }

    method = ("READ-ONLY dry run, in one process, of the HEAD code over the live pinned inputs: for each firm, "
              "the box default S3 client, HoldingsPublication.begin() (a read), VersionedInputs, build_snapshot once at the "
              "selected business date, then served_publication; the WITHOUT arm runs evaluate_publish_gate with no evidence "
              "provider on a deep copy, and the WITH arm runs it on a second deep copy with the provider run_firm builds, "
              "applying _absent_scope_listing only on a PUBLISHED gate that exempted an account; the second fire gates the "
              "WITHOUT candidate again with the provider over the served set of the served publication plus the WITH account ids "
              "(the literal WITH-only set is recorded beside it as second_fire_literal). Nothing is landed or written.")
    notes = [
        "Each count is node-level arithmetic over the one build: the exemption alone is the node-by-node difference by node_id between the WITH and WITHOUT copies, with no fresh build per arm.",
        "Not read: the publication bytes beyond the served index manifest and gold parquet the gate needs, the refusal record, any landed object, and any Lambda function.",
        "A REFUSED WITH gate applies no listing (run_firm lists only on PUBLISHED), so its exemption_alone is zero; listing_if_applied is information only and is not the exemption alone.",
        "The WITHOUT arm of a firm whose directory marks no closures lists a lost account as not refused (listed_not_refused), not as an account_lost condition; the record states the conditions as measured.",
        "Sparse directories added locally (never committed): the investor-reporting gold and silver scripts, the investor-reporting Lambda, the mdpf gold and silver scripts, the v2_portal shared package, the investor-reporting contracts.",
        "The six bound counters are 0: no AWS write, no sign-in, no Lambda invocation, no record or figure written, no vendor request; the harness calls module functions in-process and writes only this record.",
    ]
    record = {
        "base_commit": base, "read_date": read_date, "method": method, "claim": "measured",
        "firms": firms_out, "notes": notes,
        "functions_invoked": 0, "sign_ins_made": 0, "aws_writes_made": 0,
        "rows_written": 0, "figures_written": 0, "vendor_requests_sent": 0,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n", encoding="ascii")
    print("OK: wrote record with %d firm block(s) to %s" % (len(firms_out), out.name))


if __name__ == "__main__":
    main()
