#!/usr/bin/env python
"""OG-ap-19 Phase B step 6: write the TRUNK EC2_MANIFEST record for the G3/G6 release.

Same shape as hv2_manifest_record.py and for the same two reasons: the deploy wrapper writes its
record on the branch it RUNS from (here rel-nfra-oplgtw-yr2, which never merges to box/sitez), and it
never recomputes file_checksums. Measured here: that branch's pre-image carried deployed_commit
a value older than trunk's, because the release worktree is cut at a base whose manifest predates
later deploys -- so MERGING that commit to trunk would REGRESS the record. Trunk's own value is the only
correct previous_deployed_commit. Measured again here: the wrapper's commit 5f4278f22d sits on the
release branch, which never merges to box/sitez.

ONE LIMB THIS ADDS over the hv-2 version: every recomputed checksum is cross-checked against the md5
the HOST actually reported for that path in W/YR_SERVED.json, and a disagreement REFUSES the write.
`git show <release>:<path>` reads the BLOB, and the page in this very release proves blob and shipped
bytes can differ (eol=lf: blob 3bbd5ab2, shipped 0d828b51). None of the ten keys is that path, but
"none of them is affected" is a claim, so it is measured rather than asserted.

WHAT IT REFUSES TO DO: anything if the outside-span bytes would change, if any replacement does not
hit exactly once, if the result does not parse, if the key set of the entry changes, if ANY other
service's entry differs afterwards, or if a recomputed checksum disagrees with the measured host md5.

Usage: python org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/yr_manifest_record.py
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys

MANIFEST = "infra/aws/ec2/EC2_MANIFEST.json"
SERVED = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/G36_SERVED.json"
SERVICE = "opal-gateway"
RELEASE = "ee23dd004c985c46d479908db46d2ad9b4f3b1c8"
BASE = "047f11aa991e5c7ed188876f07a8599447cf2849"
DEPLOYED_AT = "2026-10-15T04:23:28Z"          # the wrapper's own write, read back from its commit
DEPLOYED_BY = "0.7.0_AE_CloudOps~Z"
GW = "infra/aws/ec2/opal-gateway"

NOTE = (
    "NFRA_OPLGTW OG-ap-19 (round 37, workstream G3G6-RELEASE, FWD-22): release commit " + RELEASE
    + " (branch rel-nfra-oplgtw-g36, local, never merged; SIXTEEN files vs " + BASE
    + ") deployed " + DEPLOYED_AT + " with DEPLOY_BASE_REF=" + BASE
    + " (the stale-base guard read the live ref at both checkpoints and it was equal both times); SSM"
    + " 54b35429-625f-4ec0-98f1-eb45112c03eb Success. THIRTEEN READ TOOLS go live, eight G3 portal and five G6"
    + " news: portal_get_model_positioning, portal_get_model_attribution, portal_get_market_returns,"
    + " portal_get_market_regime, portal_get_macro, portal_get_valuation, portal_get_security_scan,"
    + " portal_get_pipeline_freshness, news_search_articles, news_trending_topics, news_keyword_intelligence,"
    + " news_market_mood and news_for_security -- all SAFE in destructive_ops and legacy class in"
    + " data_entitlement (NATIVE_TOOLS), each admitting through the typed_scope seam before any read."
    + " TWO GRANTS, ON TWO DIFFERENT PRINCIPALS, applied ONE AT A TIME through safe-apply with an IAM read-back"
    + " between them: gateway-global-news-read-policy on the GATEWAY INSTANCE role opal-gateway-role"
    + " (dynamodb:Query and dynamodb:GetItem on opal-news-articles, opal-news-trending-daily,"
    + " opal-keyword-intelligence and that table index/date-index, 1 statement, no wildcard), and"
    + " gateway-global-portal-tiered-read-policy on the ASSUMED internal reader role"
    + " gateway-global-internal-reader-role (s3:GetObject on exactly"
    + " arn:aws:s3:::opal-data-portal-v2/json-tiered/market-overview/*, 1 statement, no wildcard). The G3"
    + " resource list was DERIVED from the code by AST, not typed: 12 prefixes the modules read, 9 already covered"
    + " by the pre-existing json/* grant, 3 residue, 1 after an asserted collapse -- and three readings of the"
    + " bucket (the code, the naming registry, the live policy) had to agree before the generator emitted"
    + " anything. The pre-existing gateway-global-internal-reader-policy is PROVEN UNTOUCHED: its Resource list"
    + " read [json/*, platinum/*] both before and after. ONE FILE RODE THAT THE ORDER DID NOT LIST:"
    + " app/typed_scope.py, the scope seam from cell OG-gt-6, without which app/tools.py cannot import"
    + " portal_models at start-up and the service would not have come back -- ruled in by amendment A2 after this"
    + " seat found it with the order's own host-shaped import check and refused to ship a release that could not"
    + " start (row Z-S137, resolved by Z-S138). Read-back, all against the INSTALLED code (W/G36_SERVED.json,"
    + " verdict PASS): /health {\"ok\":true}; 117 of 117 files under app/, deploy/ AND lib/ md5-EQUAL to the"
    + " release with 0 mismatches and 0 paths on either side only; app/typed_scope.py on the host at md5"
    + " 15a9301c165f89756daaef9f8a483673; the three NEWS_* .env key NAMES present where the pre-deploy read"
    + " measured zero of them; the registry 56 -> 69 on ONE named instrument"
    + " (app.tools.mcp._tool_manager.list_tools()), delta exactly 13, with the repo-side pin reported separately"
    + " as the different instrument it is (75 -> 88) and OG-ap-18 19-name INTEGRATION|INDEX identity re-checked"
    + " and still holding; all THIRTEEN tools serving an enveloped answer to an Opal principal and refusing a"
    + " non-Opal one, with ZERO reads on any refusal path measured by TWO counters -- S3 for the eight G3 tools"
    + " and DynamoDB for the five G6 tools, because one counter would have left the news tools unguarded while"
    + " reporting a clean zero; and a numeric trading_days_behind_t1 where a tool states freshness. The CVO ALB"
    + " condition is DECLARED rather than implied: every one of the thirteen runs far under the 60 s idle timeout"
    + " (slowest news_for_security 7.29 s, the rest under 1 s, no 502/504), which is what the condition turns on,"
    + " but the AUTHENTICATED end-to-end call through mcp.opalinvest.dev was not performed by this seat -- the"
    + " edge demands a per-user delegated Bearer, minting one is stop-the-line, and this seat own live connection"
    + " to that endpoint carries a tool catalogue predating the deploy. Halves, all three signed at this"
    + " release_sha on ask sha256 cdefc9a139a4: CTO acd42eab53, COO 1fab9a19d5, CVO 80cddeb748. Rollback:"
    + " redeploy " + BASE + " through safe-ec2-deploy.sh with DEPLOY_BASE_REF=" + RELEASE + ", and destroy the two"
    + " policies through safe-apply targeted by name -- aws_iam_role_policy.gw_news_read and"
    + " aws_iam_role_policy.portal_tiered_read, which are the only keys these acts created; the internal reader"
    + " pre-existing policy is a DIFFERENT name and must not be touched. A rollback leaves"
    + " /opt/opal-gateway/lib/ in place (OG-ap-18 member) and removes typed_scope.py with the thirteen tools."
    + " Ledger nfra-oplgtw-gateway-release-g36. NOTE on safe-apply: it must run from the REPO ROOT with -chdir,"
    + " or its naming limb resolves infra/logic/registry/root_map.json against the CWD, cannot find it, and"
    + " REFUSES the addition fail-closed; it blocked that way once and applied nothing."
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
