"""Planted defect for OG-en-13 (control only; the committed tree is unchanged): _weight drops the print floor, so a
0.00001 weight is served as 1e-05 with rounded_to_zero false. Loaded with pytest -p from the gateway directory."""
from app import client_adapter_bd49f as bd


def _weight_no_floor(value):
    number = bd._num(value)
    if number is None:
        return None, False
    return round(number, bd.WEIGHT_DECIMALS) + 0.0, False


bd._weight = _weight_no_floor
