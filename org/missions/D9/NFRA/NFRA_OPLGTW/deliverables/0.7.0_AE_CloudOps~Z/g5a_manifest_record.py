#!/usr/bin/env python
"""OG-ap-20 Phase B step 8: write the TRUNK EC2_MANIFEST record for the G5 wave A / category-views release.

Same shape as g36_manifest_record.py and for the same two reasons, both re-measured here rather than
inherited:

 1. THE DEPLOY WRAPPER WRITES ITS RECORD ON THE BRANCH IT RAN FROM. Its commit is cf59f54019 on
    rel-nfra-oplgtw-g5a, which never merges to box/sitez, so trunk's manifest is untouched by the
    deploy (measured: git status reports EC2_MANIFEST.json unmodified on trunk after DEPLOYMENT
    COMPLETE).
 2. AND ITS previous_deployed_commit IS STALE BY CONSTRUCTION. That branch's record reads
    previous_deployed_commit 2c0f84966dc452d367ab1e4fc5d4849f08c1625e, because the release worktree is
    cut at a base whose manifest predates later deploys -- so MERGING that commit to trunk would
    REGRESS the record. Trunk's own value, 1b18b94979d2ba0e4c6eba8ee4a0a5a0cae52bc0, is the only
    correct previous_deployed_commit, and it is what this writes.

The wrapper also never recomputes file_checksums, so they are recomputed here from the RELEASE blobs
and then CROSS-CHECKED against the md5 the HOST actually reported for that same path in
W/G5A_SERVED.json. A disagreement REFUSES the write: `git show <release>:<path>` reads the BLOB, and
OG-yr-1 proved blob and shipped bytes can differ (eol: blob 3bbd5ab2 against shipped 0d828b51), so
"none of these ten keys is affected" is a claim that gets measured rather than asserted.

WHAT IT REFUSES TO DO: anything if the bytes outside the service's own span would change, if any
replacement does not hit exactly once, if the result does not parse, if the entry's key set changes, if
ANY other service's entry differs afterwards, or if a recomputed checksum disagrees with the measured
host md5.
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys

MANIFEST = "infra/aws/ec2/EC2_MANIFEST.json"
SERVED = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/G5A_SERVED.json"
SERVICE = "opal-gateway"
RELEASE = "06cfb6db6471972c7304cd3d7a5b93e6f521ad72"
BASE = "1b18b94979d2ba0e4c6eba8ee4a0a5a0cae52bc0"
DEPLOYED_AT = "2026-10-15T10:49:37Z"          # the wrapper's own write, read back from its commit cf59f54019
DEPLOYED_BY = "0.7.0_AE_CloudOps~Z"
GW = "infra/aws/ec2/opal-gateway"

NOTE = (
    "NFRA_OPLGTW OG-ap-20 (round 37, workstream G5A-CV, FWD-22): release commit " + RELEASE
    + " (branch rel-nfra-oplgtw-g5a, local, never merged; TWELVE files vs " + BASE
    + ") deployed " + DEPLOYED_AT + " with DEPLOY_BASE_REF=" + BASE
    + " (the wrapper's own stale-base guard read the live ref on a SECOND instrument -- s3-metadata"
    + " git-ref on opal-gateway-latest -- at both checkpoints, early and immediately-before-upload, and it"
    + " was equal both times). SIX READ TOOLS go live: etfs_get_partner_ownership,"
    + " etfs_get_ownership_rollup, etfs_get_monthly_report, etfs_get_fund_nav_history,"
    + " etfs_get_fund_holdings and mdpf_get_category_views -- all SAFE in destructive_ops and legacy class"
    + " in data_entitlement (NATIVE_TOOLS), each admitting through typed_scope.admit_scope BEFORE any S3"
    + " call, and each deriving its bucket and served prefixes from its DATA_CATALOG row AT CALL TIME."
    + " ONE GRANT, on the ASSUMED internal reader role gateway-global-internal-reader-role (the identity"
    + " that makes the S3 call), applied through safe-apply targeted and read back from IAM:"
    + " gateway-global-etfs-read-policy on opal-data-etfs, TWO statements -- s3:GetObject on 9 addresses,"
    + " and s3:ListBucket on the bucket ARN confined by an s3:prefix condition to the 7 DIRECTORY prefixes."
    + " TWO OF THE NINE ARE SINGLE OBJECTS AND CARRY NO TRAILING STAR"
    + " (platinum/etf_ownership_dashboard.json, silver/netassets_daily.parquet): an ARN of <key>/* matches"
    + " NOTHING, a silent under-grant whose only symptom is a runtime AccessDenied, so the CVO's second"
    + " condition exercised it and etfs_get_ownership_rollup served source_keys exactly"
    + " [platinum/etf_ownership_dashboard.json] with keys_read 1 and no refusal. The grant is DERIVED, not"
    + " typed: a committed generator reads the named catalog rows and emits the 9 addresses, and the"
    + " catalog at the base is v0.5 md5 5e11a65fca98ce9f570c9aaade49e58c, EQUAL to trunk's, so the tools'"
    + " runtime key reads and the grant cannot disagree. The rival-funds prefixes rivalfunds/etfs/gold/*"
    + " and rivalfunds/etfs/platinum/page/* are granted now and read by NOTHING yet, under the CTO's"
    + " one-ask ruling (msg 34198); the CVO carries that if no released tool reads them by the G5 wave B"
    + " release the next grant edit removes them. THE HOOKUP CARRIED A SEVENTH TOOL THAT THIS RELEASE MUST"
    + " NOT SHIP: OG-gt-12 (3532daff79) sits on a parent that already had OG-gt-5's"
    + " harvest_get_published_analysis, and app/harvest_published.py is ABSENT at this base, so taking the"
    + " 3-way theirs side whole would have written an import of a module that does not exist and the"
    + " gateway would have died at import on the host; every conflict was resolved to the base plus exactly"
    + " the six G5 names, verified structurally by @mcp.tool decorators 69 -> 75, and the two re-pinned"
    + " counts are the BASE'S plus six (88 -> 94 registered, 79 -> 85 non-data) rather than the hookup's"
    + " own 95 and 86 which counted gt-5's tool too. Read-back, all against the INSTALLED code"
    + " (W/G5A_SERVED.json, verdict PASS): /health 200 {\"ok\":true}; 120 of 120 files under app/, deploy/"
    + " AND lib/ md5-EQUAL to the release with 0 mismatches, 0 paths on either side only and 0 explained by"
    + " line endings (dashboard/ is excluded BY GRAIN, being a build product of the mcportal repo at the"
    + " manifest pin, and no md5 verdict is claimed for it); the registry 69 -> 75 on ONE named instrument"
    + " (app.tools.mcp._tool_manager.list_tools()), delta exactly 6, with the repo-side pin reported"
    + " separately as the different instrument it is (88 -> 94); all SIX tools serving an enveloped answer"
    + " to an Opal principal and refusing a non-Opal one with ZERO reads on any refusal path -- the read"
    + " guard was installed on FOUR module clients (etfs_ownership._client, etfs_funds._client,"
    + " portal_mdpf._client, portal_mdpf._s3) because each module builds its own Scope client and a guard on"
    + " typed_scope alone would have left three unguarded while reporting a clean zero; and a numeric"
    + " trading_days_behind_t1 at denominator.trading_days_behind_t1, one level below the answer's top,"
    + " recorded explicitly so no grader reads the top-level null as absent. The probe arguments were"
    + " DERIVED from the host's own catalog at call time and never typed -- firms 49financial, cottonwood,"
    + " inflection; funds DIVZ, IDVZ, PFDE, PFOE; scopes global plus the three firms -- because FIVE of the"
    + " six tools require an argument and a no-argument probe is correctly refused on the contract, which"
    + " would have read as a failing tool. The CVO ALB condition is DECLARED rather than implied: the"
    + " slowest of the six is etfs_get_partner_ownership at 0.5 s against the 60 s idle timeout, no 502 or"
    + " 504, and the edge measured through the ALB answers 401 with a Bearer challenge in 0.144 s so the"
    + " edge and the service behind it are healthy and the auth wall is intact; but the AUTHENTICATED"
    + " end-to-end call of the six through mcp.opalinvest.dev was NOT performed by this seat -- the edge"
    + " demands a per-user delegated Bearer, minting one is stop-the-line, and a search of this seat's own"
    + " live catalogue returns only the OLD etfs_get_positioning, so the six are not callable on it this"
    + " session. Halves, all three signed at this release_sha on ask sha256 47a9c749db1c: CTO d53b7dbba1,"
    + " COO 4ffb7a40c0, CVO d463859c97. The CTO's condition 2 was RULED (msg 34411) satisfied by the cone"
    + " fix, the trunk ENFORCE grade of the grant at f12b5d39bd, and one read proving the release carries"
    + " the SAME BLOB (1efa01e5fd9d3cf66a51e11d0df1568a8f563e95 at both commits, 5181 bytes, with"
    + " app/tools.py as a negative control) -- the release commit's own ENFORCE grade refuses by"
    + " construction, because the S3PREFIX clause derives the committing project from the staged paths and"
    + " a release commit stages release files only (row Z-S144). Rollback: redeploy " + BASE
    + " through safe-ec2-deploy.sh with DEPLOY_BASE_REF=" + RELEASE + ", and destroy the ONE policy through"
    + " safe-apply targeted at aws_iam_role_policy.etfs_read, which is the only key this act created and"
    + " whose prior state was ABSENCE (get-role-policy returned NoSuchEntity immediately before the apply),"
    + " so the destroy returns the role to exactly the three policies it carried; the role's three"
    + " pre-existing policies are DIFFERENT names and must not be touched. Ledger"
    + " nfra-oplgtw-gateway-release-g5a. TWO INSTRUMENT NOTES: safe-apply must run from the REPO ROOT with"
    + " -chdir, or its naming limb resolves infra/logic/registry/root_map.json against the CWD, cannot find"
    + " it and REFUSES fail-closed; and safe-ec2-deploy.sh takes TWO positional arguments, the service name"
    + " AND the deploy script, so a one-argument call dies silently at shift 2 under set -e with rc=1 and"
    + " zero output, which is what it did once here before anything ran."
)


def md5_at(ref: str, path: str) -> str:
    out = subprocess.run(["git", "show", "%s:%s" % (ref, path)], capture_output=True)
    if out.returncode != 0 or not out.stdout:
        raise SystemExit("REFUSED: cannot read %s at %s (a mangled git show returns clean-empty)" % (path, ref))
    return hashlib.md5(out.stdout).hexdigest()


def span(text: str, key: str) -> tuple:
    """The brace-matched VALUE object of services[key]. Naive first-}-after is the OG-ap-14 defect."""
    m = re.search(r'"%s"\s*:\s*\{' % re.escape(key), text)
    if not m:
        raise SystemExit("REFUSED: no %s entry" % key)
    i = text.index("{", m.end() - 1)
    depth, j, instr, esc = 0, i, False, False
    while j < len(text):
        c = text[j]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                instr = False
        elif c == '"':
            instr = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i, j + 1
        j += 1
    raise SystemExit("REFUSED: unbalanced braces")


def main() -> int:
    raw = io.open(MANIFEST, encoding="utf-8").read()
    before = json.loads(raw)
    i, j = span(raw, SERVICE)
    body = raw[i:j]
    print("  span: %d bytes; parses on its own: %s" % (len(body), isinstance(json.loads(body), dict)))

    checks = before["services"][SERVICE]["file_checksums"]
    new_checks = {k: md5_at(RELEASE, "%s/%s" % (GW, k)) for k in checks}
    moved = [k for k in checks if checks[k] != new_checks[k]]
    print("  file_checksums: %d recomputed from the release blobs; %d differ from the record" % (len(new_checks), len(moved)))
    for k in moved:
        print("    moved: %-40s %s -> %s" % (k, checks[k][:12], new_checks[k][:12]))

    # The added limb: the blob md5 must equal what the HOST reported for that same path.
    host = json.load(io.open(SERVED, encoding="utf-8"))["body"]["tree_md5"]
    disagree = [(k, new_checks[k], host.get(k)) for k in new_checks if host.get(k) != new_checks[k]]
    print("  cross-check against the MEASURED host md5s: %d of %d agree" % (len(new_checks) - len(disagree), len(new_checks)))
    if disagree:
        for k, blob, h in disagree:
            print("    DISAGREE: %-40s blob %s  host %s" % (k, blob[:12], str(h)[:12]))
        raise SystemExit("REFUSED: a recomputed checksum disagrees with the running bytes -- the record would be false")

    def one(pat: str, repl: str, what: str) -> None:
        nonlocal body
        n = len(re.findall(pat, body))
        if n != 1:
            raise SystemExit("REFUSED: %s matched %d times in the span, want exactly 1" % (what, n))
        body = re.sub(pat, repl.replace("\\", "\\\\"), body, count=1)

    one(r'"deployed_commit"\s*:\s*"[0-9a-f]{7,40}"', '"deployed_commit": "%s"' % RELEASE, "deployed_commit")
    one(r'"previous_deployed_commit"\s*:\s*"[0-9a-f]{7,40}"',
        '"previous_deployed_commit": "%s"' % BASE, "previous_deployed_commit")
    one(r'"deployed_at"\s*:\s*"[^"]*"', '"deployed_at": "%s"' % DEPLOYED_AT, "deployed_at")
    one(r'"deployed_by"\s*:\s*"[^"]*"', '"deployed_by": "%s"' % DEPLOYED_BY, "deployed_by")

    old_note = before["services"][SERVICE].get("release_note") or ""
    note = NOTE + (" ||| PREVIOUS: " + old_note if old_note else "")
    one(r'"release_note"\s*:\s*"(?:[^"\\]|\\.)*"', '"release_note": ' + json.dumps(note), "release_note")

    # The replacement carries the file's OWN indentation, READ from the block it replaces rather than
    # guessed: a correct value at the wrong indent still lands as 10 rewritten lines inside a
    # never-widen act's diff. Both the entry indent and the closing-brace indent are measured.
    ck_i, ck_j = span(body, "file_checksums")
    block = body[ck_i:ck_j]
    entry_pad = re.search(r'\n(\s*)"', block).group(1)
    close_pad = re.search(r'\n(\s*)\}$', block).group(1)
    body = (body[:ck_i] + "{\n"
            + ",\n".join('%s"%s": "%s"' % (entry_pad, k, new_checks[k]) for k in checks)
            + "\n" + close_pad + "}" + body[ck_j:])

    out = raw[:i] + body + raw[j:]
    after = json.loads(out)                                     # refuses a malformed result
    if raw[:i] != out[:i] or raw[j:] != out[len(out) - len(raw[j:]):]:
        raise SystemExit("REFUSED: bytes outside the span changed")
    for name in sorted(before["services"]):
        if name == SERVICE:
            continue
        if before["services"][name] != after["services"][name]:
            raise SystemExit("REFUSED: sibling service %s changed -- the span over-reached" % name)
    if sorted(before["services"][SERVICE]) != sorted(after["services"][SERVICE]):
        raise SystemExit("REFUSED: the entry's key set changed")
    g = after["services"][SERVICE]
    io.open(MANIFEST, "w", encoding="utf-8", newline="\n").write(out)
    print("  siblings unchanged: %d of %d services compared" % (len(before["services"]) - 1, len(before["services"])))
    print("  WROTE %s: deployed=%s previous=%s checksums=%d note=%d chars"
          % (MANIFEST, g["deployed_commit"][:10], g["previous_deployed_commit"][:10],
             len(g["file_checksums"]), len(g["release_note"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
