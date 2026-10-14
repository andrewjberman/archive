"""AR332-y-AC3 -- the scope of the candidate branch (0.9.0_WK_IRPT_ANLREQ~140).

Prints SCOPE-OK only when:
 (1) `git diff --name-only origin/PROD <candidate>` lists only: src/api/endpoints/investor-reporting.ts,
     src/pages/TicketCenter/AnalysisRequestParts.tsx, files under src/pages/TicketCenter/__tests__/, and files
     under src/pages/InvestorReporting/;
 (2) every changed line under src/pages/InvestorReporting/ and in investor-reporting.ts is one of:
       - a line that mentions the operation: analysis-request-commentary-pdf, AnalysisRequestCommentaryPdf
         (the type and the client method), or commentary-pdf (the route's path segment);
       - an insertion in a hunk that also inserts such a line (a block of the new operation, e.g. a JSON entry);
       - a count that rose by ONE, paired with a removed line that holds the same text but for that number;
       - any line of a file whose own path names the operation (the new request record);
 (3) no changed line removes or edits an entry for any other operation: a removed line is valid only as the
     count pair above, or as the same line with an insertion that names the operation.
Otherwise prints SCOPE-BAD <why> and exits 1.

The candidate is compared with origin/PROD as the criterion states it; the record's prod_tip is that same commit.
"""
import difflib
import re
import subprocess
import sys

WT = 'C:/dev/wk-irpt-anlreq-140'
PORTAL = WT + '/portal'
CANDIDATE = 'cand/dell2/anlreq-ticket-commentary-pdf-reader'
TOKENS = ('analysis-request-commentary-pdf', 'AnalysisRequestCommentaryPdf', 'commentary-pdf')
ALLOWED_EXACT = ('src/api/endpoints/investor-reporting.ts', 'src/pages/TicketCenter/AnalysisRequestParts.tsx')
ALLOWED_PREFIX = ('src/pages/TicketCenter/__tests__/', 'src/pages/InvestorReporting/')
IR_PREFIX = 'src/pages/InvestorReporting/'


def bad(why):
    print('SCOPE-BAD ' + why)
    sys.exit(1)


def git(*args):
    res = subprocess.run(['git', '-C', PORTAL] + list(args), capture_output=True, text=True)
    if res.returncode != 0:
        bad('git %s failed (rc=%d): %s' % (' '.join(args), res.returncode, res.stderr.strip()[:200]))
    return res.stdout


def mentions(text):
    return any(token in text for token in TOKENS)


def count_pair(removed, added):
    """True when the two lines differ only by numbers, and at least one number rose by exactly one."""
    nr = re.findall(r'\d+', removed)
    na = re.findall(r'\d+', added)
    if not nr or len(nr) != len(na) or nr == na:
        return False
    if re.sub(r'\d+', '#', removed) != re.sub(r'\d+', '#', added):
        return False
    pairs = list(zip(nr, na))
    if not all(int(y) == int(x) or int(y) == int(x) + 1 for x, y in pairs):
        return False
    return any(int(y) == int(x) + 1 for x, y in pairs)


def insertion_naming(removed, added):
    """True when `added` is `removed` with only inserted text, and the inserted text names the operation."""
    ops = difflib.SequenceMatcher(None, removed, added, autojunk=False).get_opcodes()
    if any(tag not in ('equal', 'insert') for tag, _, _, _, _ in ops):
        return False
    inserted = ''.join(added[j1:j2] for tag, _, _, j1, j2 in ops if tag == 'insert')
    return mentions(inserted)


def partner(removed, added_lines):
    return any(count_pair(removed, a) or insertion_naming(removed, a) for a in added_lines)


def parse_hunks(diff_text):
    """Yield (path, removed_lines, added_lines) per hunk, from a -U0 diff."""
    path = None
    removed, added = [], []
    hunks = []

    def flush():
        if path is not None and (removed or added):
            hunks.append((path, list(removed), list(added)))

    for line in diff_text.split('\n'):
        if line.startswith('diff --git '):
            flush()
            removed, added = [], []
            path = None
        elif line.startswith('+++ '):
            target = line[4:].strip()
            path = target[2:] if target.startswith('b/') else None
        elif line.startswith('@@'):
            flush()
            removed, added = [], []
        elif line.startswith('-') and not line.startswith('---'):
            removed.append(line[1:])
        elif line.startswith('+') and not line.startswith('+++'):
            added.append(line[1:])
    flush()
    return hunks


def main():
    names = [n for n in git('diff', '--name-only', 'origin/PROD', CANDIDATE).split('\n') if n.strip()]
    if not names:
        bad('the candidate changes no file against origin/PROD')
    for name in names:
        if name not in ALLOWED_EXACT and not name.startswith(ALLOWED_PREFIX):
            bad('file outside the granted scope: ' + name)

    checked = [n for n in names if n == 'src/api/endpoints/investor-reporting.ts' or n.startswith(IR_PREFIX)]
    if not checked:
        bad('no file under the InvestorReporting scope to check')
    diff = git('diff', '-U0', 'origin/PROD', CANDIDATE, '--', *checked)
    hunks = parse_hunks(diff)
    line_count = 0
    for path, removed, added in hunks:
        line_count += len(removed) + len(added)
        if mentions(path):
            continue  # a file that is the new operation's own (its path names it)
        if not removed:
            if not any(mentions(a) for a in added):
                bad('added lines in %s with no mention of the operation: %s' % (path, (added[0] if added else '')[:90]))
            continue
        for r in removed:
            if not partner(r, added):
                bad('removed line in %s is neither a count that rose by one nor a commentary insertion: %s' % (path, r.strip()[:90]))
        for a in added:
            if not mentions(a) and not any(count_pair(r, a) or insertion_naming(r, a) for r in removed):
                bad('added line in %s is unexplained: %s' % (path, a.strip()[:90]))
    print('SCOPE-OK %d files (%d checked under InvestorReporting or investor-reporting.ts), %d hunks, %d changed lines'
          % (len(names), len(checked), len(hunks), line_count))
    sys.exit(0)


if __name__ == '__main__':
    main()
