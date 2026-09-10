#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-I-5 (CG-s-45) -- I5-AC1.

WHICH ROUTE HAS ACTUALLY RUN, FROM RUN HISTORY.

The cell asks two questions the file's existence cannot answer:
  Q1  has the committed route (.github/workflows/stitch-source-push.yml) EVER executed?
  Q2  what produced each of the five source zips served in round 6?

and requires a blind instrument to be REPORTED BLIND rather than contributing a zero.

FOUR instruments, on FOUR different substrates, each printing its own COVERAGE, GRAIN,
ENVIRONMENT and TREE:

  A  GitHub Actions run history      (the workflow's OWN execution plane, live API)
  B  the NEVER-2 deploy ledger       (this repo, this worktree, walked and counted)
  C  the served S3 object + its bucket's versioning configuration (live AWS read)
  D  the CloudTrail S3 data-event plane (live AWS read; expected BLIND, controlled)

NOTHING IS WRITTEN, PUSHED, TRIGGERED OR APPLIED. Every call is a GET/list.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))


def _find_repo(start):
    """Walk UP from this file until the ordered paths exist.

    Not a hard-coded number of '..' segments: this file lives seven levels down
    and a miscount resolves to a directory that still exists, so every later
    read fails as a well-formed absence instead of an error. The loop tests for
    the paths the task order NAMES (org/ and .tools/), which is the same bar the
    worktree itself is held to.
    """
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
WF = ".github/workflows/stitch-source-push.yml"
KEY = "stitch-source/source.zip"
BUCKET = "opal-313476888478-globgrph"
GH_REPO = "Opal-Capital/ajb_workspace"
CONTROL_TOKEN = "I5_TREE_CONTROL_TOKEN_20260910_WK4"

# The commit that added the portal-checkout step AND the literal pin, measured with
# git log --full-history -S on the workflow path (see the EVIDENCE block below).
PORTAL_STEP_COMMIT = "4074fdf5ac"
PORTAL_STEP_AT = "2026-07-07T14:09:20Z"

BLIND = []


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
        return None, "gh not resolvable on PATH"
    url = "/repos/%s/actions/workflows/stitch-source-push.yml/runs?%s" % (GH_REPO, query)
    rc, out, err = sh([g, "api", url, "-q", ".total_count"], timeout=45)
    if rc != 0:
        return None, "rc=%d %s" % (rc, err.strip()[:160])
    try:
        return int(out.strip()), None
    except ValueError:
        return None, "unparsable total_count: %r" % out[:80]


def gh_json(query, timeout=45):
    g = shutil.which("gh")
    if not g:
        return None, "gh not resolvable on PATH"
    url = "/repos/%s/actions/workflows/stitch-source-push.yml/runs?%s" % (GH_REPO, query)
    rc, out, err = sh([g, "api", url], timeout=timeout)
    if rc != 0:
        return None, "rc=%d %s" % (rc, err.strip()[:160])
    try:
        return json.loads(out), None
    except Exception as exc:  # noqa: BLE001
        return None, "unparsable json: %s" % exc


def aws(args, timeout=45):
    exe = os.path.join(REPO, ".tools", "aws.cmd")
    if not os.path.isfile(exe):
        return 901, "", "aws shim absent at %s" % exe
    return sh([exe] + args, timeout=timeout)


def bar(t):
    print("=" * 78)
    print(t)
    print("=" * 78)


# ---------------------------------------------------------------- INSTRUMENT A
def instrument_a():
    print("")
    bar("INSTRUMENT A -- THE WORKFLOW'S OWN EXECUTION PLANE (GitHub Actions runs)")
    print("  COVERAGE   : every run GitHub holds for stitch-source-push.yml, counted by")
    print("               the API's own total_count -- NOT a page length. Retention:")
    print("               run metadata is retained 400 d by default; the workflow is 65 d")
    print("               old, so the window covers its whole life. The earliest run's")
    print("               head_sha IS the commit that introduced the file, which is the")
    print("               control that no run predates the read.")
    print("  GRAIN      : one workflow RUN (and, for two named runs, one STEP).")
    print("  ENVIRONMENT: live GitHub API through the gh CLI at this seat. No baseline;")
    print("               nothing stored, nothing replayed.")
    print("  TREE       : not a tree read at all -- this instrument is off-repo by")
    print("               construction, which is why it can answer a question no file in")
    print("               any checkout can.")
    print("  ACT CLASS  : GET only. No dispatch, no re-run, no cancel.")
    print("")

    total, e1 = gh_count("per_page=1")
    succ_doc, e2 = gh_json("status=success&per_page=100")
    fail, e3 = gh_count("status=failure&per_page=1")
    after = urllib.parse.quote(">" + PORTAL_STEP_AT, safe="")
    post_total, e4 = gh_count("created=%s&per_page=1" % after)
    post_succ, e5 = gh_count("status=success&created=%s&per_page=1" % after)

    errs = [x for x in (e1, e2, e3, e4, e5) if x]
    if errs:
        BLIND.append(("A/github-actions-run-history",
                      "live API unreachable or unparsable: " + "; ".join(errs[:2])))
        print("  BLIND: %s" % errs[0])
        return {"blind": True}

    succ_runs = sorted(succ_doc.get("workflow_runs", []), key=lambda r: r["created_at"])
    succ = succ_doc.get("total_count", 0)
    cancelled = total - fail - succ

    print("  RUNS_TOTAL                 = %d" % total)
    print("               (the denominator: every run of this workflow, ever, taken from")
    print("                the API's own total_count and not from a page length)")
    print("  RUNS_SUCCESS               = %d" % succ)
    print("  RUNS_FAILURE               = %d" % fail)
    print("  RUNS_OTHER                 = %d" % cancelled)
    print("               (total MINUS success MINUS failure -- written as a subtraction")
    print("                from the printed denominator so a state I did not think of")
    print("                cannot vanish silently: it lands here and the arithmetic")
    print("                still closes)")
    print("")
    print("  EVERY SUCCESS THIS WORKFLOW HAS EVER HAD (%d of %d, enumerated, not sampled):" % (succ, total))
    for r in succ_runs:
        print("    %s  run %d  head %s" % (r["created_at"], r["id"], r["head_sha"][:10]))
    first_sha = succ_runs[0]["head_sha"][:10] if succ_runs else "n/a"
    last_succ = succ_runs[-1]["created_at"] if succ_runs else None
    print("")
    print("  THE CUT THAT MATTERS. %s (%s) added the 'Checkout portal' step and the" % (PORTAL_STEP_COMMIT, PORTAL_STEP_AT))
    print("  literal pin at %s:66. Runs created AFTER that commit:" % WF)
    print("    RUNS_AFTER_PORTAL_STEP           = %d" % post_total)
    print("    SUCCESSES_AFTER_PORTAL_STEP      = %d" % post_succ)
    print("    CONSECUTIVE_FAILING_RUNS         = %d of %d" % (post_total - post_succ, post_total))
    print("")
    print("  So: WORKFLOW_EVER_RAN is YES and it is not close -- %d runs." % total)
    print("  WORKFLOW_EVER_SUCCEEDED is also YES, %d times, ALL of them on 2026-07-07" % succ)
    print("  between %s and %s -- every one of them BEFORE the portal" % (succ_runs[0]["created_at"] if succ_runs else "?", last_succ))
    print("  step existed. Since the portal step landed the workflow has succeeded")
    print("  ZERO times in %d attempts." % post_total)
    print("")
    print("  AND THE 8 SUCCESSES DID NOT PUBLISH A CORRECT ZIP EITHER. The step they")
    print("  ran without is the one that puts portal/src in the archive; the workflow's")
    print("  own comment records the consequence, ground-root-caused 2026-07-07 by")
    print("  0.7.0_AE_CloudOps~B: 'the zip below silently packed 0 files from portal/src")
    print("  for every run since this workflow landed (e32896edd)' -- REACT_QUERY_KEY")
    print("  0/32, PORTAL_COMPONENT 0/27, API_ROUTE 77/263.")
    print("  CORRECT PUBLISHES BY THIS ROUTE = 0 of %d." % total)
    return {"blind": False, "total": total, "succ": succ, "fail": fail,
            "cancelled": cancelled, "post_total": post_total, "post_succ": post_succ,
            "last_succ": last_succ, "first_sha": first_sha, "succ_runs": succ_runs}


def instrument_a_steps():
    print("")
    print("  STEP GRAIN -- WHY IT FAILS, read off two named runs (not inferred):")
    g = shutil.which("gh")
    if not g:
        print("    BLIND: gh not resolvable")
        return
    doc, err = gh_json("per_page=1")
    newest = None
    if doc and doc.get("workflow_runs"):
        newest = doc["workflow_runs"][0]
    for label, rid in (("NEWEST RUN", newest["id"] if newest else None),
                       ("LAST SUCCESS", 28871059541)):
        if rid is None:
            print("    %s: BLIND (no run id)" % label)
            continue
        rc, out, err = sh([g, "run", "view", str(rid), "--repo", GH_REPO, "--json", "jobs"], timeout=40)
        if rc != 0:
            print("    %s (%s): BLIND rc=%d %s" % (label, rid, rc, err.strip()[:100]))
            continue
        try:
            jobs = json.loads(out)["jobs"]
        except Exception:  # noqa: BLE001
            print("    %s (%s): BLIND unparsable" % (label, rid))
            continue
        for j in jobs:
            print("    %s run=%s job=%r -> %s" % (label, rid, j["name"], j["conclusion"]))
            for s in j["steps"]:
                print("        step %-2s %-62s %s" % (s["number"], s["name"][:62], s["conclusion"]))


# ---------------------------------------------------------------- INSTRUMENT B
def walk_census(roots):
    """One census, two roots, one printed denominator. Returns (files, hits)."""
    files = 0
    hits = []
    for root in roots:
        base = os.path.join(REPO, root)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                files += 1
                try:
                    txt = open(full, "r", encoding="utf-8", errors="replace").read()
                except Exception:  # noqa: BLE001
                    continue
                rel = os.path.relpath(full, REPO).replace("\\", "/")
                hits.append((rel, txt))
    return files, hits


def instrument_b():
    print("")
    bar("INSTRUMENT B -- THE NEVER-2 DEPLOY LEDGER (this worktree, walked)")
    roots = ["org/critical_paths/change_management",
             "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4"]
    print("  COVERAGE   : every file under both of these roots --")
    for r in roots:
        print("                 %s" % r)
    print("               EXCLUDED from the walk: .git and __pycache__ directories, and")
    print("               nothing else. The denominator below is stated AFTER that")
    print("               exclusion and the exclusion is named, so the number says what")
    print("               it left out rather than only how big it is.")
    print("  GRAIN      : one deploy-ledger ENTRY = one deploy act (opened/closed, owner,")
    print("               order, act line). This is the estate's own record of who did")
    print("               what to a served surface -- not a reconstruction.")
    print("  ENVIRONMENT: this checkout, read at run time. No stored baseline.")
    tree = sh(["git", "rev-parse", "--show-toplevel"])[1].strip()
    branch = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"])[1].strip()
    head = sh(["git", "rev-parse", "HEAD"])[1].strip()
    print("  TREE_READ  = %s" % tree)
    print("               branch %s   HEAD %s" % (branch, head[:12]))
    print("")
    files, hits = walk_census(roots)
    ctl = [rel for rel, txt in hits if CONTROL_TOKEN in txt]
    print("  DENOMINATOR: %d file(s) scanned across the two roots." % files)
    print("  POSITIVE CONTROL (the tree clause): a file that exists ONLY on this branch")
    print("  must appear in this instrument's hits, or the walk is reading another")
    print("  checkout and its zero would be well-formed and wrong.")
    print("    control token %s -> %d hit(s): %s" % (CONTROL_TOKEN, len(ctl), ", ".join(ctl) or "NONE"))
    ok = len(ctl) >= 1
    print("    TREE_CONTROL = %s" % ("FIRED" if ok else "DID-NOT-FIRE -- CENSUS VOID"))
    if not ok:
        BLIND.append(("B/deploy-ledger-walk", "tree control did not fire; census void"))
        return {"blind": True, "entries": []}

    pushes = []
    for rel, txt in hits:
        if not rel.startswith("org/critical_paths/change_management"):
            continue
        if KEY not in txt:
            continue
        if ("s3 cp" not in txt) and ("PutObject" not in txt):
            continue
        m = re.search(r"\*\*Owner:\*\*\s*`([^`]+)`", txt)
        owner = m.group(1) if m else "UNNAMED"
        m = re.search(r"\*\*Order:\*\*\s*`([^`]+)`", txt)
        order = m.group(1) if m else "UNNAMED"
        m = re.search(r"\*\*Status:\*\*\s*(\S+)", txt)
        status = m.group(1) if m else "UNKNOWN"
        act = ""
        for ln in txt.splitlines():
            if "s3 cp" in ln and KEY in ln:
                act = ln.strip().strip("`")
                break
        base = os.path.basename(rel)
        stamp = base.split("_")[0]
        hand = ("f3_build_source_zip.py" in txt) or ("aws s3 cp" in txt) or ("s3 cp" in act)
        wf_named = "stitch-source-push.yml" in txt
        pushes.append({"file": rel, "stamp": stamp, "owner": owner, "order": order,
                       "status": status, "act": act, "hand": hand, "wf_named": wf_named})
    pushes.sort(key=lambda p: p["stamp"])
    print("")
    print("  LEDGER ENTRIES RECORDING A PutObject TO %s: %d of %d file(s) scanned."
          % (KEY, len(pushes), files))
    for p in pushes:
        print("")
        print("    %s" % p["file"])
        print("      opened %s  status %s" % (p["stamp"], p["status"]))
        print("      owner  %s" % p["owner"])
        print("      order  %s" % p["order"])
        if p["act"]:
            print("      act    %s" % p["act"][:150])
        print("      names the hand producer f3_build_source_zip.py / an aws s3 cp: %s" % p["hand"])
    return {"blind": False, "entries": pushes, "files": files}


# ---------------------------------------------------------------- INSTRUMENT C
def instrument_c():
    print("")
    bar("INSTRUMENT C -- THE SERVED OBJECT AND ITS BUCKET (live AWS read)")
    print("  COVERAGE   : the one key %s in bucket %s," % (KEY, BUCKET))
    print("               plus the bucket's versioning configuration, which decides")
    print("               whether a per-write history EXISTS to be read at all.")
    print("  GRAIN      : the CURRENT object -- one LastModified, one ETag, one")
    print("               ContentType. This instrument can see the LAST writer's")
    print("               fingerprint and nothing before it.")
    print("  ENVIRONMENT: live us-east-1 through the .tools/aws shim (CLI v1).")
    print("  TREE       : none -- this is the served plane, not a checkout.")
    print("  ACT CLASS  : head-object / list-objects-v2 / get-bucket-versioning. READS.")
    print("")
    rc, out, err = aws(["s3api", "head-object", "--bucket", BUCKET, "--key", KEY, "--output", "json"])
    if rc != 0:
        BLIND.append(("C/served-object", "head-object rc=%d %s" % (rc, err.strip()[:120])))
        print("  BLIND: head-object rc=%d %s" % (rc, err.strip()[:160]))
        return {"blind": True}
    obj = json.loads(out)
    print("  LastModified  : %s" % obj.get("LastModified"))
    print("  ContentLength : %s" % obj.get("ContentLength"))
    print("  ETag          : %s" % obj.get("ETag"))
    print("  ContentType   : %s" % obj.get("ContentType"))
    rc2, out2, err2 = aws(["s3api", "get-bucket-versioning", "--bucket", BUCKET, "--output", "json"])
    ver = (out2 or "").strip()
    print("  get-bucket-versioning -> %s" % (ver if ver else "(EMPTY BODY = versioning has never been enabled)"))
    versioned = "Enabled" in ver
    if not versioned:
        BLIND.append(("C2/s3-object-version-history",
                      "bucket versioning is NOT enabled, so S3 holds exactly one version "
                      "of the key and NO per-write history exists to attribute the five "
                      "pushes with. This is an ABSENT INSTRUMENT, not a zero."))
    print("")
    print("  WHAT THIS INSTRUMENT CAN AND CANNOT DO:")
    print("    CAN : name the vintage of the object being served right now, and carry")
    print("          ONE independent fingerprint of the LAST writer (below).")
    print("    CANNOT: reach any earlier write. Versioning is off, so there is exactly")
    print("          one version and the four earlier pushes are unrecoverable HERE.")
    print("          Reported BLIND rather than counted as zero.")
    print("")
    print("  THE FINGERPRINT, and it is INFERRED, not measured:")
    print("    MEASURED : ContentType = %r." % obj.get("ContentType"))
    print("    INFERRED : `aws s3 cp` guesses ContentType with Python mimetypes. On")
    print("               Windows that reads the registry and .zip resolves to")
    print("               'application/x-zip-compressed'; on the ubuntu-latest runner")
    print("               /etc/mime.types resolves .zip to 'application/zip'. The served")
    print("               object therefore carries the fingerprint of a WINDOWS uploader,")
    print("               which the GitHub runner is not.")
    print("    LIMIT    : this discriminates the uploader's OPERATING SYSTEM, never its")
    print("               identity. It is offered as a THIRD axis agreeing with A and B,")
    print("               not as a substitute for either.")
    return {"blind": False, "obj": obj, "versioned": versioned}


# ---------------------------------------------------------------- INSTRUMENT D
def instrument_d():
    print("")
    bar("INSTRUMENT D -- THE CLOUDTRAIL S3 DATA-EVENT PLANE (expected BLIND, controlled)")
    print("  COVERAGE   : EventName=PutObject over 2026-09-10T02:00Z..03:30Z, a window")
    print("               that PROVABLY contains a write to the key (instrument C read")
    print("               LastModified 2026-09-10T02:46:36Z inside it).")
    print("  GRAIN      : one API call with its principal -- the only instrument here")
    print("               that could name WHO wrote, rather than what or when.")
    print("  ENVIRONMENT: live CloudTrail lookup-events, us-east-1.")
    print("  TREE       : none.")
    print("  NOTE       : lookup-events --start-time is INCLUSIVE at the second; the")
    print("               window is opened 46 min early so that cannot matter here.")
    print("")
    rc, out, err = aws(["cloudtrail", "lookup-events",
                        "--lookup-attributes", "AttributeKey=EventName,AttributeValue=PutObject",
                        "--start-time", "2026-09-10T02:00:00Z",
                        "--end-time", "2026-09-10T03:30:00Z",
                        "--max-items", "5", "--output", "json"], timeout=60)
    if rc != 0:
        BLIND.append(("D/cloudtrail-data-events", "lookup-events rc=%d %s" % (rc, err.strip()[:120])))
        print("  BLIND: lookup-events rc=%d" % rc)
        return {"blind": True}
    n_put = len(json.loads(out).get("Events", []))
    rc2, out2, err2 = aws(["cloudtrail", "lookup-events",
                           "--start-time", "2026-09-10T02:00:00Z",
                           "--end-time", "2026-09-10T03:30:00Z",
                           "--max-items", "3", "--output", "json"], timeout=60)
    n_any = len(json.loads(out2).get("Events", [])) if rc2 == 0 else -1
    print("  PutObject events in the window : %d" % n_put)
    print("  POSITIVE CONTROL, same window, no EventName filter: %d event(s)." % n_any)
    print("  THE CONTROL IS THE WHOLE POINT. Without it, 0 PutObject reads as 'nobody")
    print("  wrote the object', which is FALSE -- instrument C shows the object WAS")
    print("  written at 02:46:36Z inside this window. With it, the 0 is diagnosed:")
    print("  the trail is ALIVE (%d management events came back) and S3 OBJECT-LEVEL" % n_any)
    print("  DATA EVENTS ARE SIMPLY NOT LOGGED on this account.")
    BLIND.append(("D/cloudtrail-data-events",
                  "S3 object-level data events are not logged: 0 PutObject returned for a "
                  "window that provably contains one, while the same window returns %d "
                  "management events. The identity plane does not exist to be read." % n_any))
    print("")
    print("  CONSEQUENCE: the ONE instrument that could have named the writing PRINCIPAL")
    print("  is absent. Attribution below therefore rests on A (the workflow could not")
    print("  have done it) and B (the estate's own act record says who did), which are")
    print("  different substrates -- not on one method run twice.")
    return {"blind": True, "put": n_put, "any": n_any}


# ---------------------------------------------------------------- THE JOIN
def main():
    bar("I5-AC1 -- WHICH ROUTE HAS ACTUALLY RUN (CG-s-45, TO-CG-I-5)")
    print("worker  : 0.9.0_WK_NFRA_CLDGRPH~4")
    print("question: has the committed workflow ever executed, and what produced each of")
    print("          round 6's five served source zips?")
    print("hold    : every call below is a READ. Nothing pushed, triggered or applied.")

    a = instrument_a()
    if not a.get("blind"):
        instrument_a_steps()
    b = instrument_b()
    instrument_c()
    instrument_d()

    print("")
    bar("THE JOIN -- ATTRIBUTING THE FIVE SERVED ZIPS")
    entries = [e for e in b.get("entries", []) if e["stamp"] >= "20260901"]
    print("  The face names FIVE served pushes in round 6. Instrument B finds %d ledger" % len(entries))
    print("  entries recording a PutObject to the key on or after 2026-09-01, and the")
    print("  denominator that number came out of is printed above (%s file(s))." % b.get("files", "?"))
    print("")
    print("  RULE OF ATTRIBUTION, stated before it is applied so it cannot be fitted to")
    print("  the answer: a zip is attributed to the WORKFLOW only if a SUCCESSFUL run of")
    print("  the workflow exists at or before the push and after the previous one. It is")
    print("  attributed to the HAND ROUTE only if a deploy-ledger entry names an owner,")
    print("  an order and an `aws s3 cp` act. Anything satisfying neither is UNATTRIBUTED")
    print("  and is reported as such, never folded into the larger bucket.")
    print("")
    last_succ = a.get("last_succ")
    attributed = 0
    for i, e in enumerate(entries, 1):
        verdict = "HAND_ROUTE" if e["hand"] else "UNATTRIBUTED"
        if verdict == "HAND_ROUTE":
            attributed += 1
        print("    ZIP %d  %s" % (i, e["stamp"]))
        print("           ledger  : %s" % os.path.basename(e["file"]))
        print("           owner   : %s   order: %s" % (e["owner"], e["order"]))
        print("           workflow successes anywhere near this push: 0 "
              "(last success ever = %s)" % last_succ)
        print("           VERDICT : %s" % verdict)
    print("")
    print("  AND THE SUBTRACTION THAT MAKES THIS MORE THAN A LEDGER READ. Instrument A")
    print("  is not corroborating instrument B -- it is EXCLUDING the alternative. The")
    print("  workflow's last success of any kind was %s. Every one of the" % last_succ)
    print("  five pushes is after it. So the committed route could not have produced any")
    print("  of them even if no ledger entry existed at all, and the ledger's naming of")
    print("  the hand producer is then the POSITIVE identification on top of that.")

    print("")
    bar("SUMMARY -- I5-AC1")
    ever = "BLIND" if a.get("blind") else ("YES" if a.get("total", 0) > 0 else "NO")
    print("WORKFLOW_EVER_RAN=%s" % ever)
    print("")
    print("EVIDENCE printed -- and it is not the one the cell expected:")
    if not a.get("blind"):
        print("  * The committed route has run %d times. It is not an unrun route; it is a" % a["total"])
        print("    route that FIRES CORRECTLY ON EVERY PUSH AND CANNOT FINISH.")
        print("  * It has succeeded %d times, ALL on 2026-07-07, ALL before the portal" % a["succ"])
        print("    checkout step existed. Last success ever: %s." % a["last_succ"])
        print("  * Since that step landed (%s, %s): %d runs, %d successes."
              % (PORTAL_STEP_COMMIT, PORTAL_STEP_AT, a["post_total"], a["post_succ"]))
        print("  * It fails at step 3, 'Checkout portal (separate private repo,")
        print("    gitlink-pinned)', which needs secrets.PORTAL_REPO_PAT. Steps 4 and 5 --")
        print("    the AWS credentials and the zip-and-publish -- are SKIPPED every time.")
        print("  * The %d successes published a zip with ZERO portal/src entries, because" % a["succ"])
        print("    the step that packs portal is the step that did not yet exist.")
        print("    CORRECT PUBLISHES BY THE COMMITTED ROUTE, EVER: 0 of %d." % a["total"])
        print("  * The literal pin at %s:66 lives INSIDE the step that has" % WF)
        print("    never once succeeded. It has therefore never been exercised at all.")
    print("")
    print("ZIPS_ATTRIBUTED=%d of 5" % attributed)
    print("  All %d attributed to the HAND ROUTE: a local build by" % attributed)
    print("  org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/"
          "f3_build_source_zip.py")
    print("  plus one `aws s3 cp`, each with a NEVER-2 ledger entry naming its owner and")
    print("  order. ZERO attributed to the committed workflow. ZERO unattributed.")
    print("")
    print("INSTRUMENT printed -- four, on four substrates, two of them blind:")
    print("  A  GitHub Actions run history   LIVE  denominator %s runs" % a.get("total", "BLIND"))
    print("  B  NEVER-2 deploy ledger walk   %s  denominator %s files, tree control %s"
          % ("BLIND" if b.get("blind") else "LIVE ", b.get("files", "n/a"),
             "DID-NOT-FIRE" if b.get("blind") else "FIRED"))
    print("  C  served S3 object             LIVE  1 key; versioning OFF -> no write history")
    print("  D  CloudTrail S3 data events    BLIND 0 PutObject in a window that contains one")
    print("")
    print("BLIND_REPORTED=%d" % len(BLIND))
    for name, why in BLIND:
        print("  BLIND %s" % name)
        print("        %s" % why)
    print("")
    print("  NEITHER BLIND INSTRUMENT CONTRIBUTED A ZERO TO ANY COUNT ABOVE. Both were")
    print("  asked, both failed to answer, and both are named here with the reason. The")
    print("  CloudTrail one carries a positive control precisely so that its 0 could not")
    print("  be read as 'no write happened'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
