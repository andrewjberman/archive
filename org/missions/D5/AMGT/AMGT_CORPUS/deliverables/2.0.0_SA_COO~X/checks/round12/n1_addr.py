"""AMGT_CORPUS round 12 -- n1_AC2's checker. Read-only; writes nothing.

Prints the dossier store's table name, the key prefix the store writes under, whether that prefix equals the naming builder's
own `address()` output for the same table, and how many times the hyphen literal remains in `lib/research/corpus/dossier.py`.
"""
import os

from lib import opal_naming
from lib.research.corpus import dossier, gold

HERE = os.path.dirname(os.path.abspath(dossier.__file__))


def main():
    prefix = gold.table_prefix(dossier.TABLE)
    built = opal_naming.address(gold.SOURCE, gold.SCOPE, gold.TIER, "research_dossier", "p=x")
    built_prefix = built.split("://", 1)[1].split("/", 1)[1].rsplit("/", 1)[0] + "/"
    src = open(os.path.join(HERE, "dossier.py"), encoding="utf-8").read()
    print("n1 table %s prefix %s equals_builder %s hyphen_literal %d"
          % (dossier.TABLE, prefix, prefix == built_prefix, src.count("research" + "-" + "dossier")))


if __name__ == "__main__":
    main()
