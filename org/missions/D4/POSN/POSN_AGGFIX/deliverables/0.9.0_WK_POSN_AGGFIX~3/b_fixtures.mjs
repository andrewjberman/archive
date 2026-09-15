// POSN_AGGFIX.TO-B1-1 (slot ~3) -- THE FIXTURES FOR <FIVE_BOOKS_DOM_B>, BUILT FROM SERVED BYTES BY VERSIONID.
//
// The order names them: the served AGG block of s3://opal-data-portal-v2/json/positioning/positioning_data.json
// VersionId aJ7nhwRKko3H_AMRzsNvvwkf1NiO9aou re-keyed into the 1.1 payload (status OK) is the aggregate fixture;
// the same object minus current_holdings.AGG is the shared-file fixture. Beside them, pinned the same way so a
// BEFORE and an AFTER run read identical bytes: the attribution feed and the ETF artifact the page also asks for.
//
// Every raw object is accepted ONLY on md5 equality with this manifest; a missing raw is fetched BY VERSIONID,
// never by key alone (a key-only read returns whatever is served that minute).
import { readFileSync, existsSync, mkdirSync } from 'node:fs'
import { spawnSync } from 'node:child_process'
import { gunzipSync } from 'node:zlib'
import { createHash } from 'node:crypto'
import path from 'node:path'

export const MANIFEST = [
  {
    urlkey: '/api/general/positioning/positioning_data.json',
    bucket: 'opal-data-portal-v2',
    key: 'json/positioning/positioning_data.json',
    VersionId: 'aJ7nhwRKko3H_AMRzsNvvwkf1NiO9aou',
    local: '.scratch/fx/posn.raw',
    gzip: true,
    md5: '797a5947d5c2a4a93920c6dd9d3096e8',
  },
  {
    urlkey: '/api/general/positioning/holdings_attribution_data.json',
    bucket: 'opal-data-portal-v2',
    key: 'json/positioning/holdings_attribution_data.json',
    VersionId: 'mOBBmXhjOyNPM2ue_.3C9G1eR79lUrlk',
    local: '.scratch/fx/attr.raw',
    gzip: false,
    md5: '6455a15c85827a4e3f58a181b7d28114',
  },
  {
    urlkey: '/api/general/etfs/positioning_data.json',
    bucket: 'opal-data-portal-v2',
    key: 'platinum/etfs/positioning_data.json',
    VersionId: 'MkASX8obEltFZpHHzNa81cuAVXKf7wR2',
    local: '.scratch/fx/etf.raw',
    gzip: false,
    md5: '570bfd51281a5316dd36aabf13797843',
  },
]

export const AGG_URLKEY = '/api/general/positioning/opal_aggregate.json'
const MODEL_CODES = ['UST', 'ST', 'INT', 'LT', 'ULT']
const md5 = (b) => createHash('md5').update(b).digest('hex')

/**
 * @param root   the workspace root (the fixtures live under <root>/.scratch/fx)
 * @param opts.mutate  optional (fixtures) => description; applied to a DEEP COPY after the build (the control)
 * @returns { fixtures, lines } -- lines is the printed provenance, one fixture key per line
 */
export function buildFixtures(root, opts = {}) {
  const lines = []
  const raws = {}
  for (const m of MANIFEST) {
    const local = path.join(root, m.local)
    if (!existsSync(local)) {
      mkdirSync(path.dirname(local), { recursive: true })
      const r = spawnSync('bash', ['.tools/aws', 's3api', 'get-object', '--bucket', m.bucket, '--key', m.key,
        '--version-id', m.VersionId, local.replace(/\\/g, '/')], { cwd: root, encoding: 'utf8',
        env: { ...process.env, MSYS_NO_PATHCONV: '1' } })
      lines.push('FETCHED ' + m.key + ' @' + m.VersionId + ' rc=' + r.status)
    }
    const raw = readFileSync(local)
    const got = md5(raw)
    if (got !== m.md5) {
      throw new Error('BLOCKED: ' + m.key + ' md5 ' + got + ' differs from the manifest ' + m.md5)
    }
    raws[m.urlkey] = JSON.parse((m.gzip ? gunzipSync(raw) : raw).toString('utf8'))
    lines.push('FIXTURE ' + m.urlkey + '  <- s3://' + m.bucket + '/' + m.key + ' VersionId=' + m.VersionId +
      ' bytes=' + raw.length + ' md5=' + got + ' (manifest match)')
  }

  const posn = raws['/api/general/positioning/positioning_data.json']
  const agg = posn.current_holdings && posn.current_holdings.AGG
  if (!agg || !Array.isArray(agg.holdings) || agg.holdings.length === 0) {
    throw new Error('BLOCKED: the pinned positioning_data.json carries no current_holdings.AGG holdings')
  }

  // THE SHARED-FILE FIXTURE: the same object minus current_holdings.AGG, and nothing else changed.
  const shared = JSON.parse(JSON.stringify(posn))
  delete shared.current_holdings.AGG

  // THE AGGREGATE FIXTURE: the served AGG block, byte-for-byte as a value, inside the 1.1 keys. The fields the
  // served shared file does not carry (weights, members, reconciliation) are derived from its own per-book aum
  // and LABELLED as fixture-derived; the page reads none of them.
  const aum = Object.fromEntries(MODEL_CODES.map((c) => [c, Number(posn.current_holdings[c]?.aum ?? 0)]))
  const sum = MODEL_CODES.reduce((s, c) => s + aum[c], 0)
  const weights = Object.fromEntries(MODEL_CODES.map((c) => [c, sum > 0 ? aum[c] / sum : 0]))
  const fileTotal = Number(agg.total_aum ?? sum)
  const aggregate = {
    status: 'OK',
    reason: null,
    generated_at: posn.generated_at,
    data_as_of: posn.data_as_of,
    current_holdings: { AGG: JSON.parse(JSON.stringify(agg)) },
    weights,
    weights_source: {
      key: 'json/positioning/positioning_data.json',
      version_id: MANIFEST[0].VersionId,
      period: 'FIXTURE: the served AGG block re-keyed; weights from current_holdings[code].aum',
    },
    members: { ...aum, blends: [] },
    left_out: [],
    reconciliation: {
      five_primary_sum: sum,
      members_sum: sum,
      file_total_model_aum: fileTotal,
      gap: fileTotal - sum,
      gap_explanation_ref: 'FIXTURE: not a producer output',
    },
  }

  let fixtures = {
    '/api/general/positioning/positioning_data.json': shared,
    '/api/general/positioning/holdings_attribution_data.json': raws['/api/general/positioning/holdings_attribution_data.json'],
    '/api/general/etfs/positioning_data.json': raws['/api/general/etfs/positioning_data.json'],
    [AGG_URLKEY]: aggregate,
  }
  lines.push('SHARED-FILE FIXTURE: current_holdings keys ' + JSON.stringify(Object.keys(shared.current_holdings)) +
    ' (AGG removed; the source carried ' + JSON.stringify(Object.keys(posn.current_holdings)) + ')')
  lines.push('AGGREGATE FIXTURE (1.1, status OK): AGG holdings=' + agg.holdings.length + ' total_aum=' + agg.total_aum +
    ' per-book aum=' + JSON.stringify(aum) + ' weights=' + JSON.stringify(weights))

  if (opts.mutate) {
    fixtures = JSON.parse(JSON.stringify(fixtures))
    lines.push('MUTATED (control): ' + opts.mutate(fixtures))
  }
  const keys = Object.keys(fixtures)
  const shadow = []
  for (const a of keys) for (const b of keys) if (a !== b && b.includes(a)) shadow.push(a + ' < ' + b)
  lines.push('SHADOW PAIRS among fixture keys: ' + (shadow.length ? shadow.join(' | ') : 'NONE (0 of ' + keys.length + ')'))
  lines.push('BUILT FIXTURES md5=' + md5(Buffer.from(JSON.stringify(fixtures))))
  return { fixtures, lines }
}
