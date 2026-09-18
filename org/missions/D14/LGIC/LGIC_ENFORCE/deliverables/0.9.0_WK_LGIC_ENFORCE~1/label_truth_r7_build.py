"""LGIC_ENFORCE round 7, cell EN-t-34 -- the instrument behind LABEL_TRUTH_R7.json.

IT RESOLVES NOTHING. It re-identifies two groups of round-6 carded rows and writes, for each,
a label that INSTRUCTS instead of describing: every remedy names its CARRIER (where the value
comes from) and its ACT (what to do with it).

GROUP ONE, the two-carrier rows. Re-identified INDEPENDENTLY of round 6's own
CADENCE_PLUS_SYSTEM label: a row is in the group if its canonical form carries BOTH '{system}'
and '{cadence}'. The label is not the test; agreement with the declared count is the
corroboration.

GROUP TWO, the key format templates. Re-identified BY SUBTRACTION from a printed denominator
(Rule 24 i): the brace tokens of the row's own text MINUS the four sanctioned placeholders
NAMING_SCHEMA.json grade.placeholder enumerates ({system}, {source}, {scope}, {cadence}). A
non-empty remainder is an unsanctioned brace. Never a forward list of tokens recalled.

BOTH SUBTRACTIONS ARE RUN OVER THE WHOLE CARRIED POPULATION -- resolved + carded + deferred --
not over the carded list alone, so the domain is falsified rather than assumed.

THE {cadence} CARRIER IS NOT ONE STRING. Measured per row from the repo's Terraform:
  SCHEDULE_EXPRESSION            the rule's own schedule_expression -> cadence.values
  EVENT_PATTERN                  the rule's own event_pattern -> cadence.event_form 'on-{event}'
  EVENT_PATTERN_VIA_TARGET_EDGE  a LOG_GROUP has no cadence of its own; the carrier is the rule
                                 that TARGETS it, reached through aws_cloudwatch_event_target
  LIVE_RULE_NO_REPO_DECLARATION  no literal-name declaration in this repo; the carrier is the
                                 live rule, read-only `aws events describe-rule`
A reader who assumes 'schedule_expression' and meets an event-driven rule finds NOTHING and
cannot tell that from an absent carrier. That distinction is the point of naming the carrier.

LIMIT OF THE TERRAFORM SCAN, stated because it bounds every claim it feeds: it matches a
LITERAL `name = "..."` inside an aws_cloudwatch_event_rule block. A rule whose name is built by
interpolation is invisible to it, so NOT-FOUND means 'no literal-name declaration', never 'not
declared'. Those rows are labelled LIVE_RULE_NO_REPO_DECLARATION, which names a carrier that
exists either way.

AND A SECOND LIMIT, MEASURED BY BEING WRONG: the firing attribute is read as an ATTRIBUTE
(`^\\s*<name>\\s*=` after comment lines are stripped), never as a substring. The first run of
this instrument used a substring test and reported exec_summary_trigger_placeholder as carrying
BOTH a schedule_expression and an event_pattern, because a COMMENT in that block names
event_pattern as future work. See attr_kinds().

Run:  python <this file> build     writes LABEL_TRUTH_R7.json beside itself
      python <this file> census    prints the denominators only, writes nothing
"""

import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
SOURCE = ("org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/"
          "PLACEHOLDER_CAMPAIGN_R6.json")
REGISTRY = "infra/logic/registry/resources.json"
OUT = os.path.join(HERE, "LABEL_TRUTH_R7.json")

SANCTIONED = ("system", "source", "scope", "cadence")
BRACE = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")
RULE_BLOCK = re.compile(r'resource\s+"aws_cloudwatch_event_rule"\s+"([^"]+)"\s*\{')
LG_BLOCK = re.compile(r'resource\s+"aws_cloudwatch_log_group"\s+"([^"]+)"\s*\{')
TGT_BLOCK = re.compile(r'resource\s+"aws_cloudwatch_event_target"\s+"([^"]+)"\s*\{')
LITERAL_NAME = re.compile(r'\bname\s*=\s*"([^"]+)"')

BASE_COMMIT = "2c3d7b0cb24a20e40d6f8852fc8755109c80504a"

LABEL = "TWO_CARRIER_PLACEHOLDER_ROW"

LABEL_DEFINITION = (
    "TWO_CARRIER_PLACEHOLDER_ROW -- a carded row whose canonical form carries BOTH {system} and "
    "{cadence}, so the name is cleared only by values from TWO DIFFERENT CARRIERS and NEITHER "
    "REMEDY ALONE clears it: taking one leaves a brace in the name and records a resolution that "
    "is not one. "
    "CARRIER 1, the {system} half: infra/logic/registry/resources.json -- the resource-to-system "
    "row keyed (name, type), read at lib/opal_naming.py:1030-1032. IN a cell's grant; the act is "
    "to MINT that row, its system read from the Terraform ROOT that declares the resource and "
    "checked against infra/logic/registry/systems.json, cited as the row's evidence. "
    "CARRIER 2, the {cadence} half: the RULE'S OWN EXPRESSION, and WHICH expression is a measured "
    "property of the row, not a constant -- schedule_expression mapped onto NAMING_SCHEMA.json "
    "cadence.values (daily|weekly|monthly|hourly), or event_pattern mapped onto cadence.event_form "
    "'on-{event}'. NOT in that grant. For a LOG_GROUP the carrier is not the group at all: it is "
    "the rule that TARGETS the group, reached through aws_cloudwatch_event_target. "
    "MECHANICAL TEST a later census runs with no judgment and no owner's opinion: '{system}' in "
    "canonical AND '{cadence}' in canonical. "
    "PER ROW, remedies[].carrier names WHERE the value comes from (file and declaration, or the "
    "read-only live call), remedies[].act names WHAT TO DO with it, and remedies[].in_a_cells_grant "
    "says whether a worker could take it inside the round-6 grant. A row leaves this label only "
    "when BOTH acts are taken; a census that takes one and re-labels the row has re-created the "
    "defect this label exists to end."
)

FIFTEEN_REASON_HEAD = "ROW_IS_NOT_A_NAME"

NOT_DONE = {
    "no_placeholder_is_resolved_here": (
        "This cell makes two labels true. It resolves nothing and re-grades nothing. The 1093 "
        "deferred rows are not attempted: R-60 read FWD-5's ACCEPT at the bytes -- 'THIS IS THE "
        "LIST CLEAN-UP PROJECTS START FROM' -- so the outcome IS the list and resolution is the "
        "clean-up projects' work."
    ),
    "the_15_are_not_removed_from_any_grade": (
        "R-62 REFUSED removing S3Key from the name grade: it would drop EVERY S3 key in the estate "
        "to fix 15 templates, and Rule 30 makes S3 addresses the core naming surface. This record "
        "does not touch org/standards/NAMING_SCHEMA.json, which is outside this cell's grant. "
        "types_not_graded_by_kind is a ROUTING table whose name is the opposite of its behaviour -- "
        "lib/opal_naming.py:493 unions the whole table INTO graded_types and :1012 removes a type "
        "only when its prose reason begins 'NOT GRADED', so 8 of its 15 entries are genuinely out "
        "and 7 (S3Key among them) are still graded. Rewording one reason moves a type across that "
        "switch silently; the guard t34-no-grade-change re-counts the split."
    ),
    "a_mechanism_separating_a_template_from_a_key": (
        "Round 8 material. A schema change needs Rule 24's four-postulate record and a token "
        "census, never a rider on a label repair."
    ),
}


def read_text(path):
    with io.open(path, encoding="utf-8", errors="replace", newline="") as fh:
        return fh.read()


def load_json(path):
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


def attr_kinds(body):
    """Which firing attribute does this rule block DECLARE?

    A SUBSTRING TEST IS WRONG HERE AND WAS MEASURED WRONG. The first run of this instrument
    classified aws_cloudwatch_event_rule.exec_summary_trigger_placeholder
    (infra/aws/terraform/exec-summary/main.tf) as carrying BOTH expressions, because a COMMENT in
    that block -- ':225  # Schedule placeholder -- TO 7 will replace with event_pattern matching
    the ...' -- contains the exact token the classifier keyed on. The block declares
    schedule_expression only. So: strip comment lines first, then require the ATTRIBUTE form
    `<name> =`. A classifier that reads prose about an attribute as the attribute reports a
    carrier the world does not have, and names the wrong source in an instruction.
    """
    lines = []
    for ln in body.splitlines():
        s = ln.strip()
        if s.startswith("#") or s.startswith("//"):
            continue
        lines.append(ln)
    stripped = "\n".join(lines)
    kinds = []
    if re.search(r"(?m)^\s*schedule_expression\s*=", stripped):
        kinds.append("schedule_expression")
    if re.search(r"(?m)^\s*event_pattern\s*=", stripped):
        kinds.append("event_pattern")
    return tuple(kinds)


def block_body(text, start):
    """Return the brace-balanced body beginning at the '{' at index start."""
    depth = 0
    for j in range(start, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[start:j + 1]
    return text[start:]


def tf_files():
    out = []
    for root, dirs, files in os.walk(os.path.join(REPO, "infra")):
        dirs[:] = [d for d in dirs if d not in (".terraform", "node_modules")]
        for f in files:
            if f.endswith(".tf"):
                out.append(os.path.join(root, f))
    return sorted(out)


def scan_terraform():
    """rules: literal name -> (relpath, tf_label, kind). log_groups: literal name -> relpath.
    targets: (relpath, log_group_label) -> rule tf_label."""
    rules, lgs, targets = {}, {}, {}
    files = tf_files()
    nrules = 0
    for path in files:
        rel = os.path.relpath(path, REPO).replace("\\", "/")
        text = read_text(path)
        for m in RULE_BLOCK.finditer(text):
            nrules += 1
            body = block_body(text, m.end() - 1)
            kinds = attr_kinds(body)
            nm = LITERAL_NAME.search(body)
            if nm:
                rules.setdefault(nm.group(1), (rel, m.group(1), kinds))
        for m in LG_BLOCK.finditer(text):
            body = block_body(text, m.end() - 1)
            nm = LITERAL_NAME.search(body)
            if nm:
                lgs.setdefault(nm.group(1), (rel, m.group(1)))
        for m in TGT_BLOCK.finditer(text):
            body = block_body(text, m.end() - 1)
            rule = re.search(r"\brule\s*=\s*aws_cloudwatch_event_rule\.([A-Za-z0-9_]+)", body)
            arn = re.search(r"\barn\s*=\s*aws_cloudwatch_log_group\.([A-Za-z0-9_]+)", body)
            if rule and arn:
                targets[(rel, arn.group(1))] = (rule.group(1), m.group(1))
    return rules, lgs, targets, len(files), nrules


def rule_label_to_name(rules, label):
    for nm, (rel, lab, _k) in rules.items():
        if lab == label:
            return nm, rel
    return None, None


def cadence_remedy(row, rules, lgs, targets, scan_note):
    """The {cadence} half, with its carrier MEASURED per row."""
    name, rtype = row["current"], row["type"]
    if rtype == "LOG_GROUP":
        lg = lgs.get(name)
        edge = None
        if lg:
            for (rel, lab), (rule_label, tgt_label) in sorted(targets.items()):
                if lab == lg[1]:
                    edge = (rel, rule_label, tgt_label)
                    break
        if edge:
            rel, rule_label, tgt_label = edge
            rule_name, rule_rel = rule_label_to_name(rules, rule_label)
            kinds = rules.get(rule_name, (None, None, ()))[2] if rule_name else ()
            kind = "EVENT_PATTERN_VIA_TARGET_EDGE" if "event_pattern" in kinds \
                else "SCHEDULE_EXPRESSION_VIA_TARGET_EDGE"
            carrier = (
                "NOT this log group's own declaration (%s declares only the group). The carrier is "
                "THE RULE THAT TARGETS IT: aws_cloudwatch_event_target.%s in %s points rule "
                "aws_cloudwatch_event_rule.%s (name \"%s\", declared %s) at this group, so the "
                "group's cadence is THAT rule's %s." % (
                    lg[0], tgt_label, rel, rule_label, rule_name, rule_rel,
                    " and ".join(kinds) or "expression")
            )
            act = (
                "follow the target edge to rule \"%s\", read its %s, and map it onto "
                "NAMING_SCHEMA.json %s. Reading the log group alone yields nothing and cannot be "
                "told apart from an absent carrier." % (
                    rule_name,
                    "event_pattern" if "event_pattern" in kinds else "schedule_expression",
                    "cadence.event_form 'on-{event}'" if "event_pattern" in kinds
                    else "cadence.values")
            )
            return kind, carrier, act, "measured"
        return ("LOG_GROUP_NO_TARGET_EDGE_FOUND",
                "no aws_cloudwatch_event_target in this repo was measured pointing a rule at log "
                "group \"%s\"; %s The carrier is then the LIVE wiring: `aws logs "
                "describe-log-groups` plus `aws events list-targets-by-rule`, read-only." % (
                    name, scan_note),
                "read the live target wiring, find the rule that writes into this group, then take "
                "that rule's expression as above.", "measured-absence-bounded-by-the-scan-limit")
    hit = rules.get(name)
    if hit:
        rel, label, kinds = hit
        if "event_pattern" in kinds and "schedule_expression" not in kinds:
            return ("EVENT_PATTERN",
                    "the rule's OWN event_pattern, declared at aws_cloudwatch_event_rule.%s in %s "
                    "(or `aws events describe-rule --name %s`, read-only)." % (label, rel, name),
                    "map the event this rule fires on onto NAMING_SCHEMA.json cadence.event_form "
                    "'on-{event}' (event_token_regex ^[a-z0-9]+(-[a-z0-9]+)*$). This rule carries "
                    "NO schedule_expression: cadence.values (daily|weekly|monthly|hourly) does not "
                    "apply to it, and a reader who looks for a clock here finds nothing.",
                    "measured")
        if "schedule_expression" in kinds and "event_pattern" in kinds:
            return ("SCHEDULE_EXPRESSION_AND_EVENT_PATTERN",
                    "the rule's OWN declaration at aws_cloudwatch_event_rule.%s in %s carries BOTH "
                    "a schedule_expression and an event_pattern (or `aws events describe-rule "
                    "--name %s`, read-only)." % (label, rel, name),
                    "read BOTH and decide which one this rule actually fires on before mapping: a "
                    "clock maps onto cadence.values, an event onto cadence.event_form 'on-{event}'. "
                    "Two expressions in one block is itself a finding for the owner, not a pick.",
                    "measured")
        if "schedule_expression" in kinds:
            return ("SCHEDULE_EXPRESSION",
                    "the rule's OWN schedule_expression, declared at aws_cloudwatch_event_rule.%s "
                    "in %s (or `aws events describe-rule --name %s`, read-only)." % (
                        label, rel, name),
                    "map the cron/rate expression onto NAMING_SCHEMA.json cadence.values "
                    "(daily|weekly|monthly|hourly).",
                    "measured")
        return ("RULE_DECLARED_WITH_NEITHER_EXPRESSION",
                "aws_cloudwatch_event_rule.%s in %s declares this name but carries neither a "
                "schedule_expression nor an event_pattern." % (label, rel),
                "read the live rule (`aws events describe-rule --name %s`, read-only) before "
                "assuming either form." % name,
                "measured")
    return ("LIVE_RULE_NO_REPO_DECLARATION",
            "the LIVE EventBridge rule itself: `aws events describe-rule --name %s` (read-only). "
            "%s" % (name, scan_note),
            "read ScheduleExpression or EventPattern off the live rule and branch: a clock maps "
            "onto NAMING_SCHEMA.json cadence.values, an event onto cadence.event_form 'on-{event}'.",
            "measured-absence-bounded-by-the-scan-limit")


def system_remedy(row, rules, lgs, registry_has, n_registry_rows, n_absent, n_group):
    name, rtype = row["current"], row["type"]
    where = None
    if rtype == "LOG_GROUP":
        where = lgs.get(name, (None,))[0]
    else:
        hit = rules.get(name)
        where = hit[0] if hit else None
    if where:
        root = "/".join(where.split("/")[:4])
        value_act = (
            "read the owning system from the Terraform ROOT that declares this resource (%s), "
            "check that token against infra/logic/registry/systems.json, and cite the declaring "
            "file:line as the row's evidence -- the convention every existing row in the registry "
            "follows." % root)
    else:
        value_act = (
            "no declaring Terraform root was measured for this resource, so read the owning system "
            "from the rule's own targets (`aws events list-targets-by-rule`, read-only) and check "
            "that token against infra/logic/registry/systems.json before minting.")
    return {
        "token": "system",
        "carrier": (
            "infra/logic/registry/resources.json -- the resource-to-system row keyed "
            "(name=\"%s\", type=\"%s\"), read at lib/opal_naming.py:1030-1032." % (name, rtype)),
        "carrier_state": (
            "PRESENT: a resources.json row already exists for this (name, type); the act is a READ, "
            "not a mint." if registry_has else
            "ABSENT: measured at this record's write time, %d of the %d rows in this group carry no "
            "resources.json row, against a registry holding %d rows. The act is a MINT, not a "
            "lookup." % (n_absent, n_group, n_registry_rows)),
        "in_a_cells_grant": True,
        "act": (
            "MINT the (name, type, system, evidence) row in infra/logic/registry/resources.json: "
            "%s" % value_act),
        "claim": "measured",
    }


def brace_tokens(row):
    return set(BRACE.findall((row.get("canonical") or "") + " " + (row.get("current") or "")))


def partition(camp):
    """Both groups, by subtraction, over the WHOLE carried population."""
    lists = [(k, camp.get(k) or []) for k in ("resolved", "carded", "deferred")]
    denom = sum(len(v) for _k, v in lists)
    two, fifteen, per_list = [], [], {}
    for k, rows in lists:
        t = [r for r in rows
             if "{system}" in (r.get("canonical") or "") and "{cadence}" in (r.get("canonical") or "")]
        f = [r for r in rows if brace_tokens(r) - set(SANCTIONED)]
        per_list[k] = {"rows": len(rows), "two_carrier": len(t), "unsanctioned_brace": len(f)}
        two.extend(t)
        fifteen.extend(f)
    return two, fifteen, denom, per_list


def census():
    camp = load_json(os.path.join(REPO, SOURCE))
    two, fifteen, denom, per_list = partition(camp)
    print("source: %s" % SOURCE)
    print("carried rows (resolved + carded + deferred): %d" % denom)
    for k, v in per_list.items():
        print("  %-9s rows %5d  two-carrier %3d  unsanctioned-brace %3d"
              % (k, v["rows"], v["two_carrier"], v["unsanctioned_brace"]))
    print("TWO-CARRIER rows re-identified: %d" % len(two))
    print("UNSANCTIONED-BRACE rows re-identified: %d" % len(fifteen))
    types2 = {}
    for r in two:
        types2[r["type"]] = types2.get(r["type"], 0) + 1
    types15 = {}
    for r in fifteen:
        types15[r["type"]] = types15.get(r["type"], 0) + 1
    print("  two-carrier by type: %s" % sorted(types2.items()))
    print("  unsanctioned by type: %s" % sorted(types15.items()))
    return two, fifteen, denom, per_list


def build():
    two, fifteen, denom, per_list = census()
    rules, lgs, targets, nfiles, nrules = scan_terraform()
    scan_note = ("No aws_cloudwatch_event_rule block with a LITERAL name field matching it was "
                 "found in %d .tf files carrying %d such blocks; the scan cannot see a name built "
                 "by interpolation, so this is 'no literal-name declaration', never 'not declared'."
                 % (nfiles, nrules))
    reg = load_json(os.path.join(REPO, REGISTRY))
    reg_rows = reg.get("resources") or []
    have = set()
    for r in reg_rows:
        if isinstance(r, dict):
            have.add((r.get("name"), r.get("type")))
    already = [r for r in two if (r["current"], r["type"]) in have]

    two_out = []
    kinds_count = {}
    for r in two:
        kind, carrier, act, claim = cadence_remedy(r, rules, lgs, targets, scan_note)
        kinds_count[kind] = kinds_count.get(kind, 0) + 1
        two_out.append({
            "current": r["current"],
            "type": r["type"],
            "plane": r["plane"],
            "canonical": r["canonical"],
            "label": LABEL,
            "remedies": [
                system_remedy(r, rules, lgs, (r["current"], r["type"]) in have, len(reg_rows),
                              len(two) - len(already), len(two)),
                {
                    "token": "cadence",
                    "carrier": carrier,
                    "carrier_kind": kind,
                    "in_a_cells_grant": False,
                    "act": act,
                    "claim": claim,
                },
            ],
            "neither_alone_clears_it": (
                "minting the {system} row leaves '{cadence}' in the canonical and vice versa, so a "
                "cell holding one carrier must hand the row on rather than record a resolution."),
        })

    fif_out = []
    for r in fifteen:
        toks = sorted(brace_tokens(r))
        runtime = sorted(set(BRACE.findall(r.get("current") or "")))
        opened = sorted(t for t in toks if t not in runtime)
        fif_out.append({
            "current": r["current"],
            "type": r["type"],
            "plane": r["plane"],
            "canonical": r["canonical"],
            "reason": (
                "%s: this row's `current` is an S3 KEY FORMAT TEMPLATE, not a key. The brace "
                "token(s) %s are the PRODUCER'S RUNTIME SUBSTITUTION FIELDS -- python format fields "
                "the producer fills at write time -- and they are already present in the row's OWN "
                "`current` before any grade ran, which is the measured discriminator. "
                "NAMING_SCHEMA.json grade.placeholder opens a slot 'the name does not carry', which "
                "PRESUPPOSES A NAME; a format string is not one. So the census graded a template as "
                "though it were an address, and 'resolve the substitution from a declared source' "
                "had no source BECAUSE THERE WAS NEVER A SUBSTITUTION QUESTION -- not because a "
                "source is missing or late. Nothing here is pending a lookup, and no later census "
                "should open one. R-62 (c): the row stays CARDED under this reason."
                % (FIFTEEN_REASON_HEAD, "{" + "}, {".join(runtime) + "}")),
            "producer_runtime_fields": ["{%s}" % t for t in runtime],
            "grade_opened_placeholders": ["{%s}" % t for t in opened],
            "not_resolvable_and_not_pending": True,
            "stays_in_the_grade": (
                "This row is NOT removed from any grade. R-62 refused that: S3Key sits in "
                "types_not_graded_by_kind but that table is a ROUTING table, and S3Key is one of "
                "the 7 entries STILL GRADED. Rewording its reason would move it across the 'NOT "
                "GRADED' prefix switch at lib/opal_naming.py:1012 and silently drop every S3 key in "
                "the estate."),
            "claim": "measured",
        })

    record = {
        "_about": (
            "LGIC_ENFORCE round 7, cell EN-t-34 (TO LGIC_ENFORCE.TO-EN-t-34-r7). TWO LABELS THAT "
            "LIED, MADE TRUE. Nothing is resolved, nothing is re-graded, and no grading behaviour "
            "changes. Group one: 51 rows a one-remedy label hid, each now naming BOTH remedies AND "
            "EACH REMEDY'S CARRIER. Group two: 15 key format templates whose reason said THE TOKEN "
            "IS NOT A SYSTEM, now saying what R-62 ruled -- THE ROW IS NOT A NAME."),
        "to_id": "LGIC_ENFORCE.TO-EN-t-34-r7",
        "cell": "EN-t-34",
        "outcome_ref": "FWD-5",
        "author": "0.9.0_WK_LGIC_ENFORCE~1",
        "issued_by": "2.0.0_SA_COO~G",
        "base_commit_pinned_by_R7_BASE": BASE_COMMIT,
        "rulings_carried": ["R-60", "R-62", "R-47", "R-40"],
        "instrument": ("org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/"
                       "label_truth_r7_build.py"),
        "instrument_reproduction": (
            "python org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/"
            "label_truth_r7_build.py build   -- regenerates this file byte-for-byte from the "
            "round-6 record, the registry and the repo's Terraform. `census` prints the "
            "denominators and writes nothing."),
        "source_record": SOURCE,
        "denominators": {
            "carried_rows_swept": denom,
            "per_list": per_list,
            "_note": (
                "The subtraction ran over the WHOLE carried population, not the carded list alone. "
                "Both groups fall entirely inside `carded`: that is a MEASURED result here, not the "
                "domain assumed at the start."),
            "two_carrier_rows_re_identified": len(two_out),
            "two_carrier_declared_by_round_6": 51,
            "unsanctioned_brace_rows_re_identified": len(fif_out),
            "unsanctioned_declared_by_round_6": 15,
            "terraform_files_scanned": nfiles,
            "aws_cloudwatch_event_rule_blocks_scanned": nrules,
            "resources_json_rows": len(reg_rows),
            "of_the_two_carrier_rows_already_carrying_a_registry_row": len(already),
        },
        "re_identification_instrument": {
            "two_carrier": (
                "'{system}' in canonical AND '{cadence}' in canonical -- INDEPENDENT of round 6's "
                "CADENCE_PLUS_SYSTEM label, which is not read anywhere in this record's derivation. "
                "Agreement with the declared 51 is the corroboration."),
            "unsanctioned_brace": (
                "the row's own brace tokens MINUS the four NAMING_SCHEMA.json grade.placeholder "
                "sanctions ({system}, {source}, {scope}, {cadence}); a non-empty remainder is an "
                "unsanctioned brace. Written as a subtraction from a printed denominator, never as "
                "a forward list of tokens recalled (Rule 24 i)."),
            "cadence_carrier": (
                "measured per row from the repo's Terraform: brace-balanced "
                "aws_cloudwatch_event_rule blocks, literal `name` field, presence of "
                "schedule_expression vs event_pattern; for a LOG_GROUP, the "
                "aws_cloudwatch_event_target edge that points a rule at the group."),
            "measured_limits_of_that_scan": [
                "It matches a LITERAL `name = \"...\"`; a rule whose name is interpolated is "
                "invisible to it, so NOT-FOUND means 'no literal-name declaration', never 'not "
                "declared'. Those rows carry carrier_kind LIVE_RULE_NO_REPO_DECLARATION, which "
                "names a carrier that exists either way.",
                "The firing attribute is read as an ATTRIBUTE after comment lines are stripped, "
                "never as a substring -- MEASURED BY BEING WRONG FIRST: a substring test reported "
                "aws_cloudwatch_event_rule.exec_summary_trigger_placeholder "
                "(infra/aws/terraform/exec-summary/main.tf) as carrying BOTH expressions, because "
                "the block's COMMENT at :225 names event_pattern as future work. The block "
                "declares schedule_expression only. A classifier that reads PROSE ABOUT an "
                "attribute as the attribute names a carrier the world does not have.",
            ],
        },
        "label_definition": LABEL_DEFINITION,
        "the_label_this_replaces": {
            "class_name": "NON_SYSTEM_PLACEHOLDER_TOKEN",
            "why_it_lied": (
                "It is a ONE-REMEDY label ('the token is not a system'), and 51 of the rows filed "
                "under it need TWO carriers. A row needing two remedies filed under a one-remedy "
                "label is INVISIBLE TO BOTH: the seat holding the registry grant sees a row it "
                "cannot finish, the seat holding the schedule read sees the same, and neither is "
                "wrong. Rule 24 INTENT COHERENCE failing inside the campaign built to enumerate."),
            "note_on_the_name": (
                "The 15 key-template rows carried the SAME class name for a different and also "
                "false reason, which is why one label repair covers two groups."),
        },
        "cadence_carrier_kinds_measured": kinds_count,
        "two_remedy_rows": two_out,
        "the_15_replaced_reason": {
            "old_reason_value": "NON_SYSTEM_PLACEHOLDER_TOKEN",
            "old_reason_says": "THE TOKEN IS NOT A SYSTEM -- which implies a system token was "
                               "expected and something else turned up.",
            "new_reason_says": "THE ROW IS NOT A NAME -- the graded object is a producer's key "
                               "FORMAT TEMPLATE, so the name grade's placeholder question never "
                               "applied to it at all.",
            "ruled": "R-62 (c), on R7_BASE.json's the_15_key_templates.disposition.",
            "_note": "This block is the ONLY place the superseded value appears in this record; no "
                     "row under key_template_rows carries it.",
        },
        "key_template_rows": fif_out,
        "not_done_here_and_why": NOT_DONE,
        "claim": "measured",
    }
    text = json.dumps(record, indent=1, sort_keys=False, ensure_ascii=True) + "\n"
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("wrote %s (%d bytes)" % (OUT, len(text)))
    print("two_remedy_rows: %d ; key_template_rows: %d" % (len(two_out), len(fif_out)))
    print("cadence carrier kinds: %s" % sorted(kinds_count.items()))
    return 0


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "build"
    if cmd == "census":
        census()
        return 0
    if cmd == "build":
        return build()
    print("usage: label_truth_r7_build.py [build|census]")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
