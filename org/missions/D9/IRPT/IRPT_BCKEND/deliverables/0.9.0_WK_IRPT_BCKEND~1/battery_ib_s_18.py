#!/usr/bin/env python3
"""IB-s-18 acceptance battery -- S18-AC1, five arms, every number beside its denominator.

Prints IBS18-FOUNDATION-COMPLETE on the last line ONLY when all five arms hold.

  (a) ELEVEN OF ELEVEN, FROM THE TABLE -- both directions. Forward: every
      'required meaning / fields' item of every CONTRACTS row at the pin has a property
      whose description quotes it VERBATIM. Backward (the anti-fabrication control): every
      quoted source string in every property description RESOLVES in the CONTRACTS section
      at that pin, so a property cannot be invented and then justified with prose.
  (b) EVERY FIXTURE PAIR DISCRIMINATES -- the valid fixture validates and the invalid one
      is REFUSED, 11 of 11 each way. A schema whose invalid fixture passes fails the arm.
  (c) THE MANIFEST COVERS THE PRD'S PATHS TABLE -- coverage is matched on the RAW TABLE
      TOKEN, not on the manifest's own resolved path, so a resolution bug cannot make this
      arm pass falsely; the resolutions are then verified separately against git.
  (d) NINE ROOTS, NINE DISTINCT STATE KEYS, ZERO STATE.
  (e) THE REGISTER CARRIES PART V -- the seven items, each with a non-empty owner.

Reads only. No AWS call, no vendor call, no network, no write.
"""
from __future__ import annotations

import io
import json
import os
import re
import subprocess
import sys

PIN = "62301f71e0"
BASE = "261c8d2080"
PRD = "org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md"
DECOMP = "org/missions/D9/IRPT/IRPT_BCKEND/decompositions/IRPT_BCKEND_DECOMP.md"
LAMBDA_HOME = "infra/aws/lambda/investor-reporting"
TF_HOME = "infra/aws/terraform/investor-reporting"
GOLD_HOME = "data/assets/scripts/gold/investor_reporting"
CONTRACTS_DIR = os.path.join(LAMBDA_HOME, "_contracts")
MANIFEST = os.path.join(LAMBDA_HOME, "PATH_MANIFEST.json")
REGISTER = os.path.join(LAMBDA_HOME, "DEPENDENCY_REGISTER.md")
NEW_HOMES = [LAMBDA_HOME + "/", TF_HOME + "/", GOLD_HOME + "/"]
PART_V_PREFIX = "B18 dependency register:"

FAILS = []
ARMS = {}


def fail(arm, msg):
    FAILS.append("%s: %s" % (arm, msg))
    print("ERROR: [%s] %s" % (arm, msg))


def check(arm, cond, msg):
    if not cond:
        fail(arm, msg)
    return bool(cond)


def git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True)


def git_show(ref_path):
    r = git("show", ref_path)
    if r.returncode != 0:
        raise SystemExit("ERROR: git show %s failed rc=%d" % (ref_path, r.returncode))
    return r.stdout.decode("utf-8")


def in_git(path):
    return git("cat-file", "-e", "%s:%s" % (BASE, path.rstrip("/"))).returncode == 0


def section(text, head):
    lines = text.split("\n")
    start = end = None
    for i, ln in enumerate(lines):
        if ln.startswith(head):
            start = i
        elif start is not None and i > start and ln.startswith("## "):
            end = i
            break
    if start is None:
        raise SystemExit("ERROR: section %r not found" % head)
    return lines[start:end]


def table_rows(lines, ncols):
    out = []
    for ln in lines:
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) != ncols:
            continue
        if cells[0] in ("---", "") or set(cells[0]) == set("-"):
            continue
        out.append(cells)
    return out


def descriptions(node, path, acc):
    if isinstance(node, dict):
        if isinstance(node.get("description"), str):
            acc.append((path, node["description"]))
        for k, v in node.items():
            descriptions(v, "%s.%s" % (path, k), acc)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            descriptions(v, "%s[%d]" % (path, i), acc)


def expand_braces(tok):
    m = re.search(r"\{([^{}]*,[^{}]*)\}", tok)
    if not m:
        return [tok]
    out = []
    for alt in m.group(1).split(","):
        out += expand_braces(tok[:m.start()] + alt.strip() + tok[m.end():])
    return out


# ------------------------------------------------------------------ arm (a)
def arm_a(prd):
    print("")
    print("(a) ELEVEN OF ELEVEN, FROM THE TABLE -- forward coverage AND the backward")
    print("    anti-fabrication control.")
    sec_lines = section(prd, "## CONTRACTS")
    sec_text = "\n".join(sec_lines)
    rows = table_rows(sec_lines, 5)
    rows = [r for r in rows if r[0] != "contract"]
    print("    DENOMINATOR: %d contract row(s) parsed from the CONTRACTS table at %s" % (len(rows), PIN))
    ok = check("a", len(rows) == 11, "expected 11 contract rows, parsed %d" % len(rows))

    files = sorted(f for f in os.listdir(CONTRACTS_DIR) if f.endswith(".schema.json"))
    print("    DENOMINATOR: %d schema file(s) under %s" % (len(files), CONTRACTS_DIR))
    ok = check("a", len(files) == 11, "expected 11 schema files, found %d" % len(files)) and ok

    total_items = 0
    total_cov = 0
    total_quotes = 0
    total_resolved = 0
    for cells in rows:
        name = cells[0].strip("`")
        items = [s.strip() for s in cells[4].split(";") if s.strip()]
        path = os.path.join(CONTRACTS_DIR, "%s.schema.json" % name)
        if not os.path.exists(path):
            fail("a", "no schema for contract %s at %s" % (name, path))
            ok = False
            continue
        doc = json.load(io.open(path, encoding="utf-8"))
        acc = []
        descriptions(doc, "$", acc)
        covered = []
        for it in items:
            hit = [p for p, d in acc if ('"%s"' % it) in d]
            if hit:
                covered.append(it)
        # backward: every quoted span in every description must resolve in the section
        quotes = 0
        resolved = 0
        for p, d in acc:
            for q in re.findall(r'"([^"]+)"', d):
                quotes += 1
                if q in sec_text:
                    resolved += 1
                else:
                    fail("a", "%s %s quotes a string absent from the CONTRACTS section: %r"
                         % (name, p, q[:70]))
                    ok = False
        total_items += len(items)
        total_cov += len(covered)
        total_quotes += quotes
        total_resolved += resolved
        top_ap = doc.get("additionalProperties")
        if top_ap is not False:
            fail("a", "%s: additionalProperties at the top level is %r, not false" % (name, top_ap))
            ok = False
        if len(covered) != len(items):
            missing = [i for i in items if i not in covered]
            fail("a", "%s: %d of %d items covered; missing %r" % (name, len(covered), len(items), missing))
            ok = False
        print("    %-18s %2d of %2d item(s) covered by a quoting property | %3d quote(s), %3d resolve at the pin"
              % (name, len(covered), len(items), quotes, resolved))
    print("    TOTAL: %d of %d required-meaning item(s) carried by a property whose description quotes them"
          % (total_cov, total_items))
    print("    TOTAL: %d of %d description quote(s) resolve VERBATIM in the CONTRACTS section at %s"
          % (total_resolved, total_quotes, PIN))
    print("    additionalProperties:false at the top level: %d of %d schema(s)"
          % (sum(1 for f in files
                 if json.load(io.open(os.path.join(CONTRACTS_DIR, f), encoding="utf-8"))
                 .get("additionalProperties") is False), len(files)))
    ARMS["a"] = ok
    return ok


# ------------------------------------------------------------------ arm (b)
def arm_b():
    print("")
    print("(b) EVERY FIXTURE PAIR DISCRIMINATES -- the difference control.")
    try:
        import jsonschema
    except ImportError:
        fail("b", "jsonschema is not installed -- the arm cannot run and is NOT a pass")
        ARMS["b"] = False
        return False
    files = sorted(f for f in os.listdir(CONTRACTS_DIR) if f.endswith(".schema.json"))
    accepted = 0
    refused = 0
    ok = True
    for f in files:
        name = f[:-len(".schema.json")]
        doc = json.load(io.open(os.path.join(CONTRACTS_DIR, f), encoding="utf-8"))
        v = jsonschema.Draft202012Validator(doc)
        vp = os.path.join(CONTRACTS_DIR, "fixtures", "%s.valid.json" % name)
        xp = os.path.join(CONTRACTS_DIR, "fixtures", "%s.invalid.json" % name)
        if not (os.path.exists(vp) and os.path.exists(xp)):
            fail("b", "%s: fixture pair incomplete (%s / %s)" % (name, os.path.exists(vp), os.path.exists(xp)))
            ok = False
            continue
        good = json.load(io.open(vp, encoding="utf-8"))["instance"]
        bad = json.load(io.open(xp, encoding="utf-8"))["instance"]
        ge = sorted(v.iter_errors(good), key=str)
        be = sorted(v.iter_errors(bad), key=str)
        if ge:
            fail("b", "%s: the VALID fixture does not validate -- %s" % (name, ge[0].message[:90]))
            ok = False
        else:
            accepted += 1
        if not be:
            fail("b", "%s: the INVALID fixture VALIDATES -- no difference control" % name)
            ok = False
        else:
            refused += 1
        print("    %-18s valid=%-8s invalid=%-8s refusal: %s"
              % (name, "ACCEPTED" if not ge else "REJECTED",
                 "REFUSED" if be else "ACCEPTED", (be[0].message[:60] if be else "-")))
    print("    %d of %d valid fixture(s) ACCEPTED; %d of %d invalid fixture(s) REFUSED"
          % (accepted, len(files), refused, len(files)))
    ok = check("b", accepted == 11 and refused == 11,
               "expected 11 of 11 each way, got %d accepted / %d refused" % (accepted, refused)) and ok
    ARMS["b"] = ok
    return ok


# ------------------------------------------------------------------ arm (c)
def arm_c(prd):
    print("")
    print("(c) THE MANIFEST COVERS THE PRD'S PATHS TABLE -- matched on the RAW TABLE TOKEN.")
    rows = table_rows(section(prd, "## PATHS"), 4)
    rows = [r for r in rows if r[0] != "kind"]
    reuse = sum(1 for r in rows if r[0] == "reuse")
    new = len(rows) - reuse
    print("    DENOMINATOR: %d PATHS row(s) at %s -- %d reuse, %d new" % (len(rows), PIN, reuse, new))
    tokens = []
    for cells in rows:
        for t in re.findall(r"`([^`]+)`", cells[1]):
            for tok in expand_braces(t):
                tokens.append((tok, cells[0], cells[2]))
    print("    DENOMINATOR: %d token(s) after brace expansion" % len(tokens))

    doc = json.load(io.open(MANIFEST, encoding="utf-8"))
    entries = doc["entries"]
    by_token = {}
    for e in entries:
        by_token.setdefault(e.get("path_as_written"), []).append(e)
    print("    DENOMINATOR: %d manifest entry(ies) in %s" % (len(entries), MANIFEST))

    ok = True
    covered = 0
    fielded = 0
    for tok, kind, cellcol in tokens:
        hits = by_token.get(tok, [])
        if not hits:
            fail("c", "PRD token not in the manifest: %r" % tok)
            ok = False
            continue
        covered += 1
        e = hits[0]
        problems = []
        if e.get("kind") not in ("reuse", "new"):
            problems.append("kind=%r" % e.get("kind"))
        if not e.get("cell"):
            problems.append("cell empty")
        if not e.get("owner"):
            problems.append("owner empty")
        if not e.get("use"):
            problems.append("use empty")
        expect_kind = "reuse" if kind == "reuse" else "new"
        if e.get("kind") != expect_kind:
            problems.append("kind %r != PRD %r" % (e.get("kind"), expect_kind))
        for num in re.findall(r"B([0-9]+)", cellcol):
            if ("B%s " % num) not in e.get("cell", "") + " " and ("B%s(" % num) not in e.get("cell", ""):
                if ("B%s" % num) not in e.get("cell", ""):
                    problems.append("cell missing B%s" % num)
        if problems:
            fail("c", "%s: %s" % (tok, "; ".join(problems)))
            ok = False
        else:
            fielded += 1
    print("    %d of %d PRD token(s) present in the manifest" % (covered, len(tokens)))
    print("    %d of %d present token(s) carry a non-empty kind, cell, owner and use" % (fielded, covered))

    # the resolutions the manifest claims, verified independently against git
    claimed = [e for e in entries if e.get("presence_at_base") == "PRESENT_AT_PIN"]
    verified = sum(1 for e in claimed if in_git(e["path"]))
    print("    %d of %d entry(ies) claiming PRESENT_AT_PIN verify with `git cat-file -e %s:<path>`"
          % (verified, len(claimed), BASE))
    ok = check("c", verified == len(claimed), "%d PRESENT_AT_PIN claim(s) do not verify" % (len(claimed) - verified)) and ok

    breakdown = {}
    for e in entries:
        breakdown[e.get("presence_at_base")] = breakdown.get(e.get("presence_at_base"), 0) + 1
    total = sum(breakdown.values())
    print("    PRESENCE BREAKDOWN (sums to the entry denominator %d):" % total)
    for k in sorted(breakdown):
        print("      %-32s %d" % (k, breakdown[k]))
    ok = check("c", total == len(entries), "presence breakdown %d != %d entries" % (total, len(entries))) and ok

    print("    THE THREE NEW HOMES, ABSENT-BY-DESIGN at %s (this cell creates them):" % BASE)
    absent = 0
    for home in NEW_HOMES:
        present = in_git(home)
        ent = [e for e in entries if e["path"].rstrip("/") == home.rstrip("/")]
        state = ent[0]["presence_at_base"] if ent else "NOT-IN-MANIFEST"
        print("      %-46s in git at %s: %-5s manifest: %s" % (home, BASE, present, state))
        if (not present) and state == "ABSENT_BY_DESIGN_NEW_HOME":
            absent += 1
    print("    %d of %d new home(s) ABSENT-BY-DESIGN at the base commit and recorded as such" % (absent, len(NEW_HOMES)))
    ok = check("c", absent == 3, "expected 3 of 3 new homes ABSENT-BY-DESIGN, got %d" % absent) and ok
    ok = check("c", covered == len(tokens), "manifest coverage %d of %d" % (covered, len(tokens))) and ok
    ARMS["c"] = ok
    return ok


# ------------------------------------------------------------------ arm (d)
def arm_d():
    print("")
    print("(d) NINE ROOTS, NINE DISTINCT STATE KEYS, ZERO STATE.")
    roots = sorted(d for d in os.listdir(TF_HOME) if os.path.isdir(os.path.join(TF_HOME, d)))
    print("    DENOMINATOR: %d directory(ies) under %s" % (len(roots), TF_HOME))
    ok = check("d", len(roots) == 9, "expected 9 roots, found %d: %r" % (len(roots), roots))
    keys = []
    for r in roots:
        mt = os.path.join(TF_HOME, r, "main.tf")
        if not os.path.exists(mt):
            fail("d", "%s has no main.tf" % r)
            ok = False
            continue
        text = io.open(mt, encoding="ascii").read()
        m = re.search(r'key\s*=\s*"([^"]+)"', text)
        b = re.search(r'bucket\s*=\s*"([^"]+)"', text)
        reg = re.search(r'region\s*=\s*"([^"]+)"', text)
        prov = re.search(r'version\s*=\s*"(~> 5\.0)"', text)
        tags = all(t in text for t in ('Project   = "OpalPortal"', 'ManagedBy = "Terraform"',
                                       'System    = "InvestorReporting"'))
        if not m:
            fail("d", "%s/main.tf has no backend key" % r)
            ok = False
            continue
        keys.append(m.group(1))
        good = (b and b.group(1) == "opal-313476888478-terraform-state" and reg
                and reg.group(1) == "us-east-1" and prov and tags
                and m.group(1).startswith("investor-reporting/"))
        if not good:
            fail("d", "%s/main.tf backend or provider shape is wrong (bucket=%r region=%r provider=%r tags=%s)"
                 % (r, b and b.group(1), reg and reg.group(1), bool(prov), tags))
            ok = False
        print("    %-14s key=%-42s bucket/region/provider/tags OK=%s" % (r + "/", m.group(1), bool(good)))
    print("    %d of %d state key(s) pairwise DISTINCT" % (len(set(keys)), len(keys)))
    print("    %d of %d state key(s) under investor-reporting/"
          % (sum(1 for k in keys if k.startswith("investor-reporting/")), len(keys)))
    ok = check("d", len(set(keys)) == len(keys) == 9, "state keys are not 9 distinct: %r" % keys) and ok

    state_hits = []
    for dp, dn, fn in os.walk(TF_HOME):
        for d in dn:
            if d == ".terraform":
                state_hits.append(os.path.join(dp, d))
        for f in fn:
            if f.startswith("terraform.tfstate"):
                state_hits.append(os.path.join(dp, f))
    print("    STATE ON DISK: %d `.terraform/` dir(s) and %d `terraform.tfstate*` file(s) under %s -- %d of %d roots initialised"
          % (sum(1 for h in state_hits if h.endswith(".terraform")),
             sum(1 for h in state_hits if "tfstate" in os.path.basename(h)),
             TF_HOME, 0 if not state_hits else len(state_hits), len(roots)))
    ok = check("d", not state_hits, "state artifacts exist: %r" % state_hits) and ok
    ARMS["d"] = ok
    return ok


# ------------------------------------------------------------------ arm (e)
def arm_e(prd):
    print("")
    print("(e) THE REGISTER CARRIES PART V.")
    row = None
    for ln in prd.split("\n"):
        if ln.startswith("| 25 |"):
            row = [c.strip() for c in ln.strip().strip("|").split("|")]
            break
    if row is None:
        fail("e", "BRIEF COVERAGE entry 25 not found at the pin")
        ARMS["e"] = False
        return False
    consumed = row[2]
    ok = check("e", consumed.startswith(PART_V_PREFIX), "entry 25 does not open with %r" % PART_V_PREFIX)
    items = [s.strip() for s in consumed[len(PART_V_PREFIX):].split(";") if s.strip()]
    print("    DENOMINATOR: %d Part V item(s) parsed from PRD BRIEF COVERAGE entry 25 at %s" % (len(items), PIN))
    ok = check("e", len(items) == 7, "expected 7 Part V items, parsed %d" % len(items)) and ok

    text = io.open(REGISTER, encoding="ascii").read()
    rows = table_rows(text.split("\n"), 5)
    rows = [r for r in rows if r[0].isdigit()]
    print("    DENOMINATOR: %d row(s) in %s" % (len(rows), REGISTER))
    carried = 0
    owned = 0
    for it in items:
        hit = [r for r in rows if r[1] == it]
        if not hit:
            fail("e", "Part V item not carried verbatim by the register: %r" % it[:70])
            ok = False
            continue
        carried += 1
        owner = hit[0][2]
        if owner.strip():
            owned += 1
            print("    %-72s owner: %s" % (it[:72], owner[:60]))
        else:
            fail("e", "register row for %r has an EMPTY owner" % it[:60])
            ok = False
    print("    %d of %d Part V item(s) carried VERBATIM; %d of %d carry a non-empty owner"
          % (carried, len(items), owned, len(items)))
    ok = check("e", carried == len(items) == owned, "coverage %d / owners %d of %d" % (carried, owned, len(items))) and ok
    ARMS["e"] = ok
    return ok


def main():
    print("IB-s-18 BATTERY -- S18-AC1, five arms. Reads only: no AWS call, no vendor call, no write.")
    print("PRD pin %s | base commit %s | cwd %s" % (PIN, BASE, os.getcwd()))
    for p in (CONTRACTS_DIR, MANIFEST, REGISTER, TF_HOME, GOLD_HOME):
        if not os.path.exists(p):
            fail("pre", "required deliverable path is missing: %s" % p)
    prd = git_show("%s:%s" % (PIN, PRD))
    print("PRD at the pin: %d byte(s), %d line(s)" % (len(prd.encode("utf-8")), len(prd.split("\n"))))
    arm_a(prd)
    arm_b()
    arm_c(prd)
    arm_d()
    arm_e(prd)
    print("")
    held = sum(1 for v in ARMS.values() if v)
    print("arms: %d of %d evaluated; arms holding: %d of 5; assertions failed: %d"
          % (len(ARMS), 5, held, len(FAILS)))
    for f in FAILS:
        print("  FAILED -- %s" % f)
    if len(ARMS) == 5 and held == 5 and not FAILS:
        print("IBS18-FOUNDATION-COMPLETE")
        return 0
    print("BLOCKED: the token is withheld -- %d of 5 arm(s) held" % held)
    return 1


if __name__ == "__main__":
    sys.exit(main())
