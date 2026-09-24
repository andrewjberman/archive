// IRPT_BCKEND.TO-IB-rtr-e -- THE ONE OFFLINE ACTUAL-MODULE CHAIN, Node half.
//
// Bridges the REAL V3 edge branch (auth-validator-edge/index.mjs, render_auth.mjs) and the REAL
// V2 render branch (portal-authorizer/index.mjs's authorizeRenderToken) into one offline call a
// Python driver can subprocess. Pattern taken directly from the CVO's own cross-module probe
// (org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R17_PROBE.mjs, read-only reference for
// this cell, never edited): block every AWS SDK network call at the module-loader level so the
// REAL production files run unmodified and unmocked at the function level -- only the network
// edge (SecretsManagerClient.send / DynamoDBClient.send / S3Client.send) is replaced, and it
// throws if ever reached, which is itself a control: this cell's positive paths never reach it
// (render-key slots and the render public key PEM are injected through each module's own
// documented test seam, never through a live Secrets Manager fetch).
//
// Protocol: one JSON object on stdin, one JSON object on stdout.
//   in:  { token, uri, method, route: {routeKey, pathParameters}, renderPublicKeyPem }
//   out: { v3: {admitted, status, headers, message}, v2: {authorized, context} }
//
// `headers`, when v3 admits, is the CloudFront multi-value shape
// (request.headers[name] = [{key, value}]) exactly as index.mjs/render_auth.mjs produce it --
// never flattened here, so the Python side feeds it to the REAL `_scope.normalize_headers`,
// which already documents and handles this exact shape, rather than this bridge re-implementing
// that parsing a second time.
import { registerHooks } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const root = process.argv[2];
if (!root) {
  console.error(JSON.stringify({ error: 'chain_bridge.mjs requires the worktree root as argv[2]' }));
  process.exit(2);
}
const edgePath = path.join(root, 'infra/aws/lambda-edge/auth-validator-edge');
const v2Path = path.join(root, 'infra/aws/users/lambda/portal-authorizer');

const jwtUrl = pathToFileURL(path.join(edgePath, 'node_modules/jsonwebtoken/index.js')).href;
const fake = `export class SecretsManagerClient { async send(){throw Error('NETWORK FORBIDDEN -- offline chain test')} }
export class GetSecretValueCommand {constructor(input){this.input=input}}
export class DynamoDBClient {async send(){throw Error('NETWORK FORBIDDEN -- offline chain test')}}
export class ScanCommand {constructor(input){this.input=input}}
export class S3Client {async send(){throw Error('NETWORK FORBIDDEN -- offline chain test')}}
export class GetObjectCommand {constructor(input){this.input=input}}`;
const fakeUrl = 'data:text/javascript,' + encodeURIComponent(fake);
registerHooks({
  resolve(specifier, context, next) {
    if (specifier === 'jsonwebtoken') return { url: jwtUrl, shortCircuit: true };
    if (specifier.startsWith('@aws-sdk/client-')) return { url: fakeUrl, shortCircuit: true };
    return next(specifier, context);
  },
});

async function main() {
  const raw = await readStdin();
  const cmd = JSON.parse(raw);
  const { token, uri, method, route, renderPublicKeyPem } = cmd;

  const edge = await import(pathToFileURL(path.join(edgePath, 'index.mjs')));
  const ra = await import(pathToFileURL(path.join(edgePath, 'render_auth.mjs')));
  const v2 = await import(pathToFileURL(path.join(v2Path, 'index.mjs')));

  // The SAME test seam the CVO's probe uses -- production code never calls this.
  ra.__setRenderKeySlotsForTest({ current: renderPublicKeyPem, previous: null });
  process.env.IRPT_RENDER_JWT_PUBLIC_KEY_PEM = renderPublicKeyPem;

  const event = {
    Records: [{
      cf: {
        request: {
          uri, method, querystring: '',
          headers: { authorization: [{ key: 'Authorization', value: 'Bearer ' + token }] },
        },
      },
    }],
  };

  const v3Result = await edge.handler(event);
  let v3;
  if (v3Result && v3Result.status) {
    // A refusal shape ({status, statusDescription, headers, body}) -- V3 refused.
    let message = null;
    try { message = JSON.parse(v3Result.body).error; } catch { /* leave null */ }
    v3 = { admitted: false, status: v3Result.status, headers: null, message };
  } else {
    // The forwarded CloudFront request -- V3 admitted and injected headers.
    v3 = { admitted: true, status: null, headers: v3Result.headers, message: null };
  }

  // authorizeRenderToken is called DIRECTLY (never through v2's handler()), exactly as the
  // CVO's own probe does -- handler() runs the DynamoDB-backed origin gate first, which this
  // cell's BOUNDS forbid touching (no AWS call of any kind); authorizeRenderToken itself makes
  // none. This is the REAL exported function, not a restatement of it.
  let v2Out;
  try {
    const answer = v2.authorizeRenderToken(token, route);
    v2Out = { authorized: !!answer.isAuthorized, context: answer.context || {} };
  } catch (e) {
    v2Out = { authorized: false, context: {}, error: e.message || String(e) };
  }

  process.stdout.write(JSON.stringify({ v3, v2: v2Out }));
}

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (chunk) => { data += chunk; });
    process.stdin.on('end', () => resolve(data));
    process.stdin.on('error', reject);
  });
}

main().catch((e) => {
  console.error(JSON.stringify({ error: e.message || String(e), stack: e.stack || '' }));
  process.exit(1);
});
