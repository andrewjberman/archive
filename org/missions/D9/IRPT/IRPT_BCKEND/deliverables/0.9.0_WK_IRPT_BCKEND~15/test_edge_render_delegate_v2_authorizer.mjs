// Node test for cell IB-rtq-2's V2 branch -- `infra/aws/users/lambda/portal-authorizer/
// index.mjs`. Task order IRPT_BCKEND.TO-IB-rtq-2, criterion R117-AC2 (the V2 portion).
//
// Uses this repo's convention for a `.mjs` Lambda test -- Node's own built-in test runner
// (`node:test` + `node:assert`), the SAME runner IB-rtq-3's sibling criterion invokes
// (`node --test test_edge_render_delegate.mjs`). No new devDependency: `node:test` is
// stdlib as of Node 18+ (this box: v26.9.0, measured this session).
//
// A THROWAWAY RSA keypair is generated in-process for every run (arm (d) of BOUNDS: "generate
// your own throwaway keypair", never IB-rtq-1's actual minter module). The public half is
// injected via `IRPT_RENDER_JWT_PUBLIC_KEY_PEM`, this cell's OWN fixture injection point --
// see `getRenderPublicKeyPem()` in `index.mjs` and row IRPT_BCKEND-W15-S4 for why the REAL
// secret fetch is a later round's integration, not this one's (BOUNDS: no Secrets Manager
// entry, no SSM parameter, no AWS call this round).

import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import jwt from 'jsonwebtoken';
import { test, before } from 'node:test';

const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
  modulusLength: 2048,
  publicKeyEncoding: { type: 'spki', format: 'pem' },
  privateKeyEncoding: { type: 'pkcs8', format: 'pem' },
});

// A SECOND, unrelated keypair -- used to prove a token signed by the WRONG key is refused
// even when every other claim is a perfect match (never exercised as a positive case).
const { privateKey: wrongPrivateKey } = crypto.generateKeyPairSync('rsa', {
  modulusLength: 2048,
  publicKeyEncoding: { type: 'spki', format: 'pem' },
  privateKeyEncoding: { type: 'pkcs8', format: 'pem' },
});

process.env.IRPT_RENDER_JWT_PUBLIC_KEY_PEM = publicKey;

// The human-portal verification key this file's OWN human-path arm needs, matching the
// EXISTING key-slot shape `getJwtKeySlots()`/`verifyWithSlots` read (current + previous).
// Generated fresh, never IB-rtq-1's or the estate's real key.
const { publicKey: humanPublicKey, privateKey: humanPrivateKey } = crypto.generateKeyPairSync(
  'rsa', { modulusLength: 2048, publicKeyEncoding: { type: 'spki', format: 'pem' },
          privateKeyEncoding: { type: 'pkcs8', format: 'pem' } });

const ORIGIN_SECRET_VALUE = 'test-cloudfront-origin-secret-value';

let mod;

before(async () => {
  // The shared `jwtPublicKeys.mjs` module and `originVerify.mjs` (imported by `index.mjs`)
  // both resolve their OWN Secrets Manager client at call time; this cell owns no wiring into
  // either (BOUNDS: no AWS call, no Secrets Manager entry). To exercise arm (f) -- the human
  // path's UNCHANGED behavior -- without any live secret, this test monkeypatches the shared
  // `SecretsManagerClient.prototype.send` just enough to answer BOTH reads, matching each
  // module's own documented shape exactly (`originVerify.mjs`: JSON `{current, previous}`;
  // `jwtPublicKeys.mjs`: accepts a bare PEM OR a `{current, previous}` JSON envelope, per its
  // own docstring) -- never touching `index.mjs`'s render branch, which needs neither.
  const { SecretsManagerClient } = await import('@aws-sdk/client-secrets-manager');
  SecretsManagerClient.prototype.send = async function (command) {
    const secretId = command?.input?.SecretId || '';
    if (secretId.includes('origin-verify')) {
      return { SecretString: JSON.stringify({ current: ORIGIN_SECRET_VALUE, previous: null }) };
    }
    if (secretId.includes('jwt-public-key')) {
      return { SecretString: humanPublicKey };
    }
    throw new Error('unstubbed secret id in test: ' + secretId);
  };
  mod = await import('../../../../../../../infra/aws/users/lambda/portal-authorizer/index.mjs');
});

function signRenderToken(claims, { key = privateKey, audience = 'irpt-render',
                                   issuer = 'opal-irpt-render', expiresIn = '5m' } = {}) {
  return jwt.sign(claims, key, { algorithm: 'RS256', issuer, audience, expiresIn });
}

function eventFor(routeKey, pathParameters, token) {
  return {
    routeKey,
    path: routeKey.split(' ')[1],
    httpMethod: 'GET',
    pathParameters,
    headers: { Authorization: 'Bearer ' + token, 'x-opal-origin-verify': ORIGIN_SECRET_VALUE },
  };
}

const BASE_CLAIMS = {
  sub: 'render:r-1', role: 'renderer', tier: 'render', firmId: '49financial',
  delegator: 'advisor.a@49financial.com', bundle: 'bundle-1', revision: 'rev-1',
  accountSetId: 'AS-1', jobId: 'JOB-1', reportId: 'REP-1',
};

// -------------------------------------------------------------- arm (a): route table shape
test('RENDER_ROUTE_CLAIMS names exactly the three GETs, each to its own path-id claim', () => {
  assert.deepEqual(Object.keys(mod.RENDER_ROUTE_CLAIMS).sort(), [
    'GET /api/scoped/investor-reporting/analysis/{jobId}/sections',
    'GET /api/scoped/investor-reporting/narrative/{reportId}',
    'GET /api/scoped/investor-reporting/performance/{accountSetId}',
  ]);
  assert.equal(
    mod.RENDER_ROUTE_CLAIMS['GET /api/scoped/investor-reporting/performance/{accountSetId}'],
    'accountSetId');
  assert.equal(
    mod.RENDER_ROUTE_CLAIMS['GET /api/scoped/investor-reporting/analysis/{jobId}/sections'],
    'jobId');
  assert.equal(
    mod.RENDER_ROUTE_CLAIMS['GET /api/scoped/investor-reporting/narrative/{reportId}'],
    'reportId');
});

// -------------------------------------------------------- the three routes, matching ids: PASS
test('the three named routes, each with its matching path id, are authorized', async () => {
  const cases = [
    ['GET /api/scoped/investor-reporting/performance/{accountSetId}',
     { accountSetId: 'AS-1' }],
    ['GET /api/scoped/investor-reporting/analysis/{jobId}/sections', { jobId: 'JOB-1' }],
    ['GET /api/scoped/investor-reporting/narrative/{reportId}', { reportId: 'REP-1' }],
  ];
  for (const [routeKey, pathParameters] of cases) {
    const token = signRenderToken(BASE_CLAIMS);
    const result = await mod.handler(eventFor(routeKey, pathParameters, token));
    assert.equal(result.isAuthorized, true, routeKey);
    assert.equal(result.context.renderDelegate, 'true');
    assert.equal(result.context.renderDelegator, BASE_CLAIMS.delegator);
  }
});

// ------------------------------------------------- arm (b), route half: a FOURTH route: DENY
test('a fourth, non-render-scoped route is denied outright, never a fallthrough', async () => {
  const token = signRenderToken(BASE_CLAIMS);
  const result = await mod.handler(
    eventFor('GET /api/scoped/investor-reporting/holdings/{accountSetId}',
            { accountSetId: 'AS-1' }, token));
  assert.equal(result.isAuthorized, false);
});

// --------------------------------------------------- arm (b), id half: a SWAPPED path id: DENY
test('the same route with a swapped path id is denied', async () => {
  const token = signRenderToken(BASE_CLAIMS);
  const result = await mod.handler(eventFor(
    'GET /api/scoped/investor-reporting/performance/{accountSetId}',
    { accountSetId: 'AS-DIFFERENT' }, token));
  assert.equal(result.isAuthorized, false);
});

test('a render token on a print-adjacent but unlisted route is denied', async () => {
  const token = signRenderToken(BASE_CLAIMS);
  const result = await mod.handler(eventFor('GET /investor-reporting/print', {}, token));
  assert.equal(result.isAuthorized, false);
});

// ------------------------------------------------------------------- wrong signing key: DENY
test('a token claiming the render audience but signed by the WRONG key is denied', async () => {
  const token = signRenderToken(BASE_CLAIMS, { key: wrongPrivateKey });
  const result = await mod.handler(eventFor(
    'GET /api/scoped/investor-reporting/performance/{accountSetId}',
    { accountSetId: 'AS-1' }, token));
  assert.equal(result.isAuthorized, false);
});

test('an expired render token is denied', async () => {
  const token = signRenderToken(BASE_CLAIMS, { expiresIn: '-1s' });
  const result = await mod.handler(eventFor(
    'GET /api/scoped/investor-reporting/performance/{accountSetId}',
    { accountSetId: 'AS-1' }, token));
  assert.equal(result.isAuthorized, false);
});

test('a wrong-issuer render-audience token is denied', async () => {
  const token = signRenderToken(BASE_CLAIMS, { issuer: 'not-opal-irpt-render' });
  const result = await mod.handler(eventFor(
    'GET /api/scoped/investor-reporting/performance/{accountSetId}',
    { accountSetId: 'AS-1' }, token));
  assert.equal(result.isAuthorized, false);
});

// ------------------------------------------------------------------ isRenderAudienceToken()
test('isRenderAudienceToken is a claim PEEK, true only for aud=irpt-render', () => {
  const renderToken = signRenderToken(BASE_CLAIMS);
  assert.equal(mod.isRenderAudienceToken(renderToken), true);

  const humanToken = jwt.sign({ sub: 'advisor.a@49financial.com', tier: 'partner',
                                role: 'user', userType: 'Advisor' },
                              humanPrivateKey, { algorithm: 'RS256', issuer: 'opal-portal-auth',
                                                 audience: 'opal-portal-api', expiresIn: '1h' });
  assert.equal(mod.isRenderAudienceToken(humanToken), false);
  assert.equal(mod.isRenderAudienceToken('not-even-a-jwt'), false);
});

// -------------------------------------------------------------------------- arm (f): human path
test('arm (f) -- a human portal token behaves exactly as before on the SAME routes ' +
    '(negative-widening: this cell never touches the human path)', async () => {
  const humanToken = jwt.sign(
    { sub: 'advisor.a@49financial.com', tier: 'partner', role: 'user',
     userType: 'Advisor', firmId: '49financial', advisorId: 'ADV-A-0001' },
    humanPrivateKey,
    { algorithm: 'RS256', issuer: 'opal-portal-auth', audience: 'opal-portal-api',
     expiresIn: '1h' });

  const onRenderRoute = await mod.handler(eventFor(
    'GET /api/scoped/investor-reporting/performance/{accountSetId}',
    { accountSetId: 'AS-1' }, humanToken));
  // The CURRENT default-allow behavior (index.mjs's own docstring: "Currently default-allow"):
  // an authenticated human token is authorized regardless of route, exactly as before this
  // cell -- this cell adds a NEW explicit-deny branch for RENDER tokens; it does not add any
  // new restriction to the human path.
  assert.equal(onRenderRoute.isAuthorized, true);
  assert.equal(onRenderRoute.context.email, 'advisor.a@49financial.com');
  assert.equal(onRenderRoute.context.role, 'user');
  assert.equal(Object.prototype.hasOwnProperty.call(onRenderRoute.context, 'renderDelegate'),
              false, 'a human context must never carry a render-delegate marker');

  const onOrdinaryRoute = await mod.handler(
    eventFor('GET /api/scoped/investor-reporting/holdings/{accountSetId}',
            { accountSetId: 'AS-1' }, humanToken));
  assert.equal(onOrdinaryRoute.isAuthorized, true);
});

test('a human token that happens to name accountSetId in pathParameters still ' +
    'authorizes normally (not accidentally parsed by the render route table)', async () => {
  const humanToken = jwt.sign(
    { sub: 'advisor.a@49financial.com', tier: 'partner', role: 'user', userType: 'Advisor' },
    humanPrivateKey,
    { algorithm: 'RS256', issuer: 'opal-portal-auth', audience: 'opal-portal-api',
     expiresIn: '1h' });
  const result = await mod.handler(eventFor(
    'GET /api/scoped/investor-reporting/performance/{accountSetId}',
    { accountSetId: 'anything' }, humanToken));
  assert.equal(result.isAuthorized, true);
});
