"""AR364-y-AC3: the shared prospect.ts must not move. Prints SCOPE-OK only when the candidate branch changes paths under
src/pages/TicketCenter/ alone and src/api plus src/pages/InvestorReporting carry no diff against a168015b; otherwise
SCOPE-BAD <why>, exit 1.
"""
import subprocess
import sys

PORTAL = 'C:/dev/wk-irpt-anlreq-161/portal'
BASE = 'a168015b'
BRANCH = 'cand/dell2/anlreq-filing-decision-tree-gate'
ALLOWED = 'src/pages/TicketCenter/'


def git(*args):
    r = subprocess.run(['git', '-C', PORTAL] + list(args), capture_output=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError('git %s rc=%d: %s' % (' '.join(args), r.returncode, r.stderr.decode('utf-8', 'replace').strip()))
    return r.stdout.decode('utf-8', 'replace')


def main():
    try:
        names = [n for n in git('diff', '--name-only', BASE, BRANCH).splitlines() if n.strip()]
        if not names:
            print('SCOPE-BAD no changed paths between %s and %s' % (BASE, BRANCH))
            return 1
        outside = [n for n in names if not n.startswith(ALLOWED)]
        if outside:
            print('SCOPE-BAD paths outside %s: %s' % (ALLOWED, ', '.join(outside)))
            return 1
        shared = git('diff', BASE, BRANCH, '--', 'src/api', 'src/pages/InvestorReporting')
        if shared.strip():
            print('SCOPE-BAD shared paths carry a diff (src/api or src/pages/InvestorReporting)')
            return 1
    except (RuntimeError, subprocess.TimeoutExpired) as e:
        print('SCOPE-BAD %s' % e)
        return 1
    print('SCOPE-OK %d paths, all under %s; src/api and src/pages/InvestorReporting diff empty' % (len(names), ALLOWED))
    return 0


if __name__ == '__main__':
    sys.exit(main())
