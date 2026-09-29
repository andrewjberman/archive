"""AMGT_CORPUS round 11 -- m1_AC3's checker (AMENDMENT 1: the CTO's SHOP carve-out). Read-only; writes nothing.

Resolves SHOP_CN_Equity's Base case through the build's own path (listing + `_pdf_words_reader`) and prints its currency and
basis, and the same for one planted USD-listing `$` name (CPA_US_Equity), which must still read USD.
"""
from lib.research.corpus import dossier
from lib.research.harvest import store


def main():
    client = store._default_client()
    words = dossier._pdf_words_reader(client)
    for key in ("SHOP_CN_Equity", "CPA_US_Equity"):
        _items, pick_a, pick_b = dossier._picked_reports(key, client)
        label_a, label_b = dossier._period_label(pick_a), dossier._period_label(pick_b)
        block, _rec = dossier._model_block_read(key, client)
        listing = dossier._listing_currency(block)
        field, _state = dossier._resolve_case_field(
            "base", dossier.CASE_SECTION_NAMES["base"], pick_a, pick_b, label_a, label_b, listing, words)
        print("m1 %s listing %s currency %s basis %s" % (key, listing, field.get("currency"), field.get("currency_basis")))


if __name__ == "__main__":
    main()
