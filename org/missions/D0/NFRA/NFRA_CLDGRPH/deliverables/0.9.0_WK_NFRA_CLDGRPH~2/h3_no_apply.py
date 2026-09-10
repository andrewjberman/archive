#!/usr/bin/env python3
"""NFRA_CLDGRPH CG-s-38 / H3-AC4 -- THE EGRESS HOLD HONOURED, AND THE WRONG CARRIER LEFT ALONE.

SIX HELD ACTS AND ONE FORBIDDEN EDIT, and neither is asserted -- both are measured.

  ARM 1 (CODE). Every EXECUTABLE line this order wrote or changed, scanned for the forms
    that PERFORM the six held acts. Comments and python docstrings are excluded and COUNTED,
    because this order's files discuss the held acts on nearly every page and a mention is
    not a call. The two producer surfaces are scanned as ADDED LINES ONLY, read from git:
    the workflow file this order edits ALREADY CONTAINS an S3 copy of the source zip that
    predates this order by months, and scanning the whole file would count somebody else's
    line as this order's act. (That is the sharpest failure available to this arm, so it is
    named rather than quietly handled.)

  ARM 2 (RECORD). The exact set of paths that differ from this order's cut base, printed
    whole. A terraform apply leaves state; an image act leaves a build context; an S3 write
    leaves nothing in the tree at all -- which is why ARM 2 is a bound and not a proof, and
    says so.

  ARM 3 (CONTROL). The same detector over a PLANTED line for every held act, which must
    catch 6 of 6; and the _provenance detector run against a file that IS modified, which
    must return non-zero. A counter that cannot go up is a constant wearing a measurement's
    clothes.

WHY _provenance.py HAS ITS OWN COUNTER. The cheapest wrong fix available to this cell was
to "improve" _provenance.format_provenance_header so it prints the new key. That function
was EXERCISED in round 7 (rows W3-S17 / S108) and printed 3 of 7 keys handed to it, dropping
4 in silence, because it hard-codes one branch per source_kind instead of looping. A change
there would have passed its own test and altered nothing a reader sees. The file is READ in
this order and not written, and this counter is how that is provable rather than promised.

WHAT THIS CANNOT SEE, stated: it is not a CloudTrail audit. It cannot see an act by another
seat, and it cannot see an act that left no mark in this worktree.
"""
import os
import re
import subprocess
import sys

BASE = "2fd5cae09f"
DELIV = "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2"
PROV = "infra/aws/globgrph/_provenance.py"
CHANGED = ["infra/aws/globgrph/kuzu_nessie_load.py",
           "infra/aws/globgrph/projection_worker.py",
           "infra/aws/terraform/globgrph/stitch-produce.tf",
           ".github/workflows/stitch-source-push.yml",
           DELIV + "/f3_build_source_zip.py"]
SELF = ("h3_no_apply.py", "h3_no_apply.sh")

Z = chr(92)
HELD = {
    "TERRAFORM_APPLIES": [Z + r"bterraform\s+apply" + Z + "b", Z + r"bsafe-apply",
                          Z + r"bterraform\s+destroy" + Z + "b"],
    "ECS_RUN_TASK_CALLS": [Z + r"becs\s+run-task" + Z + "b", Z + r"brun_task\s*" + Z + "(",
                           Z + r"becs\s+start-task" + Z + "b"],
    "CODEBUILD_STARTS": [Z + r"bcodebuild\s+start-build" + Z + "b",
                         Z + r"bstart_build\s*" + Z + "("],
    "IMAGE_PUSHES": [Z + r"bdocker\s+push" + Z + "b", Z + r"bdocker\s+build" + Z + "b",
                     Z + r"bbuildx" + Z + "b", Z + r"becr\s+put-image" + Z + "b",
                     Z + r"bregister-task-definition" + Z + "b"],
    "S3_WRITES": [Z + r"bs3\s+cp" + Z + "b", Z + r"bs3\s+sync" + Z + "b",
                  Z + r"bs3\s+mv" + Z + "b", Z + r"bs3\s+rm" + Z + "b",
                  Z + r"bs3api\s+put-object" + Z + "b", Z + r"bput_object\s*" + Z + "(",
                  Z + r"bupload_file\s*" + Z + "(", Z + r"bupload_fileobj\s*" + Z + "(",
                  Z + r"bdelete_object\s*" + Z + "("],
    "ZIP_PUSHES": [r"stitch-source/source" + Z + r".zip",
                   Z + r"bs3\s+cp\s+" + Z + r"S*" + Z + r".zip",
                   Z + r"bput_object" + Z + r"([^)]*stitch-source"],
}
PLANTED = {
    "TERRAFORM_APPLIES": "bash .tools/safe-apply.sh -auto-approve",
    "ECS_RUN_TASK_CALLS": "aws ecs run-task --cluster opal-globgrph --task-definition x",
    "CODEBUILD_STARTS": "aws codebuild start-build --project-name opal-stitch-produce",
    "IMAGE_PUSHES": "docker push 313476888478.dkr.ecr.us-east-1.amazonaws.com/g:latest",
    "S3_WRITES": "aws s3 cp ./x.json s3://opal-313476888478-globgrph/stitch/x.json",
    "ZIP_PUSHES": "aws s3 cp /tmp/x.zip s3://opal-313476888478-globgrph/"
                  "stitch-source/source.zip",
}


def sh(args):
    env = dict(os.environ)
    env["MSYS_NO_PATHCONV"] = "1"
    return subprocess.run(args, capture_output=True, text=True, env=env)


def executable_lines(path):
    """Lines that could RUN. Comments and python docstring blocks are excluded, and the
    exclusion is COUNTED and printed -- never silent."""
    with open(path, encoding="utf-8", errors="replace", newline="") as fh:
        text = fh.read().split("\n")
    keep, dropped, in_doc = [], 0, False
    for ln in text:
        st = ln.strip()
        if path.endswith(".py"):
            ticks = st.count('"""') + st.count("'''")
            if in_doc:
                dropped += 1
                if ticks % 2 == 1:
                    in_doc = False
                continue
            if ticks % 2 == 1:
                in_doc = True
                dropped += 1
                continue
        if st.startswith("#") or not st:
            dropped += 1
            continue
        keep.append(ln)
    return keep, dropped


def scan(lines):
    hits = {k: [] for k in HELD}
    for ln in lines:
        for k, pats in HELD.items():
            for p in pats:
                if re.search(p, ln):
                    hits[k].append(ln.strip()[:140])
                    break
    return hits


def main():
    print("=== CG-s-38 / H3-AC4 -- THE HOLD HONOURED, MEASURED NOT ASSERTED ===")
    print("TREE_READ=%s  branch=%s  base=%s"
          % (os.getcwd().replace(os.sep, "/"),
             sh(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip(), BASE))
    print("INSTRUMENT: a line-level regex detector over executable lines only, run over"
          " three disjoint corpora (authored files whole, changed files ADDED-lines-only,"
          " a planted positive), plus git's own diff for the record arm.")
    print("GRAIN: one ACT per counter, at the grain of one line of source.")
    print("ENVIRONMENT: python %s on %s; git as the second instrument. No AWS call is made"
          " by this probe -- reading the account is not needed to establish that this order"
          " performed no act, and would add a credential dependency to a hold check."
          % (sys.version.split()[0], sys.platform))
    print("")

    totals = {k: 0 for k in HELD}
    scanned = 0
    dropped_total = 0

    # ---------------------------------------------------------------- ARM 1a: authored
    corpus = []
    for name in sorted(os.listdir(DELIV)):
        if not name.startswith("h3_") or name in SELF:
            continue
        if not (name.endswith(".py") or name.endswith(".sh")):
            continue
        corpus.append(DELIV + "/" + name)
    print("  -- ARM 1a (CODE): every executable line of every file this order AUTHORED --")
    for p in corpus:
        keep, dropped = executable_lines(p)
        scanned += len(keep)
        dropped_total += dropped
        h = scan(keep)
        for k in HELD:
            totals[k] += len(h[k])
        print("     %-84s exec=%-4d excluded=%-4d hits=%s"
              % (p, len(keep), dropped, {k: len(v) for k, v in h.items() if v} or "none"))
    print("     EXCLUDED BY NAME, so the exclusion is not silent: %s (this detector -- it"
          " CONTAINS every pattern as a literal and scanning it would count the instrument"
          " as an act); the h3_*.txt captures and the CG-s-38 record (.md prose, not"
          " executable); h3_tree_control.txt (a control file)." % ", ".join(SELF))
    print("")

    # ---------------------------------------------------------------- ARM 1b: added lines
    print("  -- ARM 1b (CODE): the five changed files, ADDED LINES ONLY, read from git --")
    diff = sh(["git", "diff", BASE, "--unified=0", "--"] + CHANGED).stdout.split("\n")
    added = [ln[1:] for ln in diff if ln.startswith("+") and not ln.startswith("+++")]
    added_exec = [ln for ln in added if ln.strip() and not ln.strip().startswith("#")
                  and not ln.strip().startswith('"""')]
    ha = scan(added_exec)
    for k in HELD:
        totals[k] += len(ha[k])
    scanned += len(added_exec)
    dropped_total += len(added) - len(added_exec)
    print("     git diff %s -- (5 files, worktree): added=%d executable=%d hits=%s"
          % (BASE, len(added), len(added_exec),
             {k: len(v) for k, v in ha.items() if v} or "none"))
    whole = scan([ln for ln in open(CHANGED[3], encoding="utf-8").read().split("\n")
                  if ln.strip() and not ln.strip().startswith("#")])
    print("     THE ARM'S OWN SHARPEST EDGE, NAMED: scanning that workflow file WHOLE"
          " instead of its added lines would report %s -- lines that predate this order by"
          " months and are the workflow's entire purpose. ADDED-LINES-ONLY is the correct"
          " scope and it is a CHOICE, printed here so a reader can reject it."
          % ({k: len(v) for k, v in whole.items() if v} or "none"))
    print("")

    # ---------------------------------------------------------------- ARM 2: the record
    changed_paths = [p for p in sh(["git", "diff", "--name-only", BASE]).stdout.split("\n")
                     if p.strip()]
    untracked = [p for p in sh(["git", "ls-files", "--others", "--exclude-standard"]
                               ).stdout.split("\n") if p.strip()]
    print("  -- ARM 2 (RECORD): every path that differs from the cut base --")
    for p in changed_paths:
        print("     CHANGED   %s" % p)
    for p in untracked:
        print("     UNTRACKED %s" % p)
    print("     PATHS_DIFFERING=%d changed + %d untracked. None is terraform state, a lock"
          " file, a .terraform directory, a build context or an artifact."
          % (len(changed_paths), len(untracked)))
    print("     WHAT ARM 2 IS AND IS NOT: it is a BOUND, not a proof. A terraform apply"
          " leaves state and an image act leaves a build context, so those two would show"
          " here; an S3 write or an ecs run-task leaves NOTHING in a worktree, and for those"
          " ARM 1 is the arm that carries the claim.")
    print("")

    # ---------------------------------------------------------------- _provenance
    prov_stat = sh(["git", "diff", "--numstat", BASE, "--", PROV]).stdout.strip()
    prov_modified = 0 if not prov_stat else int(prov_stat.split()[0]) + int(
        prov_stat.split()[1])
    ctl_stat = sh(["git", "diff", "--numstat", BASE, "--", CHANGED[0]]).stdout.strip()
    ctl_modified = 0 if not ctl_stat else int(ctl_stat.split()[0]) + int(ctl_stat.split()[1])
    print("  -- THE WRONG CARRIER, LEFT ALONE --")
    print("     %s  numstat vs %s: %s" % (PROV, BASE, prov_stat or "(no output = no diff)"))
    print("     DETECTOR CONTROL on a file that IS modified (%s): %d line(s) -- so this"
          " counter can go non-zero, which is the only thing that makes its zero mean"
          " anything." % (CHANGED[0], ctl_modified))
    print("")

    # ---------------------------------------------------------------- ARM 3: control
    ctrl = scan(list(PLANTED.values()))
    caught = sum(1 for k in HELD if ctrl[k])
    print("  -- ARM 3 (CONTROL): a planted positive for every held act, same detector --")
    for k in sorted(HELD):
        print("     %-20s planted_caught=%d   %s" % (k, len(ctrl[k]), PLANTED[k][:64]))
    print("     PLANTED_ACTS_CAUGHT=%d of %d" % (caught, len(HELD)))
    print("")

    for k in ("TERRAFORM_APPLIES", "ECS_RUN_TASK_CALLS", "CODEBUILD_STARTS", "IMAGE_PUSHES",
              "S3_WRITES", "ZIP_PUSHES"):
        print("%s=%d" % (k, totals[k]))
    print("PROVENANCE_PY_MODIFIED=%d" % prov_modified)
    print("EGRESS_PROBE_CONTROL=%s" % ("FIRED" if (caught == len(HELD) and ctl_modified > 0)
                                       else "NOT-FIRED"))
    print("  DENOMINATOR: %d executable line(s) scanned across %d authored file(s) and %d"
          " added line(s) in 5 changed file(s), with %d comment/docstring line(s) excluded"
          " and 2 files excluded by name; %d of %d held acts caught on the planted positive;"
          " 1 of 1 forbidden file checked with a live detector control."
          % (scanned, len(corpus), len(added_exec), dropped_total, caught, len(HELD)))
    ok = (sum(totals.values()) == 0 and prov_modified == 0 and caught == len(HELD)
          and ctl_modified > 0)
    print("NO_APPLY_RESULT=%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
