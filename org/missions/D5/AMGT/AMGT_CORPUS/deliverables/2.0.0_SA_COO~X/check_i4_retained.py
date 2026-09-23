"""One retained IMB payload check; no producer, vendor, API or browser execution."""
import collections
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace

from measure_corpus import ReadOnlyS3
from lib.research.corpus import substrate, typed


def main():
    home = Path(__file__).resolve().parent
    output = home / 'evidence/I4_IMB_PAYLOAD_CHECK_20260923.json'
    if output.exists():
        raise RuntimeError('Refusing to overwrite an existing observation')
    client = ReadOnlyS3()
    calls = collections.Counter()

    def guard(model, params, **kwargs):
        if model.name not in {'GetObject', 'HeadObject', 'ListObjectsV2', 'ListObjectVersions'}:
            raise RuntimeError('Read-only payload check refuses ' + model.name)
        if params.get('Bucket') != 'opal-data-harvest':
            raise RuntimeError('Read outside the corpus harvest bucket refused')
        address = params.get('Key', params.get('Prefix', ''))
        if not address.startswith('amgt/'):
            raise RuntimeError('Unscoped or non-AMGT read refused')
        if sum(calls.values()) >= 1000:
            raise RuntimeError('Bounded request budget exhausted')
        calls[model.name] += 1

    try:
        guard(SimpleNamespace(name='PutObject'), {})
    except RuntimeError:
        refusal_control = True
    else:
        raise AssertionError('Write refusal control failed')
    client.client.meta.events.register('before-parameter-build.s3', guard)
    measured_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = substrate.substrate('IMB_LN_Equity', client=client)
    assert result['security_key'] == 'IMB_LN_Equity'
    assert set(result) == {'security_key', 'prior_reports', *substrate.DERIVED_MEMBERS}
    rows = typed.reports_for('IMB_LN_Equity', client=client)
    assert rows and len(rows) == len(result['prior_reports'])
    assert typed.period_order_ok([row for row in rows if row.get('period')])
    lineage = []
    for row, entry in zip(rows, result['prior_reports']):
        extraction_bytes = substrate._get_bytes(client, row['extract_key'])
        extraction = json.loads(extraction_bytes)
        bronze_bytes = substrate._get_bytes(client, row['bronze_key'])
        extraction_hash = hashlib.sha256(extraction_bytes).hexdigest()
        bronze_hash = hashlib.sha256(bronze_bytes).hexdigest()
        assert entry['bronze_key'] == row['bronze_key'] == extraction['bronze_key']
        assert entry['sha256'] == extraction_hash
        assert extraction['bronze_sha256'] == bronze_hash
        lineage.append({'bronze_uri': row['bronze_key'], 'bronze_byte_sha256': bronze_hash,
                        'extract_uri': row['extract_key'], 'extract_byte_sha256': extraction_hash,
                        'period': row.get('period')})
    documents = {}
    for member in substrate.DERIVED_MEMBERS:
        entry = result[member]
        if 'absent' in entry:
            assert isinstance(entry['absent'], str) and entry['absent']
            documents[member] = entry
            continue
        raw = substrate._get_bytes(client, entry['uri'])
        document = json.loads(raw)
        assert entry['content_sha256'] == document['content_sha256']
        assert entry['method_version'] == document['method_version']
        assert entry['inputs_count'] == len(document['inputs'])
        assert isinstance(entry['current'], bool)
        documents[member] = {'uri': entry['uri'], 'retained_byte_sha256': hashlib.sha256(raw).hexdigest(),
                             'artifact_content_sha256': document['content_sha256'], 'document': document}
    old = json.loads((home / 'evidence/I4_RETAINED_EXAMPLE.json').read_bytes())
    changes = sorted(key for key in result if result[key] != old['substrate'].get(key))
    observed = {'measured_at': measured_at, 'finished_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'evidence_level': 'retained-data read', 'scope': 'one existing resolved security; no full-population replay',
                'implementation_pin': 'dc2c0193ef',
                'pre_check_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], encoding='ascii').strip(),
                'check_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'payload_check': 'PASS', 'live_journey_acceptance': 'NOT_EVALUATED',
                'substrate': result, 'lineage': lineage, 'referenced_documents': documents,
                'period_order_ok': True, 'prior_report_count': len(rows),
                'changed_response_keys_since_prior_observation': changes,
                'previous_observation_at': old['measured_at'],
                'aws_read_calls': dict(calls), 'write_refusal_positive_control': refusal_control,
                'actual_s3_writes': 0, 'acceptance_ids_graded': [],
                'object_reads': [{'bucket': bucket, 'key': key, 'sha256': hashlib.sha256(raw).hexdigest(),
                                 'bytes': len(raw)} for (bucket, key), (_, raw) in sorted(client.cache.items())],
                'limits': 'No browser, auth, API, deployed-package or consumer proof; no vendor/model calls or source-library access. Reads cached per object during this observation; no cross-object atomic snapshot claimed.'}
    output.write_bytes((json.dumps(observed, indent=2, ensure_ascii=True, default=str) + '\n').encode('ascii'))
    print(json.dumps({'evidence': str(output), 'prior_reports': len(rows), 'read_calls': dict(calls),
                      'member_states': {key: {'current': result[key].get('current'), 'absent': result[key].get('absent')}
                                        for key in substrate.DERIVED_MEMBERS},
                      'changed_response_keys': changes, 'live_journey': 'NOT_EVALUATED'}, indent=2))


if __name__ == '__main__':
    main()
