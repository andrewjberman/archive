"""Battery for IRPT_BCKEND.TO-IB-s-9 -- S9-AC1.

Invocation the task order names:
    timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/
        0.9.0_WK_IRPT_BCKEND~3/battery_ib_s_9.py
Prints IBS9-GENERATION-CHAIN only when every arm passes.

NO LIVE YCHARTS CALL. Arms (a)-(g), (v0.8), (v0.10), (amend) and the offline half of (h) run
in a SUBPROCESS under an outbound-network guard that refuses every non-loopback destination;
the rest of (h) reads the AWS control plane and the git record FROM THE PARENT, where those
reads belong. A guard with an allow-list for "our own AWS calls" would have a hole shaped
exactly like the thing it guards against.

NO SECRET VALUE, NO SIGNED URL AND NO REFUSED VALUE IS PRINTED -- only counts.

Author: 0.9.0_WK_IRPT_BCKEND~3. Cell IB-s-9.
"""
from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import zipfile

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
IR = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting")
GEN = os.path.join(IR, "ycharts", "generate")
SUITE = os.path.join(GEN, "tests", "run_offline_suite.py")
AWS = os.path.join(REPO, ".tools", "aws.cmd")
SOURCE_MAP = os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")

FUNCTION = "irpt-ycharts-generate"
LEDGER_SLUG = "irpt-bckend-s9"
SENTINEL = os.path.join(REPO, "org", "critical_paths", ".open_deploys",
                        LEDGER_SLUG + ".json")
VARIANTS_PACKET_COMMIT = "72acd16e66"

results = {}


def say(text=""):
    print(text)


def run(cmd, cwd=None, timeout=300, env=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
                          shell=False, env=env)


def aws_json(args):
    proc = run([AWS] + args + ["--region", "us-east-1", "--output", "json"], timeout=150)
    if proc.returncode != 0:
        return {"_error": proc.stderr.strip()[:200]}
    text = proc.stdout.replace("\r", "").strip()
    return json.loads(text) if text else None


def offline_suite():
    proc = run([sys.executable, SUITE], cwd=REPO, timeout=420)
    if "RESULT-BEGIN" not in proc.stdout:
        return {"_suite_failed": True, "rc": proc.returncode,
                "stderr_tail": proc.stderr[-2000:], "stdout_tail": proc.stdout[-1000:]}
    data = json.loads(proc.stdout.split("RESULT-BEGIN", 1)[1].split("RESULT-END", 1)[0])
    data["_rc"] = proc.returncode
    return data


def rebuild_zip_hash():
    """Rebuild the registered zip from the WORKTREE source, deterministically.

    The member list comes from the source map's own `files[]`, so the registration and the
    served bytes are checked AGAINST EACH OTHER rather than both being asserted.
    """
    sm = json.load(io.open(SOURCE_MAP, encoding="utf-8"))
    entry = sm["functions"][FUNCTION]
    where = {"enforce.py": ("_authz", "enforce.py"), "gate.py": ("_gate", "gate.py"),
             "keys.py": ("_keys", "keys.py"), "resolve.py": ("_scope", "resolve.py")}
    members = []
    for rel in entry["files"]:
        if rel in where:
            path = os.path.join(IR, *where[rel])
        elif rel == "firm_destination_policy.json":
            path = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting",
                                "core", rel)
        elif rel == "firm_registry.json":
            path = os.path.join(REPO, "data", rel)
        elif rel == "settings.json":
            path = os.path.join(IR, "intake", rel)
        else:
            path = os.path.join(GEN, rel.replace("/", os.sep))
        members.append((rel, path))
    members.sort(key=lambda t: t[0])
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for arc, path in members:
            info = zipfile.ZipInfo(arc, date_time=(2026, 9, 11, 0, 0, 0))
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(path, "rb") as fh:
                z.writestr(info, fh.read())
    data = buf.getvalue()
    return (base64.b64encode(hashlib.sha256(data).digest()).decode("ascii"),
            len(data), len(members), entry.get("artifact_sha256"))


def ledger_state():
    entry_dir = os.path.join(REPO, "org", "critical_paths", "change_management")
    name = next((f for f in sorted(os.listdir(entry_dir)) if LEDGER_SLUG in f), None)
    text = ""
    if name:
        with io.open(os.path.join(entry_dir, name), encoding="utf-8") as fh:
            text = fh.read()
    sentinel_log = run(["git", "log", "--format=%h %s", "--",
                        "org/critical_paths/.open_deploys/" + LEDGER_SLUG + ".json"],
                       cwd=REPO).stdout.strip()
    entry_log = run(["git", "log", "--format=%h %s", "-n", "3", "--",
                     "org/critical_paths/change_management/" + (name or "")],
                    cwd=REPO).stdout.strip()
    return {
        "entry_file": name,
        "closed": bool(re.search(r"(?i)\bstatus\b.{0,40}\bCLOSED\b", text)),
        "open_leg_markers": len(re.findall(r"(?i)\bOPEN\b\s*\|", text)),
        "legs_declared": len(re.findall(r"(?m)^\|\s*L\d+\s*\|", text)),
        "sentinel_present_on_disk": os.path.exists(SENTINEL),
        "sentinel_commits": [ln for ln in sentinel_log.split("\n") if ln],
        "entry_commits": [ln for ln in entry_log.split("\n") if ln],
    }


def manifest_freshness():
    """RE-DERIVE every fixture row and both fixture denominators FROM DISK.

    FIXTURE_MANIFEST.json is the provenance carrier for the whole fixture set -- which rows are
    MEASURED and which are EXTENDED -- and it went STALE at 88c97c1529, which changed two
    fixtures and did not regenerate it (row IRPT_BCKEND-W3-S9). A stale hash in a provenance
    record is WORSE than no hash, because it reads as measured. So nothing here is read from the
    manifest and then believed: every value is recomputed and compared, and the file list is
    derived from the DIRECTORY BY SUBTRACTION so a fixture added without a manifest row cannot
    hide. This measurement is load-bearing in arm (h).
    """
    base = os.path.join(GEN, "fixtures", "har")
    manifest = json.load(io.open(os.path.join(base, "FIXTURE_MANIFEST.json"), encoding="utf-8"))
    rows = manifest["files"]
    stale = []
    for row in rows:
        data = open(os.path.join(base, row["path"]), "rb").read()
        if (row["sha256"] != hashlib.sha256(data).hexdigest()
                or row["bytes"] != len(data)):
            stale.append(row["path"])
    on_disk = sorted(f for f in os.listdir(base) if f != "FIXTURE_MANIFEST.json")
    unlisted = sorted(set(on_disk) - set(r["path"] for r in rows))
    branches = json.load(io.open(os.path.join(base, "decision_branches.json"), encoding="utf-8"))
    declared = manifest["_meta"]["denominators"]
    counted = {"files": len(on_disk),
               "decision_branches": len([k for k in branches if not k.startswith("_")])}
    disagreeing = sorted(k for k, v in counted.items() if declared.get(k) != v)
    return {
        "rows_checked": len(rows), "rows_matching": len(rows) - len(stale),
        "stale_rows": stale, "files_on_disk": len(on_disk), "unlisted_files": unlisted,
        "declared_denominators": {k: declared.get(k) for k in counted},
        "counted_denominators": counted, "disagreeing_denominators": disagreeing,
        "fresh": not stale and not unlisted and not disagreeing,
    }


def packet_reachability():
    """The variants packet is NOT in this branch. Measure it rather than assert it."""
    path = "docs/research/investor_reporting_ycharts_variants_20260911/"
    on_disk = os.path.isdir(os.path.join(REPO, path))
    at_commit = run(["git", "ls-tree", "-r", "--name-only", VARIANTS_PACKET_COMMIT, "--", path],
                    cwd=REPO).stdout.strip().split("\n")
    ancestor = run(["git", "merge-base", "--is-ancestor", VARIANTS_PACKET_COMMIT, "HEAD"],
                   cwd=REPO).returncode == 0
    control = run(["git", "merge-base", "--is-ancestor", "1f795d1f71", "HEAD"],
                  cwd=REPO).returncode == 0
    return {"path": path, "present_in_worktree": on_disk,
            "files_at_%s" % VARIANTS_PACKET_COMMIT: len([f for f in at_commit if f]),
            "commit_is_ancestor_of_head": ancestor,
            "positive_control_known_ancestor": control}


def main():
    say("=" * 78)
    say("BATTERY IB-s-9 -- S9-AC1: the seven steps, the job's durability, the read-back")
    say("repo: " + REPO)
    say("=" * 78)

    suite = offline_suite()
    if suite.get("_suite_failed"):
        say("BLOCKED: the offline suite produced no result block (rc=%s)" % suite.get("rc"))
        say(suite.get("stderr_tail", ""))
        return 1
    arms = suite["arms"]

    # ---- (a) -------------------------------------------------------------
    a = arms["a_seven_steps"]
    say("")
    say("(a) SEVEN OF SEVEN -- each recipe step against the replay, %d of %d"
        % (a["ran"], a["denominator"]))
    say("    declared steps: %s" % (a["declared_steps"],))
    for step, row in a["per_step"].items():
        say("      %-12s ok=%-5s status=%s" % (step, row["ok"], row["status"]))
    say("    identity checks (all four required): %s" % json.dumps(a["identity_checks"]))
    say("    wrong-user-id CONTROL rejected: %s" % a["wrong_user_id_control_rejected"])
    say("    upload multipart field: %r | create multipart fields: %s  (MEASURED, PRD v0.8"
        " SUPP VI.5 @d67e9813b5)" % (a["upload_multipart_field"], a["create_multipart_fields"]))
    say("    empty `sections` array accepted as legitimate: %s" % a["empty_sections_accepted"])
    results["a"] = bool(a["pass"])

    # ---- (b) -------------------------------------------------------------
    b = arms["b_submitting_before_side_effect"]
    say("")
    say("(b) SUBMITTING BEFORE THE SIDE EFFECT -- THE DIFFERENCE CONTROL")
    say("    kill: %s" % b["killed_at"])
    say("    state after the kill: %s | intent claimed BEFORE the POST: %s"
        % (b["state_after_kill"], b["intent_claimed_before_the_post"]))
    c = b["correct_build"]
    say("    CORRECT BUILD on restart: resumed=%s resubmitted=%s create POSTs=%d"
        " adopted_by=%s portfolio=%s"
        % (c["resumed"], c["resubmitted"], c["create_posts_on_restart"], c["adopted_by"],
           c["model_portfolio_id"]))
    bb = b["broken_build"]
    say("    BROKEN BUILD (resubmits instead of reconciling): create POSTs=%d -> %s"
        % (bb["create_posts_on_restart"], bb["arm_predicate_on_this_build"]))
    results["b"] = bool(b["pass"])

    # ---- (c) -------------------------------------------------------------
    c2 = arms["c_never_the_newest"]
    say("")
    say("(c) NEVER THE NEWEST ROW")
    say("    candidates: %d | NEWEST row: id=%s created_at=%s name=%r"
        % (c2["candidates"], c2["newest_row"]["id"], c2["newest_row"]["created_at"],
           c2["newest_row"]["name"]))
    say("    adopted: %s by %s | newest adopted: %s"
        % (c2["adopted"], c2["adopted_reason"], c2["newest_row_adopted"]))
    say("    the owned name is deterministic (derived BEFORE the submit): %s"
        % c2["owned_name_is_deterministic"])
    results["c"] = bool(c2["pass"])

    # ---- (d) -------------------------------------------------------------
    d = arms["d_settings_read_back"]
    say("")
    say("(d) SETTINGS READ BACK -- %d of %d" % (d["matched"], d["denominator"]))
    for row in d["rows"]:
        say("      %-20s -> %-24s expected=%-16s actual=%-16s %s"
            % (row["setting"], row["vendor_field"], json.dumps(row["expected"]),
               json.dumps(row["actual"]), "OK" if row["matches"] else "DRIFT"))
    dc = d["drift_control"]
    say("    DRIFT CONTROL (a replay that returns a drifted setting): %d of %d matched,"
        " drifted=%s, job outcome=%s, job state=%s"
        % (dc["matched"], dc["denominator"], dc["drifted"], dc["job_outcome"],
           dc["job_state"]))
    results["d"] = bool(d["pass"])

    # ---- (e) -------------------------------------------------------------
    e = arms["e_bodies_per_s8"]
    say("")
    say("(e) BODIES PER S8")
    say("    root keys: August %d / July %d | modal fields: August %d / July %d"
        % (e["august_key_count"], e["july_key_count"], e["august_modal_field_count"],
           e["july_modal_field_count"]))
    say("    the ONLY August-extra root key: %s | modal: %s"
        % (e["august_only_root_key"], e["august_only_modal_fields"]))
    say("    secondarySecurity.securityId by variant: %s" % json.dumps(e["secondary_security"]))
    say("    comparisonSecurities length by variant: %s"
        % json.dumps(e["comparison_array_len"]))
    say("    asymmetric empties (type per field): %s" % json.dumps(e["asymmetric_empty_types"]))
    say("    duplicate cover fields agree: %s across %d pairs"
        % (e["duplicate_cover_fields_agree"], e["duplicate_cover_pairs"]))
    say("    cardinality refused when wrong: %s" % str(e["cardinality_refused"])[:110])
    say("    templates read from %s: %s" % (e["templates_source"], e["templates_from_config"]))
    say("    global-preference PUT census: %s" % json.dumps(e["global_preference_puts"]))
    results["e"] = bool(e["pass"])

    # ---- (f) -------------------------------------------------------------
    f = arms["f_the_201_is_wrapped"]
    say("")
    say("(f) THE 201 IS WRAPPED -- the job id is OPAL'S")
    say("    Opal attempt id: %s" % f["opal_attempt_id"])
    say("    vendor-job-id census over the attempt row: %s" % json.dumps(f["vendor_job_id_census"]))
    say("    the vendor's measured 201 keys: %s  (no job id exists to invent)"
        % f["measured_vendor_response_keys"])
    say("    artifact key: %s" % f["artifact_key"])
    say("      under the bound firm's generations prefix: %s"
        % f["artifact_under_bound_firm_generations_prefix"])
    say("    PDF: sha256=%s bytes=%d credential headers sent=%s header names sent=%s"
        % (f["pdf"]["sha256"][:16], f["pdf"]["bytes"], f["pdf"]["credential_headers_sent"],
           f["pdf"]["header_names_sent"]))
    say("    separate unauthenticated client, headers per request: %s"
        % f["separate_unauthenticated_client_headers"])
    say("    SIGNED-PARAM CENSUS over every log line: %s" % json.dumps(f["signed_param_census"]))
    say("    job states in order: %s" % f["states"])
    results["f"] = bool(f["pass"])

    # ---- (g) -------------------------------------------------------------
    g = arms["g_schema_valid"]
    say("")
    say("(g) SCHEMA-VALID -- the AnalysisReport attempt row")
    say("    validated=%s against %s; required: %s"
        % (g["validated"], g.get("schema"), g.get("required_present")))
    if g.get("error"):
        say("    error: %s" % g["error"])
    results["g"] = bool(g["pass"])

    # ---- (v0.8) ----------------------------------------------------------
    v8 = arms["v08_measured_contracts_and_decision_table"]
    say("")
    say("(v0.8) THE MEASURED CONTRACTS AND THE DECISION TABLE, ON THE REPLAY")
    say("    upload field %r; save fields %s -- %s"
        % (v8["upload_field"], v8["save_fields"], v8["field_names_source"]))
    say("    full payload (%d keys) -> 201 | minimal payload -> %s, classified %s / %s"
        % (v8["full_payload_201"]["keys"], v8["minimal_payload"]["status"],
           v8["minimal_payload"]["classified"], v8["minimal_payload"]["decision"]))
    say("    fee 0 -> %s %s | the captured 0.003 annual recipe succeeds"
        % (v8["zero_fee"]["status"], v8["zero_fee"]["error"]))
    say("    empty `sections` accepted: %s" % v8["empty_sections_legitimate"])
    say("    PDF client separate and unauthenticated: %s; session-cookie headers on that"
        " request: %d" % (v8["pdf_client"]["separate_unauthenticated"],
                          v8["pdf_client"]["session_cookie_headers_on_that_request"]))
    jb = v8["job_budget"]
    say("    JOB BUDGET: %ss measured for the live Overview invocation, budget %ss (%sx"
        " headroom)" % (jb["measured_overview_seconds"], jb["lambda_budget_seconds"],
                        jb["headroom_x"]))
    say("      %s" % jb["rule"])
    say("    DECISION TABLE -- %d of %d branches classified as declared:"
        % (v8["branches_matched"], v8["branches_denominator"]))
    for row in v8["decision_branches"]:
        say("      %-24s status=%-5s -> %s" % (row["branch"], row["status"], row["decision"]))
    say("    ONE refresh allowed: %s | repeat eviction refused: %s"
        % (v8["one_refresh_allowed"], v8["repeat_eviction_refused"]))
    results["v08"] = bool(v8["pass"])

    # ---- (v0.10) ---------------------------------------------------------
    v10 = arms["v010_three_recipes_one_handler"]
    say("")
    say("(v0.10) THREE RECIPES IN ONE HANDLER (issuer supplement, channel row"
        " IRPT_BCKEND-S14)")
    say("    packet: %s" % v10["packet"])
    say("    VARIANT FROM THE COMPARISON COUNT -- %d of %d correct:"
        % (v10["selection_correct"], v10["selection_denominator"]))
    for row in v10["variant_selection_by_comparison_count"]:
        say("      %d comparison(s) -> %-10s template %s  %s"
            % (row["comparisons"], row["variant"], row["template_id"],
               "OK" if row["correct"] else "WRONG"))
    say("    6 comparisons refused: %s" % str(v10["over_cardinality_refused"])[:100])
    say("    a declared variant that disagrees with the count refused: %s"
        % str(v10["declared_variant_mismatch_refused"])[:100])
    say("    PRE-ACCESS CONTROLS -- each with the vendor-request count AT THE REFUSAL:")
    for label, row in v10["pre_access_refusals"].items():
        say("      %-32s %-38s vendor requests: %d"
            % (label, row["code"], row["vendor_requests_at_refusal"]))
    say("      total vendor requests during all refusals: %d"
        % v10["vendor_requests_during_all_refusals"])
    dr = v10["duplicate_redelivery"]
    say("    DUPLICATE RE-DELIVERY: first run %s with %d vendor requests; the duplicate ->"
        " %s with %d vendor requests"
        % (dr["first_outcome"], dr["first_vendor_requests"], dr["duplicate_outcome"],
           dr["duplicate_vendor_requests"]))
    say("      receipt key: %s" % dr["receipt_key"])
    wf = v10["waf_header_classification"]
    say("    WAF: the same 202 WITH the x-amzn-waf-action header -> %s; WITHOUT it -> %s"
        % (wf["with_header"], wf["without_header"]))
    say("      measured case: %s" % wf["measured_case"])
    cc = v10["comparison_catalog"]
    say("    COMPARISON CATALOG: %d entries, %d typed model_portfolio, %d live-proven: %s"
        % (cc["entries"], cc["typed_model_portfolio"], cc["live_proven"], cc["ids"]))
    say("    MEASURED VARIANT OUTPUTS (the CRO's live run, not this cell's):")
    for tid, m in sorted(v10["measured_variant_outputs"].items()):
        say("      %s  %d pages  %s  %d bytes  sha256 %s"
            % (tid, m["pages"], m["orientation"], m["bytes"], m["sha256"][:16]))
    ur = v10["upload_reconciliation"]
    say("    UPLOAD RECONCILED (not merely parsed): %s -- %d rows sent, %d echoed, unit %r"
        % (ur["reconciled"], ur["rows_sent"], ur["rows_echoed"], ur["weight_unit_echoed"]))
    results["v010"] = bool(v10["pass"])

    # ---- (amend) ---------------------------------------------------------
    am = arms["amend_guarded_bound_silent"]
    say("")
    say("(amend) GUARDED, BOUND, AND SILENT ON THE REFUSED VALUE")
    say("    this cell ships NO route handler -- %s" % am["why"])
    gc = am["census_over_this_cells_routes"]
    say("    unguarded_routes(job.ROUTES) -> %d of %d unguarded  %s"
        % (gc["unguarded"], gc["routes"], gc["verdict"]))
    say("      THE CENSUS IS VACUOUS: %s. %s" % (am["census_is_vacuous"],
                                                 am["routes_json_status"]))
    say("      CONTROL, an UNGUARDED handler wired to a route: %d of %d unguarded"
        % (am["control_unguarded"]["unguarded"], am["control_unguarded"]["routes"]))
    say("      CONTROL, the SAME handler wrapped by guard():   %d of %d unguarded"
        % (am["control_guarded"]["unguarded"], am["control_guarded"]["routes"]))
    say("      public callables added by this cell: %d, route-reachable: %d"
        % (am["public_callables"], am["public_callables_route_reachable"]))
    fb = am["firm_binding"]
    say("    FIRM BINDING: a non-reconciling binding -> ok=%s code=%s; opaque id echoed: %s"
        % (fb["non_reconciling_result"], fb["refusal_code"], fb["opaque_id_echoed"]))
    say("      envelope: %s" % json.dumps(fb["envelope"]))
    ks = am["keys_silence"]
    say("    _keys SILENCE: code=%s, audit entries=%d, envelope %d bytes,"
        " OCCURRENCES OF THE REFUSED VALUE: %d"
        % (ks["refusal_code"], ks["audit_entries"], ks["envelope_bytes"],
           ks["occurrences_of_refused_value"]))
    say("      reason (parameter NAMES only): %s" % str(ks["reason"])[:150])
    results["amend"] = bool(am["pass"])

    # ---- (h) -------------------------------------------------------------
    h = arms["h_offline"]
    guard, control = h["netguard"], h["positive_control"]
    built, built_bytes, built_members, registered = rebuild_zip_hash()
    cfg = aws_json(["lambda", "get-function-configuration", "--function-name", FUNCTION,
                    "--query", "{CodeSha256:CodeSha256,Layers:Layers,Timeout:Timeout}"])
    host = aws_json(["ec2", "describe-instances", "--instance-ids", "i-0167fd745ad906a66",
                     "--query", "Reservations[0].Instances[0].State.Name"])
    led = ledger_state()
    packet = packet_reachability()
    fresh = manifest_freshness()
    served = (cfg or {}).get("CodeSha256")
    say("")
    say("(h) NOTHING LEFT THE MACHINE; THE LEDGER CLOSED")
    say("    netguard (offline subprocess): %d external of %d connection attempt(s)"
        % (guard["external_refused"], guard["attempts_observed"]))
    say("      %s" % guard["denominator_note"])
    say("    POSITIVE CONTROL: attempted %s -> refused=%s, guard external %s -> %s"
        % (control["attempted"], control["refused"], control["guard_external_before"],
           control["guard_external_after"]))
    say("      %s" % control["message"])
    say("    replay requests made by the chain: %d over routes %s"
        % (h["replay_requests"], h["replay_routes"]))
    say("    served bytes: CodeSha256 %s" % served)
    say("      rebuilt zip %s (%d bytes, %d members); registration %s"
        % (built, built_bytes, built_members, registered))
    say("      served == rebuilt: %s | registered == rebuilt: %s"
        % (served == built, registered == built))
    say("      Layers: %s | Timeout: %ss" % ((cfg or {}).get("Layers"),
                                             (cfg or {}).get("Timeout")))
    say("    the IB-s-8 host after this cell's apply: %s (untouched)" % host)
    say("    ledger %s: CLOSED=%s, legs=%d, open markers=%d, sentinel on disk=%s"
        % (led["entry_file"], led["closed"], led["legs_declared"], led["open_leg_markers"],
           led["sentinel_present_on_disk"]))
    say("      THE SENTINEL'S OWN COMMITS (the W3-S4 rule applied):")
    for line in led["sentinel_commits"]:
        say("        %s" % line)
    say("      entry commits:")
    for line in led["entry_commits"]:
        say("        %s" % line)
    say("    THE VARIANTS PACKET IS NOT IN THIS BRANCH (row W3-S7): %s" % json.dumps(packet))
    say("    FIXTURE MANIFEST RE-DERIVED FROM DISK (row W3-S9): %d of %d rows match,"
        " %d file(s) on disk, %d unlisted"
        % (fresh["rows_matching"], fresh["rows_checked"], fresh["files_on_disk"],
           len(fresh["unlisted_files"])))
    say("      declared %s vs counted %s -- disagreeing: %s"
        % (json.dumps(fresh["declared_denominators"], sort_keys=True),
           json.dumps(fresh["counted_denominators"], sort_keys=True),
           fresh["disagreeing_denominators"] or "none"))
    say("      the manifest is the MEASURED-vs-EXTENDED carrier, so it is recomputed here and"
        " never believed; it went stale at 88c97c1529 and arm (h) now fails if it does again")
    results["h"] = (bool(h["pass"]) and served == built and registered == built
                    and fresh["fresh"]
                    and host == "stopped" and led["closed"]
                    and led["open_leg_markers"] == 0
                    and not led["sentinel_present_on_disk"]
                    and len(led["sentinel_commits"]) >= 2
                    and packet["present_in_worktree"] is False
                    and packet["commit_is_ancestor_of_head"] is False
                    and packet["positive_control_known_ancestor"] is True)

    # ---- verdict ---------------------------------------------------------
    say("")
    say("=" * 78)
    order = ["a", "b", "c", "d", "e", "f", "g", "v08", "v010", "amend", "h"]
    for key in order:
        say("  arm (%s): %s" % (key, "PASS" if results[key] else "FAIL"))
    passed = sum(1 for k in order if results[k])
    say("  ARMS: %d of %d" % (passed, len(order)))
    say("=" * 78)
    if passed == len(order):
        say("IBS9-GENERATION-CHAIN")
        return 0
    say("BLOCKED: not every arm passed -- IBS9-GENERATION-CHAIN withheld")
    return 1


if __name__ == "__main__":
    sys.exit(main())
