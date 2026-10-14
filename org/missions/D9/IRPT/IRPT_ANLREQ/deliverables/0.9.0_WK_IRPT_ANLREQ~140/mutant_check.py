"""AR332-y-AC2 -- the one mutant that must fail (0.9.0_WK_IRPT_ANLREQ~140).

Builds a scratch copy of the portal source OUTSIDE the product tree: every folder is a junction to the candidate
worktree's folder, except the TicketCenter page and its tests, which are real folders. In the copy of
AnalysisRequestParts.tsx the Commentary item is made to open through getAnalysisRequestPdf (the REPORT's PDF).
Runs the new test file against that copy.

Prints MUTANT-FIRES only when that run FAILS (otherwise MUTANT-SURVIVES, exit 1). A control run on the unmutated
copy must pass first; if it does not, the harness is at fault and the result is MUTANT-SURVIVES with that reason.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

WT = 'C:/dev/wk-irpt-anlreq-140'
PORTAL = WT + '/portal'
NEW_TEST = 'src/pages/TicketCenter/__tests__/commentary-pdf-reader.test.tsx'
PAGE = 'src/pages/TicketCenter/AnalysisRequestParts.tsx'
GOOD = 'await ir.getAnalysisRequestCommentaryPdf!(requestId, firm)'
MUTANT = 'await ir.getAnalysisRequestPdf!(requestId, firm)'

JUNCTIONS = []


def out(line):
    print(line)
    sys.exit(1)


def junction(link, target):
    res = subprocess.run(['cmd', '/c', 'mklink', '/J', link.replace('/', '\\'), target.replace('/', '\\')],
                         capture_output=True, text=True)
    if res.returncode != 0 or not os.path.isdir(link):
        raise RuntimeError('junction failed: %s %s' % (link, res.stdout + res.stderr))
    JUNCTIONS.append(link)


def fill(src_dir, dst_dir, skip):
    """Every entry of src_dir except those in skip: a junction for a folder, a copy for a file."""
    for name in os.listdir(src_dir):
        if name in skip:
            continue
        src = os.path.join(src_dir, name)
        dst = os.path.join(dst_dir, name)
        if os.path.isdir(src):
            junction(dst, src)
        else:
            shutil.copy2(src, dst)


def build(root, mutated):
    os.makedirs(root)
    for name in os.listdir(PORTAL):
        src = os.path.join(PORTAL, name)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(root, name))
    junction(os.path.join(root, 'node_modules'), PORTAL + '/node_modules')
    src_root = os.path.join(root, 'src')
    os.makedirs(src_root)
    fill(PORTAL + '/src', src_root, skip={'pages'})
    pages = os.path.join(src_root, 'pages')
    os.makedirs(pages)
    fill(PORTAL + '/src/pages', pages, skip={'TicketCenter'})
    ticket = os.path.join(pages, 'TicketCenter')
    os.makedirs(ticket)
    fill(PORTAL + '/src/pages/TicketCenter', ticket, skip={'AnalysisRequestParts.tsx', '__tests__'})
    with open(os.path.join(PORTAL, PAGE), 'r', encoding='utf-8') as fh:
        text = fh.read()
    if mutated:
        if text.count(GOOD) != 1:
            raise RuntimeError('the commentary call is not found exactly once (%d)' % text.count(GOOD))
        text = text.replace(GOOD, MUTANT)
    with open(os.path.join(ticket, 'AnalysisRequestParts.tsx'), 'w', encoding='utf-8', newline='') as fh:
        fh.write(text)
    tests = os.path.join(ticket, '__tests__')
    os.makedirs(tests)
    fill(PORTAL + '/src/pages/TicketCenter/__tests__', tests, skip={'commentary-pdf-reader.test.tsx'})
    shutil.copy2(os.path.join(PORTAL, NEW_TEST), os.path.join(tests, 'commentary-pdf-reader.test.tsx'))


def run_new_test(root, outdir, label):
    bun = shutil.which('bun')
    if bun is None:
        raise RuntimeError('bun is not on PATH')
    report = os.path.join(outdir, label + '.junit.xml')
    res = subprocess.run(
        [bun, 'test', 'src/pages/TicketCenter/__tests__/commentary-pdf-reader.test.tsx', '--reporter=junit', '--reporter-outfile=' + report],
        cwd=root, capture_output=True, text=True, timeout=600,
    )
    if not os.path.exists(report):
        raise RuntimeError('%s: no junit report (rc=%s)' % (label, res.returncode))
    cases = list(ET.parse(report).getroot().iter('testcase'))
    failed = [c.get('name', '') for c in cases if c.find('failure') is not None or c.find('error') is not None]
    return len(cases), failed, res.returncode


FILE_ATTRIBUTE_REPARSE_POINT = 0x400


def safe_remove(path):
    """Delete a scratch tree WITHOUT entering a junction: a reparse point (junction or symlink) is removed as a link."""
    if not os.path.lexists(path):
        return
    attrs = getattr(os.lstat(path), 'st_file_attributes', 0)
    if attrs & FILE_ATTRIBUTE_REPARSE_POINT:
        os.rmdir(path)
        return
    if os.path.isdir(path):
        for name in os.listdir(path):
            safe_remove(os.path.join(path, name))
        os.rmdir(path)
    else:
        os.remove(path)


def teardown(root):
    if os.path.lexists(root):
        safe_remove(root)


def main():
    scratch = tempfile.mkdtemp(prefix='mutant_', dir=WT + '/.scratch')
    control_root = os.path.join(scratch, 'control')
    mutant_root = os.path.join(scratch, 'mutant')
    try:
        build(control_root, mutated=False)
        n_c, failed_c, rc_c = run_new_test(control_root, scratch, 'control')
        if failed_c or n_c == 0:
            out('MUTANT-SURVIVES harness control failed on the unmutated copy (%d cases, %d failing, rc=%s)' % (n_c, len(failed_c), rc_c))
        build(mutant_root, mutated=True)
        n_m, failed_m, rc_m = run_new_test(mutant_root, scratch, 'mutant')
        if failed_m:
            print('MUTANT-FIRES %d of %d cases fail on the report-PDF mutant (rc=%s); first: %s' % (
                len(failed_m), n_m, rc_m, failed_m[0][:80]))
            sys.exit(0)
        out('MUTANT-SURVIVES the mutant passed all %d cases (rc=%s)' % (n_m, rc_m))
    finally:
        teardown(control_root)
        teardown(mutant_root)
        safe_remove(scratch)


if __name__ == '__main__':
    main()
