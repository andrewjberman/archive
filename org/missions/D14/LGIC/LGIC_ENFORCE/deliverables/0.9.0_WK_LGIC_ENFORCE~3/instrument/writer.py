"""writer.py -- writes org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/TF_LABEL_CENSUS.md from census.build().

EN-t-1, 0.9.0_WK_LGIC_ENFORCE~3. Run from the worktree root: python <instrument>/writer.py
"""
import collections
import contextlib
import io
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census  # noqa: E402

ORDER = ["CONFORMANT", "ALIAS", "OUT-OF-PATTERN", "RAISE", "NOT-GRADED"]
BASE = subprocess.run(["git", "merge-base", "HEAD", "CLOUD"], capture_output=True, text=True, check=True).stdout.strip()[:10]


def vcount(rows):
    c = collections.Counter(r["verdict"] for r in rows)
    return c


def vline(c, total):
    return ", ".join("%s %d" % (v, c.get(v, 0)) for v in ORDER) + " (of %d)" % total


def step_of(r):
    return r["why"].split(":")[0].split(" (via")[0].strip()


def main():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        bad = census.selftest()
    m = re.search(r"WORKED CASES: (\d+)  GRADED: (\d+)  SKIPPED: (\d+)  DISAGREE: (\d+)", buf.getvalue())
    wc, graded, skipped, disagree = (int(x) for x in m.groups())
    assert disagree == bad
    r = census.build()
    lab, nam, files = r["labels"], r["names"], r["files"]
    raw_heads = 0
    for f in files:
        t = open(f, encoding="utf-8").read().replace("\r\n", "\n")
        raw_heads += len(re.findall(r'(?m)^[ \t]*resource[ \t]+"[^"]+"[ \t]+"[^"]+"', t))
    types = collections.Counter(x["type"] for x in lab)
    name_types = collections.Counter(x["type"] for x in nam)

    def cls(t):
        if t in census.TF_NODE:
            node, at = census.TF_NODE[t]
            if node in census.NOT_GRADED:
                return "B"
            return "A" if at else "A0"
        if t in census.TF_OWN_UNMAPPED:
            return "C"
        return "D"
    part = collections.defaultdict(lambda: [0, 0, 0])
    for t, n in types.items():
        p = part[cls(t)]
        p[0] += 1
        p[1] += n
        p[2] += name_types.get(t, 0)
    assert sum(p[1] for p in part.values()) == len(lab) and sum(p[2] for p in part.values()) == len(nam)
    k_needed = sum(1 for x in nam if x["why"].startswith(("K5/K6", "K4a")))
    lv, nv = vcount(lab), vcount(nam)
    lsteps = collections.Counter(step_of(x) for x in lab if x["verdict"] == "RAISE")
    nsteps = collections.Counter(step_of(x) for x in nam if x["verdict"] == "RAISE")
    g23 = [x for x in nam if x["why"].startswith("G2.3")]
    forms = r["stats"]
    g3 = sum(1 for x in nam if x["why"].startswith("G3"))
    alias_bd = sum(1 for x in nam if x["verdict"] == "ALIAS" and "bd" in re.split(r"[-/_.]", x.get("resolved", x["value"])))
    by_node = collections.defaultdict(collections.Counter)
    for x in nam:
        by_node[x["node_type"] or "(no node type)"][x["verdict"]] += 1
    lab_by_node = collections.defaultdict(collections.Counter)
    for x in lab:
        lab_by_node[x["node_type"] or "(no node type)"][x["verdict"]] += 1
    kinds = r["kinds"]
    mod_args = r["module_args"]

    L = []
    w = L.append
    w("# TF_LABEL_CENSUS -- the Terraform-label census (LGIC_ENFORCE EN-t-1)")
    w("")
    w("**Cell:** LGIC_ENFORCE `EN-t-1` (PRD candidate E8, its first half), task order `LGIC_ENFORCE.TO-EN-t-1`, written by")
    w("`0.9.0_WK_LGIC_ENFORCE~3` on branch `wk-lgic-enforce-1-3` off CLOUD @`%s`. Every file and line below is read at that" % BASE)
    w("base, and every count is recomputable from the fenced json at the end.")
    w("")
    w("## 1. What was graded, and with what")
    w("")
    w("- **The instrument.** `lib/opal_naming.py` is absent at the base, so EN-b-1's `grade()` could not be called. This census")
    w("  applies `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md` **by its written steps** -- G1, G2, G3, then the")
    w("  grammar of the type (R, S, L, B, K), then G6; the first step that returns an output decides -- hand-coded in")
    w("  `deliverables/0.9.0_WK_LGIC_ENFORCE~3/instrument/census.py`, over a stdlib Terraform block scanner (`instrument/tfscan.py`).")
    w("  `writer.py` beside them writes this file.")
    w("- **The control on the hand-coding.** `python <instrument>/census.py selftest` grades the rule's own worked cases:")
    w("  **%d of %d graded cases agree, %d disagree.** %d of the %d cases are not graded by it: the platinum and tier-first key" % (graded - disagree, graded, disagree, skipped, wc))
    w("  forms (K4a, K5, K6), which walk the LIST and are not hand-coded. **No Terraform name in this census needed them: %d of %d.**" % (k_needed, len(nam)))
    w("- **The rule's vintage.** GRADING_RULE.md says it reads NAMING_SCHEMA.json v1.4; the base carries v1.6. The census applies")
    w("  the rule as written and reads the schema only for `kind.by_type`, `types_not_graded_by_kind` and `bucket.standing_shared`.")
    w("  Two later schema rulings the rule does not carry would move a grade here. `aws_fixed` (AW1, v1.5) puts log groups")
    w("  prefixed `aws-waf-logs-` OUTSIDE the domain, where the rule's G2.3 RAISES them: %d name(s) here, %s." % (len(g23), ", ".join("`%s` (%s:%d)" % (x["value"], x["file"], x["line"]) for x in g23)))
    w("  And FN1 (v1.5) writes an agent noun as its verb (publisher -> publish), which no canonical form here applies. Row `LGIC_ENFORCE-W3-S4`.")
    w("- **Labels are graded, and kept apart.** A label is graded as a name of the node type its resource maps to (the order: *\"grade")
    w("  them by the rule anyway, and keep them apart\"*). NAMING_SCHEMA.json v1.6 lists \"Terraform resource labels and module names\"")
    w("  under `not_covered`, so every label verdict is the rule applied outside the schema's domain, on the order's word. Labels are")
    w("  snake_case by Terraform convention, so a label almost never equals its kebab canonical form; the label verdicts measure that,")
    w("  and the systems and scopes labels carry.")
    w("")
    w("## 2. The denominators")
    w("")
    w("- `tf_files` = **%d**: `git ls-files infra/aws/terraform` restricted to `.tf`, at the base." % len(files))
    w("- `labels` = **%d**: every `resource \"<type>\" \"<label>\"` block the scanner reads, over %d Terraform resource types." % (len(lab), len(types)))
    w("  A raw line regex over the same files finds %d heads. The %d it finds and the scanner does not sit inside `/* ... */`" % (raw_heads, len(r["commented"])))
    w("  pre-stage comment blocks, so they are not Terraform and are not in the census: %s." % "; ".join("%s:%d `%s.%s`" % c for c in r["commented"]))
    w("- `name_attributes` = **%d**: one row per own-name attribute of a resource block (section 3)." % len(nam))
    w("- Top-level blocks that are not resources are outside the order's census: %s." % ", ".join("%d `%s`" % (kinds[k], k) for k in sorted(kinds) if k != "resource"))
    w("  The %d `module` calls pass names INTO modules: %s literal name-like argument(s) (%s). They are arguments, not resource" % (kinds["module"], sum(mod_args.values()), ", ".join("%d `%s`" % (n, k) for k, n in mod_args.items())))
    w("  attributes, so they are not rows here; the module's own resource names them by `var.<x>`, which does not resolve inside the")
    w("  module (row `LGIC_ENFORCE-W3-S3`, which also records that the order's `role_name` is on no tracked resource block).")
    w("")
    w("**The partition of the %d resource blocks.** Every block falls in exactly one line; the name rows sum to the denominator." % len(lab))
    w("")
    w("| class | Terraform types | blocks | name rows |")
    w("|---|---|---|---|")
    labels_cls = {"A": "maps to a graded node type, named by its own attribute", "A0": "maps to a graded node type, names nothing (none at this base)",
                  "B": "maps to a NOT GRADED node type (G1.2)", "C": "carries its own name, maps to no node type (G1.1 RAISE)",
                  "D": "names nothing (attachments, targets, permissions, configurations, integrations)"}
    for k in ("A", "A0", "B", "C", "D"):
        if k in part:
            p = part[k]
            w("| %s | %d | %d | %d |" % (labels_cls[k], p[0], p[1], p[2]))
    w("| **total** | **%d** | **%d** | **%d** |" % (len(types), len(lab), len(nam)))
    w("")
    w("## 3. The Terraform-type map (this census's reading; row `LGIC_ENFORCE-W3-S1`)")
    w("")
    w("G1.1 grades a node type, one of the 33; a Terraform resource type is none of them, and the order gives no map. The census")
    w("maps a Terraform type onto the node type of the AWS object it creates, and names it by the attribute AWS names that object by:")
    w("")
    w("| Terraform type | node type | own-name attribute | blocks |")
    w("|---|---|---|---|")
    for t in sorted(census.TF_NODE, key=lambda t: (census.TF_NODE[t][0], t)):
        if t in types:
            node, at = census.TF_NODE[t]
            w("| `%s` | %s | %s | %d |" % (t, node, "`%s`" % at if at else "-- (none)", types[t]))
    w("")
    w("- `aws_instance` is named by its `Name` tag, the one graded type AWS names only by a tag; no other tag is read.")
    w("- `aws_iam_role_policy` and `aws_iam_user_policy` (inline policies) map to IAM_POLICY, as the live plane's IAM_POLICY")
    w("  nodes carry inline policy names; `aws_s3_bucket_policy` is S3_BUCKET_POLICY and carries its bucket's name (B5).")
    w("- **Own name, no node type (G1.1 RAISE, label and name alike):** %s." % ", ".join("`%s`.`%s` (%d)" % (t, census.TF_OWN_UNMAPPED[t], types[t]) for t in sorted(census.TF_OWN_UNMAPPED) if t in types))
    dtypes = sorted((t for t in types if cls(t) == "D"), key=lambda t: (-types[t], t))
    w("- **Names nothing** (a `bucket`, `function_name`, `role` or `rule` there REFERS to another resource and is not this block's")
    w("  name; label graded, G1.1 RAISE): %s." % ", ".join("`%s` (%d)" % (t, types[t]) for t in dtypes))
    w("")
    w("## 4. How a value is read")
    w("")
    w("- **Literal** (`value_claim` = measured): graded as written -- %d of %d." % (forms["literal"], len(nam)))
    w("- **Expression resolved in the same directory** (`value_claim` = inferred): `local.<x>`, a `var.<x>` default, or")
    w("  `aws_<type>.<label>.<id|name|own attribute>` of a same-directory resource, substituted into a template; `resolved` carries the")
    w("  string graded -- %d of %d. A variable default can be overridden at apply; no `.tfvars` file is tracked under" % (forms["resolved"], len(nam)))
    w("  `infra/aws/terraform` at the base." )
    w("- **Expression not resolvable** (`value_claim` = absent): `each.*`, a module input with no default, an index, or an")
    w("  attribute that is not a name -- %d of %d. A graded type's row RAISES at G3 (the tokeniser cannot place it): %d; the rest are" % (forms["unresolved"], len(nam), g3))
    w("  decided at G1 before the name is read. Row `LGIC_ENFORCE-W3-S2`.")
    w("")
    w("## 5. What the census found")
    w("")
    w("| list | %s | total |" % " | ".join(ORDER))
    w("|---|%s---|" % ("---|" * len(ORDER)))
    w("| labels | %s | %d |" % (" | ".join(str(lv.get(v, 0)) for v in ORDER), len(lab)))
    w("| name attributes | %s | %d |" % (" | ".join(str(nv.get(v, 0)) for v in ORDER), len(nam)))
    w("")
    w("**Where the RAISES come from** (the step that raised):")
    w("")
    w("- labels: %s." % ", ".join("%s %d" % (k, n) for k, n in sorted(lsteps.items(), key=lambda kv: -kv[1])))
    w("- name attributes: %s." % ", ".join("%s %d" % (k, n) for k, n in sorted(nsteps.items(), key=lambda kv: -kv[1])))
    w("- R1.c and R2 are a V2 token in the system slot (row `LGIC_NAMING-W1-S2`: `agentbus`, `globgrph`, `opsec`, `imo` and the")
    w("  rest wait on the registry's platform-subsystem rows). R1.f is a first token in no vocabulary. G2.3 on a label is a label")
    w("  graded as a log group, which never begins `/`.")
    w("")
    w("**ALIAS:** %d name attributes, %d of them through the refused `bd` (R3: `bd` beside a firm is the vendor `blackdiamond`, alone" % (nv.get("ALIAS", 0), alias_bd))
    w("it is the firm `49financial`); the rest are a short firm form in a data bucket, which takes the long form (B2).")
    w("")
    w("**Name attributes by node type:**")
    w("")
    w("| node type | %s | total |" % " | ".join(ORDER))
    w("|---|%s---|" % ("---|" * len(ORDER)))
    for k in sorted(by_node):
        c = by_node[k]
        w("| %s | %s | %d |" % (k, " | ".join(str(c.get(v, 0)) for v in ORDER), sum(c.values())))
    w("")
    w("**Labels by node type:**")
    w("")
    w("| node type | %s | total |" % " | ".join(ORDER))
    w("|---|%s---|" % ("---|" * len(ORDER)))
    for k in sorted(lab_by_node):
        c = lab_by_node[k]
        w("| %s | %s | %d |" % (k, " | ".join(str(c.get(v, 0)) for v in ORDER), sum(c.values())))
    w("")
    w("## 6. What this census does not decide")
    w("")
    w("- Whether labels SHOULD be graded: the schema keeps them `not_covered` until their flagger is specified (E8, second half).")
    w("- The names module calls pass in (section 2), `data` sources, tag keys and values other than `aws_instance`'s `Name`.")
    w("- The Terraform-type map and the value resolution are readings (rows W3-S1, W3-S2), not rulings.")
    w("- FN1-FN4 and the other v1.5/v1.6 slot rulings the rule does not carry (row W3-S4). The K4a/K5/K6 LIST walk (0 names needed it).")
    w("- Nothing live was read and no Terraform ran: the values are the repo's, at the base.")
    w("")
    w("## 7. Rows filed on the channel")
    w("")
    w("`org/missions/D14/LGIC/LGIC_ENFORCE/surprise-channel/investigations/INVESTIGATION_v1.md`:")
    w("")
    w("- `LGIC_ENFORCE-W3-S1` -- G1.1 grades a node type; Terraform types are not node types and the order gives no map.")
    w("- `LGIC_ENFORCE-W3-S2` -- %d of %d name values are Terraform expressions, not names; %d resolved statically, %d not." % (forms["resolved"] + forms["unresolved"], len(nam), forms["resolved"], forms["unresolved"]))
    w("- `LGIC_ENFORCE-W3-S3` -- the order's `role_name` is on no tracked resource block; module-call names are outside a resource census.")
    w("- `LGIC_ENFORCE-W3-S4` -- GRADING_RULE.md is v1.4-vintage against NAMING_SCHEMA v1.6: G2.3 RAISES what `aws_fixed` excludes (%d names)." % len(g23))
    w("")
    w("## 8. The rows")
    w("")
    w("`labels` and `name_attributes` are separate lists. Beyond the order's fields each row carries `node_type` (section 3's map;")
    w("`null` = no node type) and `why` (the rule steps applied, in the worked cases' style). A name row also carries `value_claim`,")
    w("and `resolved` when the value is an expression resolved in its directory. `canonical` is empty on RAISE and NOT-GRADED.")
    w("")
    den = {"tf_files": len(files), "labels": len(lab), "name_attributes": len(nam)}
    w("```json")
    w('{"denominator": %s,' % json.dumps(den))
    w(' "labels": [')
    for i, x in enumerate(lab):
        w("  " + json.dumps(x, ensure_ascii=True) + ("," if i < len(lab) - 1 else ""))
    w(" ],")
    w(' "name_attributes": [')
    for i, x in enumerate(nam):
        w("  " + json.dumps(x, ensure_ascii=True) + ("," if i < len(nam) - 1 else ""))
    w(" ]}")
    w("```")
    text = "\n".join(L) + "\n"
    text.encode("ascii")  # no non-ASCII in the record
    with open(census.OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("WROTE %s  bytes=%d  tf_files=%d labels=%d name_attributes=%d  selftest %d/%d agree" % (census.OUT, len(text), len(files), len(lab), len(nam), graded - disagree, graded))
    print("labels:", vline(lv, len(lab)))
    print("names:", vline(nv, len(nam)))
    print("forms:", dict(forms), "G3:", g3, "G2.3 names:", len(g23), "partition:", {k: v for k, v in part.items()})


if __name__ == "__main__":
    main()
