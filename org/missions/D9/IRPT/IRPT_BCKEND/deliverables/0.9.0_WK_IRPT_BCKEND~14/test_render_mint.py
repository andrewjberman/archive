#!/usr/bin/env python3
"""Tests for the render-key minter (cell IB-rtq-1, round 17).

Runnable as the criterion invocation names it:
    cd org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~14
    py -3.12 -m pytest test_render_mint.py -v

Every arm cell requirement (e) names, by function name so `pytest -v` shows each by
name: claim shape (`test_claim_shape_and_values`, `test_jti_unique_across_two_mints`,
`test_sub_equals_render_prefix_plus_jti`, `test_exp_minus_iat_within_five_minutes`), key
separation (`test_decoding_with_wrong_key_fails`), expiry (`test_expired_token_fails_decode`),
and structural admin-bypass refusal (`test_admin_bypass_claims_are_refused`).

ASCII only. Python 3.12, python-jose[cryptography] + cryptography (estate dependencies,
already declared in other lambdas' requirements.txt -- see
infra/aws/lambda/opal_pm_upload_urls/requirements.txt et al.).
"""
from __future__ import annotations

import datetime
import os
import sys

import pytest
from jose import jwt as jose_jwt
from jose.exceptions import ExpiredSignatureError, JWSError, JWTError

# --------------------------------------------------------------------------- path setup


def _repo_root():
    """Walk up (bounded) for the directory that CONTAINS both `infra` and `.tools` --
    the repo root marker -- same depth-agnostic shape as
    infra/aws/lambda/investor-reporting/_keys/keys.py's `_find_registry`, for the same
    reason: a hardcoded `..` count breaks the moment either this test file or the module
    it imports moves one directory.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    d = here
    for _ in range(12):
        if os.path.isdir(os.path.join(d, "infra")) and os.path.isdir(os.path.join(d, ".tools")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    raise RuntimeError("could not locate repo root walking up from %s" % here)


_ROOT = _repo_root()
_MODULE_DIR = os.path.join(_ROOT, "infra", "aws", "lambda", "investor-reporting",
                            "_render_identity")
sys.path.insert(0, _MODULE_DIR)

import mint  # noqa: E402


# --------------------------------------------------------------------------- fixtures

_FIXTURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
_PRIVATE_KEY_PATH = os.path.join(
    _FIXTURE_DIR, "irpt_render_jwt_TEST_FIXTURE_private_key.pem")
_PUBLIC_KEY_PATH = os.path.join(
    _FIXTURE_DIR, "irpt_render_jwt_TEST_FIXTURE_public_key.pem")


@pytest.fixture(scope="module")
def private_key_pem():
    with open(_PRIVATE_KEY_PATH, "r", encoding="ascii") as fh:
        return fh.read()


@pytest.fixture(scope="module")
def public_key_pem():
    with open(_PUBLIC_KEY_PATH, "r", encoding="ascii") as fh:
        return fh.read()


@pytest.fixture(scope="module")
def wrong_public_key_pem():
    """A SECOND, genuinely different keypair -- generated fresh, never written to
    fixtures/ (only the ONE throwaway keypair cell (a) asks for lives there). Proves the
    render key really is separate: a token signed with the fixture private key must fail
    to decode against THIS key.
    """
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub_pem = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pub_pem.decode("ascii")


@pytest.fixture()
def synthetic_bundle():
    """A synthetic frozen-`ExportBundle`-shaped mapping. Every field the minter reads."""
    return {
        "firm_id": "49financial",
        "bundle_id": "bundle-test-0001",
        "revision": "r7",
        "account_set_id": "acct-set-42",
        "job_id": "job-9931",
        "report_id": "report-555",
        "delegator_subject": "advisor:alice@49financial.example",
    }


def _decode(token, public_key_pem):
    return jose_jwt.decode(
        token, public_key_pem, algorithms=["RS256"],
        issuer="opal-irpt-render", audience="irpt-render",
    )


# --------------------------------------------------------------------------- claim shape


def test_claim_shape_and_values(synthetic_bundle, private_key_pem, public_key_pem):
    result = mint.mint_render_token(synthetic_bundle, private_key_pem=private_key_pem)
    claims = _decode(result.token, public_key_pem)

    assert claims["iss"] == "opal-irpt-render"
    assert claims["aud"] == "irpt-render"
    assert claims["role"] == "renderer"
    assert claims["tier"] == "render"
    assert claims["firmId"] == synthetic_bundle["firm_id"]
    assert claims["bundle"] == synthetic_bundle["bundle_id"]
    assert claims["revision"] == synthetic_bundle["revision"]
    assert claims["accountSetId"] == synthetic_bundle["account_set_id"]
    assert claims["jobId"] == synthetic_bundle["job_id"]
    assert claims["reportId"] == synthetic_bundle["report_id"]
    assert claims["delegator"] == synthetic_bundle["delegator_subject"]
    assert claims["jti"] == result.jti
    assert claims["sub"] == "render:" + claims["jti"]
    # nbf/iat at most 60s skew leeway (PRD item 2) -- this minter emits nbf == iat (0s of
    # its own skew), which trivially satisfies "at most 60s".
    assert 0 <= claims["nbf"] - claims["iat"] <= mint.SKEW_LEEWAY_SECONDS \
        or 0 <= claims["iat"] - claims["nbf"] <= mint.SKEW_LEEWAY_SECONDS


def test_exp_minus_iat_within_five_minutes(synthetic_bundle, private_key_pem, public_key_pem):
    result = mint.mint_render_token(synthetic_bundle, private_key_pem=private_key_pem)
    claims = _decode(result.token, public_key_pem)
    assert claims["exp"] - claims["iat"] <= 300


def test_jti_unique_across_two_mints(synthetic_bundle, private_key_pem):
    first = mint.mint_render_token(synthetic_bundle, private_key_pem=private_key_pem)
    second = mint.mint_render_token(synthetic_bundle, private_key_pem=private_key_pem)
    assert first.jti != second.jti


def test_sub_equals_render_prefix_plus_jti(synthetic_bundle, private_key_pem, public_key_pem):
    result = mint.mint_render_token(synthetic_bundle, private_key_pem=private_key_pem)
    claims = _decode(result.token, public_key_pem)
    assert claims["sub"] == "render:" + result.jti
    assert claims["jti"] == result.jti


# --------------------------------------------------------------------------- key separation


def test_decoding_with_wrong_key_fails(synthetic_bundle, private_key_pem, wrong_public_key_pem):
    result = mint.mint_render_token(synthetic_bundle, private_key_pem=private_key_pem)
    with pytest.raises((JWSError, JWTError)):
        _decode(result.token, wrong_public_key_pem)


# --------------------------------------------------------------------------- expiry


def test_expired_token_fails_decode(synthetic_bundle, private_key_pem, public_key_pem):
    stale_now = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=10)
    result = mint.mint_render_token(
        synthetic_bundle, private_key_pem=private_key_pem, now=stale_now)
    with pytest.raises(ExpiredSignatureError):
        _decode(result.token, public_key_pem)


# --------------------------------------------------------------------------- admin-bypass refusal


@pytest.mark.parametrize("forbidden_field,forbidden_value", [
    ("role", "admin"),
    ("firmRole", "admin"),
    ("tier", "internal"),
    ("userType", "Dev"),
])
def test_admin_bypass_claims_are_refused(synthetic_bundle, private_key_pem,
                                          forbidden_field, forbidden_value):
    """Cell requirement (c): attempting to pass an admin-bypass claim through the bundle
    is REFUSED outright (this module's chosen arm of "absent or refused")."""
    poisoned = dict(synthetic_bundle)
    poisoned[forbidden_field] = forbidden_value
    with pytest.raises(mint.RenderMintRefused):
        mint.mint_render_token(poisoned, private_key_pem=private_key_pem)


def test_no_admin_bypass_claim_ever_appears_when_bundle_is_clean(
        synthetic_bundle, private_key_pem, public_key_pem):
    """The positive half of (c): a CLEAN bundle (no forbidden keys at all) still never
    produces a token whose claims could be read as an admin-bypass -- role/tier are
    always the fixed renderer/render values, and firmRole/userType are never present."""
    result = mint.mint_render_token(synthetic_bundle, private_key_pem=private_key_pem)
    claims = _decode(result.token, public_key_pem)
    assert claims["role"] != "admin"
    assert claims["tier"] != "internal"
    assert "firmRole" not in claims
    assert "userType" not in claims


# --------------------------------------------------------------------------- bundle-only minting


def test_missing_bundle_field_is_refused(synthetic_bundle, private_key_pem):
    incomplete = dict(synthetic_bundle)
    del incomplete["delegator_subject"]
    with pytest.raises(mint.RenderMintRefused):
        mint.mint_render_token(incomplete, private_key_pem=private_key_pem)


def test_no_private_key_source_raises(synthetic_bundle, monkeypatch):
    monkeypatch.delenv(mint.PRIVATE_KEY_ENV, raising=False)
    with pytest.raises(mint.RenderKeyUnavailable):
        mint.mint_render_token(synthetic_bundle)


def test_private_key_from_env_var(synthetic_bundle, private_key_pem, public_key_pem, monkeypatch):
    monkeypatch.setenv(mint.PRIVATE_KEY_ENV, private_key_pem)
    result = mint.mint_render_token(synthetic_bundle)
    claims = _decode(result.token, public_key_pem)
    assert claims["firmId"] == synthetic_bundle["firm_id"]


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
