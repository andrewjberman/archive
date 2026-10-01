"""AMGT_CORPUS round 22, CRPS-x-1 -- would `dossier.write_one` WRITE? Its no-op gate compares the stored object's
method_version with the code's METHOD_VERSION; a stored object naming a different method is never "unchanged". Read on three
real served names (read-only, S3 reads; nothing is written). The issuer's file.

  -> 'x1 code_method <METHOD_VERSION> stored_differs N of 3'
"""
from lib.research.corpus import dossier
from lib.research.harvest import store

NAMES = ["IMB_LN_Equity", "ADBE_US_Equity", "AZN_LN_Equity"]
client = store._default_client()
differs = 0
for k in NAMES:
    stored = dossier.read_dossier(k, client=client)["document"].get("method_version")
    differs += int(stored is not None and stored != dossier.METHOD_VERSION)
print("x1 code_method %s stored_differs %d of %d" % (dossier.METHOD_VERSION, differs, len(NAMES)))
