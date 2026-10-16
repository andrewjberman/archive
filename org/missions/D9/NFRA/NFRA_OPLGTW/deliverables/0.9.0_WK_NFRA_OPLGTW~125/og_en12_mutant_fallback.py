"""Planted defect for the OG-en-12 mutant control: a live read falls back to the default client when its role variable is
unset (the refusal is removed). Loaded with -p from the gateway directory with PYTHONPATH pointing at this folder; it
never touches the committed tree."""
from app import client_role

_real_client_for = client_role.client_for


def _mutant_client_for(vendor, live=False):
    return _real_client_for(vendor, live=False)


client_role.client_for = _mutant_client_for
