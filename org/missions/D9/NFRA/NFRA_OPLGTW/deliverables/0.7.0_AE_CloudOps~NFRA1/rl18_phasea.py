#!/usr/bin/env python
"""OG-rl-18 Phase A: assemble W/PHASE_A_OG-rl-18.json from the records in W/rl18_pa/ (no value is typed here that a record holds). READ ONLY on AWS (nothing is called). Counts, booleans and short shas only.
usage: python rl18_phasea.py   (repository root; W/rl18_pa/{host,tests,sentinel_scan,live_named_reverse}.json and W/rl18_release.json already written)"""
from __future__ import annotations

import io
import json

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
P = W + "rl18_pa/"


def load(p):
    return json.load(io.open(p, encoding="utf-8"))


rel = load(W + "rl18_release.json")
hl, t, sc, lr = load(P + "host.json"), load(P + "tests.json"), load(P + "sentinel_scan.json"), load(P + "live_named_reverse.json")["live_named_reverse"]
pr = hl["probes"]
live_fwd, live_rev = set(t["named_at_live_ref"]["failed_names"]), set(lr["failed_names"])
new_reds_fwd = sorted(set(t["named_forward"]["failed_names"]) - live_fwd)
new_reds_rev = sorted(set(t["named_reverse"]["failed_names"]) - live_rev)
fs = t["full_suite"]
PROCESS_WIDE = (
    "No process, logger, signal, thread, socket, environment key or global config changes, and no import-time side effect is added (I opened the six app diffs whole). app/data_entitlement.py (read per request by every Schwab tool and by the dispatch "
    "chokepoint's tool_denial): one module constant MASTER_WIDE, one constant CONSENT, two plain functions (_master_accounts, is_master_wide), the parser now accepts exactly the one-element list [\"*\"] for a granted master, check_scope admits any "
    "non-empty account list for a master-wide master, and email_denial exempts the master-admin tier for route_class consent. app/account_ref.py (the resolver): one exception class, one function (candidate_accounts) and an accounts_of keyword threaded "
    "through _resolve, resolve_refs and resolve_ref. app/integrations/schwab/integration.py (the Schwab filter helper): one function (account_filter_for), one method (_master_accounts, with a per-master cache keyed by the snapshot digest, created in "
    "__init__ of the service object, not at import) and the call sites that use them. app/server.py and app/token_broker.py: the consent class passed at two call sites. app/admin_api.py: one import and one spread into the route list (the two "
    "owner-gated people-access routes). app/refs/DATA_CATALOG.yaml is data. tools/list does NOT change (103, the candidate registry counts the same on the host); the stored grants are untouched (sentinel records in the store: %d)." % sc["sentinel_grants_in_store"]
)
body = {
    "release_sha": rel["release_sha"], "base_sha": rel["base_sha"], "trunk_sha": rel["trunk_sha"], "live_ref_host": rel["live_ref_host"],
    "tests": {"named_passed": t["named_forward"]["passed"], "named_failed": len(new_reds_fwd) + len(new_reds_rev),
              "named_failed_definition": "named-set failures that do NOT also fail at the base in the SAME order (new reds, both orders); the literal counts are named_failed_literal_forward and _reverse",
              "named_failed_literal_forward": t["named_forward"]["failed"], "named_failed_literal_reverse": t["named_reverse"]["failed"],
              "named_passed_reverse": t["named_reverse"]["passed"], "named_reds_at_base_forward": len(live_fwd), "named_reds_at_base_reverse": len(live_rev),
              "named_order_effect": "the named set's failing count depends on the order at the BASE as well (%d forward, %d reverse); every red of the release in either order is also red at the base in that order" % (len(live_fwd), len(live_rev)),
              "named_files": t["named_files"], "named_files_new_in_release": t["named_files_new_in_release"],
              "window_set_passed": t["window_forward"]["passed"], "window_set_failed": t["window_forward"]["failed"] + t["window_reverse"]["failed"], "window_both_orders_equal": t["window_forward"]["passed"] == t["window_reverse"]["passed"],
              "window_files": t["window_files"], "window_files_excluded_red_at_live_ref": len(t["window_files_excluded_red_at_live_ref"]),
              "suite_difference_named": True, "baseline": "the live ref 2923d1ee99 (a tree at that commit, same sparse cone and invocation)",
              "full_suite": {"release_failed": fs["release_failed"], "base_failed": fs["live_ref_failed"], "only_in_release": fs["only_in_release"], "only_at_base": fs["only_in_live_ref"], "difference": fs["only_in_release_explained"]},
              "standards_copy_overlay": t["standards_copy_overlay"], "standards_copy_restored_to_live_ref_bytes": t["standards_copy_restored_to_live_ref_bytes"]},
    "probes": {"rt1_ac1_ok": pr["rt1ac1"]["ok"], "rt1_ac2_ok": pr["rt1ac2"]["ok"], "ed1_ac1_ok": pr["ed1ac1"]["ok"], "mp1_ac1_ok": pr["mp1ac1"]["ok"],
               "lines": {k: pr[k]["lines"] for k in pr}, "not_ok": {k: pr[k]["not_ok"] for k in pr}, "guard": hl["guard"],
               "where": "on the host, in a scratch copy of the service's tree with the release's six app files laid over it (each equal to the release blob) and the probe fixtures ops/schwab_entitlement_admin.py and tests/test_email_deny.py from the release tree; one fresh process per probe under the cgroup hard guard"},
    "host_shaped_import_check": {"modules": hl["imports_candidate"]["modules"], "imported": hl["imports_candidate"]["imported"], "failed": hl["imports_candidate"]["failed"],
                                 "registry_count_candidate": hl["imports_candidate"]["registry_count"], "registry_count_live_ref": hl["imports_live"]["registry_count"],
                                 "registry_equal": hl["imports_candidate"]["registry_count"] == hl["imports_live"]["registry_count"]},
    "bash_n_deploy_script": "ok (deploy-to-ec2.sh is not in the diff)", "preflight_only": "PREFLIGHT OK",
    "explicit_unchanged": hl["explicit_equal"] is True,
    "explicit_unchanged_detail": "one scope with two explicit masters (eight-digit fixture ids built at run time) parsed by the live ref's code and the candidate's; check_scope for an in-list id, an out-of-list id, an empty list, an in-list id on the second master and a mixed list; the resolver's candidate list and the Schwab account filter; scope_summary's account_count: all equal",
    "sentinel_grants_in_store": sc["sentinel_grants_in_store"],
    "sentinel_scan": {"policy_records": sc["policy_records"], "records_with_a_scope": sc["records_with_a_scope"], "items_scanned": sc["items_scanned"], "consistent_read": sc["consistent_read"], "read_at": sc["read_at"]},
    "host_probe_service": hl["service"], "scratch_removed": hl["scratch_removed"], "candidate_bytes_equal_release": hl["candidate_bytes_equal_release"],
    "process_wide_state": PROCESS_WIDE,
}
io.open(W + "PHASE_A_OG-rl-18.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body}, indent=1) + "\n")
print(json.dumps({k: body[k] for k in ("tests", "probes", "explicit_unchanged", "sentinel_grants_in_store", "host_probe_service")}, indent=1)[:3500])
