"""AMGT_CORPUS round 11 -- m1_AC2's checker. Read-only; writes nothing.

For every resolved name, resolves the three case fields through the SAME resolver build() calls
(`dossier._resolve_case_field`) and reads the Base case's `currency`. Prints one line per name whose Base case carries a
currency, and the summary `m1 currency_set <n> <KEY=CCY ...>` with the names sorted.
"""
from lib.research.corpus import dossier
from lib.research.harvest import store


def main():
    client = store._default_client()
    keys = dossier._resolved_security_keys(client=client)
    setp = []
    for key in keys:
        _items, pick_a, pick_b = dossier._picked_reports(key, client)
        label_a = dossier._period_label(pick_a)
        label_b = dossier._period_label(pick_b)
        model_block, _record = dossier._model_block_read(key, client)
        listing = dossier._listing_currency(model_block)
        names = dossier.CASE_SECTION_NAMES["base"]
        field, _state = dossier._resolve_case_field("base", names, pick_a, pick_b, label_a, label_b, listing)
        ccy = field.get("currency")
        if ccy:
            setp.append("%s=%s" % (key, ccy))
            print("m1 %s currency %s basis %s" % (key, ccy, field.get("currency_basis")))
    print("m1 names %d currency_set %d %s" % (len(keys), len(setp), " ".join(sorted(setp))))


if __name__ == "__main__":
    main()
