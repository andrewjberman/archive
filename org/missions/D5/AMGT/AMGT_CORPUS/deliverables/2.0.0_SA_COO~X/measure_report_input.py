"""Exercise the new corpus report-input interface against existing retained IMB bytes."""
import collections
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

from measure_corpus import ReadOnlyS3
from lib.research.corpus import report_input


def main():
    home = Path(__file__).resolve().parent
    output = home / 'evidence/I4_REPORT_INPUT_RETAINED.json'
    if output.exists():
        raise RuntimeError('Refusing to replace retained observation')
    client = ReadOnlyS3()
    calls = collections.Counter()

    def guard(model, params, **kwargs):
        if model.name not in {'GetObject', 'HeadObject', 'ListObjectsV2'}:
            raise RuntimeError('Read-only adapter proof refuses ' + model.name)
        if (params.get('Bucket') != 'opal-data-harvest'
                or not params.get('Key', params.get('Prefix', '')).startswith('amgt/')):
            raise RuntimeError('Non-AMGT or unscoped read refused')
        if sum(calls.values()) >= 1000:
            raise RuntimeError('Read budget exhausted')
        calls[model.name] += 1

    try:
        guard(SimpleNamespace(name='PutObject'), {})
    except RuntimeError:
        refusal_control = True
    else:
        raise AssertionError('Refusal inactive')
    client.client.meta.events.register('before-parameter-build.s3', guard)
    result = report_input.read_report_input('IMB_LN_Equity', client=client)
    assert result['state'] == 'CURRENT', result
    assert len(result['prior_reports']) == 15
    assert result['member_states'] == {'continuation': 'CURRENT', 'sector_template': 'ABSENT',
                                       'fund_form': 'CURRENT', 'typecast': 'CURRENT'}
    old = json.loads((home / 'evidence/I4_IMB_PAYLOAD_CHECK_20260923.json').read_bytes())
    assert result['substrate'] == old['substrate']
    evidence = {'evidence_level': 'retained-data read through new report-input adapter',
                'adapter_source_sha256': hashlib.sha256(Path(report_input.__file__).read_bytes()).hexdigest(),
                'result': result, 'aws_read_calls': dict(calls), 'write_refusal_control': refusal_control,
                'actual_s3_writes': 0, 'acceptance_ids_graded': [], 'live_journey': 'NOT_EVALUATED',
                'population': json.loads((home / 'evidence/C02_RECONCILIATION.json').read_bytes())['summary'],
                'population_vintage': json.loads((home / 'evidence/C02_RECONCILIATION.json').read_bytes())['measured_at'],
                'limits': 'No browser/API/deployment/revision-store proof. Population is earlier census, not recomputed by this one-security read.'}
    output.write_bytes((json.dumps(evidence, indent=2, default=str) + '\n').encode('ascii'))
    print(json.dumps({'state': result['state'], 'reports': len(result['prior_reports']),
                      'manifest_objects': len(result['input_manifest']), 'read_calls': dict(calls),
                      'live_journey': 'NOT_EVALUATED'}, indent=2))


if __name__ == '__main__':
    main()
