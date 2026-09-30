"""AMGT_CORPUS round 11 -- the pair's expected outcome, per name, read from the producer's own rule. Read-only.

For every resolved name: the three case fields AS SERVED NOW (`read_dossier`, the stored object) against the same fields AS
THE BUILD WILL WRITE THEM (`_resolve_case_field` with the listing and the `_pdf_words_reader` build() passes). Prints one line
per name whose cases change, naming what moves (currency, served/absent, values), then the summary.
"""
import json

from lib.research.corpus import dossier
from lib.research.harvest import store


def _shape(field):
    return {
        "served": field.get("value") is not None,
        "currency": field.get("currency"),
        "unit": field.get("unit_as_written"),
        "value": json.dumps(field.get("value"), sort_keys=True),
    }


def main():
    client = store._default_client()
    words = dossier._pdf_words_reader(client)
    keys = dossier._resolved_security_keys(client=client)
    moved = 0
    currency_moves = []
    served_moves = []
    for key in keys:
        now = dossier.read_dossier(key, client=client)["document"]["fields"]["cases"]
        _items, pick_a, pick_b = dossier._picked_reports(key, client)
        label_a, label_b = dossier._period_label(pick_a), dossier._period_label(pick_b)
        block, _rec = dossier._model_block_read(key, client)
        listing = dossier._listing_currency(block)
        changes = []
        for case_name, names in dossier.CASE_SECTION_NAMES.items():
            new, _state = dossier._resolve_case_field(case_name, names, pick_a, pick_b, label_a, label_b, listing, words)
            a, b = _shape(now.get(case_name) or {}), _shape(new)
            if a["currency"] != b["currency"]:
                changes.append("%s currency %s->%s" % (case_name, a["currency"], b["currency"]))
            if a["served"] != b["served"]:
                changes.append("%s served %s->%s" % (case_name, a["served"], b["served"]))
            elif a["value"] != b["value"]:
                changes.append("%s value changed" % case_name)
        if changes:
            moved += 1
            if any("currency" in c for c in changes):
                currency_moves.append(key)
            if any("served" in c for c in changes):
                served_moves.append(key)
            print("move %s listing %s | %s" % (key, listing, "; ".join(changes)))
    print("expected names %d moved %d currency_moves %d [%s] served_moves %d [%s]"
          % (len(keys), moved, len(currency_moves), " ".join(currency_moves), len(served_moves), " ".join(served_moves)))


if __name__ == "__main__":
    main()
