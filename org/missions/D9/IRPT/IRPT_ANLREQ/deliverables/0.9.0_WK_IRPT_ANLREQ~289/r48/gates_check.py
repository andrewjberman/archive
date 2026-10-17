#!/usr/bin/env python3
"""AR389-y-AC2 -- gates for the reconcile candidate branch, with AMENDMENT 1 (CTO msg 10556).

Recomputed live from git: the Trade Request lines of TicketCenter.tsx against origin/DEV, the path
names matching trade, and AMENDMENT 1's two tests against origin/PROD (file names subset of the
DEV-only set; trade/Trade diff lines equal). Read from the recorded run logs under r48/logs (the
typecheck, eslint and bun test outputs, ANSI stripped here): typecheck and eslint error counts, the
failing test lines compared as a multiset with origin/DEV's, and the load errors new on the branch.
The recorded counts in r48/GATES.json must equal the recomputed ones.

Prints GATES-OK ... only when every condition holds; otherwise GATES-BAD <why>, exit 1.
"""
import collections
import json
import os
import re
import subprocess
import sys

BR = 'cand/dell2/prod-into-dev-reconcile'
HERE = os.path.dirname(os.path.abspath(__file__))
TICKET_CENTER = 'src/pages/TicketCenter/TicketCenter.tsx'
ANSI = re.compile(r'\x1b\[[0-9;]*m')
FAIL_MARK = '✗ '  # the bun test failing-line mark, written as an escape so the source stays ASCII
TIMING = re.compile(r' \[[0-9.]+(ms|s)\]$')


def git(args, cwd):
    p = subprocess.run(['git'] + args, cwd=cwd, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    return p.returncode, p.stdout


def bad(why):
    print('GATES-BAD ' + why)
    return 1


def read_log(name, logs):
    with open(os.path.join(logs, name), encoding='utf-8', errors='replace') as fh:
        return ANSI.sub('', fh.read())


def last_rc(text):
    rcs = re.findall(r'^rc=(\d+)\s*$', text, re.M)
    return int(rcs[-1]) if rcs else None


def failing_lines(text):
    out = []
    for line in text.splitlines():
        if line.startswith(FAIL_MARK):
            out.append(TIMING.sub('', line.rstrip()))
    return collections.Counter(out)


def load_errors(text):
    return collections.Counter(ln.rstrip() for ln in text.splitlines() if ln.startswith('error: '))


def trade_lines(text):
    return [ln for ln in text.splitlines() if 'trade' in ln or 'Trade' in ln]


def main():
    portal = os.path.join(subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=HERE,
                                         capture_output=True, text=True).stdout.strip(), 'portal')
    logs = os.path.join(HERE, 'logs')
    with open(os.path.join(HERE, 'GATES.json'), encoding='utf-8') as fh:
        gates = json.load(fh)

    # --- typecheck and eslint: the recorded runs on the branch ---
    tc = read_log('typecheck_branch.txt', logs)
    if last_rc(tc) != 0:
        return bad('typecheck rc is not 0 at the branch')
    tc_errors = len(re.findall(r'error TS\d+', tc))
    if tc_errors != 0:
        return bad('typecheck reports %d errors' % tc_errors)
    es = read_log('eslint_branch.txt', logs)
    if last_rc(es) != 0:
        return bad('eslint rc is not 0 at the branch')
    m = re.search(r'\((\d+) errors?', es)
    es_errors = int(m.group(1)) if m else 0
    if es_errors != 0:
        return bad('eslint reports %d errors' % es_errors)

    # --- failing test lines: branch against origin/DEV at the same path ---
    t_branch = read_log('test_branch.txt', logs)
    t_dev = read_log('test_dev_samepath.txt', logs)
    if last_rc(t_branch) is None or last_rc(t_dev) is None:
        return bad('a recorded test run lacks its rc line')
    f_branch = failing_lines(t_branch)
    f_dev = failing_lines(t_dev)
    if f_branch != f_dev:
        only_b = sum((f_branch - f_dev).values())
        only_d = sum((f_dev - f_branch).values())
        return bad('failing test lines differ from origin/DEV: %d only on branch, %d only on DEV' % (only_b, only_d))
    k = sum(f_branch.values())

    # --- new load errors: error lines on the branch that origin/DEV does not have ---
    e_branch = load_errors(t_branch)
    e_dev = load_errors(t_dev)
    new = e_branch - e_dev
    e = sum(new.values())
    explained = gates.get('tests', {}).get('new_load_errors_explained', {})
    unexplained = [line for line in new if line not in explained]
    if unexplained:
        return bad('%d new load error line(s) not explained in GATES.json, first: %s' % (len(unexplained), unexplained[0][:160]))

    # --- Trade Request code: no trade-named path differs, and TicketCenter.tsx trade lines equal DEV's ---
    rc, names = git(['diff', '--name-only', 'origin/DEV', BR], portal)
    trade_paths = [n for n in names.splitlines() if 'trade' in n.lower()]
    if trade_paths:
        return bad('trade-named paths differ from origin/DEV: %s' % trade_paths)
    rc1, dev_tc = git(['show', 'origin/DEV:' + TICKET_CENTER], portal)
    rc2, br_tc = git(['show', BR + ':' + TICKET_CENTER], portal)
    if rc1 != 0 or rc2 != 0:
        return bad('cannot read %s at DEV or the branch' % TICKET_CENTER)
    t_dev_set = set(trade_lines(dev_tc))
    t_br_set = set(trade_lines(br_tc))
    if t_dev_set != t_br_set:
        return bad('trade lines of %s differ from DEV (%d only on branch, %d only on DEV)'
                   % (TICKET_CENTER, len(t_br_set - t_dev_set), len(t_dev_set - t_br_set)))
    t_count = len(trade_lines(br_tc))

    # --- AMENDMENT 1 (CTO msg 10556): against origin/PROD ---
    rc3, names_prod_br = git(['diff', '--name-only', 'origin/PROD', BR], portal)
    rc4, names_prod_dev = git(['diff', '--name-only', 'origin/PROD', 'origin/DEV'], portal)
    set_pb = set(n for n in names_prod_br.splitlines() if n)
    set_pd = set(n for n in names_prod_dev.splitlines() if n)
    if not set_pb <= set_pd:
        return bad('origin/PROD..branch names files outside the DEV-only set: %s' % sorted(set_pb - set_pd)[:5])

    def diff_trade(a, b):
        rc, out = git(['diff', a, b], portal)
        if rc != 0:
            raise RuntimeError('git diff %s %s rc=%d' % (a, b, rc))
        keep = []
        for line in out.splitlines():
            if line.startswith('+++') or line.startswith('---'):
                continue
            if line[:1] in ('+', '-') and ('trade' in line or 'Trade' in line):
                keep.append(line)
        return keep

    pb_lines = diff_trade('origin/PROD', BR)
    pd_lines = diff_trade('origin/PROD', 'origin/DEV')
    if set(pb_lines) != set(pd_lines):
        return bad('trade/Trade lines of origin/PROD..branch differ from origin/PROD..origin/DEV')

    # --- the recorded numbers in GATES.json must equal what was recomputed ---
    rec = gates.get('tests', {})
    rec_b = rec.get('branch', {})
    rec_d = rec.get('dev_same_path', {})
    if rec_b.get('failing_lines_branch') != k or rec_d.get('failing_lines_dev_same_path') != sum(f_dev.values()):
        return bad('GATES.json failing-line counts differ from the logs')
    if rec.get('new_load_errors') != e:
        return bad('GATES.json new_load_errors differs from the logs')

    print('GATES-OK typecheck 0 eslint 0 errors failing-lines-equal-DEV %d new-load-errors %d explained trade-lines-equal %d'
          % (k, e, t_count))
    print('  AMENDMENT-1 names-subset-of-DEV-only-set %d of %d; trade-lines-PROD-vs-branch equal (%d lines in each)'
          % (len(set_pb), len(set_pd), len(pb_lines)))
    print('  typecheck errors %d; eslint errors %d; typecheck/eslint ran on the branch (logs/typecheck_branch.txt, logs/eslint_branch.txt)'
          % (tc_errors, es_errors))
    return 0


if __name__ == '__main__':
    sys.exit(main())
