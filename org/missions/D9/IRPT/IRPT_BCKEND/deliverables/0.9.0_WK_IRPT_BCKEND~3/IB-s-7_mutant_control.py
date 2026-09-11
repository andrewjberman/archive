"""MUTANT CONTROL for IB-s-7.

Two claims this cell rests on, each mutated by monkeypatch in a process that edits no
production file. A passing assertion never mutated has never been tested, and the risk here
is the usual one: a parser's own tests, written by the parser's author, agree with it.

  M1  RevisionStore.put OVERWRITES instead of refusing  -> "revision r is never rewritten"
      must break: r0's hash must move and the overwrite must stop being refused.
  M2  the share-class mapping is APPLIED instead of proposed -> "an unmatched holding is
      never silently substituted" must break: the holding must stop being what the advisor
      sent.

A third control is not here because it is already INSIDE the battery: arm (b) builds the
parser with `drop_unmatched=True` and shows the reconciliation identity go to
`unaccounted: 1, balances: false`. That one is a mutant that ships.

Run: python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/IB-s-7_mutant_control.py
"""
import json
import os
import sys

ROOT = os.path.abspath('.')
INTAKE = os.path.join(ROOT, 'infra', 'aws', 'lambda', 'investor-reporting', 'intake')
AUTHZ = os.path.join(ROOT, 'infra', 'aws', 'lambda', 'investor-reporting', '_authz')
for p in (INTAKE, AUTHZ, os.path.join(AUTHZ, 'tests')):
    sys.path.insert(0, p)

import corrections          # noqa: E402
import enforce as authz     # noqa: E402
import fixtures as authz_fixtures  # noqa: E402
import parse                # noqa: E402

F = os.path.join(INTAKE, 'fixtures', 'holdings')
REQUEST_ID = 'REQ-' + '99' * 12


def parsed(name):
    with open(os.path.join(F, name), 'rb') as fh:
        return parse.parse_holdings(fh.read(), name, 'att-' + name)


def immutability_probe(label):
    directory = authz_fixtures.DIRECTORY
    binding = authz.FirmBinding(authz_fixtures.TENANT, directory['firm_id_opaque'])
    store = corrections.RevisionStore()
    r = parsed('holdings_share_class.csv')
    opened, _ = corrections.open_revision(r, REQUEST_ID, binding, directory, store)
    before = opened['hash']
    corrections.apply_corrections(
        store, REQUEST_ID,
        [{'finding_code': 'SHARE_CLASS_SUBSTITUTION_PROPOSED', 'approved_by': 'analyst:a',
          'from_value': 'VTSAX', 'to_value': 'VTI'}], binding, directory)
    after = corrections.revision_hash(store.get(REQUEST_ID, 0))
    overwrite_refused = True
    try:
        store.put(REQUEST_ID, 0, {'tampered': True})
        overwrite_refused = False
    except corrections.RevisionExists:
        pass
    after_tamper = corrections.revision_hash(store.get(REQUEST_ID, 0))
    return {
        'label': label,
        'hash_r0_at_open': before[:16],
        'hash_r0_after_r1': after[:16],
        'hash_r0_after_tamper_attempt': after_tamper[:16],
        'overwrite_refused': overwrite_refused,
        'arm_d_predicate_holds': before == after and overwrite_refused and before == after_tamper,
    }


def substitution_probe(label):
    r = parsed('holdings_share_class.csv')
    identifiers = [h['identifier'] for h in r.normalized_holdings]
    proposed = [f['code'] for f in r.findings
                if f['code'] == 'SHARE_CLASS_SUBSTITUTION_PROPOSED']
    return {
        'label': label,
        'identifiers_as_parsed': identifiers,
        'advisor_sent_VTSAX_and_it_is_still_there': 'VTSAX' in identifiers,
        'a_substitution_was_applied_by_the_parser': 'VTI' in identifiers,
        'proposals_emitted': len(proposed),
        'arm_b_predicate_holds': 'VTSAX' in identifiers and 'VTI' not in identifiers,
    }


out = {'baseline_immutability': immutability_probe('baseline'),
       'baseline_substitution': substitution_probe('baseline')}

# ---- M1: the store overwrites --------------------------------------------
real_put = corrections.RevisionStore.put


def overwriting_put(self, request_id, revision, payload):
    import copy
    self._items[(request_id, int(revision))] = copy.deepcopy(payload)
    self.writes += 1
    return corrections.revision_hash(payload)


corrections.RevisionStore.put = overwriting_put
try:
    out['M1_store_overwrites'] = immutability_probe('M1')
finally:
    corrections.RevisionStore.put = real_put

# ---- M2: the mapping is APPLIED ------------------------------------------
real_classify = parse.classify_identifier


def substituting_classify(raw, mapping):
    namespace, identifier, note = real_classify(raw, mapping)
    hit = mapping['share_classes'].get(identifier)
    if hit:
        return 'TICKER', hit['to'], note      # THE SILENT SUBSTITUTION
    return namespace, identifier, note


parse.classify_identifier = substituting_classify
try:
    out['M2_mapping_applied'] = substitution_probe('M2')
finally:
    parse.classify_identifier = real_classify

out['verdict'] = {
    'baseline_immutability_holds': out['baseline_immutability']['arm_d_predicate_holds'],
    'M1_breaks_it': not out['M1_store_overwrites']['arm_d_predicate_holds'],
    'baseline_substitution_holds': out['baseline_substitution']['arm_b_predicate_holds'],
    'M2_breaks_it': not out['M2_mapping_applied']['arm_b_predicate_holds'],
}
out['verdict']['mutants_fired_as_expected'] = all(out['verdict'].values())
print(json.dumps(out, indent=1, sort_keys=True))
