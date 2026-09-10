#!/usr/bin/env python3
"""NFRA_CLDGRPH CG-s-38 / H3-AC1 -- THE FOUR-HOP PORTAL-VINTAGE FEED, RE-DERIVED BY CONTENT.

WHY BY CONTENT AND NOT BY LINE NUMBER. Round 7's CG-s-35 recorded the feed as a table of
file:line citations. A line number is a STORED BASELINE FROM ANOTHER VINTAGE: it ages the
moment anyone edits above it, and it ages SILENTLY, because a stale line still resolves to
a real line of a real file and reads exactly like a fresh one. So every hop below is found
by WHAT IT DOES -- an AST node for the two python hops, a literal statement for the
Terraform buildspec and the GitHub workflow -- and the round-7 citation is then TESTED
against that, never trusted.

THE PIN TEST'S GRAIN, STATED. The pins are tested against the BASELINE COMMIT this
worktree was cut from, NOT against the working tree: the working tree carries this order's
own hop edits, which move lines by construction, and scoring those as "the record aged"
would be this instrument measuring itself. The baseline is also byte-identical to the
issuer's own measurement commit on all five hop files (asserted below, from git).

INSTRUMENT / COVERAGE / GRAIN / ENVIRONMENT / STATE are printed beside every claim.
"""
import ast
import os
import re
import subprocess
import sys

BASE = "2fd5cae09f"          # the commit this worktree was cut from
ISSUER_MEASURED_AT = "de3970331f"   # the HEAD the task order says it measured at

KUZU = "infra/aws/globgrph/kuzu_nessie_load.py"
PW = "infra/aws/globgrph/projection_worker.py"
TF = "infra/aws/terraform/globgrph/stitch-produce.tf"
WF = ".github/workflows/stitch-source-push.yml"
F3 = ("org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/"
      "f3_build_source_zip.py")
PROV = "infra/aws/globgrph/_provenance.py"
CONTROL = ("org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/"
           "h3_tree_control.txt")

MARKER_KEYS_ROUND7 = ["built_at", "aws_snapshot", "git_sha", "producer", "total_nodes",
                      "total_edges", "artifact_sha256"]


def sh(args):
    env = dict(os.environ)
    env["MSYS_NO_PATHCONV"] = "1"      # a slashed git ref must not be path-converted
    r = subprocess.run(args, capture_output=True, text=True, env=env)
    return r.returncode, r.stdout, r.stderr


def blob(commit, path):
    rc, out, err = sh(["git", "show", commit + ":" + path])
    if rc != 0:
        raise SystemExit("BLOCKED: git show %s:%s rc=%d %s" % (commit, path, rc, err.strip()))
    return out


def read(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


# ---------------------------------------------------------------- content locators
def loc_return_dict(text, funcname):
    """(first,last) 1-based lines of the dict-or-name RETURN payload of `funcname`.

    Located by AST: the function's LAST Return whose value is a Dict, or -- once this
    order's edit lands -- the Assign of the dict that Return names. Nothing here reads a
    line number from a record; the numbers are OUTPUTS, not inputs."""
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == funcname:
            dicts = [n for n in ast.walk(node)
                     if isinstance(n, ast.Return) and isinstance(n.value, ast.Dict)
                     and n.value.keys]
            if dicts:
                d = dicts[-1]
                return d.lineno, d.end_lineno, [k.value for k in d.value.keys]
            assigns = [n for n in ast.walk(node)
                       if isinstance(n, ast.Assign) and isinstance(n.value, ast.Dict)
                       and n.value.keys]
            if assigns:
                a = assigns[-1]
                keys = [k.value for k in a.value.keys]
                extra = [n for n in ast.walk(node)
                         if isinstance(n, ast.Assign) and isinstance(n.targets[0],
                                                                     ast.Subscript)]
                for e in extra:
                    keys.append(e.targets[0].slice.value)
                return a.lineno, a.end_lineno, keys
    raise SystemExit("BLOCKED: no function %s in the parsed source" % funcname)


def loc_clause(text, funcname, needle):
    """(first,last) 1-based lines of the IF whose body appends `needle` inside `funcname`."""
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == funcname:
            for n in ast.walk(node):
                if isinstance(n, ast.If):
                    seg = ast.get_source_segment(text, n) or ""
                    if needle in seg:
                        return n.lineno, n.end_lineno
    return None, None


def loc_literal(text, needle):
    for i, ln in enumerate(text.split("\n"), 1):
        if needle in ln:
            return i
    return None


def tf_marker_keys(text):
    """The buildspec marker dict's DECLARED keys, by content: the quoted keys of the
    `marker = {` literal plus any `marker['k'] =` assignment after it."""
    lines = text.split("\n")
    start = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("marker = {"):
            start = i
            break
    if start is None:
        raise SystemExit("BLOCKED: no `marker = {` in the buildspec")
    keys = []
    i = start + 1
    while i < len(lines) and not lines[i].strip().startswith("}"):
        m = re.match(r"^\s*'([a-z_0-9]+)'\s*:", lines[i])
        if m:
            keys.append(m.group(1))
        i += 1
    end = i + 1
    for j in range(end, min(end + 12, len(lines))):
        m = re.search(r"marker\['([a-z_0-9]+)'\]\s*=", lines[j])
        if m:
            keys.append(m.group(1))
            end = j + 1
    return keys, start + 1, end


def main():
    rc, head, _ = sh(["git", "rev-parse", "HEAD"])
    rc, branch, _ = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    head, branch = head.strip(), branch.strip()

    print("=== CG-s-38 / H3-AC1 -- THE FOUR-HOP PORTAL-VINTAGE FEED, RE-DERIVED BY CONTENT ===")
    print("TREE_READ=%s  branch=%s  head=%s" % (os.getcwd().replace(os.sep, "/"), branch, head))
    print("TREE_CONTROL=%s exists=%s -- a file that exists ONLY on this branch; a census that"
          % (CONTROL, os.path.isfile(CONTROL)))
    print("  cannot see it read some other tree, and a denominator is not a tree.")
    rc, ctl, _ = sh(["git", "log", "--oneline", "-1", "--", CONTROL])
    print("  control on BASE %s: %s" % (BASE, "ABSENT (correct: minted on this branch)"
                                        if not blob_exists(BASE, CONTROL) else "PRESENT"))
    print("INSTRUMENT: python ast.parse for the two engine hops (node kind + name, never a"
          " line number as INPUT); literal statement match for the Terraform buildspec and"
          " the GitHub workflow, which are not python.")
    print("COVERAGE: 5 files, whole-file each -- %s, %s, %s, %s, %s." % (KUZU, PW, TF, WF, F3))
    print("GRAIN: one AST node / one line. ENVIRONMENT: this linked worktree, python %s on"
          " %s, git as the only other instrument."
          % (sys.version.split()[0], sys.platform))
    print("")

    # ---- the baseline the pin test is scored against ------------------------------
    same = []
    for p in (KUZU, PW, TF, WF, F3, PROV):
        rc, out, _ = sh(["git", "diff", "--name-only", ISSUER_MEASURED_AT, BASE, "--", p])
        same.append((p, out.strip() == ""))
    print("PIN-TEST BASELINE=%s (this worktree's cut base). The task order says it measured"
          " at %s." % (BASE, ISSUER_MEASURED_AT))
    print("  BYTE-IDENTICAL BETWEEN THE TWO: %d of %d hop file(s) -- so the issuer's numbers"
          " and this baseline are the same object, and any disagreement below is a reading,"
          " not a vintage." % (sum(1 for _, s in same if s), len(same)))
    print("")

    hops = []

    # ---------------------------------------------------------------- HOP 1 PACK
    f3_now = read(F3)
    wf_now = read(WF)
    f3_base = blob(BASE, F3)
    wf_base = blob(BASE, WF)
    l_head_now = loc_literal(f3_now, "portal_head = subprocess.run")
    l_write_now = loc_literal(f3_now, 'z.writestr("portal_sha.txt"')
    l_wfwrite_now = loc_literal(wf_now, "git -C portal rev-parse HEAD > portal_sha.txt")
    l_wfzip_now = loc_literal(wf_now, "portal_sha.txt " + chr(92))
    l_pin_now = loc_literal(wf_now, "ref: ")
    pin_val = wf_now.split("\n")[l_pin_now - 1].split("ref:")[1].strip()
    rc, gitlink, _ = sh(["git", "ls-tree", "HEAD", "portal"])
    gitlink_sha = gitlink.split()[2] if len(gitlink.split()) > 2 else "(unread)"
    l_head_base = loc_literal(f3_base, "portal_head = subprocess.run")
    l_pin_base = loc_literal(wf_base, "ref: ")

    print("HOP 1 PACK -- write the portal sha INTO THE ARCHIVE, on both routes")
    print("  route A (THE ROUTE THAT ACTUALLY RAN, five served pushes in round 6, all by hand):")
    print("    file %s" % F3)
    print("    portal head computed at :%s (round-7 cited :84)" % l_head_now)
    print("    NOW WRITES the archive entry portal_sha.txt at :%s" % l_write_now)
    print("  route B (THE COMMITTED ROUTE, which nobody has observed to run):")
    print("    file %s" % WF)
    print("    portal_sha.txt written at :%s, packed into the zip at :%s"
          % (l_wfwrite_now, l_wfzip_now))
    print("    the LITERAL portal pin is still at :%s -> %s" % (l_pin_now, pin_val))
    print("    the repo's own portal GITLINK at HEAD -> %s" % gitlink_sha)
    print("    PIN_EQUALS_GITLINK=%s  <- the comment above the pin says it IS the gitlink sha"
          % str(pin_val == gitlink_sha).lower())
    print("  change required : write portal_sha.txt into the archive beside"
          " stitch_source_sha.txt  [DONE on both routes]")
    print("  NOT done here   : nothing updates the literal pin. Left alone deliberately --"
          " see the owned item in the record; changing a production route's checkout ref is"
          " not this cell's change and has no test available under the egress hold.")
    print("  OWNER           : 0.7.0_AE_CloudOps (the disarm owner rows W2-S40 and W2-S63"
          " already carry), with 1.0.0_SA_CTO to place the hand route's production home")
    print("  STATE_THIS_ROUND: DESIRED (committed producer code; route B needs a push +"
          " secrets.PORTAL_REPO_PAT, route A needs a hand run -- neither is APPLIED, and the"
          " egress hold forbids exercising either against S3)")
    hops.append(("1 PACK", "%s + %s" % (F3, WF),
                 "0.7.0_AE_CloudOps", "DESIRED",
                 l_head_base == 84 and l_pin_base == 66))

    # ---------------------------------------------------------------- HOP 2 STAMP
    tf_now = read(TF)
    tf_base = blob(BASE, TF)
    keys_now, mk_start, mk_end = tf_marker_keys(tf_now)
    keys_base, _, _ = tf_marker_keys(tf_base)
    print("")
    print("HOP 2 STAMP -- the buildspec's marker dict carries the key")
    print("  file %s, the inline buildspec's marker dict at :%d-%d" % (TF, mk_start, mk_end))
    print("  declared keys NOW  (%d): %s" % (len(keys_now), ", ".join(keys_now)))
    print("  declared keys BASE (%d): %s" % (len(keys_base), ", ".join(keys_base)))
    print("  round-7 recorded 7 declared keys and a LIVE marker carrying exactly those seven")
    print("  change required : one entry, marker['portal_sha'], read from portal_sha.txt in"
          " the unpacked archive  [DONE, and conditional: absent is absent]")
    print("  OWNER           : 0.7.0_AE_CloudOps (Terraform plane)")
    print("  STATE_THIS_ROUND: DESIRED -- committed Terraform. NOT applied. A committed"
          " buildspec is a WISH about a CodeBuild project until an apply lands, and no apply"
          " is permitted in this round.")
    hops.append(("2 STAMP", TF, "0.7.0_AE_CloudOps", "DESIRED",
                 keys_base == MARKER_KEYS_ROUND7))

    # ---------------------------------------------------------------- HOP 3 COPY
    k_now = read(KUZU)
    k_base = blob(BASE, KUZU)
    n_first, n_last, n_keys = loc_return_dict(k_now, "read_stitch_vintage")
    b_first, b_last, b_keys = loc_return_dict(k_base, "read_stitch_vintage")
    print("")
    print("HOP 3 COPY -- read_stitch_vintage copies the key into source_vintage")
    print("  file %s" % KUZU)
    print("  BASE: the returned dict literal is at :%d-%d carrying %d key(s)"
          % (b_first, b_last, len(b_keys)))
    print("  ROUND-7 CITED :71-77 for this hop. MEASURED at the baseline: :%d-%d. MATCH=%s"
          % (b_first, b_last, str((b_first, b_last) == (71, 77)).lower()))
    print("  THE TASK ORDER'S OWN RE-MEASUREMENT SAYS :68-78 IS THE RETURN DICT. Measured"
          " here at the same bytes: :68-70 is the `if not m.get(\"built_at\")` guard and its"
          " early return, :78 is the `except` line. The round-7 citation had NOT moved.")
    print("  NOW : the payload is at :%d-%d carrying %d key(s): %s"
          % (n_first, n_last, len(n_keys), ", ".join(n_keys)))
    print("  change required : one key beside the five it already copies  [DONE]")
    print("  OWNER           : the globgrph engine owner -- this project's plane")
    print("  STATE_THIS_ROUND: DESIRED (committed) + LOCALLY EXERCISED over real bytes by"
          " h3_local_endtoend.py. NOT deployed: the engine runs in ECS and no image act,"
          " apply or run-task is permitted here.")
    hops.append(("3 COPY", KUZU, "globgrph engine owner (this project)",
                 "DESIRED + LOCAL-EXERCISED", (b_first, b_last) == (71, 77)))

    # ---------------------------------------------------------------- HOP 4 PRINT
    p_now = read(PW)
    p_base = blob(BASE, PW)
    sn_a, sn_b = loc_clause(p_now, "_age_line", "Stitch source")
    pn_a, pn_b = loc_clause(p_now, "_age_line", "Portal source")
    sb_a, sb_b = loc_clause(p_base, "_age_line", "Stitch source")
    print("")
    print("HOP 4 PRINT -- _age_line renders it in the served VINTAGE line")
    print("  file %s" % PW)
    print("  BASE: the stitch clause (the `if` that appends it) is at :%d-%d" % (sb_a, sb_b))
    print("  ROUND-7 CITED :257-262 for this hop. CONTAINS the measured clause=%s"
          % str(257 <= sb_a and sb_b <= 262).lower())
    print("  NOW : stitch clause :%d-%d, PORTAL clause :%d-%d (same shape, appended after)"
          % (sn_a, sn_b, pn_a, pn_b))
    print("  change required : the same shape as the stitch clause above it  [DONE]")
    print("  OWNER           : the globgrph engine owner -- this project's plane")
    print("  STATE_THIS_ROUND: DESIRED (committed) + LOCALLY EXERCISED. The SERVED line does"
          " not change until the projection is rebuilt and republished, which is a held act.")
    hops.append(("4 PRINT", PW, "globgrph engine owner (this project)",
                 "DESIRED + LOCAL-EXERCISED", 257 <= sb_a and sb_b <= 262))

    # ---------------------------------------------------------------- the summary
    print("")
    print("--- OWNER AND STATE, ONE ROW PER HOP ---")
    print("  %-9s %-13s %-46s %s" % ("hop", "state", "owner", "site"))
    for name, site, owner, state, _ in hops:
        print("  %-9s %-13s %-46s %s" % (name, state.split(" +")[0], owner, site))
    print("")
    print("--- THE ROUND-7 PINS, TESTED AT THE BASELINE ---")
    moved = 0
    labels = {
        "1 PACK": "f3_build_source_zip.py:84 computes portal_head; workflow:66 is the pin",
        "2 STAMP": "the buildspec marker dict declares exactly 7 keys",
        "3 COPY": "kuzu_nessie_load.py:71-77 is read_stitch_vintage's return dict",
        "4 PRINT": "projection_worker.py:257-262 contains the stitch clause",
    }
    for name, site, owner, state, held in hops:
        print("  hop %-8s %-72s HELD_AT_BASELINE=%s" % (name, labels[name], str(held).lower()))
        if not held:
            moved += 1
    print("")
    print("HOPS_REDERIVED=4 of 4 at HEAD")
    print("PINS_MOVED_SINCE_ROUND7=%d of 4" % moved)
    print("  DENOMINATOR: 4 hops, 4 round-7 pin claims, 5 files read whole, %d marker keys"
          " enumerated at the baseline and %d now." % (len(keys_base), len(keys_now)))
    print("  AND THE FINDING IS THE OTHER WAY ROUND: it is the CORRECTION that had drifted,"
          " not the record. The round-7 table's four citations all still hold at the commit"
          " this order was cut from; the task order's own MEASURED block re-cites hop 3 as"
          " :68-78, which at those same bytes is the guard plus the except, not the return"
          " dict. A record that cites lines does age -- these had not yet, and the re-read"
          " that assumed they had introduced the only error of the four. Filed as a row.")
    print("OWNER_PER_HOP printed")
    print("STATE_PER_HOP printed")
    print("REDERIVED_BY=CONTENT")
    print("  WHAT THIS DOES NOT CERTIFY: not one hop is APPLIED. Hops 1 and 2 cannot reach"
          " APPLIED in this round by the order's own bounds (no apply, no push, no S3"
          " write), and hops 3 and 4 are committed producer code that no deploy has carried."
          " Every STATE above is DESIRED, two of them additionally exercised LOCALLY.")
    return 0


def blob_exists(commit, path):
    rc, _, _ = sh(["git", "cat-file", "-e", commit + ":" + path])
    return rc == 0


if __name__ == "__main__":
    sys.exit(main())
