"""IB-pr-451: ONE owner read of a SERVED vendor report's sections, KEY NAMES AND TOKENS ONLY.

    python ib451_read.py <out.json>

Row DSGN_IRPTV1-D2-S21 asks two questions about a served vendor answer that only a served answer can
settle: does any section carry a title or label member, and which `units` tokens does the wire send.
2.0.0_SA_COO~D2's code read predicts NO title member and lower-case census tokens; nobody has read a
served vendor answer. This reads one.

GET ONLY. Nothing is submitted, generated, retried or re-requested. At most FOUR GETs after the login:
two history reads (one per tenant) and at most two sections reads. No call reaches the vendor -- the
sections route serves the STORED report.

NO VALUE IS WRITTEN: no figure, no section date, no person, client, account or file name. What is kept
is key NAMES, counts, the `section_type` tokens (census codes) and the `units` tokens, each with its
count. The raw answer is held in memory only. The password is read by NAME into memory by the
instrument's own login() and is never printed or written.

Reuses, and edits neither:
  org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r7/w6_reads.py          login()
  org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/f1_svc_release/f1_svc_run.py
                                                                   call, scrub, say, stamp, API, BASE
ASCII only. Author 0.7.0_AE_CloudOps~IB2.
"""
import collections
import json
import os
import sys
import urllib.error
import urllib.request

def _workspace_root(start):
    """Walk up to the checkout root rather than counting .. levels: the marker is a directory that holds
    both org/ and .tools/, so a moved deliverables path cannot silently resolve to the wrong place."""
    here = os.path.dirname(os.path.abspath(start))
    while True:
        if os.path.isdir(os.path.join(here, "org")) and os.path.isdir(os.path.join(here, ".tools")):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            raise SystemExit("cannot locate the checkout root above " + os.path.abspath(start))
        here = parent


WS = _workspace_root(__file__)
G2 = os.path.join(WS, "org", "missions", "D9", "IRPT", "IRPT_YCDGEN", "deliverables", "2.0.0_SA_COO~G2")
sys.path.insert(0, os.path.join(G2, "r7"))
sys.path.insert(0, os.path.join(G2, "f1_svc_release"))

import f1_svc_run as f1  # noqa: E402
import w6_reads  # noqa: E402

# The instrument's own modes name these two: R3 reads the service principal's native firm, and its other
# modes select the second tenant with ?selected_tenant=. One history GET each, two in total.
TENANTS = ("cottonwood", "49financial")
TITLEISH = ("title", "label", "name", "display_name")
PROVIDERISH = ("provider", "kind", "variant", "engine", "source", "provider_kind")
STATEISH = ("state", "status", "job_state")
READY = ("READY", "COMPLETE", "COMPLETED", "SUCCEEDED", "DONE")
# The Opal engine's own token, so a vendor request is "a provider that is not this".
OPAL = ("OPAL", "OPAL_ENGINE", "OPAL_CAPITAL", "NATIVE", "ENGINE")


def items_of(node, out):
    """Every dict in the answer that names a request id, with no value kept."""
    if isinstance(node, dict):
        ident = node.get("identity") if isinstance(node.get("identity"), dict) else {}
        rid = ident.get("request_id") or node.get("request_id")
        if isinstance(rid, str) and rid:
            merged = dict(node)
            for key, val in ident.items():
                merged.setdefault(key, val)
            out.append(merged)
        for val in node.values():
            items_of(val, out)
    elif isinstance(node, list):
        for val in node:
            items_of(val, out)
    return out


def first_member(row, names):
    for name in names:
        if name in row and isinstance(row[name], str) and row[name]:
            return name, row[name]
    return None, None


def token_counts(rows, member):
    tally = collections.Counter()
    for row in rows:
        val = row.get(member)
        tally[val if isinstance(val, str) and val else "(absent)"] += 1
    return dict(sorted(tally.items()))


def key_sets(rows):
    tally = collections.Counter()
    for row in rows:
        tally[tuple(sorted(row.keys()))] += 1
    return [{"keys": list(k), "count": n} for k, n in sorted(tally.items(), key=lambda kv: (-kv[1], kv[0]))]


def get_plain(path, headers):
    """A plain opener, as the instrument's CENSUS mode does, so the raw answer is seen before any scrub."""
    req = urllib.request.Request(f1.API + path, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", "replace")
        try:
            return err.code, json.loads(body)
        except ValueError:
            return err.code, {"_non_json": body[:200]}


def read_history(headers, result):
    """One GET per tenant, at most two. Returns the candidate rows with their tenant."""
    reads = []
    candidates = []
    members = {"provider_member": None, "state_member": None}
    for tenant in TENANTS:
        path = f1.BASE + "/analysis/requests?selected_tenant=" + tenant
        status, answer = f1.call("GET", path, None, headers)
        rows = items_of(answer, [])
        uniq = {}
        for row in rows:
            rid = row.get("request_id") or (row.get("identity") or {}).get("request_id")
            if isinstance(rid, str):
                uniq.setdefault(rid, row)
        rows = list(uniq.values())
        pname = sname = None
        for row in rows:
            if pname is None:
                pname = first_member(row, PROVIDERISH)[0]
            if sname is None:
                sname = first_member(row, STATEISH)[0]
        pairs = collections.Counter()
        for row in rows:
            pairs[(str(row.get(pname)) if pname else "(no provider member)",
                   str(row.get(sname)) if sname else "(no state member)")] += 1
        reads.append({"tenant": tenant, "http": status, "requests_listed": len(rows),
                      "by_provider_and_state": {(k[0] + " | " + k[1]): n for k, n in sorted(pairs.items())},
                      "item_key_union": sorted({k for row in rows for k in row.keys()})})
        members["provider_member"] = members["provider_member"] or pname
        members["state_member"] = members["state_member"] or sname
        for row in rows:
            candidates.append((tenant, row))
        f1.say("history", tenant, "HTTP", status, "requests", len(rows),
               "provider member", pname, "state member", sname)
    result["history_reads"] = reads
    result["history_members_read"] = members
    return candidates, members


def choose(candidates, members):
    """The most recent request whose provider is not the Opal engine's and whose state is ready."""
    pname, sname = members["provider_member"], members["state_member"]
    ranked = []
    for tenant, row in candidates:
        prov = str(row.get(pname) or "") if pname else ""
        state = str(row.get(sname) or "") if sname else ""
        if sname and state.upper() not in READY:
            continue
        if pname and prov.upper() in OPAL:
            continue
        when = ""
        for key in ("accepted_at", "created_at", "submitted_at", "updated_at", "completed_at"):
            if isinstance(row.get(key), str):
                when = row[key]
                break
        rid = row.get("request_id") or (row.get("identity") or {}).get("request_id")
        ranked.append((when, rid, tenant, prov, state))
    ranked.sort(reverse=True)
    return ranked


def census(data, result):
    dated = data.get("sections") if isinstance(data.get("sections"), list) else []
    undated = data.get("undated_sections") if isinstance(data.get("undated_sections"), list) else []
    rows = [r for r in list(dated) + list(undated) if isinstance(r, dict)]
    union = sorted({k for r in rows for k in r.keys()})
    result.update(
        provider=data.get("provider"),
        answer_data_keys=sorted(data.keys()),
        dated_sections=len(dated),
        undated_sections=len(undated),
        sections_counted=len(dated) + len(undated),
        dated_section_keys=sorted(dated[0].keys()) if dated and isinstance(dated[0], dict) else [],
        undated_section_keys=sorted(undated[0].keys()) if undated and isinstance(undated[0], dict) else [],
        section_keys_union=union,
        section_key_sets=key_sets(rows),
        any_section_has_a_title_or_label_member=any(n in union for n in TITLEISH),
        section_type_tokens=token_counts(rows, "section_type"),
        units_tokens=token_counts(rows, "units"),
        top_level_validation_keys=sorted(k for k in data.keys()
                                         if "validation" in k.lower() or "source" in k.lower()),
    )
    units = [t for t in result["units_tokens"] if t != "(absent)"]
    result["units_tokens_lower_case"] = sum(1 for t in units if t == t.lower())
    types = [t for t in result["section_type_tokens"] if t != "(absent)"]
    result["section_type_tokens_matching_S_two_digits"] = sum(
        1 for t in types if len(t) == 3 and t[0] == "S" and t[1:].isdigit())


def main(argv):
    out = argv[1]
    result = {"to_id": "IRPT_BCKEND.TO-IB-pr-451", "operator": "0.7.0_AE_CloudOps~IB2",
              "started_at": f1.stamp(), "api": f1.API, "submitted": 0, "values_written": 0,
              "instrument": "w6_reads.login(); f1_svc_run.call/scrub/stamp/say; plain opener as CENSUS does",
              "outcome": None, "request": None, "sections_http": None,
              "how_the_vendor_request_was_chosen": (
                  "Of every request listed by the two history GETs, keep those whose state member reads a ready "
                  "token and whose provider member is NOT the Opal engine's, then take the most recent by the "
                  "first present of accepted_at, created_at, submitted_at, updated_at, completed_at. If the item "
                  "carries no provider member the provider filter is not applied and that is recorded in "
                  "history_members_read as a null provider_member; if no request survives, the outcome is "
                  "NO_VENDOR_REPORT_FOUND.")}

    def dump(code):
        result.update(ended_at=f1.stamp(), calls=f1.log, rc=code)
        json.dump(result, open(out, "w", encoding="utf-8", newline="\n"), indent=1)
        return code

    try:
        headers = w6_reads.login()
    except Exception as err:  # noqa: BLE001 -- any credential or transport refusal is the REFUSED outcome
        name = type(err).__name__
        code = "ACCESS_DENIED" if "AccessDenied" in str(err) else name.upper()
        result.update(outcome="REFUSED", public_reason_code=code,
                      stopped_because="the service login could not be attempted: reading the password by name was "
                                      "refused (" + name + "). No API call was made, no history was read, and the "
                                      "principal was NOT widened.",
                      login_refusal_class=name)
        return dump(1)
    if not headers:
        result.update(outcome="REFUSED", public_reason_code="LOGIN_NO_TOKEN",
                      stopped_because="the service login returned no access token; nothing further was read")
        return dump(1)

    candidates, members = read_history(headers, result)
    ranked = choose(candidates, members)
    f1.say("ready non-Opal candidates", len(ranked))
    if not ranked:
        result.update(outcome="NO_VENDOR_REPORT_FOUND",
                      stopped_because="no listed request had both a ready state and a provider that is not the "
                                      "Opal engine's; no sections read was made")
        return dump(0)

    for attempt, (_when, rid, tenant, prov, state) in enumerate(ranked[:2]):
        path = f1.BASE + "/analysis/" + rid + "/sections?selected_tenant=" + tenant
        status, answer = get_plain(path, headers)
        f1.log.append({"at": f1.stamp(), "method": "GET", "path": path, "status": status,
                       "request_body": None, "response": f1.scrub(answer)})
        result.update(request=rid, sections_http=status, chosen_provider_token=prov, chosen_state_token=state)
        f1.say("sections", rid, "HTTP", status, "provider", prov, "state", state)
        if status != 200:
            env = answer.get("status") if isinstance(answer, dict) else None
            env = env if isinstance(env, dict) else {}
            result.update(outcome="REFUSED", public_reason_code=env.get("public_reason_code"),
                          stopped_because="the sections read was refused; no further request was read")
            return dump(1)
        data = answer.get("data") if isinstance(answer, dict) and isinstance(answer.get("data"), dict) else {}
        if not data.get("provider") and attempt == 0 and len(ranked) > 1:
            f1.say("no data.provider on the first chosen request; reading ONE more")
            continue
        census(data, result)
        result["outcome"] = "READ"
        return dump(0)
    result.update(outcome="NO_VENDOR_REPORT_FOUND",
                  stopped_because="neither of the two requests read carried a data.provider member")
    return dump(0)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
