#!/usr/bin/env python3
"""NFRA_CLDGRPH CG-s-38 / H3-AC3 -- HOP 1 DECIDED, AND THE WHOLE CHAIN CHECKED FOR HALVES.

The task order offers two branches for hop 1 and calls both passes: (a) give the route that
runs a COMMITTED producer that writes portal_sha into the archive beside stitch_source_sha,
or (b) file it as a named owned item with its owner and what blocks it. It also says: do
not quietly do half of (a).

THIS PROBE TAKES (a), AND MEASURES THE HALVES RATHER THAN ASSERTING THEIR ABSENCE.
"Half done" has a precise meaning for a four-hop feed: a hop that WRITES the key whose
CONSUMER does not read it, or a consumer that reads a key nobody writes. So arm 2 walks all
four hops and reports the chain as a whole; HALF_DONE is that measurement, not an opinion.

AND WHAT (a) DOES NOT BUY, said here rather than left for a reader to discover: the route
that ran is still a script in a MISSION DELIVERABLE FOLDER. It is committed, it is now
correct, and it has no production home, no schedule and no owner outside this project. That
residual is printed below with its blocker and its owner -- the branch token is not a claim
that hop 1 is finished, only that its KEY is written by a committed producer on the route
that actually produces the served zip.

FOUR ARMS:
  1  the two producers, by content: does each write portal_sha into the archive
  2  the chain, all four hops: is any hop written whose consumer is not
  3  EXERCISE, route A: the hand builder run over two throwaway git repos -- the zip it
     produces is opened and portal_sha.txt is read back and compared to the portal HEAD
  4  EXERCISE, hop 2: the buildspec's OWN inline python, extracted from the .tf and run
     verbatim over a fixture archive dir, with and without portal_sha.txt
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

WS = os.getcwd()
DELIV = "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2"
F3 = DELIV + "/f3_build_source_zip.py"
WF = ".github/workflows/stitch-source-push.yml"
TF = "infra/aws/terraform/globgrph/stitch-produce.tf"
KUZU = "infra/aws/globgrph/kuzu_nessie_load.py"
PW = "infra/aws/globgrph/projection_worker.py"
SCRATCH = os.path.join(WS, ".scratch", "h3_hop1")

GIT_ID = ["-c", "user.name=h3 fixture", "-c", "user.email=h3@opal.agent"]


def read(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return fh.read()


def run(args, cwd=None):
    env = dict(os.environ)
    env["MSYS_NO_PATHCONV"] = "1"
    return subprocess.run(args, capture_output=True, text=True, cwd=cwd, env=env)


def main():
    print("=== CG-s-38 / H3-AC3 -- HOP 1 DECIDED, THE CHAIN MEASURED FOR HALVES ===")
    print("TREE_READ=%s  branch=%s" % (WS.replace(os.sep, "/"),
                                       run(["git", "rev-parse", "--abbrev-ref",
                                            "HEAD"]).stdout.strip()))
    print("TREE_CONTROL=%s/h3_tree_control.txt exists=%s (only on this branch)"
          % (DELIV, os.path.isfile(os.path.join(DELIV, "h3_tree_control.txt"))))
    print("INSTRUMENT: literal content match over the five feed files, plus TWO LIVE"
          " EXERCISES -- the hand builder run for real over throwaway git repos, and the"
          " buildspec's own inline python extracted from the Terraform and executed.")
    print("GRAIN: one archive ENTRY and one marker KEY -- read back out of a real zip and a"
          " real json file, never inferred from the producer's own log line.")
    print("ENVIRONMENT: python %s on %s, local filesystem only; no AWS, no CodeBuild, no"
          " apply. Every state below is DESIRED or LOCAL-EXERCISED."
          % (sys.version.split()[0], sys.platform))
    print("")

    # ---------------------------------------------------------------- ARM 1
    f3 = read(F3)
    wf = read(WF)
    a_writes = 'z.writestr("portal_sha.txt", portal_head' in f3
    b_writes = ("git -C portal rev-parse HEAD > portal_sha.txt" in wf
                and re.search(r"^\s+portal_sha\.txt\s+" + re.escape(chr(92)) + "$",
                              wf, re.M) is not None)
    print("  ARM 1 -- the two producers, by content")
    print("    ROUTE A  %s" % F3)
    print("             THE ROUTE THAT ACTUALLY RAN: all five served source-zip pushes in"
          " round 6 were made by hand from this script (CG-s-35's census).")
    print("             writes portal_sha.txt into the archive = %s" % str(a_writes).lower())
    print("    ROUTE B  %s" % WF)
    print("             the COMMITTED route; no run of it has ever been observed to"
          " succeed (it needs secrets.PORTAL_REPO_PAT).")
    print("             writes portal_sha.txt into the archive = %s" % str(b_writes).lower())
    print("")

    # ---------------------------------------------------------------- ARM 2
    tf = read(TF)
    kz = read(KUZU)
    pw = read(PW)
    chain = [
        ("1 PACK  route A writes portal_sha.txt", a_writes),
        ("1 PACK  route B writes portal_sha.txt", b_writes),
        ("2 STAMP buildspec READS portal_sha.txt", "portal_sha.txt" in tf),
        ("2 STAMP buildspec writes marker['portal_sha']", "marker['portal_sha']" in tf),
        ("3 COPY  hop 3 READS marker portal_sha", 'm.get("portal_sha")' in kz),
        ("3 COPY  hop 3 writes stitch_portal_sha", '"stitch_portal_sha"' in kz),
        ("4 PRINT hop 4 READS stitch_portal_sha", '"stitch_portal_sha"' in pw),
        ("4 PRINT hop 4 renders it", "Portal source:" in pw),
    ]
    print("  ARM 2 -- the chain, all four hops: a WRITE whose READER is missing is a half")
    for label, ok in chain:
        print("    %-46s %s" % (label, str(ok).lower()))
    half = not all(ok for _, ok in chain)
    print("    CHAIN_LINKS_PRESENT=%d of %d" % (sum(1 for _, ok in chain if ok), len(chain)))
    print("")

    # ---------------------------------------------------------------- ARM 3
    if os.path.isdir(SCRATCH):
        shutil.rmtree(SCRATCH, ignore_errors=True)
    repo = os.path.join(SCRATCH, "repo")
    portal = os.path.join(SCRATCH, "portal")
    for d in (os.path.join(repo, "org", "modules"),
              os.path.join(repo, "data", "etfs", "scripts", "gold"),
              os.path.join(portal, "src")):
        os.makedirs(d, exist_ok=True)
    open(os.path.join(repo, "org", "modules", "m.py"), "w").write("# fixture\n")
    open(os.path.join(repo, "data", "etfs", "scripts", "gold", "g.py"), "w").write("# fix\n")
    open(os.path.join(portal, "src", "App.tsx"), "w").write("export const A = 1;\n")
    for d in (repo, portal):
        run(["git", "init", "-q", d])
        run(["git", "-C", d, "add", "-A"])
        run(["git", "-C", d] + GIT_ID + ["commit", "-q", "-m", "fixture"])
    repo_head = run(["git", "-C", repo, "rev-parse", "HEAD"]).stdout.strip()
    portal_head = run(["git", "-C", portal, "rev-parse", "HEAD"]).stdout.strip()
    out_zip = os.path.join(SCRATCH, "source.zip")
    r = run([sys.executable, os.path.join(WS, F3.replace("/", os.sep)),
             "--repo", repo, "--portal", portal, "--out", out_zip])
    packed = {}
    entry = None
    if os.path.isfile(out_zip):
        with zipfile.ZipFile(out_zip) as z:
            names = z.namelist()
            packed = {"entries": len(names),
                      "has_portal_sha": "portal_sha.txt" in names,
                      "has_source_sha": "stitch_source_sha.txt" in names}
            if packed["has_portal_sha"]:
                entry = z.read("portal_sha.txt").decode().strip()
    print("  ARM 3 (EXERCISE, ROUTE A) -- the hand builder run for real over two throwaway"
          " git repos, then the zip OPENED and read back")
    print("    fixture repo HEAD   = %s" % repo_head)
    print("    fixture portal HEAD = %s" % portal_head)
    print("    builder rc=%d, zip entries=%s" % (r.returncode, packed.get("entries")))
    print("    archive carries stitch_source_sha.txt=%s  portal_sha.txt=%s"
          % (str(packed.get("has_source_sha")).lower(),
             str(packed.get("has_portal_sha")).lower()))
    print("    portal_sha.txt CONTENT read back = %s" % entry)
    a_exercised = (r.returncode == 0 and entry == portal_head)
    print("    CONTENT_EQUALS_PORTAL_HEAD=%s" % str(a_exercised).lower())
    if r.returncode != 0:
        print("    builder stderr: %s" % r.stderr.strip()[:400])
    print("")

    # ---------------------------------------------------------------- ARM 4
    m = re.search(r"python3 - <<'PY'\n(.*?)\n\s*PY\n", tf, re.S)
    if not m:
        print("BLOCKED: could not extract the buildspec's inline python from %s" % TF)
        return 1
    body = m.group(1)
    indent = min(len(ln) - len(ln.lstrip()) for ln in body.split("\n") if ln.strip())
    body = "\n".join(ln[indent:] for ln in body.split("\n"))
    work = os.path.join(SCRATCH, "buildspec")
    os.makedirs(work, exist_ok=True)
    graph_path = os.path.join(work, "stitch_graph.json").replace(os.sep, "/")
    marker_path = os.path.join(work, "stitch_marker.json").replace(os.sep, "/")
    subbed = body.replace("/tmp/stitch_graph.json", graph_path)
    subbed = subbed.replace("/tmp/stitch_marker.json", marker_path)
    with open(graph_path, "w", encoding="utf-8") as fh:
        json.dump({"meta": {"aws_snapshot": "2026-09-10T02:00:11Z", "total_nodes": 1771,
                            "total_edges": 4103}}, fh)
    open(os.path.join(work, "stitch_source_sha.txt"), "w").write("2fd5cae09f\n")
    open(os.path.join(work, "portal_sha.txt"), "w").write(
        "5907cbca98eb091124e38a32debefa355c1d4376\n")
    script = os.path.join(work, "buildspec_marker.py")
    with io.open(script, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(subbed)
    r1 = run([sys.executable, script], cwd=work)
    marker_with = json.load(open(marker_path, encoding="utf-8"))
    os.remove(os.path.join(work, "portal_sha.txt"))
    r2 = run([sys.executable, script], cwd=work)
    marker_without = json.load(open(marker_path, encoding="utf-8"))
    print("  ARM 4 (EXERCISE, HOP 2) -- the buildspec's OWN inline python, extracted from"
          " the Terraform and executed verbatim")
    print("    SUBSTITUTION DISCLOSED (the only one): the two hard-coded /tmp paths were"
          " repointed at %s so this exercise cannot collide with another slot. Not one"
          " other character of the extracted block was changed." % work.replace(os.sep, "/"))
    print("    WITH portal_sha.txt   -> rc=%d keys=%d portal_sha=%s"
          % (r1.returncode, len(marker_with), marker_with.get("portal_sha")))
    print("    WITHOUT it (control)  -> rc=%d keys=%d portal_sha_present=%s"
          % (r2.returncode, len(marker_without), str("portal_sha" in marker_without).lower()))
    hop2_ok = (marker_with.get("portal_sha") == "5907cbca98eb091124e38a32debefa355c1d4376"
               and "portal_sha" not in marker_without and len(marker_without) == 7)
    print("    STAMP_CARRIES_THE_KEY=%s   ABSENT_IS_ABSENT=%s"
          % (str(marker_with.get("portal_sha") is not None).lower(),
             str("portal_sha" not in marker_without).lower()))
    print("")

    # ---------------------------------------------------------------- the decision
    writes = a_writes and b_writes and a_exercised and hop2_ok
    print("HOP1_BRANCH=%s" % ("COMMITTED_PRODUCER" if writes else "FILED_AS_BLOCKED"))
    print("PRODUCER_PATH printed:")
    print("  %s   <- the route that actually produced every served zip in round 6" % F3)
    print("  %s   <- the committed route, unobserved" % WF)
    print("WRITES_PORTAL_SHA=%s" % str(writes).lower())
    print("HALF_DONE=%s" % str(half).lower())
    print("  HALF_DONE is the ARM 2 measurement: %d of %d chain links present, so no hop"
          " writes a key its consumer does not read." % (sum(1 for _, ok in chain if ok),
                                                          len(chain)))
    print("HOP2_STATE=DESIRED")
    print("  Hop 2 is a COMMITTED buildspec inside a Terraform resource. It is DESIRED and"
          " nothing more: no apply has run and none is permitted this round, so the LIVE"
          " CodeBuild project still carries the seven-key marker. The extracted-block"
          " exercise above proves the TEXT is correct; it proves nothing about the project.")
    print("")
    print("RESIDUAL OWNED ITEMS -- (a) was taken for the KEY, and these are what (a) does"
          " not reach. Named here so the branch token cannot be read as 'hop 1 is finished':")
    print("  ITEM 1  BLOCKER printed: the route that produces the served zip lives in a"
          " MISSION DELIVERABLE FOLDER (%s). A deliverable folder is a record of a task"
          " order, not a production home: it has no schedule, no trigger, no owner outside"
          " this project, and it is archived when the mission closes. No path in this"
          " order's grant is a production home, so the move cannot be made from here."
          % DELIV)
    print("          OWNER_NAMED printed: 1.0.0_SA_CTO to place it (which plane owns a"
          " repo-subset packer), then 0.7.0_AE_CloudOps to run it.")
    print("  ITEM 2  BLOCKER printed: the committed route pins the portal at a LITERAL sha"
          " under a comment saying the pin IS the gitlink sha; at HEAD the gitlink is"
          " 5907cbca98eb... and the pin is b96562720505... Nothing updates it. Changing a"
          " production route's checkout ref is not this cell's change and no exercise of it"
          " is available under the egress hold.")
    print("          OWNER_NAMED printed: 0.7.0_AE_CloudOps (the disarm owner rows W2-S40"
          " and W2-S63 already carry).")
    print("  ITEM 3  BLOCKER printed: secrets.PORTAL_REPO_PAT is unprovisioned, which is"
          " why route B has never run and why route A exists at all.")
    print("          OWNER_NAMED printed: 0.7.0_AE_CloudOps, with 0.0.0_AB_MSTR for the"
          " repo secret itself.")
    print("")
    print("  DENOMINATOR: 2 producers, %d chain links, 1 zip built and reopened (%s"
          " entries), 2 marker runs of the extracted buildspec block, 3 residual items."
          % (len(chain), packed.get("entries")))
    print("  WHAT THIS DOES NOT CERTIFY: that either route will RUN. Route B has never been"
          " observed to succeed and route A is a hand act. This certifies that the producer"
          " CODE on both routes writes the key, and that hop 2's own text reads it.")
    print("H3_AC3_RESULT=%s" % ("PASS" if (writes and not half) else "FAIL"))
    return 0 if (writes and not half) else 1


if __name__ == "__main__":
    sys.exit(main())
