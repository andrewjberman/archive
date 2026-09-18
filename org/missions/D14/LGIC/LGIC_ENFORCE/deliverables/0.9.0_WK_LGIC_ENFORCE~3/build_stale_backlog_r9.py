"""EN-b-42 round 9 -- builds STALE_BACKLOG_R9.json: one NAMED owner (a serial or a registered project
code) per stale remediation row, or a DEFERRED entry carrying a reason and an un-defer condition.

It SEATS OWNERSHIP ONLY. It closes, disarms, graduates and remediates nothing, and it writes nothing
but the record beside it.

Population: the gate's own limb, CALLED at write time --
    srg._stale_open_row(srg._remediation_rows_for_project(root, "LGIC_ENFORCE")[0],
                        CURRENT_ROUND, srg.STALE_OPEN_ROW_N_ROUNDS)
Both census reads return a TUPLE (value, note) and are unpacked explicitly; the intermediate
denominators are printed.

Owner rule: the row's OWN `remediation.owner` is kept where the act its remedy names lies inside that
party's grant; OVERRIDES below replace it where the remedy names a category ("each tool's owner",
"the checker's author", "a seat whose grant reaches ...") or a party that is not the one able to act.
Every owner is then RESOLVED: a serial shape, or a project code present in org/missions/DIRECTIVES.yaml.

COVERAGE is asserted AFTER the write, by re-calling the limb and re-reading the written file.

Usage: python build_stale_backlog_r9.py <current_round:int>
"""

import importlib.util
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "STALE_BACKLOG_R9.json")
CODE = "LGIC_ENFORCE"
SERIAL_RE = re.compile(r"^[0-4]\.[0-9]+\.[0-9]+_[A-Z]{2}_[A-Za-z0-9]+(~[A-Za-z0-9]+)?$")

# --- overrides: the owner the remedy's act actually lands on ------------------------------------
OVERRIDES = {
    "LGIC_ENFORCE-S18": ("0.0.0_AB_MSTR",
        "Same remedy text, verbatim, as LGIC_ENFORCE-S17, whose own remediation.owner is 0.0.0_AB_MSTR: find the "
        "writer that restores the SHARED index around its commit and make safe-merge.sh check recorded paths "
        "against the branch diff. Both are integration-plane acts on the shared checkout the integrator runs; "
        "one remedy with two owners is the category shape (.tools/** is lane ANY, so no lane names it)."),
    "LGIC_ENFORCE-W1-S3": ("NFRA_COMPEFFICACY",
        "Remedy names 'each tool's owner' -- a category. The tool is comp-find (.scratch/ read, :(exclude) "
        "scanning 0 files). .tools/** is lane ANY, so no lane owns it; the ACTIVE registered project whose scope "
        "is comp-tool accounts is NFRA_COMPEFFICACY (status active; its tree carries "
        "deliverables/0.8.0_AE_CloudComp/comp-find.result.md and 60 files naming comp-find)."),
    "LGIC_ENFORCE-W2-S1": ("NFRA_COMPEFFICACY",
        "Remedy names 'each tool's owner' -- a category. The tool is comp-iam role (0 of 94 roles resolved). "
        "NFRA_COMPEFFICACY is the ACTIVE registered project carrying the per-tool account "
        "deliverables/0.8.0_AE_CloudComp/comp-iam.result.md (47 files in its tree name comp-iam); "
        "NFRA_COMPTOOLS, the older comp-tool project, is status closed and cannot act."),
    "LGIC_ENFORCE-W1-S24": ("LGIC_CANON",
        "The remedy itself names the party: 'Fix at LGIC_CANON's next canon/checklist cell'. The carriers "
        "(10_ONBOARDING_CHECKLIST.md, 02_DOCTRINE.md) sit under infra/logic/** lane PLATFORM_LOGIC_DOCS, which "
        "admits only 4.0.0_SA_CRO serials -- so 1.0.0_SA_CTO, the prior owner, cannot write them. LGIC_CANON is "
        "registered, status active, and its decomposition names ONBOARDING_CHECKLIST 7 times."),
    "LGIC_ENFORCE-S72": ("0.7.0_AE_CloudOps",
        "Remedy names 'a seat whose grant reaches infra/aws/terraform/modules/opal_name/tests/' -- a category -- "
        "and states the prior owner (2.0.0_SA_COO~G, the issuer) CANNOT be it. That path resolves to "
        "infra/aws/** lane CLOUD_OPS_OR_ETL; 0.7.0_AE_CloudOps is the base serial in that lane whose remit is "
        "Terraform (the refresh is a generator re-render of two test fixtures)."),
    "LGIC_ENFORCE-W1-S70": ("1.0.0_SA_CTO",
        "Remedy says choosing among (a) sanction the token in NAMING_SCHEMA grade.placeholder, (b) rule the "
        "canonical form wrong, (c) card the row out 'belongs to the round that takes it' -- a category. Each "
        "branch is a RULING on the naming contract, which is 1.0.0_SA_CTO's (L2/L4 author of the endpoint "
        "and PRD); the issuer (the prior owner) cuts only what the ruling decides."),
}

# --- per-owner basis for rows whose own remediation.owner is KEPT ------------------------------
KEEP_BASIS = {
    "1.0.0_SA_CTO": "Own remediation.owner kept: the remedy's act is a RULING on the PRD, the rule or a "
                    "FWD's grade, or a change to a tool whose lane or authorship is 1.0.0_SA_CTO's "
                    "(to-pipeline-gate.py and surprise-row-gate.py are lane LOOP_MECHANISM = CTO+CVO; "
                    "proof-of-spec-check.py, halt-gate-check.sh and deploy_ledger.py are lane ANY with "
                    "1.0.0_SA_CTO their most frequent recent author).",
    "2.0.0_SA_COO~G": "Own remediation.owner kept: the remedy's act is the issuer's -- re-cutting a criterion, "
                      "a fixed input, a face or a deliverable this project's issuer wrote, or recording that an "
                      "already-served remedy closes. 2.0.0_SA_COO~G is the LGIC_ENFORCE round issuer.",
    "0.0.0_AB_MSTR": "Own remediation.owner kept: the remedy is on the shared index and the drain path "
                     "(safe-merge.sh), the integrator's plane.",
}

# --- deferrals: reason + the condition that un-defers ------------------------------------------
DEFERRED = {
    "LGIC_ENFORCE-W1-S23": (
        "The remedy is one assert in two LGIC_NAMING round-3 fixed inputs "
        "(org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r3/blind_seat.py and "
        "check_ln_r3.py). LGIC_NAMING is status COMPLETE, those instruments are frozen history no order runs, and "
        "the path resolves to org/missions/** lane TIER0_MSTR: no open order grants it, so no party can act on it "
        "today without widening an order.",
        "Un-defers the moment any task order is cut that RE-RUNS or REUSES blind_seat.py or check_ln_r3.py (or a "
        "copy) as an instrument; the issuer of that order -- by name, 2.0.0_SA_COO~G if it is LGIC's issuer -- "
        "takes the row and lands the non-empty-or-absent assert in the same cut."),
}


def load_gate(root):
    spec = importlib.util.spec_from_file_location("srg", os.path.join(root, ".tools", "surprise-row-gate.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def registered_codes(root):
    with io.open(os.path.join(root, "org", "missions", "DIRECTIVES.yaml"), encoding="utf-8") as fh:
        return set(re.findall(r"\b([A-Z]{4}_[A-Z0-9]{3,})\b", fh.read()))


def resolves(owner, codes):
    return bool(SERIAL_RE.match(owner)) or owner in codes


def ascii_only(s):
    return "".join(ch if ord(ch) < 128 else "?" for ch in str(s))


def measure(srg, root, current_round):
    ids, inote = srg._remediation_ids_for_project(root, CODE)
    rows_by_id, rnote = srg._remediation_rows_for_project(root, CODE)
    if ids is None or rows_by_id is None:
        raise SystemExit("ERROR: census could not run: %r / %r" % (inote, rnote))
    stale = srg._stale_open_row(rows_by_id, current_round, srg.STALE_OPEN_ROW_N_ROUNDS)
    if stale is None:
        raise SystemExit("ERROR: _stale_open_row returned None")
    return ids, rows_by_id, stale


def main():
    current_round = int(sys.argv[1])
    root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    srg = load_gate(root)
    codes = registered_codes(root)
    ids, rows_by_id, stale = measure(srg, root, current_round)
    n = srg.STALE_OPEN_ROW_N_ROUNDS
    print("intermediate: ids_from_tuple=%d rows=%d registered_codes=%d" % (len(ids), len(rows_by_id), len(codes)))
    print("current_round=%d N_ROUNDS=%d remediation_rows=%d stale=%d" % (current_round, n, len(rows_by_id), len(stale)))

    unknown = sorted((set(OVERRIDES) | set(DEFERRED)) - set(stale))
    if unknown:
        raise SystemExit("ERROR: override/deferral names a row outside the measured stale set: %s" % unknown)

    assignments, deferred = [], []
    for rid in stale:
        rem = rows_by_id[rid].get("remediation") or {}
        prior = str(rem.get("owner", "")).strip()
        remedy = ascii_only(rows_by_id[rid].get("remedy", ""))[:220]
        if rid in DEFERRED:
            why, when = DEFERRED[rid]
            deferred.append({"row": rid, "id": rid, "prior_owner_on_row": prior,
                             "prior_round_on_row": rem.get("round"),
                             "reason": why, "why": why, "uncondition": when, "un_defers_when": when})
            continue
        if rid in OVERRIDES:
            owner, basis = OVERRIDES[rid]
            kind = "REASSIGNED"
        else:
            owner, basis, kind = prior, KEEP_BASIS.get(prior), "KEPT"
            if not basis:
                raise SystemExit("ERROR: no keep-basis for prior owner %r on %s" % (prior, rid))
        assignments.append({"row": rid, "id": rid, "owner": owner, "owner_kind":
                            ("SERIAL" if SERIAL_RE.match(owner) else "PROJECT_CODE"),
                            "decision": kind, "prior_owner_on_row": prior,
                            "prior_round_on_row": rem.get("round"),
                            "basis": basis, "remedy_as_filed_first_220": remedy})

    unresolved = [a["row"] + " -> " + a["owner"] for a in assignments if not resolves(a["owner"], codes)]
    print("owners resolving (serial shape or registered code): %d of %d ; unresolved %s"
          % (len(assignments) - len(unresolved), len(assignments), unresolved))
    if unresolved:
        raise SystemExit("ERROR: unresolved owner(s)")

    owners = sorted(set(a["owner"] for a in assignments))
    rec = {
        "_about": "EN-b-42 round 9: ONE named owner per stale remediation row under LGIC_ENFORCE, or a DEFERRED "
                  "entry with reason + un-defer condition. Ownership only: no row is closed, disarmed, graduated "
                  "or remediated by this record. Built by build_stale_backlog_r9.py in this folder.",
        "built_at_head": head,
        "measured_at_write_time": {
            "instrument": "srg._stale_open_row(srg._remediation_rows_for_project(root,'LGIC_ENFORCE')[0], "
                          "current_round, srg.STALE_OPEN_ROW_N_ROUNDS) -- .tools/surprise-row-gate.py CALLED, "
                          "read from the INDEX of the checkout at built_at_head",
            "current_round": current_round,
            "N_ROUNDS": n,
            "remediation_rows": len(rows_by_id),
            "stale": len(stale),
            "intermediate_denominators": {"ids_from_tuple": len(ids), "rows": len(rows_by_id)},
            "moved_since": {"register_round_8": 91, "issuer_at_cut_round_9": 94, "this_write": len(stale)},
        },
        "stale_population": {
            "rows": len(stale),
            "denominator_measured_at_write_time": {"instrument": "srg._stale_open_row (called, round %d, N=%d)"
                                                   % (current_round, n), "value": len(stale)},
        },
        "assignments": assignments,
        "deferred": deferred,
        "distinct_owners": owners,
        "owner_counts": {o: sum(1 for a in assignments if a["owner"] == o) for o in owners},
        "reassigned": sum(1 for a in assignments if a["decision"] == "REASSIGNED"),
        "coverage": {"stale": len(stale), "assigned": len(assignments), "deferred": len(deferred),
                     "assertion": "assigned + deferred == stale, asserted AFTER the write"},
    }
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, indent=1, ensure_ascii=True)
        fh.write("\n")

    # ---- coverage AFTER the write: re-call the limb and re-read the file ----
    _, _, stale2 = measure(srg, root, current_round)
    with io.open(OUT, encoding="utf-8") as fh:
        back = json.load(fh)
    covered = set(a["row"] for a in back["assignments"]) | set(d["row"] for d in back["deferred"])
    a_n, d_n = len(back["assignments"]), len(back["deferred"])
    ok = (a_n + d_n == len(stale2) and covered == set(stale2) and len(covered) == a_n + d_n)
    print("AFTER WRITE: re-measured stale=%d ; assigned %d + deferred %d = %d ; set-equal %s ; remainder %d"
          % (len(stale2), a_n, d_n, a_n + d_n, covered == set(stale2), len(stale2) - (a_n + d_n)))
    print("distinct owners: %d %s" % (len(owners), owners))
    print("COVERAGE-AFTER-WRITE: %s" % ("HOLDS" if ok else "BROKEN"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
