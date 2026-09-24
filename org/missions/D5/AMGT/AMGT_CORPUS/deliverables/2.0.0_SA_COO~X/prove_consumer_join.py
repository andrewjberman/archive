"""Build a pinned owner patch and exercise its actual consumer function offline.

Writes only C evidence/patch files. Never edits or imports the owner's API file.
Other thesis helpers are fixtures; this is not a live route or browser proof.
"""
import ast
import copy
import difflib
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import sys
from unittest.mock import patch

import boto3

HOME = Path(__file__).resolve().parent
ROOT = HOME.parents[6]
sys.path.insert(0, str(ROOT))

BASE = '1b1244cecf'
API = 'lib/research/api/scoped_amgt.py'


def refuse(*args, **kwargs):
    raise RuntimeError('POISON: external operation refused')


def main():
    from lib.research.corpus import continuation, fund_form, sector_template, substrate, typecast
    from lib.research.corpus.tests.test_substrate import _seed_docx_report, _seed_xlsx_sector_report

    base = subprocess.check_output(['git', 'show', BASE + ':' + API], cwd=ROOT, encoding='utf-8')
    before_tree = ast.parse(base)
    before = next(n for n in before_tree.body if isinstance(n, ast.FunctionDef) and n.name == 'read_thesis_bundle')
    lines = base.splitlines(keepends=True)
    insertion = '''    # I4 is read for the already-resolved identity; auth and publication stay with Runtime.
    from lib.research.corpus.report_input import read_report_input
    bundle["corpus"] = (
        read_report_input(resolved_key, client=_s3_client())
        if resolved_key else read_report_input(None)
    )
'''
    assert lines[before.end_lineno - 1].strip() == 'return bundle'
    lines.insert(before.end_lineno - 1, insertion)
    after_source = ''.join(lines)
    compile(after_source, API, 'exec')
    after_tree = ast.parse(after_source)
    after = next(n for n in after_tree.body if isinstance(n, ast.FunctionDef) and n.name == before.name)
    assert [ast.dump(n) for n in before_tree.body if n is not before] == [
        ast.dump(n) for n in after_tree.body if n is not after]
    diff = ''.join(difflib.unified_diff(base.splitlines(True), after_source.splitlines(True),
                                     fromfile='a/' + API, tofile='b/' + API))
    (HOME / 'I4_RUNTIME_JOIN.patch').write_bytes(diff.encode('utf-8'))

    security = 'ACME_US_Equity'
    stub = substrate.StubS3Client()
    reader_slot = [stub]
    namespace = {
        'SCOPE_HEADER': 'header', 'DRAFTING_ABSENT': 'ABSENT',
        'read_model_block': lambda *a: None, '_figures': lambda *a: [],
        'read_model': lambda *a, **k: {'fiscal_year_figures': [], 'forecast_figures': [],
                                      'model_status': 'ABSENT', 'fiscal_years': [], 'cases': []},
        '_now_iso': lambda: '2026-09-23T00:00:00Z',
        'read_drafted_sections': lambda *a: {'drafting_status': 'FIXTURE', 'drafted_sections': []},
        'thesis_driver_chart': lambda *a: {}, 'read_management': lambda *a, **k: {},
        'read_posture': lambda *a, **k: {}, 'read_scores': lambda *a, **k: {},
        '_s3_client': lambda: reader_slot[0],
    }
    module = ast.Module(body=[ast.ImportFrom(module='__future__', names=[ast.alias(name='annotations')], level=0), after],
                        type_ignores=[])
    exec(compile(ast.fix_missing_locations(module), API, 'exec'), namespace)
    def read(key):
        return namespace['read_thesis_bundle'](key, identity={'security_key': key})
    with patch.object(boto3, 'client', refuse), patch.object(boto3, 'resource', refuse), \
            patch.object(boto3.session.Session, 'client', refuse), \
            patch.object(socket, 'create_connection', refuse), \
            patch.object(subprocess, 'run', refuse), patch.object(subprocess, 'Popen', refuse):
        try:
            boto3.client('s3')
        except RuntimeError:
            poison_control = True
        else:
            raise AssertionError('Poison inactive')
        _seed_docx_report(stub, security, 'report', [('RECOMMENDATION: Maintain 1% position in IDVZ', True)])
        _seed_xlsx_sector_report(stub, security, 'workbook', 'Health Care')
        continuation.write_one(security, client=stub)
        sector_template._run_write(client=stub)
        fund_form._run_write(client=stub)
        typecast.write(client=stub)
        cases = {'positive': read(security), 'absent': read('ABSENT_US_Equity')}
        assert cases['positive']['corpus']['state'] == 'CURRENT'
        assert cases['absent']['corpus']['state'] == 'ABSENT'
        accepted = copy.deepcopy(cases['positive'])
        substrate._add_synthetic_report(security, stub)
        cases['stale'] = read(security)
        assert cases['stale']['corpus']['state'] == 'STALE'
        continuation.write_one(security, client=stub)
        cases['rebuilt'] = read(security)
        assert cases['rebuilt']['corpus']['state'] == 'CURRENT'
        first = cases['positive']['corpus']['member_hashes']
        last = cases['rebuilt']['corpus']['member_hashes']
        changed = sorted(k for k in first if first[k] != last[k])
        assert changed == ['continuation', 'prior_reports']
        broken = substrate.StubS3Client()
        broken._objects = dict(stub._objects)
        broken._objects.pop(next(k for k in broken._objects if '/research-report-extract/' in k))
        reader_slot[0] = broken
        cases['failed_read'] = read(security)
        cases['unresolved_identity'] = read(None)
        assert cases['failed_read']['corpus']['state'] == cases['unresolved_identity']['corpus']['state'] == 'FAILED'
        assert cases['failed_read']['corpus']['substrate'] is None
        assert cases['positive'] == accepted
    evidence = {
        'evidence_level': 'offline isolated pinned consumer function', 'owner_patch_base': BASE,
        'owner_path': API, 'base_sha256': hashlib.sha256(base.encode()).hexdigest(),
        'patched_sha256': hashlib.sha256(after_source.encode()).hexdigest(),
        'patch_sha256': hashlib.sha256(diff.encode()).hexdigest(), 'changed_function': 'read_thesis_bundle',
        'other_top_level_ast_unchanged': True, 'external_poison_control': poison_control,
        'actual_connector': 'read_thesis_bundle -> read_report_input -> substrate over producer-written fixtures',
        'fixture_helpers': ['identity passed by test, not authenticated', 'model', 'drafting', 'management', 'posture', 'scores'],
        'cases': cases, 'changed_members_after_rebuild': changed, 'prior_observation_unchanged_on_failure': True,
        'acceptance_ids_graded': [], 'live_journey': 'NOT_EVALUATED',
        'limit': 'Patch is proposed for COO~Z integration; no shared source edited, no deployed API, no rendered browser, no revision-store publication exercised.',
    }
    (HOME / 'evidence/I4_CONSUMER_JOIN_OFFLINE.json').write_bytes((json.dumps(evidence, indent=2) + '\n').encode('ascii'))
    print('Six consumer cases pass; changed members continuation/prior_reports; owner patch generated, not applied.')


if __name__ == '__main__':
    main()
