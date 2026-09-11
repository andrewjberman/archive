"""MUTANT CONTROL for IB-s-6.

The central claim of arms (a) and (c) is that the CONDITIONAL completion mark is what makes
a re-read a no-op. Remove exactly that one behaviour -- nothing else -- and both arms must
break. A passing assertion never mutated has never been tested.

Two mutants, run one at a time against the real modules:
  M1  Checkpoint.is_complete always returns False (the short-circuit is removed)
  M2  the completion mark is written UNCONDITIONALLY (if_absent dropped)

No production file is edited: the mutation is a monkeypatch in this process only.
"""
import json
import os
import sys

ROOT = os.path.abspath('.')
INTAKE = os.path.join(ROOT, 'infra', 'aws', 'lambda', 'investor-reporting', 'intake')
sys.path.insert(0, INTAKE)
sys.path.insert(0, os.path.join(INTAKE, 'tests'))

import checkpoint as ckpt          # noqa: E402
import graph_client as gc          # noqa: E402
import outbox as ob                # noqa: E402
import poller                      # noqa: E402

FIXTURES = os.path.join(INTAKE, 'fixtures', 'graph')


def fresh_client(script=None):
    return gc.GraphClient(transport=gc.RecordedTransport(fixture_dir=FIXTURES, script=script),
                          clock={'sleep': lambda s: None, 'now': lambda: 0.0})


def page_script():
    def load(n):
        with open(os.path.join(FIXTURES, n), encoding='utf-8') as fh:
            return json.load(fh)
    return [(200, {}, load('delta_page1.json')),
            (200, {}, load('delta_page2.json')),
            (200, {}, load('delta_page3.json'))]


def two_deliveries(label):
    store = ckpt.MemoryStore()
    blobs = poller.MemoryBlobs()
    queue = ob.MemoryQueue()
    first = poller.run_scan(client=fresh_client(), store=store, blobs=blobs,
                            queue=queue, owner=label)
    second = poller.run_scan(client=fresh_client(script=page_script()), store=store,
                             blobs=blobs, queue=queue, owner=label)
    return {
        'first_requests_created': first['requests_created'],
        'second_requests_created': second['requests_created'],
        'second_already_complete': second['already_complete'],
        'queue_sends_total': len(queue.sent),
        'arm_c_predicate_holds': (first['requests_created'] == 5
                                  and second['requests_created'] == 0
                                  and second['already_complete'] == 5
                                  and len(queue.sent) == 5),
    }


out = {'baseline': two_deliveries('mutant-baseline')}

real_is_complete = ckpt.Checkpoint.is_complete
ckpt.Checkpoint.is_complete = lambda self, identity: False
try:
    out['M1_is_complete_always_false'] = two_deliveries('mutant-m1')
finally:
    ckpt.Checkpoint.is_complete = real_is_complete

real_put = ckpt.MemoryStore.put


def unconditional_put(self, table, key, attrs, if_absent=False):
    return real_put(self, table, key, attrs, if_absent=False)


ckpt.MemoryStore.put = unconditional_put
ckpt.Checkpoint.is_complete = lambda self, identity: False
try:
    out['M2_mark_written_unconditionally'] = two_deliveries('mutant-m2')
finally:
    ckpt.MemoryStore.put = real_put
    ckpt.Checkpoint.is_complete = real_is_complete

out['verdict'] = {
    'baseline_holds': out['baseline']['arm_c_predicate_holds'],
    'M1_breaks_it': not out['M1_is_complete_always_false']['arm_c_predicate_holds'],
    'M2_breaks_it': not out['M2_mark_written_unconditionally']['arm_c_predicate_holds'],
}
out['verdict']['mutant_fired_as_expected'] = (
    out['verdict']['baseline_holds']
    and out['verdict']['M1_breaks_it']
    and out['verdict']['M2_breaks_it'])
print(json.dumps(out, indent=1, sort_keys=True))
