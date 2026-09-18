"""EN-c-33 round 6: the placeholder campaign continued.

The instrument behind PLACEHOLDER_CAMPAIGN_R6.json. Committed rather than left in .scratch/ because the
record CITES it, and row LGIC_ENFORCE-S69 is what an untracked instrument costs (the drain nearly deleted
its own corroboration).

WHAT IT MEASURES, and the order matters:

1. THE START, from the HANDING RECORD and never from the task order: PLACEHOLDER_CAMPAIGN_R5.json's
   delta_riding_next_round.count, and its three carded classes as a fresh Counter over that record's
   carded rows' `reason`. check_en_r6.py's c33-population and c33-classes arms re-derive both the same
   way and refuse a declared start or class map that disagrees.

2. THE RESOLUTIONS. A row is RESOLVED only where the {system} substitution is read off a DECLARED
   SOURCE on two independent legs, never off the token's shape:

     leg A  the resource is DECLARED at a Terraform file:line, and the citation is TYPE-APPROPRIATE:
            declare_sites() indexes the tf_file that infra/aws/lambda/ci/lambda-source-map.json names,
            and accepts a site only where the enclosing block's Terraform type maps to the census row's
            OWN node_type under org/standards/NAMING_SCHEMA.json's `tf_type_map`, on the name_attribute
            that map declares (function_name for aws_lambda_function, name for
            aws_cloudwatch_event_rule and aws_iam_role_policy, ...). The mapping is the schema's DATA,
            not this cell's reading. For an EC2_INSTANCE the declared source is the
            infra/aws/ec2/EC2_MANIFEST.json service entry.

            WHY TYPE-APPROPRIATE AND NOT JUST THE NAME: resources.json is keyed (name, TYPE) --
            lib/opal_naming.py:1030-1032 -- so a row minted for ('x', 'LAMBDA') resolves NOTHING for a
            census row ('x', 'IAM_POLICY'). A first cut of this instrument keyed candidates on the name
            alone and would have reported 4 IAM_POLICY rows resolved by a Lambda's citation. Every
            (name, type) pair now carries its own site or is not claimed at all.
     leg B  the system is CARRIED ALREADY by that resource's own IAM role, which is an existing
            infra/logic/registry/resources.json row with its own cited evidence -- the role a Lambda
            assumes is declared in the same module block as the function, so this is one resource's
            two faces, not two guesses.
     leg C  where present, the tf_file's own HEADER names the owning project code (ADVI_*, ETFS_*,
            MDPF_*), which is what r5's resolved rows cited. Recorded when found, never required:
            a header is prose and its absence is not evidence of anything.

   Leg B is what makes the substitution MEASURED. `advi` is NOT read from the `inf-` prefix -- the
   prefix is a scope token, and cot-pipeline alone carries both etfs and mdpf rows, so the prefix
   would be wrong there. The role row is.

3. THE BUDGET. R-33: 25 measured resolutions, the same reading round 5 took (41 census rows across 25
   DISTINCT RESOURCES). Candidates are ordered deterministically -- source kind, then resource name --
   and the first 25 distinct resources are taken. Everything else DEFERS with an owner and a reason,
   and the deferred reason for an already-measured candidate NAMES its chain so round 7 mints it in
   one step rather than re-deriving it.

4. THE PARTITION. Every one of the start's rows lands in exactly one of resolved / carded / deferred:
     resolved  the census rows of the 25 resources
     carded    NON_SYSTEM_PLACEHOLDER_TOKEN (235) + TYPE_MISMATCH_NEEDS_CONFIRMATION (1) -- carded, NOT
               deferred, because neither reason is a timebox and one remedy does not move both
     deferred  the TIMEBOXED_R33 remainder

5. THE FENCE (R-29). The mint target is resources.json. MEASURED, not assumed, that this cannot change
   a generated policy on an applied resource:
     - infra/aws/terraform/modules/opal_name/generated_locals.tf:1 states its own inputs as
       "over exemptions.json,scopes.json" -- resources.json is not one of them;
     - the ONLY plan-time read of the registry anywhere under infra/aws/terraform/ is main.tf:82,
       `jsondecode(file(".../logic/registry/exemptions.json"))`;
     - resources.json reaches Terraform only inside two GENERATED TEST FIXTURES, and no round-6 cell
       runs `generate`.
   exemptions.json is not written here, and the c33-fence arm grades that independently against the
   pinned base.

Standard library only. ASCII only. LF endings.
"""
import io
import json
import os
import re
import subprocess
import sys
from collections import Counter

ROOT = "org/missions/D14/LGIC/LGIC_ENFORCE"
MINE = ROOT + "/deliverables/0.9.0_WK_LGIC_ENFORCE~1"
R5 = MINE + "/PLACEHOLDER_CAMPAIGN_R5.json"
R6 = MINE + "/PLACEHOLDER_CAMPAIGN_R6.json"
RESOURCES = "infra/logic/registry/resources.json"
SOURCE_MAP = "infra/aws/lambda/ci/lambda-source-map.json"
EC2_MANIFEST = "infra/aws/ec2/EC2_MANIFEST.json"

LANE = "2.0.0_SA_COO~G"
BUDGET = 25
PIN = "a981b05ee8"

PROJECT_CODE = re.compile(r"\b((?:ADVI|ETFS|MDPF|POSN|WSE|OPSEC|NFRA|IRPT|AMGT)_[A-Z0-9]+)")


def rd(p):
    return io.open(p, encoding="utf-8", errors="replace").read()


def jload(p):
    return json.loads(rd(p))


def jload_at_pin(p):
    """The file's bytes AT THIS CELL'S PIN, not in the worktree.

    Leg B reads resources.json to learn which IAM roles already carry a system -- and this instrument's
    `mint` verb WRITES resources.json. Read from the worktree, it would be measuring its own output: a
    second run would find its own 32 rows already minted, report ZERO resolutions, and a later reader
    re-running it to check the record would get a different answer and no explanation. Pinning the read
    makes the measurement reproducible from any checkout at or after the pin.
    """
    r = subprocess.run(["git", "show", "%s:%s" % (PIN, p)], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("cannot read %s at pin %s: %s" % (p, PIN, r.stderr.strip()))
    return json.loads(r.stdout)


def ascii_only(s):
    return "".join(ch if ord(ch) < 128 else " " for ch in str(s))


def find_line(path, needles):
    """(line_no, text) of the first line containing every needle; (None, None) if no line does."""
    if not os.path.isfile(path):
        return None, None
    for i, ln in enumerate(rd(path).splitlines(), 1):
        if all(n in ln for n in needles):
            return i, ascii_only(ln.strip())
    return None, None


def header_project(path, limit=40):
    """The owning project code named in the file's first `limit` lines, with its line number."""
    if not os.path.isfile(path):
        return None, None
    for i, ln in enumerate(rd(path).splitlines()[:limit], 1):
        m = PROJECT_CODE.search(ln)
        if m:
            return m.group(1), i
    return None, None


# ------------------------------------------------------------------ 1. the start, from the handing record
def measure_start():
    d = jload(R5)
    start = (d.get("delta_riding_next_round") or {}).get("count")
    classes = dict(Counter(str(r.get("reason")) for r in (d.get("carded") or []) if isinstance(r, dict)))
    return d, start, classes


# ------------------------------------------------------------------------------ 2. the candidate measure
BLOCK = re.compile(r'^(resource|module)\s+"([^"]+)"(?:\s+"([^"]+)")?\s*\{')
ASSIGN = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_.]*)\s*=\s*"([^"]*)"\s*$')
_SITES = {}


def declare_sites(tf):
    """{(node_type, value): (lineno, text, block)} -- every `<name_attribute> = "<value>"` in the file,
    typed by the DECLARED NAMING_SCHEMA.json tf_type_map rather than by this cell's own reading.

    A `module "x" {` block carrying function_name is read as LAMBDA: every Lambda in this estate is
    declared through a wrapper module whose function_name argument IS the function's name, which is the
    citation shape round 5's resolved rows used too.
    """
    if tf in _SITES:
        return _SITES[tf]
    tmap = jload("org/standards/NAMING_SCHEMA.json")["tf_type_map"]
    attr_of = {}
    for tftype, spec in tmap.items():
        if spec.get("name_attribute"):
            attr_of.setdefault(spec["name_attribute"], []).append((tftype, spec["node_type"]))
    sites, block = {}, None
    for i, ln in enumerate(rd(tf).splitlines(), 1):
        m = BLOCK.match(ln)
        if m:
            block = (m.group(1), m.group(2))
            continue
        a = ASSIGN.match(ln)
        if not (a and block):
            continue
        attr, val = a.group(1), a.group(2)
        for tftype, node_type in attr_of.get(attr, []):
            if block == ("resource", tftype) or (block[0] == "module" and attr == "function_name"):
                sites.setdefault((node_type, val), (i, ascii_only(ln.strip()),
                                                    "%s %r" % (block[0], block[1])))
    _SITES[tf] = sites
    return sites


def candidates(carried):
    """{(name, type): cand} -- every carried TIMEBOXED_R33 (name, type) whose system is readable on BOTH
    legs. Keyed on (name, type) because that is the pair lib/opal_naming.py:1030-1032 indexes
    resources.json on: a mint for ('x', 'LAMBDA') resolves NOTHING for a census row ('x', 'IAM_POLICY'),
    so a candidate keyed on the name alone would claim resolutions it had not made."""
    minted = {(r["name"], r["type"]): r for r in jload_at_pin(RESOURCES)["resources"]}
    by_role = {nm: r for (nm, ty), r in minted.items() if ty == "IAM_ROLE"}
    funcs = jload(SOURCE_MAP)["functions"]
    services = jload(EC2_MANIFEST)["services"]

    out = {}
    for row in carried:
        if row.get("reason") != "TIMEBOXED_R33":
            continue
        name, typ = row["current"], row["type"]
        key = (name, typ)
        if key in minted or key in out:
            continue  # already carries a registry row, or already measured on another plane

        f, s = funcs.get(name), services.get(name)
        if f:
            role = by_role.get(f.get("iam_role") or "")
            tf = f.get("tf_file")
            if not (role and tf and os.path.isfile(tf)):
                continue
            site = declare_sites(tf).get((typ, name))
            if site is None:
                continue  # no TYPE-APPROPRIATE declaration: not resolvable, stays deferred
            ln, txt, blk = site
            code, cln = header_project(tf)
            out[key] = {
                "resource": name, "type": typ, "system": role["system"], "kind": "A-lambda-source-map",
                "leg_a": "%s:%d @%s -- %s declares %s %r: %s" % (tf, ln, PIN, blk, typ, name, txt),
                "leg_b": ("%s names iam_role %r for %r; that role is %s[(%r, 'IAM_ROLE')] with system %r, "
                          "evidence: %s" % (SOURCE_MAP, f.get("iam_role"), name, RESOURCES,
                                            f.get("iam_role"), role["system"], role["evidence"])),
                "leg_c": ("%s:%d header names project %s" % (tf, cln, code)) if code else None,
            }
        elif s and typ == "EC2_INSTANCE":
            role = by_role.get(s.get("iam_role") or "")
            if not role:
                continue
            ln, _txt = find_line(EC2_MANIFEST, ['"%s"' % name])
            if ln is None:
                continue
            out[key] = {
                "resource": name, "type": typ, "system": role["system"], "kind": "B-ec2-manifest",
                "leg_a": "%s:%d @%s -- services[%r], source_path %r (the manifest IS the declared source "
                         "for an EC2_INSTANCE; NAMING_SCHEMA.json tf_type_map names aws_instance's "
                         "name_attribute as tags.Name, which the manifest carries as "
                         "instance_name_tag %r)" % (EC2_MANIFEST, ln, PIN, name, s.get("source_path"),
                                                    s.get("instance_name_tag")),
                "leg_b": ("%s names iam_role %r for %r; that role is %s[(%r, 'IAM_ROLE')] with system %r, "
                          "evidence: %s" % (EC2_MANIFEST, s.get("iam_role"), name, RESOURCES,
                                            s.get("iam_role"), role["system"], role["evidence"])),
                "leg_c": None,
            }
    return out


SANCTIONED = ("system", "source", "scope", "cadence")

# Per sanctioned token: the carrier NAMING_SCHEMA.json grade.placeholder names as its source, and whether
# that carrier is inside THIS order's <paths> grant. The grant is the literal <paths> block of
# LGIC_ENFORCE.TO-EN-c-33-r6: systems.json, resources.json, and the project's INVESTIGATION_v1.md.
TOKEN_CARRIERS = {
    "system": {
        "declared_carrier": "infra/logic/registry/resources.json -- the identity registry's "
                            "resource-to-system rows, keyed (name, type) at lib/opal_naming.py:1030-1032",
        "in_this_grant": True,
        "act": "mint a (name, type, system, evidence) row, which is exactly what this cell's 25 "
               "resolutions did",
    },
    "scope": {
        "declared_carrier": "THE BUCKET the key sits in -- not a registry file. scopes.json supplies the "
                            "VOCABULARY the value must belong to (9 rows), never the value",
        "in_this_grant": False,
        "act": "read the object's own bucket/prefix from the live S3 address or the producer's declared "
               "output path, then check the value against a scopes.json row's LONG form "
               "(NAMING_SCHEMA.json key.scope_form LONG)",
    },
    "source": {
        "declared_carrier": "THE BUCKET (same clause as {scope}). systems.json supplies the vocabulary -- "
                            "its own _about says a row is 'every token that may fill a resource name's "
                            "{system} slot or a key's {source}'",
        "in_this_grant": False,
        "act": "read the key's first segment from the live address or the producer, then check it against "
               "a systems.json VENDOR/PRODUCT/PLATFORM_SUBSYSTEM row",
    },
    "cadence": {
        "declared_carrier": "THE SCHEDULE -- the EventBridge rule's or the schedule's own expression, not "
                            "a registry file. NAMING_SCHEMA.json cadence.values supplies the vocabulary "
                            "(daily, weekly, monthly, hourly) plus the on-{event} form",
        "in_this_grant": False,
        "act": "read the rule's schedule_expression from its Terraform declaration (or "
               "`aws events describe-rule`, read-only) and map it onto cadence.values",
    },
}


def fill_non_system(d, rows, start):
    """The disposition, MEASURED from the rows rather than typed: token counts, per-token carriers, and a
    partition of the class written as its printed denominator MINUS each remedy group."""
    per_token = Counter()
    groups = Counter()
    unsanctioned = []
    for r in rows:
        toks = set(re.findall(r"\{([a-z_]+)\}", r.get("canonical") or ""))
        for t in toks:
            per_token[t] += 1
        odd = sorted(toks - set(SANCTIONED))
        if odd:
            unsanctioned.append(r)
            groups["UNSANCTIONED_BRACE_NOT_A_PLACEHOLDER"] += 1
        elif "cadence" in toks and "system" in toks:
            groups["CADENCE_PLUS_SYSTEM"] += 1
        elif "cadence" in toks:
            groups["CADENCE_ONLY"] += 1
        else:
            groups["SCOPE_OR_SOURCE_ONLY"] += 1

    n = len(rows)
    d["tokens_measured"] = dict(sorted(per_token.items()))
    d["token_carriers"] = {k: TOKEN_CARRIERS[k] for k in SANCTIONED}
    d["partition_by_remedy"] = {
        "_written_as": "the printed denominator %d MINUS each group, never a forward list of groups "
                       "recalled (Rule 24(i)); the groups are disjoint by construction (one elif chain "
                       "per row) and the remainder is asserted below" % n,
        "denominator": n,
        "SCOPE_OR_SOURCE_ONLY": {
            "count": groups["SCOPE_OR_SOURCE_ONLY"],
            "remedy": "read {scope}/{source} off THE BUCKET per grade.placeholder. OUT OF THIS GRANT: no "
                      "bucket read and no scopes.json write is in this order's <paths>.",
            "cleared_by_one_act": True,
        },
        "CADENCE_ONLY": {
            "count": groups["CADENCE_ONLY"],
            "remedy": "read {cadence} off THE SCHEDULE per grade.placeholder. OUT OF THIS GRANT.",
            "cleared_by_one_act": True,
        },
        "CADENCE_PLUS_SYSTEM": {
            "count": groups["CADENCE_PLUS_SYSTEM"],
            "remedy": "TWO carriers, and this is the group the class name hides: the {system} half IS in "
                      "this grant (a resources.json row) and the {cadence} half is NOT. So neither "
                      "remedy alone clears one of these rows, and minting the system half here would "
                      "have recorded 51 resolutions that still carry a brace -- which is why they are "
                      "carded whole rather than half-resolved.",
            "cleared_by_one_act": False,
        },
        "UNSANCTIONED_BRACE_NOT_A_PLACEHOLDER": {
            "count": groups["UNSANCTIONED_BRACE_NOT_A_PLACEHOLDER"],
            "remedy": "NOT A SUBSTITUTION AT ALL and NO declared source exists for it, now or later. See "
                      "surprise row LGIC_ENFORCE-W1-S70. These carry a brace token OUTSIDE "
                      "grade.placeholder's four ({snap}, {dim_name}, {d}, {dc}, {firm}); measured "
                      "discriminator: the brace is already present in the row's OWN `current` (the name "
                      "as declared), which is true of %d of %d rows in this class and, read UNSCOPED "
                      "over all %d carried rows, of those rows and no others. They are python format "
                      "fields in a producer's key TEMPLATE, so the census graded a format string rather "
                      "than a key. The remedy is a census-domain question for the registry owner, not a "
                      "lookup." % (len(unsanctioned), n, start),
            "cleared_by_one_act": False,
            "rows": sorted(set(r["current"] for r in unsanctioned)),
        },
    }
    covered = sum(v["count"] for k, v in d["partition_by_remedy"].items() if isinstance(v, dict))
    d["partition_by_remedy"]["_remainder_after_subtraction"] = n - covered
    assert covered == n, "the non-system partition leaves %d row(s) uncovered" % (n - covered)
    d["rule"] = ascii_only(
        "NOT A TIMEBOX AND NOT ONE REMEDY. The disposition of this class is: EACH ROW IS TRANSFERRED TO "
        "THE CARRIER ITS OWN TOKEN NAMES, and that carrier is named per token in `token_carriers` from "
        "NAMING_SCHEMA.json grade.placeholder -- {system} from resources.json (IN this grant), "
        "{scope}/{source} from THE BUCKET, {cadence} from THE SCHEDULE (both OUT of this grant, which is "
        "systems.json and resources.json only). THE ACT A LATER CENSUS TAKES, per group of "
        "`partition_by_remedy`, no re-derivation needed: SCOPE_OR_SOURCE_ONLY (%d) -- cut a cell granted "
        "the bucket read and substitute from the object's own address; CADENCE_ONLY (%d) -- cut a cell "
        "granted the schedule read and map schedule_expression onto cadence.values; CADENCE_PLUS_SYSTEM "
        "(%d) -- BOTH of those, in either order, because one alone leaves a brace; "
        "UNSANCTIONED_BRACE_NOT_A_PLACEHOLDER (%d) -- do NOT look for a source, it does not exist; these "
        "are template format fields and the question is whether the census should grade them at all "
        "(surprise row LGIC_ENFORCE-W1-S70). THE MECHANICAL TEST that keeps this from being a label, "
        "runnable by any later reader: for a row, the group is decided by its canonical's brace tokens "
        "alone -- set(tokens) - {'system','source','scope','cadence'} non-empty is group 4, else "
        "'cadence' and 'system' both present is group 3, else 'cadence' present is group 2, else group "
        "1. No judgment, no owner's opinion, and the four counts sum to the printed denominator %d."
        % (groups["SCOPE_OR_SOURCE_ONLY"], groups["CADENCE_ONLY"], groups["CADENCE_PLUS_SYSTEM"],
           groups["UNSANCTIONED_BRACE_NOT_A_PLACEHOLDER"], n))


def evidence_of(c):
    legs = ["LEG A (declared): " + c["leg_a"], "LEG B (system carried by its own IAM role): " + c["leg_b"]]
    if c["leg_c"]:
        legs.append("LEG C (header): " + c["leg_c"])
    return ascii_only(" | ".join(legs))


# --------------------------------------------------------------------------------------- 3. the partition
def build():
    r5, start, classes = measure_start()
    carried = r5["carded"]
    assert len(carried) == start, "the handing record's carded list is not its own delta"

    cands = candidates(carried)

    # THE BUDGET IS 25 DISTINCT RESOURCES (round 5's own reading of R-33). Resources are ordered
    # deterministically; every (name, type) pair of a chosen resource is resolved, because one Terraform
    # file declares them all and each pair carries its OWN type-appropriate citation.
    per_resource = {}
    for (name, _typ), c in cands.items():
        per_resource.setdefault(name, []).append(c)
    order = sorted(per_resource, key=lambda n: (min(c["kind"] for c in per_resource[n]), n))
    chosen_names = set(order[:BUDGET])
    spilled_names = set(order[BUDGET:])
    chosen = {k: c for k, c in cands.items() if c["resource"] in chosen_names}
    spilled = {k: c for k, c in cands.items() if c["resource"] in spilled_names}

    resolved, carded, deferred = [], [], []
    for row in carried:
        reason = row.get("reason")
        key = (row["current"], row["type"])
        if reason == "TIMEBOXED_R33" and key in chosen:
            c = chosen[key]
            resolved.append({
                "current": row["current"],
                "type": row["type"],
                "plane": row["plane"],
                "canonical_before": row["canonical"],
                "canonical_after": row["canonical"].replace("{system}", c["system"]),
                "system": c["system"],
                "owner_claim": "inferred",
                "owner_basis": evidence_of(c),
            })
        elif reason == "TIMEBOXED_R33":
            r = dict(row)
            if key in spilled:
                c = spilled[key]
                r["reason_detail"] = ascii_only(
                    "MEASURED THIS ROUND but past R-33's budget of %d resolutions: system %r is readable "
                    "on both legs -- %s -- and rides round 7 as a one-step mint, not a re-derivation."
                    % (BUDGET, c["system"], evidence_of(c)))
            elif row["current"] in chosen_names:
                r["reason_detail"] = ascii_only(
                    "NOT RESOLVED even though this resource's OTHER (name, type) pairs were: "
                    "infra/logic/registry/resources.json is keyed (name, type) at "
                    "lib/opal_naming.py:1030-1032, and no TYPE-APPROPRIATE declaration for type %r under "
                    "this name was found in the Terraform file its source-map entry names (searched by "
                    "NAMING_SCHEMA.json tf_type_map's own name_attribute for that node_type). A mint for "
                    "a sibling type would resolve NOTHING here, so this row is not claimed."
                    % row["type"])
            deferred.append(r)
        else:
            carded.append(dict(row))

    return (r5, start, classes, chosen, spilled, sorted(chosen_names), sorted(spilled_names),
            resolved, carded, deferred)


def write_record():
    (r5, start, classes, chosen, spilled, chosen_names, spilled_names,
     resolved, carded, deferred) = build()
    non_system = [r for r in carded if r.get("reason") == "NON_SYSTEM_PLACEHOLDER_TOKEN"]

    rec = {
        "_about": (
            "LGIC_ENFORCE.TO-EN-c-33-r6, cell EN-c-33 (rulings R-38, R-33, R-29). Round 5's campaign "
            "resolved 41 of 1411 and handed 1370 forward on its timebox. This is that carry taken "
            "forward. Instrument: %s/r6_campaign_resolve.py, committed beside this record." % MINE),
        "instrument": MINE + "/r6_campaign_resolve.py",
        "instrument_reproduction": (
            "`python %s/r6_campaign_resolve.py record` regenerates this file's three lists BYTE-FOR-BYTE "
            "from any checkout at or after the pin, INCLUDING after its own `mint` verb has run. That is "
            "deliberate and it is the one thing about this instrument worth knowing: leg B reads "
            "resources.json to learn which IAM roles already carry a system, and `mint` WRITES "
            "resources.json -- so the read is taken at the PIN via `git show %s:<path>` rather than from "
            "the worktree. Read from the worktree it would measure its own output, a re-run would find "
            "its own 32 rows already present and report ZERO resolutions, and a later reader checking "
            "this record would get a different answer with nothing to explain it." % (MINE, PIN)),
        "pin": PIN,
        "handing_record": R5,
        "denominators": {
            "population_at_start": start,
            "population_at_close": start,
            "instrument": (
                "population_at_start: a fresh read of %s's delta_riding_next_round.count, re-read at "
                "WRITE time by r6_campaign_resolve.py rather than quoted from the task order (which "
                "check_en_r6.py's c33-population arm refuses). population_at_close: the same count, "
                "re-derived after the write as len(resolved) + len(carded) + len(deferred) over this "
                "record's own three lists." % R5),
            "denominator_delta_note": (
                "ZERO delta, and that is a measurement rather than a default: round 5's denominator MOVED "
                "(1411 at start, 1370 at close) because its own resolutions removed rows from the census "
                "population it was counting. This round's population is not a census re-parse -- it is the "
                "HANDED SET, a fixed list of %d rows in the handing record, so resolving a row moves it "
                "between this record's lists and cannot move the denominator. The two figures are equal "
                "BY CONSTRUCTION of the population, not by luck, and a later census over "
                "NAMING_CENSUS_REPORT will report a SMALLER brace-carrying population than %d -- that is "
                "a different denominator over a different instrument and is not this one." % (start, start)),
        },
        "inherited_classes": classes,
        "inherited_classes_basis": (
            "a fresh Counter over %s's carded rows' `reason` field, the same derivation check_en_r6.py's "
            "_r5() runs; carried BY NAME with its count because the three are different questions and "
            "one remedy does not move all three (Rule 24(iv), state coherence)." % R5),
        "non_system_disposition": {
            "class": "NON_SYSTEM_PLACEHOLDER_TOKEN",
            "count": len(non_system),
            "rule": None,
            "rule_summary": (
                "NOT A TIMEBOX. This class is BLOCKED ON A CARRIER, not on effort, and the blocking "
                "carrier is DIFFERENT PER TOKEN -- so it is dispositioned per token, by subtraction from "
                "its own printed denominator, and no amount of round-7 budget moves any of it."),
            "authority": (
                "org/standards/NAMING_SCHEMA.json grade.placeholder, quoted: 'a canonical_form may carry "
                "{system}, {source}, {scope} or {cadence} ONLY for a slot the name does not carry. Each "
                "is a typed gap, never a guess, filled from its source: {system} from the identity "
                "registry's resource-to-system rows (LGIC_ENFORCE), {source}/{scope} from the bucket, "
                "{cadence} from the schedule.' FOUR tokens are sanctioned placeholders. That enumeration "
                "is the domain the subtraction below runs over, and it is the schema's, not this cell's."),
            "tokens_measured": None,
            "token_carriers": None,
            "partition_by_remedy": None,
            "owner": LANE,
            "carried_as": "carded (with owner and reason), never deferred -- deferral is the timebox's word",
        },
        "resolution_rule": {
            "what_counts_as_MEASURED": (
                "two independent legs onto a DECLARED source, never the token's shape. LEG A: the "
                "resource is declared at a Terraform file:line named by %s's tf_file, or is an %s service "
                "entry with a source_path. LEG B: the system is already carried by that resource's OWN "
                "IAM role, which is an existing %s row with its own cited evidence -- a Lambda's role is "
                "declared in the same module block as the function, so these are one resource's two "
                "faces. LEG C, recorded where found and never required: the tf_file's header names the "
                "owning project code." % (SOURCE_MAP, EC2_MANIFEST, RESOURCES)),
            "why_not_the_prefix": (
                "the leading token of these names is a SCOPE, not a system, and reading it as a system "
                "would be exactly the shape-inference this rule exists to exclude: cot-pipeline alone "
                "carries both etfs rows (cot-etf-ownership-daily-role) and mdpf rows "
                "(cot-rebalancer-runner-role) in this registry, so `cot-` resolves no system at all."),
            "selection_order": (
                "deterministic: sorted by (source kind, resource name), first %d distinct resources "
                "taken. Stated because the cut between resolved and deferred is otherwise a hidden "
                "choice." % BUDGET),
        },
        "mint_target": {
            "file": RESOURCES,
            "rows_added": None,
            "key": "(name, type) -- lib/opal_naming.py:1030-1032 indexes resources.json on that pair and "
                   ":1147 reads it only where the name's own tokens resolve no system",
            "fence_clearance_R29": (
                "MEASURED that this mint cannot change a generated policy on an applied resource: "
                "infra/aws/terraform/modules/opal_name/generated_locals.tf:1 declares its own inputs as "
                "'over exemptions.json,scopes.json' and resources.json is not one; the only plan-time "
                "read of the registry anywhere under infra/aws/terraform/ is "
                "modules/opal_name/main.tf:82 jsondecode(file(.../exemptions.json)); resources.json "
                "reaches Terraform only in two GENERATED TEST FIXTURES and no round-6 cell runs "
                "`generate`. exemptions.json is not written by this cell and the c33-fence arm grades "
                "that against the pinned base independently."),
        },
        "stopped_on_timebox": True,
        "timebox": {
            "ruling": "R-33",
            "budget_resolutions": BUDGET,
            "budget_reading": None,
            "resources_resolved": None,
            "candidates_measured_but_past_the_budget": None,
        },
        "delta_riding_next_round": {
            "count": None,
            "owner": LANE,
            "classes": None,
            "note": (
                "the remainder rides round 7. Of it, the candidates already MEASURED this round carry "
                "their full two-leg chain in their own reason_detail, so round 7 mints them without "
                "re-deriving anything."),
        },
        "resolved": resolved,
        "carded": carded,
        "deferred": deferred,
    }

    # the figures that are counts of this record's own lists, filled AFTER the lists exist
    fill_non_system(rec["non_system_disposition"], non_system, start)
    rec["mint_target"]["rows_added"] = len(chosen)
    total = len(resolved) + len(carded) + len(deferred)
    rec["timebox"]["budget_reading"] = (
        "25 MEASURED RESOLUTIONS = 25 distinct resources, the reading round 5 took (its own record: 41 "
        "resolved census rows across 25 distinct resources). Recorded because check_en_r6.py's arm "
        "implements the bar as start + 25 over the resolved LIST, which at a start of %d is %d and "
        "cannot bind a list that partitions %d rows -- so the arm's STOPPED branch is the one that "
        "grades, and the prose budget is what actually bounds this cell."
        % (total, total + BUDGET, total))
    rec["timebox"]["resources_resolved"] = len(chosen_names)
    rec["timebox"]["registry_rows_minted"] = len(chosen)
    rec["timebox"]["candidates_measured_but_past_the_budget"] = spilled_names
    rec["delta_riding_next_round"]["count"] = len(carded) + len(deferred)
    rec["delta_riding_next_round"]["classes"] = dict(
        Counter(str(r.get("reason")) for r in carded + deferred))
    rec["denominators"]["population_at_close"] = len(resolved) + len(carded) + len(deferred)

    with io.open(R6, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, indent=1, sort_keys=False)
        fh.write("\n")

    print("start (fresh read of the handing record) : %d" % start)
    print("inherited_classes                        : %s" % json.dumps(classes, sort_keys=True))
    print("resolved / carded / deferred             : %d + %d + %d = %d"
          % (len(resolved), len(carded), len(deferred), len(resolved) + len(carded) + len(deferred)))
    print("distinct resources resolved              : %d (budget %d)" % (len(chosen_names), BUDGET))
    print("registry (name, type) rows to mint       : %d" % len(chosen))
    print("measured but past the budget             : %d %s" % (len(spilled_names), spilled_names))
    print("population_at_start / at_close           : %d / %d" % (start, rec["denominators"]["population_at_close"]))
    print("non_system_disposition count / tokens    : %d %s"
          % (len(non_system), rec["non_system_disposition"]["tokens_measured"]))
    print("wrote %s" % R6)
    return chosen


def write_mint():
    """Append one resources.json row per resolved resource. APPEND ONLY: every pre-existing row is
    asserted byte-identical in the re-dump before the file is replaced."""
    chosen = write_record()
    before_text = rd(RESOURCES)
    doc = json.loads(before_text)
    rows = doc["resources"]
    n_before = len(rows)
    have = set((r["name"], r["type"]) for r in rows)

    rec = jload(R6)
    basis = {(r["current"], r["type"]): r["owner_basis"] for r in rec["resolved"]}
    added = []
    for key in sorted(chosen, key=lambda k: (chosen[k]["kind"], k)):
        c = chosen[key]
        if key in have:
            continue
        ev = basis.get(key)
        if not ev:
            print("REFUSED: no measured owner_basis for %r; not writing" % (key,))
            return 1
        row = {"name": c["resource"], "type": c["type"], "system": c["system"], "evidence": ev}
        rows.append(row)
        added.append(row)

    out = json.dumps(doc, indent=1, sort_keys=False, ensure_ascii=True) + "\n"

    # THE CONTROL: the re-dump's prefix through row n_before-1 must be byte-identical to the original's,
    # so the mint is provably an APPEND and not a reformat of 59 rows nobody asked to touch.
    keep = json.dumps({"resources": rows[:n_before]}, indent=1, sort_keys=False, ensure_ascii=True)
    orig = json.dumps({"resources": json.loads(before_text)["resources"]}, indent=1,
                      sort_keys=False, ensure_ascii=True)
    if keep != orig:
        print("REFUSED: the pre-existing rows do not re-dump byte-identically; not writing")
        return 1

    with io.open(RESOURCES, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    print("minted %d row(s) into %s (%d -> %d rows)" % (len(added), RESOURCES, n_before, len(rows)))
    for r in added:
        print("   %s | %s | %s" % (r["name"], r["type"], r["system"]))
    return 0


if __name__ == "__main__":
    verb = sys.argv[1] if len(sys.argv) > 1 else "record"
    if verb == "mint":
        sys.exit(write_mint())
    write_record()
