#!/usr/bin/env python3
"""fence_disposition_check -- LGIC_ENFORCE round 4, cell EN-d-26, ruling R-30.

Mechanizes DEC-4(ii)'s amended evidence rule (DEC4_II_AMENDED.r4.md, this same deliverables folder):
a NOT_A_PRINCIPAL disposition on a bucket that is not a member of a LIVE CloudTrail data-event
selector is REFUSED -- neither the org trail's ReadOnly S3 data-event selector nor the served-key
write trail's WriteOnly S3 data-event selector names it, so the prescribed CloudTrail evidence path
can never answer for it, and silence in a trail that never covered the bucket is never evidence
(R-30 parts 1 and 4).

Bucket coverage is READ from the two trail declarations themselves (the literal bucket list each
one's own `local` assigns), never from a hand-typed list here -- an enumerated list lapses silently
when a trail changes.

USAGE
    python fence_disposition_check.py <claim.json>
        claim.json: {"rows": [{"role", "bucket", "disposition", "evidence"}, ...]}
        Exit 0 if every NOT_A_PRINCIPAL row claims a covered bucket and carries evidence.
        Exit non-zero (prints the bucket and the reason) if any NOT_A_PRINCIPAL row claims an
        uncovered bucket, or a covered bucket with no evidence.
        Rows carrying any other disposition (EXEMPTED, NOT-JUDGED, ...) are not graded by this guard.

    python fence_disposition_check.py --self-test
        Exercises both directions against THIS tree's own trail declarations: a planted
        NOT_A_PRINCIPAL claim on opal-data-demo (must be refused) and one on a bucket read out of
        the trail declarations (must be accepted). Prints "SELF-TEST: N of N ..." on its own line.

Standard library only. ASCII only.
"""
import json
import os
import re
import sys

ORG_TRAIL_PATH = "infra/aws/terraform/shared-infra/cloudtrail-organization-trail.tf"
ORG_TRAIL_LOCAL = "org_trail_read_logged_buckets"

SERVED_WRITE_TRAIL_PATH = "infra/aws/terraform/globgrph/item2e_served_write_trail.tf"
SERVED_TRAIL_LOCAL = "served_write_trail_buckets"

UNCOVERED_PROBE_BUCKET = "opal-data-demo"


def _extract_bucket_list(text, local_name):
    """The string literals assigned to `local_name = [ ... ]` inside a Terraform locals block.

    Reads the literal list's own bytes (balanced-bracket scan from the assignment), never a
    hand-typed mirror of its contents -- so a bucket added to or dropped from the real list is
    picked up on the next read, with no second place to update."""
    m = re.search(re.escape(local_name) + r"\s*=\s*\[", text)
    if not m:
        return None
    start = m.end()
    depth = 1
    i = start
    n = len(text)
    while i < n and depth > 0:
        if text[i] == "[":
            depth += 1
        elif text[i] == "]":
            depth -= 1
        i += 1
    if depth != 0:
        return None
    body = text[start:i - 1]
    return re.findall(r'"([^"]+)"', body)


def read_covered_buckets(root):
    """(covered, org_buckets, served_buckets) -- covered is the union, read from both declarations."""
    org_path = os.path.join(root, ORG_TRAIL_PATH.replace("/", os.sep))
    served_path = os.path.join(root, SERVED_WRITE_TRAIL_PATH.replace("/", os.sep))
    if not os.path.isfile(org_path):
        raise SystemExit("ERROR: org trail declaration not found: %s" % ORG_TRAIL_PATH)
    if not os.path.isfile(served_path):
        raise SystemExit("ERROR: served-write trail declaration not found: %s" % SERVED_WRITE_TRAIL_PATH)
    with open(org_path, "r", encoding="utf-8") as fh:
        org_text = fh.read()
    with open(served_path, "r", encoding="utf-8") as fh:
        served_text = fh.read()
    org_list = _extract_bucket_list(org_text, ORG_TRAIL_LOCAL)
    served_list = _extract_bucket_list(served_text, SERVED_TRAIL_LOCAL)
    if org_list is None:
        raise SystemExit("ERROR: local.%s not found in %s" % (ORG_TRAIL_LOCAL, ORG_TRAIL_PATH))
    if served_list is None:
        raise SystemExit("ERROR: local.%s not found in %s" % (SERVED_TRAIL_LOCAL, SERVED_WRITE_TRAIL_PATH))
    org_buckets = set(org_list)
    served_buckets = set(served_list)
    return org_buckets | served_buckets, org_buckets, served_buckets


def grade(rows, covered):
    """Returns (rc, lines). rc is non-zero iff any NOT_A_PRINCIPAL row fails the rule."""
    rc = 0
    lines = []
    for row in rows:
        role = row.get("role") or "<unnamed-role>"
        bucket = row.get("bucket") or "<unnamed-bucket>"
        disposition = row.get("disposition") or "<no-disposition>"
        if disposition != "NOT_A_PRINCIPAL":
            lines.append(
                "SKIP: role=%s bucket=%s disposition=%s -- not a NOT_A_PRINCIPAL claim, "
                "this guard does not grade it" % (role, bucket, disposition)
            )
            continue
        if bucket not in covered:
            rc = 1
            lines.append(
                "REFUSED: role=%s bucket=%s disposition=NOT_A_PRINCIPAL -- bucket %s carries no live "
                "CloudTrail data-event selector (absent from both the org trail's ReadOnly list and the "
                "served-key write trail's WriteOnly list); silence in a trail that never covered the "
                "bucket is never evidence (R-30 parts 1 and 4)" % (role, bucket, bucket)
            )
            continue
        evidence = row.get("evidence") or ""
        if not str(evidence).strip():
            rc = 1
            lines.append(
                "REFUSED: role=%s bucket=%s disposition=NOT_A_PRINCIPAL -- bucket %s is covered by a "
                "live data-event selector but the row carries no evidence" % (role, bucket, bucket)
            )
            continue
        lines.append(
            "ACCEPTED: role=%s bucket=%s disposition=NOT_A_PRINCIPAL -- bucket %s is covered by a live "
            "data-event selector and the row carries evidence" % (role, bucket, bucket)
        )
    return rc, lines


def run(claim_path, root):
    covered, org_buckets, served_buckets = read_covered_buckets(root)
    print(
        "DENOMINATOR: %d covered bucket(s) (%d in the org trail's ReadOnly data-event selector, %d in "
        "the served-key write trail's WriteOnly data-event selector, union counted once)"
        % (len(covered), len(org_buckets), len(served_buckets))
    )
    with open(claim_path, "r", encoding="utf-8") as fh:
        claim = json.load(fh)
    rows = claim.get("rows") or []
    rc, lines = grade(rows, covered)
    for line in lines:
        print(line)
    return rc


def self_test(root):
    covered, org_buckets, served_buckets = read_covered_buckets(root)
    print(
        "DENOMINATOR: %d covered bucket(s) (%d in the org trail's ReadOnly data-event selector, %d in "
        "the served-key write trail's WriteOnly data-event selector, union counted once)"
        % (len(covered), len(org_buckets), len(served_buckets))
    )

    results = []

    # Arm 1: a planted NOT_A_PRINCIPAL claim on opal-data-demo -- must be REFUSED.
    if UNCOVERED_PROBE_BUCKET in covered:
        print(
            "SELF-TEST SETUP ERROR: %s is covered at this tree, so it is not the negative probe R-30 "
            "names" % UNCOVERED_PROBE_BUCKET
        )
        return 2
    rows_uncovered = [{
        "role": "planted-probe-role-uncovered",
        "bucket": UNCOVERED_PROBE_BUCKET,
        "disposition": "NOT_A_PRINCIPAL",
        "evidence": "planted by --self-test: CloudTrail data events show nothing for this role, but "
                    "the bucket carries no data-event selector at all",
    }]
    rc_uncovered, lines_uncovered = grade(rows_uncovered, covered)
    for line in lines_uncovered:
        print("ARM1 (uncovered, must refuse): %s" % line)
    arm1_ok = rc_uncovered != 0
    results.append(("uncovered-bucket-claim-refused", arm1_ok))

    # Arm 2: a planted NOT_A_PRINCIPAL claim on a covered bucket, with evidence -- must be ACCEPTED.
    covered_candidates = sorted(b for b in covered if b != UNCOVERED_PROBE_BUCKET)
    if not covered_candidates:
        print("SELF-TEST SETUP ERROR: no covered candidate bucket could be read from the trail declarations")
        return 2
    covered_bucket = covered_candidates[0]
    rows_covered = [{
        "role": "planted-probe-role-covered",
        "bucket": covered_bucket,
        "disposition": "NOT_A_PRINCIPAL",
        "evidence": "planted by --self-test: a covered bucket, 0 events in a stated 90-day CloudTrail "
                    "lookup-events window, query and count recorded",
    }]
    rc_covered, lines_covered = grade(rows_covered, covered)
    for line in lines_covered:
        print("ARM2 (covered, must accept): %s" % line)
    arm2_ok = rc_covered == 0
    results.append(("covered-bucket-claim-accepted", arm2_ok))

    passed = sum(1 for _name, ok in results if ok)
    total = len(results)
    for name, ok in results:
        print("  %-32s %s" % (name, "PASS" if ok else "FAIL"))
    print("SELF-TEST: %d of %d PASSED" % (passed, total))
    return 0 if passed == total else 1


def main(argv):
    if len(argv) == 2 and argv[1] == "--self-test":
        return self_test(os.getcwd())
    if len(argv) != 2:
        print("USAGE: python fence_disposition_check.py <claim.json> | --self-test")
        return 2
    return run(argv[1], os.getcwd())


if __name__ == "__main__":
    sys.exit(main(sys.argv))
