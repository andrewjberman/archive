"""TCKT_VNEXT -- the issuer's REVIEW of the meeting hunks in a PROD-into-DEV reconcile branch (the CTO's msg 10553: 2.0.0_SA_COO~Y2 merges origin/PROD into a branch from origin/DEV; this seat reviews the meeting form and outcome-line hunks before the push).

  python r20_reconcile_review.py <ref>            e.g. origin/cand/dell2/prod-into-dev-reconcile  (read-only; the portal repo is `portal`)
  python r20_reconcile_review.py --self-test      the counting on fixtures (no git)

For each meeting-related pattern it prints the count in origin/DEV, in origin/PROD and in <ref> for the file that carries it. The meeting hunks are ONE feature that reached PROD as cherry-picks of work already on DEV, so after the reconcile every pattern must read the same as origin/DEV (each change once, none doubled, none lost). It also compares the three meeting files and the two meeting test files byte for byte against origin/DEV, and scans <ref> for the Trade Request upload strings (they live on DEV only; the reconcile must not ADD them to PROD's side, and must not lose DEV's).
Prints REVIEW-OK <n checks> or REVIEW-FINDINGS <list>; exit 0/1. It does not run tests or tsc: run `r20_pf_checks.py pf-tests --portal <worktree>` and `r20_checks.py portal-tsc --portal <worktree>` on a scratch worktree of <ref>, and `bun x eslint` for the zero-errors condition.
"""
import re
import subprocess
import sys

PORTAL = "portal"
PARTS = "src/pages/TicketCenter/MeetingRequestParts.tsx"
TC = "src/pages/TicketCenter/TicketCenter.tsx"
TK = "src/api/endpoints/tickets.ts"
TESTS = ["src/pages/TicketCenter/__tests__/meeting-request.test.tsx",
         "src/pages/TicketCenter/__tests__/meeting-outcome-visibility.test.tsx",
         "src/pages/TicketCenter/__tests__/meeting-outcome-contrast.test.tsx"]
# (file, label, regex): counted in DEV, PROD and the ref; the ref must equal DEV
PATTERNS = [
    (PARTS, "showsMeetingOutcome defined", r"export function showsMeetingOutcome\("),
    (PARTS, "viewerIsCoordinator defined", r"export function viewerIsCoordinator\("),
    (PARTS, "drawsOwnForm defined", r"export function drawsOwnForm\("),
    (PARTS, "outcome line light ink", r'className="text-xs font-medium text-white/80"'),
    (PARTS, "outcome line navy ink (must be 0)", r"data-slot=\"meeting-outcome-line\" className=\{`[^`]*\$\{INK\}"),
    (TC, "meeting parts import block", r"from './MeetingRequestParts'"),
    (TC, "showsMeetingOutcome used", r"showsMeetingOutcome\(t\)"),
    (TC, "viewerIsCoordinator used", r"viewerIsCoordinator\(t, auth\.user\?\.email\)"),
    (TC, "MeetingRequestForm branch", r"newType === 'meeting_request'"),
    (TC, "drawsOwnForm guards", r"drawsOwnForm\(newType\)"),
    (TC, "Trade Request hidden from the type list", r"v !== 'trade_request'"),
    (TK, "recordMeetingOutcome defined", r"recordMeetingOutcome"),
    (TK, "TicketMeeting type", r"interface TicketMeeting|type TicketMeeting"),
    (TK, "meeting_request ticket type", r"meeting_request"),
]
TRADE = ["TradeFormOpen", "trade-form-upload", "This is the placeholder form", "attachment-upload"]


def git(*args):
    return subprocess.run(["git", "-C", PORTAL] + list(args), capture_output=True, text=True, timeout=120)


def show(ref, path):
    r = git("show", "%s:%s" % (ref, path))
    return r.stdout if r.returncode == 0 else None


def count(text, rx):
    return None if text is None else len(re.findall(rx, text))


def review(ref):
    findings, n = [], 0
    rows = []
    for path, label, rx in PATTERNS:
        c = {name: count(show(r, path), rx) for name, r in (("DEV", "origin/DEV"), ("PROD", "origin/PROD"), ("REF", ref))}
        rows.append((label, c))
        n += 1
        if c["REF"] is None:
            findings.append("%s: %s absent in the ref" % (label, path))
        elif c["DEV"] is not None and c["REF"] != c["DEV"]:
            findings.append("%s: ref %s but DEV %s (PROD %s)" % (label, c["REF"], c["DEV"], c["PROD"]))
    for path in [PARTS] + TESTS:
        n += 1
        a, b = show("origin/DEV", path), show(ref, path)
        if b is None:
            findings.append("%s absent in the ref" % path)
        elif a is not None and a != b:
            findings.append("%s differs from origin/DEV" % path)
    for token in TRADE:
        n += 1
        dev = sum((show("origin/DEV", p) or "").count(token) for p in (PARTS, TC, TK, "src/pages/TicketCenter/TradeRequestParts.tsx"))
        got = sum((show(ref, p) or "").count(token) for p in (PARTS, TC, TK, "src/pages/TicketCenter/TradeRequestParts.tsx"))
        if got != dev:
            findings.append("Trade Request string %r: ref %d but DEV %d (the reconcile must neither add nor lose DEV's)" % (token, got, dev))
    for label, c in rows:
        print("  %-42s DEV %-4s PROD %-4s REF %-4s" % (label, c["DEV"], c["PROD"], c["REF"]))
    return n, findings


def self_test():
    if count("a showsMeetingOutcome( b showsMeetingOutcome(", r"showsMeetingOutcome\(") != 2:
        return "count wrong"
    if count(None, "x") is not None:
        return "None not propagated"
    return None


def main(argv):
    if argv[:1] == ["--self-test"]:
        why = self_test()
        print("R20-REVIEW-SELFTEST-OK" if why is None else "R20-REVIEW-SELFTEST-FAIL " + why)
        return 0 if why is None else 1
    if len(argv) != 1:
        print("usage: r20_reconcile_review.py <ref> | --self-test")
        return 2
    n, findings = review(argv[0])
    if findings:
        print("REVIEW-FINDINGS " + " | ".join(findings))
        return 1
    print("REVIEW-OK %d checks: every meeting pattern in %s equals origin/DEV, the meeting files and tests are byte-identical to DEV, no Trade Request string added or lost" % (n, argv[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
