#!/usr/bin/env python3
"""POSN_AGGFIX.TO-B1-1 / B1-AC1 (cell AF1-s-3) -- THE PAGE'S PREDICATE, READ AT THE BASE.

Reads portal edf85ce503 through git objects only (never the working tree, which this worker
edits later): the isInternal and isDev bodies, every line in AuthContext.tsx that names
firmId or userType (denominator printed), the sites where claims are built and what each
builds them FROM, and the page's own predicate line in Positioning.tsx. Prints the predicate
as READ, and one line per viewer class it admits beyond firmId opal-capital.

Usage (from the workspace root): python <this>
"""
import os
import re
import subprocess
import sys

BASE = 'edf85ce503'
HERE = os.path.dirname(os.path.abspath(__file__))


def run(argv):
    r = subprocess.run(argv, capture_output=True)
    return r.returncode, r.stdout.decode('utf-8', 'replace'), r.stderr.decode('utf-8', 'replace')


rc, root, err = run(['git', '-C', HERE, 'rev-parse', '--show-toplevel'])
if rc != 0:
    print('ERROR: cannot resolve the workspace root: ' + err.strip())
    sys.exit(2)
PORTAL = os.path.join(root.strip(), 'portal')

rc, full, err = run(['git', '-C', PORTAL, 'rev-parse', BASE + '^{commit}'])
if rc != 0:
    print('ERROR: base ' + BASE + ' does not resolve in the portal repo: ' + err.strip())
    sys.exit(2)
print('BASE: portal ' + BASE + ' = ' + full.strip())


def show(path):
    rc, out, err = run(['git', '-C', PORTAL, 'show', BASE + ':' + path])
    if rc != 0 or not out:
        # A git show that fails returns an EMPTY string; an empty file here would read as
        # "no predicate", so the absence is refused rather than reported.
        print('ERROR: git show ' + BASE + ':' + path + ' rc=' + str(rc) + ' ' + err.strip())
        sys.exit(1)
    lines = out.split('\n')
    if lines and lines[-1] == '':
        lines = lines[:-1]
    print('READ: ' + BASE + ':' + path + '  (' + str(len(lines)) + ' lines, ' + str(len(out)) + ' chars)')
    return lines


AUTH = 'src/contexts/AuthContext.tsx'
PAGE = 'src/pages/Positioning/Positioning.tsx'
auth = show(AUTH)
page = show(PAGE)


def body(lines, opener):
    """Print a useCallback body from its opener through its dependency-array line."""
    for i, ln in enumerate(lines):
        if opener in ln:
            out = []
            for j in range(i, min(i + 12, len(lines))):
                out.append((j + 1, lines[j]))
                if re.match(r'^\s*\}, \[', lines[j]):
                    break
            return out
    return []


print('')
print('=== isInternal and isDev bodies (' + AUTH + ' @' + BASE + ') ===')
bodies = {}
for name in ('isInternal', 'isDev'):
    b = body(auth, 'const ' + name + ' = useCallback')
    bodies[name] = b
    if not b:
        print('ERROR: ' + name + ' body NOT FOUND')
        sys.exit(1)
    for n, t in b:
        print('  :' + str(n) + '  ' + t)

print('')
print('=== every line in ' + AUTH + ' naming firmId or userType (DENOMINATOR = all such lines) ===')
hits = [(i + 1, ln) for i, ln in enumerate(auth) if re.search(r'\b(firmId|userType)\b', ln)]
for n, t in hits:
    print('  :' + str(n) + '  ' + t.strip())
print('  DENOMINATOR: ' + str(len(hits)) + ' line(s) of ' + str(len(auth)))

print('')
print('=== where claims.firmId and claims.userType are ASSIGNED, and from what source ===')
# 1. the parser: the only place a claims object is built from a server payload.
for i, ln in enumerate(auth):
    if re.search(r'^function parseClaims\(', ln):
        print('  :' + str(i + 1) + '  ' + ln.strip() + '   <- the parser (input: the server user record)')
    if re.search(r"const userType = userData\.userType === 'Dev'", ln):
        print('  :' + str(i + 1) + '  ' + ln.strip() + "   <- userType: 'Dev' ONLY when the server sends exactly 'Dev', else null")
    if re.search(r'firmId: parseNullable\(userData\.firmId\)', ln):
        print('  :' + str(i + 1) + '  ' + ln.strip() + '   <- firmId: the server value verbatim (string "null" -> null)')
# 2. every caller of the parser, with the lines that name the payload it is handed.
callers = [i for i, ln in enumerate(auth) if 'parseClaims(' in ln and not ln.lstrip().startswith('function')]
print('  parseClaims CALL SITES: ' + str(len(callers)))
for i in callers:
    src = ''
    for j in range(max(0, i - 16), i + 1):
        m = re.search(r'fetch\(`\$\{API_BASE\}(/auth/[a-z-]+)`', auth[j])
        if m:
            src = m.group(1)
    print('    :' + str(i + 1) + '  ' + auth[i].strip() + '   <- payload of ' + (src or '(no fetch within 16 lines above)'))
# 3. every OTHER line that writes firmId or userType, classified by the object it sits in: a claims object built
#    without the parser, or an analytics payload that only READS claims (never an assignment to them).
print('  every other firmId/userType write, by the object it sits in:')
for i, ln in enumerate(auth):
    if not re.search(r'\b(firmId|userType)\b\s*:', ln) or re.search(r'^\s*(firmId|userType)\?:', ln):
        continue
    if 'parseNullable(userData.firmId)' in ln or re.match(r'^\s*userType,\s*$', ln):
        continue
    if re.search(r'\((firmId|userType)\s*:', ln):
        continue   # a function PARAMETER named firmId (canAccessFirm), not a write to any object
    window = ' '.join(x.strip() for x in auth[max(0, i - 8):i + 1])
    if re.search(r'claims\s*=\s*\{', ln):
        kind = 'a LITERAL claims object assigned here (no parser): every claim null'
        j = i
        while j > max(0, i - 12) and 'fetch(' not in auth[j]:
            j -= 1
        kind += ' -- inside the branch after the fetch at :' + str(j + 1) + ': ' + auth[j].strip()[:70]
    elif 'devClaims' in window:
        kind = 'devBypass devClaims (DEV-ONLY: window.__devBypass under import.meta.env.DEV)'
    elif 'OpalAnalytics.init' in window:
        kind = 'OpalAnalytics.init user payload -- READS claims, assigns nothing to them'
    else:
        kind = 'UNCLASSIFIED -- read the line'
    print('    :' + str(i + 1) + '  ' + ln.strip() + '   <- ' + kind)

print('')
print('=== the page predicate (' + PAGE + ' @' + BASE + ') ===')
page_auth = [(i + 1, ln) for i, ln in enumerate(page) if 'useAuth()' in ln]
page_pred = [(i + 1, ln) for i, ln in enumerate(page) if re.search(r'const internal = ', ln)]
for n, t in page_auth + page_pred:
    print('  :' + str(n) + '  ' + t.strip())

internal_txt = ' '.join(t for _, t in bodies['isInternal'])
dev_txt = ' '.join(t for _, t in bodies['isDev'])
ok_internal = "state.claims?.firmId === 'opal-capital'" in internal_txt
ok_dev = "state.claims?.userType === 'Dev'" in dev_txt
ok_page = len(page_pred) == 1 and 'isInternal() || isDev()' in page_pred[0][1]
print('  isInternal reads ONLY firmId === opal-capital : ' + str(ok_internal and 'userType' not in internal_txt))
print('  isDev reads ONLY userType === Dev               : ' + str(ok_dev and 'firmId' not in dev_txt))
print('  page joins them with OR                        : ' + str(ok_page))

print('')
if ok_internal and ok_dev and ok_page:
    print("PAGE PREDICATE: firmId === 'opal-capital' OR userType === 'Dev'")
else:
    print('PAGE PREDICATE: DIFFERS FROM THE EXPECTED FORM -- the bodies above are the reading')

print('')
print('=== viewer classes the predicate admits BEYOND firmId opal-capital ===')
if ok_dev and 'firmId' not in dev_txt:
    print("ADMITTED BEYOND OPAL STAFF: a viewer whose server-issued userType is 'Dev' at ANY firmId other than "
          "'opal-capital' -- isDev (:" + str(bodies['isDev'][0][0]) + '-' + str(bodies['isDev'][-1][0]) +
          ') does not read firmId, so the page treats a Dev-typed partner-firm account as internal.')
print('NOT ADMITTED (read from the same file): claims null (auth unresolved; ProtectedRoute holds the page), '
      "firmId null (/auth/me failed), a partner advisor or partner user (userType null, firmId a partner slug), "
      "and devBypass(advisorRole) (userType null, firmId VITE_DEV_FIRM_ID).")
print("INSIDE OPAL STAFF, NOT BEYOND: devBypass() with no argument mints firmId 'opal-capital' AND userType 'Dev' "
      '(DEV builds only).')
print("NOT READ HERE, STATED: whether any ISSUED account carries userType 'Dev' with a firmId other than "
      "'opal-capital' is a fact of the auth plane, not of this file; the portal cannot answer it.")
