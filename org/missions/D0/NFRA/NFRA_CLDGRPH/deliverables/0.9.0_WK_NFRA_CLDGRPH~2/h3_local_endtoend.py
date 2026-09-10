#!/usr/bin/env python3
"""NFRA_CLDGRPH CG-s-38 / H3-AC2 -- THE PORTAL VINTAGE REACHES A RENDERED LINE, LOCALLY.

WHY LOCAL AND NOT SERVED, stated first because the state label is half the claim. Every
act that would put this on the served plane is HELD by this order: no terraform apply, no
ecs run-task, no CodeBuild start, no image act, no S3 write. So hops 3 and 4 are proven the
only way that is honest in this round -- the REAL functions, over REAL bytes, in this
process. Round 7's CG-s-33 hit the same wall and proved its fix on a local fold; this is
that precedent applied one cell over.

WHAT IS REAL HERE AND WHAT IS A FIXTURE, so no reader has to guess:
  REAL  : kuzu_nessie_load.read_stitch_vintage and projection_worker._age_line, imported
          from this worktree and called unmodified.
  REAL  : the marker BYTES -- json.dumps of a dict, decoded by the function's own
          json.loads, exactly as it decodes an S3 body.
  FIXTURE: the S3 client. read_stitch_vintage takes one as an argument precisely so the IO
          half can be replaced; the object below implements get_object and nothing else.
  FIXTURE: the manifest. _age_line reads manifest["source_vintage"] and nothing else, so
          the manifest is that key plus the vintage string it is called with.

FOUR ARMS, and an arm that cannot fail is not a test:
  1  the portal sha travels marker -> source_vintage -> the rendered line
  2  NEGATIVE CONTROL: a marker with NO portal key renders a line that OMITS the clause
     cleanly and does not raise, and is BYTE-IDENTICAL to the pre-CG-s-38 sentence
  3  no stitch at all: {} from hop 3, and the line is the bare estate sentence
  4  the builder/validator identity: _age_line re-derived from the same manifest is the
     same string, which is the equality _validate_manifest_shape actually enforces
"""
import datetime
import io
import json
import os
import sys

WS = os.getcwd()
sys.path.insert(0, os.path.join(WS, "org", "modules", "graph"))
sys.path.insert(0, os.path.join(WS, "infra", "aws", "globgrph"))

import kuzu_nessie_load as K      # noqa: E402
import projection_worker as PW    # noqa: E402

VINTAGE = "2026-09-10T03:31:02+00:00"
PORTAL_SHA = "5907cbca98eb091124e38a32debefa355c1d4376"
LAST_MODIFIED = datetime.datetime(2026, 9, 10, 3, 1, 20, tzinfo=datetime.timezone.utc)

MARKER_WITH_PORTAL = {
    "built_at": "2026-09-10T03:01:17Z",
    "aws_snapshot": "2026-09-10T02:00:11Z",
    "git_sha": "2fd5cae09f67dd31ae1d8da1ced56c24d52c6001",
    "producer": "stitch-codebuild",
    "total_nodes": 1771,
    "total_edges": 4103,
    "artifact_sha256": "d" * 64,
    "portal_sha": PORTAL_SHA,
}
MARKER_NO_PORTAL = {k: v for k, v in MARKER_WITH_PORTAL.items() if k != "portal_sha"}
MARKER_NO_STITCH = {k: v for k, v in MARKER_NO_PORTAL.items() if k != "built_at"}


class FakeS3(object):
    """The IO half only. read_stitch_vintage takes an s3 client argument for this reason."""

    def __init__(self, marker):
        self._body = json.dumps(marker).encode("utf-8")

    def get_object(self, Bucket, Key):  # noqa: N803 -- boto3's own parameter names
        assert Bucket == K.WAREHOUSE_BUCKET and Key == K.STITCH_MARKER_KEY, \
            "the function must read the bucket/key it declares"
        return {"Body": io.BytesIO(self._body), "LastModified": LAST_MODIFIED}


def manifest_for(vintage_keys):
    return {"schema_version": 1, "vintage": VINTAGE, "committed_at": VINTAGE,
            "source_vintage": dict(vintage_keys)}


def main():
    print("=== CG-s-38 / H3-AC2 -- HOP 3 -> HOP 4, EXERCISED LOCALLY OVER REAL BYTES ===")
    print("TREE_READ=%s" % WS.replace(os.sep, "/"))
    print("INSTRUMENT: the two production functions themselves, imported from this worktree"
          " (%s, %s) and called unmodified; the only substitution is the S3 client, which"
          " the function takes as a parameter." % (K.__file__.replace(os.sep, "/"),
                                                   PW.__file__.replace(os.sep, "/")))
    print("COVERAGE: 3 marker shapes (portal present / portal absent / no stitch at all)"
          " x 2 functions = the whole reachable key-presence space of this change.")
    print("GRAIN: one marker dict -> one source_vintage dict -> one rendered line, compared"
          " as whole strings, not as substrings of a summary.")
    print("ENVIRONMENT: python %s on %s, no network, no AWS call, no Kuzu database."
          % (sys.version.split()[0], sys.platform))
    print("")

    # ---------------------------------------------------------------- ARM 1
    v1 = K.read_stitch_vintage(s3=FakeS3(MARKER_WITH_PORTAL))
    copied = v1.get("stitch_portal_sha") == PORTAL_SHA
    line1 = PW._age_line(VINTAGE, manifest_for(v1))
    contains = PORTAL_SHA in line1
    print("  ARM 1 -- the marker carries portal_sha=%s" % PORTAL_SHA)
    print("    hop 3 returned %d key(s): %s" % (len(v1), ", ".join(sorted(v1))))
    print("    RENDERED_LINE: %s" % line1)
    print("")

    # ---------------------------------------------------------------- ARM 2
    raised = False
    detail = ""
    try:
        v2 = K.read_stitch_vintage(s3=FakeS3(MARKER_NO_PORTAL))
        line2 = PW._age_line(VINTAGE, manifest_for(v2))
    except Exception as exc:  # noqa: BLE001
        raised = True
        detail = "%s: %s" % (type(exc).__name__, exc)
        v2, line2 = {}, ""
    expected_pre = ("Built from the estate as of 2026-09-10 03:31:02 UTC."
                    " Stitch source: stitch-codebuild built 2026-09-10T03:01:17Z.")
    omit_clean = ("stitch_portal_sha" not in v2 and "Portal source" not in line2
                  and line2 == expected_pre)
    print("  ARM 2 (NEGATIVE CONTROL) -- the SAME marker with the portal key removed")
    print("    hop 3 returned %d key(s): %s" % (len(v2), ", ".join(sorted(v2)) or "(none)"))
    print("    RENDERED_LINE: %s" % (line2 or "(no line -- the arm raised)"))
    print("    BYTE-IDENTICAL TO THE PRE-CG-s-38 SENTENCE=%s  (delta 0 for every reader who"
          " was there before this change)" % str(line2 == expected_pre).lower())
    print("    raised=%s %s" % (str(raised).lower(), detail))
    print("")

    # ---------------------------------------------------------------- ARM 3
    v3 = K.read_stitch_vintage(s3=FakeS3(MARKER_NO_STITCH))
    line3 = PW._age_line(VINTAGE, manifest_for(v3))
    bare = "Built from the estate as of 2026-09-10 03:31:02 UTC."
    print("  ARM 3 -- no stitch at all (the marker has no built_at): absent is absent")
    print("    hop 3 returned %d key(s); RENDERED_LINE: %s" % (len(v3), line3))
    print("    BARE_ESTATE_SENTENCE=%s" % str(line3 == bare).lower())
    print("")

    # ---------------------------------------------------------------- ARM 4
    again = PW._age_line(VINTAGE, manifest_for(v1))
    print("  ARM 4 -- the builder/validator identity (_validate_manifest_shape refuses a"
          " manifest whose age_line it cannot re-derive from the manifest itself)")
    print("    REDERIVATION_IDENTICAL=%s" % str(again == line1).lower())
    print("")

    ok = (copied and contains and omit_clean and not raised and len(v3) == 0
          and line3 == bare and again == line1)
    print("PORTAL_KEY_COPIED=%s" % str(copied).lower())
    print("AGE_LINE_CONTAINS_PORTAL=%s" % str(contains).lower())
    print("RENDERED_LINE printed: %s" % line1)
    print("NEGATIVE_CONTROL_NO_PORTAL_KEY=%s" % ("CLEAN_OMIT" if omit_clean else "DIRTY"))
    print("RAISED=%s" % str(raised).lower())
    print("STATE=DESIRED-LOCAL-EXERCISED")
    print("  DENOMINATOR: 3 marker shapes, 4 arms, 2 production functions, 0 network calls.")
    print("  WHAT THIS DOES NOT CERTIFY, AND IT IS THE WHOLE POINT OF THE STATE LABEL: it"
          " says NOTHING about the served graph. The engine that runs in ECS is a built"
          " image; the projection a reader queries was published before this change existed."
          " This is committed code exercised in a local process -- DESIRED, exercised;"
          " never APPLIED, never SERVED.")
    print("H3_AC2_RESULT=%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
