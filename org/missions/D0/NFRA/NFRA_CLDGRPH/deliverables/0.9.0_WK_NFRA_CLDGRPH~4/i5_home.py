#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-I-5 (CG-s-45) -- I5-AC2.

THE HOME, DECIDED ON AC1'S EVIDENCE.

AC1 measured, and this file decides from those numbers rather than from which
file looks more like production. THE RUN COUNTS CARRY A VINTAGE because the
population is still growing -- a push to CLOUD landed between two runs of this
cell's own harness and took the total from 854 to 855, the failure count from
831 to 832, and the success count nowhere:

  * as of 2026-09-10T18:2xZ, the committed workflow has run 854 times and
    succeeded 8, all 8 on the day it landed and all 8 BEFORE the step that
    packs portal/src existed;
  * since that step landed: 846 runs, 0 successes, dying every time on a repo
    secret that was never provisioned;
  * all five served zips came from the hand route, each with a NEVER-2 ledger
    entry naming its owner and order.

The counts below are RE-MEASURED at run time, so the file never argues from a
number it did not just read; the figures above are the vintage the surrounding
record was written against.

The premise this cell inherited was "an unrun route is not a route". The route
is not unrun. It is a route whose TRIGGER HALF WORKS PERFECTLY and whose BODY
has never once completed -- and that distinction is what decides the home,
because a trigger is the one thing the hand route can never acquire without
becoming the workflow it would be replacing.

READS ONLY. Nothing is pushed, triggered or applied.
"""
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _find_repo(start):
    d = start
    for _ in range(12):
        if os.path.isdir(os.path.join(d, "org")) and os.path.isdir(os.path.join(d, ".tools")):
            return d
        nxt = os.path.dirname(d)
        if nxt == d:
            break
        d = nxt
    raise SystemExit("BLOCKED: no ancestor of %s carries both org/ and .tools/" % start)


REPO = _find_repo(HERE)
WF = os.path.join(REPO, ".github", "workflows", "stitch-source-push.yml")
WF_REL = ".github/workflows/stitch-source-push.yml"
PRODUCER = ("org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/"
            "0.9.0_WK_NFRA_CLDGRPH~2/f3_build_source_zip.py")
GH_REPO = "Opal-Capital/ajb_workspace"
OLD_PIN = "b96562720505fa143aad7cc5dd75115e6c609912"


def sh(args, timeout=45):
    try:
        # encoding is EXPLICIT: text=True alone decodes with the locale codec, which is
        # cp1252 on this box, and `gh run view` returned a byte no cp1252 mapping covers.
        # The failure lands in a subprocess READER THREAD, so the traceback prints into
        # the capture while the script carries on and exits 0 -- a corrupted capture that
        # looks like a clean run. Measured on this file's own first capture.
        r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout, cwd=REPO)
        return r.returncode, r.stdout.replace("\r", ""), r.stderr.replace("\r", "")
    except Exception as exc:  # noqa: BLE001
        return 900, "", "EXC: %s" % exc


def gh_count(query):
    g = shutil.which("gh")
    if not g:
        return None
    url = "/repos/%s/actions/workflows/stitch-source-push.yml/runs?%s" % (GH_REPO, query)
    rc, out, _ = sh([g, "api", url, "-q", ".total_count"], timeout=40)
    if rc != 0:
        return None
    try:
        return int(out.strip())
    except ValueError:
        return None


def bar(t):
    print("=" * 78)
    print(t)
    print("=" * 78)


def _bash():
    """Resolve a REAL Git Bash.

    A bare `bash` on this box can resolve to the 504-byte WSL stub, which would
    make every arm below fail for a reason that has nothing to do with the code
    under test -- a DEAD arm reading as a WRONG arm. Size is the discriminator.
    """
    for c in (r"C:\Program Files\Git\bin\bash.exe",
              r"C:\Program Files\Git\usr\bin\bash.exe"):
        if os.path.isfile(c) and os.path.getsize(c) > 100000:
            return c
    w = shutil.which("bash")
    if w and os.path.getsize(w) > 100000:
        return w
    return None


def exercise_resolver(wf_txt, gitlink):
    """Run the workflow's OWN resolver block, extracted from the committed file."""
    try:
        import yaml
    except ImportError:
        print("    BLIND: PyYAML absent, cannot extract the block from the workflow.")
        return
    doc = yaml.safe_load(wf_txt)
    steps = doc["jobs"]["stitch-source"]["steps"]
    blocks = [s.get("run", "") for s in steps if s.get("id") == "portalpin"]
    if len(blocks) != 1:
        print("    BLIND: expected exactly 1 step with id portalpin, found %d." % len(blocks))
        return
    block = blocks[0]
    bash = _bash()
    if not bash:
        print("    BLIND: no real Git Bash resolvable (a WSL stub is not an instrument).")
        return
    print("    bash: %s (%d bytes -- not the WSL stub)" % (bash, os.path.getsize(bash)))
    import tempfile
    arms = [("POSITIVE  the committed block, verbatim", block, 0),
            ("NEGATIVE  a path that is a TREE, not a gitlink (.tools)",
             block.replace(" portal ", " .tools "), 1),
            ("NEGATIVE  a path absent from the tree",
             block.replace(" portal ", " i5_no_such_path "), 1)]
    for label, src, want_rc in arms:
        fd, outp = tempfile.mkstemp(prefix="i5_gh_output_")
        os.close(fd)
        env = dict(os.environ)
        env["GITHUB_OUTPUT"] = outp
        try:
            r = subprocess.run([bash, "-c", src], capture_output=True, text=True,
                               timeout=40, cwd=REPO, env=env)
            rc, out = r.returncode, (r.stdout + r.stderr).replace("\r", "").strip()
        except Exception as exc:  # noqa: BLE001
            rc, out = 900, "EXC %s" % exc
        wrote = open(outp, "r", encoding="utf-8", errors="replace").read().strip()
        os.unlink(outp)
        verdict = "AS EXPECTED" if rc == want_rc else "UNEXPECTED (wanted rc=%d)" % want_rc
        print("")
        print("    %s" % label)
        print("      rc=%d  %s" % (rc, verdict))
        for ln in out.splitlines():
            print("      | %s" % ln[:96])
        print("      GITHUB_OUTPUT written: %s" % (wrote if wrote else "(nothing -- no ref handed on)"))
    print("")
    print("    THE NEGATIVES ARE THE ARMS THAT MATTER. They prove the step REFUSES rather")
    print("    than handing actions/checkout an empty ref, which is the silent-default-")
    print("    branch path. The positive alone would pass just as happily if the guard")
    print("    were absent, so it bounds nothing on its own.")
    print("    superproject gitlink at HEAD, read independently: %s" % gitlink)


def main():
    bar("I5-AC2 -- THE HOME, DECIDED ON THE EVIDENCE (CG-s-45, TO-CG-I-5)")
    print("worker : 0.9.0_WK_NFRA_CLDGRPH~4")
    print("")
    print("CUT DISCIPLINE, for every number below:")
    print("  COVERAGE   : the workflow's entire run population (API total_count, not a")
    print("               page) and the workflow file as it stands in THIS worktree.")
    print("  GRAIN      : one run for the counts; one STEP for the failure point; one")
    print("               YAML key for the pin.")
    print("  ENVIRONMENT: live GitHub API + this checkout. No stored baseline is used;")
    print("               where a number is carried from AC1 it is re-measured here.")
    tree = sh(["git", "rev-parse", "--show-toplevel"])[1].strip()
    branch = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"])[1].strip()
    print("  TREE_READ  = %s   branch %s" % (tree, branch))
    print("")

    total = gh_count("per_page=1")
    succ = gh_count("status=success&per_page=1")
    post = gh_count("created=%3E2026-07-07T14%3A09%3A20Z&per_page=1")
    post_succ = gh_count("status=success&created=%3E2026-07-07T14%3A09%3A20Z&per_page=1")
    live = None not in (total, succ, post, post_succ)

    wf_txt = open(WF, "r", encoding="utf-8").read()
    m = re.search(r"^\s+ref:\s*(\S.*)$", wf_txt, re.M)
    ref_val = m.group(1).strip() if m else "(no ref: key found)"
    resolver_present = "id: portalpin" in wf_txt
    literal_pin_as_ref = ref_val.startswith(OLD_PIN[:8])
    rc, gl, _ = sh(["git", "ls-tree", "HEAD", "portal"])
    gitlink = gl.split()[2] if len(gl.split()) >= 3 else "UNRESOLVED"

    bar("STEP 1 -- WHICH ROUTE IS REAL, and the question has TWO answers")
    print("  BY OUTCOME the hand route is the only real one. It is the only route that")
    print("  has ever placed a CORRECT source zip in S3 -- 5 of 5 served zips, and the")
    print("  committed route's own 8 successes packed ZERO portal/src files, so its")
    print("  correct-publish count over its whole life is 0 of %s." % (total if live else "854 [AC1]"))
    print("")
    print("  BY TRIGGER the committed route is the only real one, and this is the half")
    print("  that decides a HOME. Its trigger fired %s times on exactly the right paths"
          % (total if live else "854 [AC1]"))
    print("  with the right branch pin, the right OIDC role, a concurrency group and a")
    print("  PR exclusion. NONE of that is broken. What is broken is one repo secret,")
    print("  three steps in.")
    print("")
    print("  THE HAND ROUTE HAS NO TRIGGER AT ALL. It ran five times because a task")
    print("  order told a worker to run it five times. That is not a cadence, it is five")
    print("  instructions. And it cannot acquire one: the only mechanism in this estate")
    print("  that could fire a repo-subset packer on a repo change IS a GitHub Action,")
    print("  because the nightly Fargate derive-runner is repo-less -- which is the")
    print("  stated reason LEG-1 exists at all (%s, header)." % WF_REL)
    print("")
    print("  So the two answers do not conflict; they are answers to different")
    print("  questions. 'Which route produced the artifact' is the hand route. 'Which")
    print("  route can OWN the artifact' is the workflow, and a home is an ownership")
    print("  question, not a history one.")
    print("")

    bar("STEP 2 -- WHAT WOULD HAVE TO BE TRUE FOR THE HAND ROUTE TO BE THE HOME")
    print("  Three things, and the third is disqualifying:")
    print("   1. a production location chosen for the script. Out of this worker's")
    print("      <paths>, and already assigned: CG-s-38 item 1 names 1.0.0_SA_CTO to")
    print("      decide which plane owns a repo-subset packer.")
    print("   2. an owner to run it. CG-s-38 item 1 names 0.7.0_AE_CloudOps.")
    print("   3. A TRIGGER. There is none, and building one means building a")
    print("      push-triggered CI job that zips the repo subset and puts it on the same")
    print("      S3 key -- which is the workflow, rebuilt beside the workflow. That is a")
    print("      SHADOW PIPELINE and a DUPLICATE OUTPUT PATH under CLAUDE.md s.5, on")
    print("      which Andrew holds a complete veto. Absent that, the hand route stays")
    print("      human-triggered forever, and 'a production input refreshed only when")
    print("      somebody remembers' is the finding this cell exists to close, not a")
    print("      resolution of it.")
    print("")
    print("  AND THE STANDING COST OF CHOOSING IT: two live producers of one served key,")
    print("  with no ordering between them. The moment the secret is provisioned the")
    print("  workflow starts publishing too, and a hand push and a pushed-triggered run")
    print("  can interleave on the same object with no lock and no versioning on the")
    print("  bucket to reconstruct which won.")
    print("")

    bar("STEP 3 -- THE DECISION")
    print("HOME_DECIDED=WORKFLOW")
    print("")
    print("ON_EVIDENCE printed:")
    if live:
        print("  [measured, this run] runs total                       = %d" % total)
        print("  [measured, this run] successes ever                   = %d" % succ)
        print("  [measured, this run] runs since the portal step landed= %d" % post)
        print("  [measured, this run] successes since it landed        = %d" % post_succ)
    else:
        print("  [BLIND this run, carried from AC1] 854 runs / 8 successes / 846 since")
        print("  the portal step / 0 successes since. The live API did not answer here;")
        print("  the numbers are AC1's and are labelled as carried, not re-measured.")
    print("  [measured, AC1]      served zips produced by the workflow = 0 of 5")
    print("  [measured, AC1]      served zips produced by hand         = 5 of 5")
    print("  [measured, AC1]      correct publishes by the workflow ever = 0")
    print("  [measured, AC1]      failing step = 3, 'Checkout portal', on the missing")
    print("                       secrets.PORTAL_REPO_PAT; steps 4 and 5 SKIPPED")
    print("  [held]               the home belongs where the TRIGGER is, because a")
    print("                       producer without a trigger is a script, and this cell")
    print("                       is about a producer having no production existence.")
    print("  [held]               the workflow's failure is ONE PROVISIONING ACT wide.")
    print("                       Everything else about it -- trigger, paths, branch")
    print("                       pin, OIDC role, recipe, S3 target -- is already right")
    print("                       and already committed.")
    print("  [inferred]           therefore f3_build_source_zip.py does not need a")
    print("                       production home; it needs a DATED interim owner and")
    print("                       then retirement by disuse. Placing it permanently")
    print("                       would ratify the second producer.")
    print("")
    print("  AND THE PART OF THE DECISION THAT IS NOT MINE, said out loud: I am deciding")
    print("  WHERE THE HOME IS, on evidence. I am not deciding that the workflow SHALL")
    print("  run -- provisioning secrets.PORTAL_REPO_PAT is a GitHub repo secret, which")
    print("  is outside every agent lane here and is 0.0.0_AB_MSTR's act with Andrew's")
    print("  word. If that act is refused, the decision above is void and the estate is")
    print("  back to HAND_ROUTE with all three costs in step 2 payable. I am not")
    print("  proposing a monitor, an alarm or a freshness check on any of this: the")
    print("  standing moratorium forbids it and a monitor on an unsettled route would")
    print("  measure the wrong thing precisely.")
    print("")

    bar("STEP 4 -- THE PIN")
    print("PIN_DISPOSITION=%s" % ("RESOLVES" if (resolver_present and not literal_pin_as_ref) else "LITERAL-WITH-OWNER"))
    print("")
    print("  MEASURED IN THIS WORKTREE, this run:")
    print("    %s ref: value        = %s" % (WF_REL, ref_val))
    print("    resolver step (id: portalpin) present   = %s" % resolver_present)
    print("    the old literal still used as the ref   = %s" % literal_pin_as_ref)
    print("    superproject gitlink at HEAD            = %s" % gitlink)
    print("")
    print("  WHY IT WAS FIXED HERE RATHER THAN FILED. Round 8's CG-s-38 held this file in")
    print("  its grant and deliberately did NOT touch the pin, on the reasoning that an")
    print("  unexercised behaviour change to a production route is what this estate keeps")
    print("  paying for. That reasoning was right on the evidence it had. AC1 changed the")
    print("  evidence: the step the pin lives in has NEVER SUCCEEDED, not once in 846")
    print("  attempts, so there is no working behaviour to break -- and the pin has")
    print("  therefore never been exercised even as a literal.")
    print("")
    print("  AND THE PIN WAS NOT WRONG WHEN IT WAS WRITTEN, which is the part that makes")
    print("  it a defect rather than a mistake. `git ls-tree 4074fdf5ac portal` reads")
    print("  %s -- exactly the literal -- and 4074fdf5ac is the commit" % OLD_PIN)
    print("  that added the step. It was a correct snapshot with no update step, and the")
    print("  comment above it went on asserting a property it had stopped having.")
    print("")
    print("  THE FAILURE MODE THE FIX IS SHAPED AROUND, because a naive fix here is worse")
    print("  than the literal: actions/checkout treats an EMPTY ref as the DEFAULT BRANCH.")
    print("  A resolver that degraded quietly would publish a zip built from an unrelated")
    print("  portal head, and every downstream vintage record would faithfully carry that")
    print("  wrong sha. The step therefore tests for 40-hex and exits 1 otherwise.")
    print("")
    print("  STATE, and it is not EXERCISED AT THE WORKFLOW GRAIN: that change is")
    print("  DESIRED. No run of the altered workflow can be observed until the PAT")
    print("  exists, and triggering one is inside this round's egress hold anyway.")
    print("")
    print("  WHAT IS EXERCISED, NOW, IN THIS RUN -- and the block executed below is")
    print("  EXTRACTED FROM THE COMMITTED WORKFLOW, not a transcription of it. A harness")
    print("  copied from the implementation scores the implementation's blind spot as a")
    print("  pass; this one cannot diverge from the file because it IS the file. The only")
    print("  substitutions are disclosed: GITHUB_OUTPUT is pointed at a temp file, and")
    print("  each NEGATIVE arm replaces the single token `portal` with the path being")
    print("  tested.")
    exercise_resolver(wf_txt, gitlink)
    print("")

    bar("STEP 5 -- THE ROAD NOT TAKEN")
    print("ALTERNATIVE_COST printed:")
    print("")
    print("  IF HOME_DECIDED HAD BEEN HAND_ROUTE:")
    print("    * one CTO ruling to choose the owning plane, plus a file move (cheap);")
    print("    * one AE owner to run it (cheap);")
    print("    * A TRIGGER THAT DOES NOT EXIST AND CANNOT BE BUILT WITHOUT DUPLICATING")
    print("      THE WORKFLOW -- a shadow pipeline and a duplicate output path, on which")
    print("      Andrew holds a complete veto. This is the disqualifying cost, and it is")
    print("      structural rather than a matter of effort;")
    print("    * permanently two writers of one served key, unordered, on a bucket with")
    print("      versioning OFF (AC1 instrument C), so a collision is not reconstructable")
    print("      afterwards;")
    print("    * and the pin question would not go away -- it would move, because the")
    print("      hand script takes its portal checkout as a command-line argument, which")
    print("      is the same unupdated literal with a human holding it.")
    print("")
    print("  IF PIN_DISPOSITION HAD BEEN LITERAL-WITH-OWNER:")
    print("    * zero cost today, because the step cannot run either way;")
    print("    * and the entire cost on the day the PAT lands: the first successful run")
    print("      in 65 days would pack a portal 65 days stale and publish it, and every")
    print("      vintage record downstream would report that sha correctly. The defect")
    print("      would be INVISIBLE precisely because the four-hop vintage feed CG-s-38")
    print("      built works. A correct pipeline reporting a wrong input is the worst")
    print("      shape available, and it was one line away.")
    print("")
    print("  IF I HAD FILED THE HOME DECISION INSTEAD OF DECIDING IT (HOME_DECIDED=FILED):")
    print("    * it costs the estate another round to learn what AC1 already measured,")
    print("      and the cell's own question -- which route is real -- would come back")
    print("      unanswered with the evidence sitting in the record. The FILING that IS")
    print("      warranted is narrower and is I5-AC3's: the interim owner of a script")
    print("      that is still production until the secret lands.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
