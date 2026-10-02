/**
 * r29c.build.cjs -- DSGN_AMGTV1 round 29, AV-zg-4 CHATTER COLLAGE fixtures and BASE captures (issuer 2.0.0_SA_COO~D).
 *
 * Usage: cd C:/tmp/wk-dsgn-amgtv1-70 && node <this file>
 *   (the cwd's portal/ must be BASE dcdc89b1 for the captures; the planted fixtures are written whatever the cwd).
 *
 * WRITES, beside this file:
 *   r29c.chatter.toned.json  -- round16/fixtures/r16g.collected.chatter.json (95 served rows, the CONTRACT s.1 shape) with the
 *       RESAPP FWD-36 row fields PLANTED on the 17 rows collected in 2026-09: `tone` (-1..+1), `voters`, `articles_total`.
 *       Row 3 of the 17 carries tone null (voters 0); rows 6 and 10 carry NO tone field (today's served shape). These are
 *       FIXTURE values, not measurements: the route does not serve tone yet.
 *   r29c.chatter.dense.json  -- the same 95 keys and served display names, ALL collected in one month (2026-09), counts
 *       falling from 60 to 1 in a hash order (so payload order is not size order). The stress case for "every name of the
 *       period in one panel": the whole covered universe lit at once (the live September walk read 57).
 *   topiccloud.keywords.json -- 22 planted keywords for the Topic Cloud render (tones on every ramp boundary).
 * CAPTURES (BASE only; refused on any other portal HEAD):
 *   TopicCloud.base.tsx.txt  -- portal/src/components/market-performance/TopicCloud.tsx at BASE, CRLF -> LF.
 *   getSentimentColor.base.txt -- the function block of that file (`function getSentimentColor(` .. its closing brace).
 *   topiccloud.base.html     -- the Topic Cloud render at BASE through round29/checks/collage/_tc.cjs.
 *   base.json                -- the BASE portal HEAD and the sha256 of portal/package.json.
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

const HERE = __dirname;
const D = path.join(HERE, '..', '..', '..');
const BASE_HEAD = 'dcdc89b1c787dd7ab75cfb26546c8dbc0412b772';
const unwrap = (x) => (x && x.payload ? x.payload : x);
const writeJson = (name, obj) => fs.writeFileSync(path.join(HERE, name), JSON.stringify(obj, null, 1) + '\n');

function hash(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619) >>> 0;
  return h;
}

const SRC = unwrap(JSON.parse(fs.readFileSync(path.join(D, 'round16', 'fixtures', 'r16g.collected.chatter.json'), 'utf8')));

// 1. toned
{
  const data = JSON.parse(JSON.stringify(SRC));
  const MONTH = '2026-09';
  const TONES = [-0.9, -0.31, -0.3, -0.12, -0.05, -0.02, 0, 0.03, 0.05, 0.12, 0.2, 0.45, 1.0, -0.6, 0.08, -0.2, 0.33];
  const lit = data.rows.filter((r) => r.by_month[MONTH] && r.by_month[MONTH].collected > 0);
  let toned = 0;
  lit.forEach((r, i) => {
    const c = r.by_month[MONTH].collected;
    if (i === 2) { r.tone = null; r.voters = 0; r.articles_total = c; return; }
    if (i === 5 || i === 9) return; // no tone field: today's served shape
    r.tone = TONES[i % TONES.length];
    r.voters = 1 + ((i * 7) % 11);
    r.articles_total = c + (i % 4);
    toned += 1;
  });
  writeJson('r29c.chatter.toned.json', {
    _plant_note: 'r16g + RESAPP FWD-36 row fields planted (tone/voters/articles_total) on the rows collected in 2026-09; tone null on ' +
      lit[2].security_key + '; no tone field on ' + lit[5].security_key + ' and ' + lit[9].security_key + '. Fixture values, not measurements.',
    payload: data,
  });
  console.log(`OK: r29c.chatter.toned.json -- ${data.rows.length} rows, ${lit.length} collected in ${MONTH}: ${toned} toned, 1 null, 2 absent`);
}

// 2. dense
{
  const order = [...SRC.rows].sort((a, b) => hash(a.security_key) - hash(b.security_key) || (a.security_key < b.security_key ? -1 : 1));
  const counts = new Map(order.map((r, j) => [r.security_key, Math.max(1, Math.round(60 * Math.pow(0.95, j)))]));
  const rows = SRC.rows.map((r) => {
    const c = counts.get(r.security_key);
    return { security_key: r.security_key, display_name: r.display_name, by_month: { '2026-09': { collected: c, by_publisher: { sa: c } } } };
  });
  writeJson('r29c.chatter.dense.json', {
    _plant_note: 'the 95 served keys of r16g, ALL collected in 2026-09, counts 60 -> 1 in a hash order. Fixture values, not measurements.',
    payload: { as_of: SRC.as_of, source: SRC.source, months: ['2026-09'], partial_months: [], rows, vintage: SRC.vintage },
  });
  const cs = [...counts.values()];
  console.log(`OK: r29c.chatter.dense.json -- ${rows.length} rows all collected; counts ${Math.max(...cs)} .. ${Math.min(...cs)}`);
}

// 3. topic cloud keywords
const KW_TONES = [-0.9, -0.5, -0.31, -0.3, -0.2, -0.05, -0.049, -0.01, 0, 0.001, 0.03, 0.05, 0.051, 0.12, 0.2, 0.21, 0.5, 0.9, 0.33, -0.12, 0.07, -0.4];
const WORDS = ['tariffs', 'earnings', 'guidance', 'buyback', 'layoffs', 'merger', 'dividend', 'rates', 'inflation', 'chips',
  'refinery', 'margins', 'recall', 'lawsuit', 'upgrade', 'downgrade', 'outlook', 'supply', 'demand', 'pricing', 'capex', 'debt'];
const keywords = WORDS.map((w, i) => ({ keyword: w, sentiment: KW_TONES[i], count: 40 - i, ...(i % 3 === 0 ? { size: 10 + (i % 7) } : {}) }));
writeJson('topiccloud.keywords.json', keywords);
console.log(`OK: topiccloud.keywords.json -- ${keywords.length} keywords`);

// 4. BASE captures
const head = spawnSync('git', ['-C', path.join(process.cwd(), 'portal'), 'rev-parse', 'HEAD'], { encoding: 'utf8' });
const at = (head.stdout || '').trim();
if (at !== BASE_HEAD) {
  console.log(`SKIP: captures -- portal HEAD under the cwd is "${at || head.stderr}", not BASE ${BASE_HEAD}`);
  process.exit(0);
}
const tcPath = path.join(process.cwd(), 'portal', 'src', 'components', 'market-performance', 'TopicCloud.tsx');
const tc = fs.readFileSync(tcPath, 'utf8').replace(/\r\n/g, '\n');
fs.writeFileSync(path.join(HERE, 'TopicCloud.base.tsx.txt'), tc);
const s = tc.indexOf('function getSentimentColor(');
const e = tc.indexOf('\n}\n', s);
if (s < 0 || e < 0) { console.log('ERROR: getSentimentColor block not found at BASE'); process.exit(1); }
fs.writeFileSync(path.join(HERE, 'getSentimentColor.base.txt'), tc.slice(s, e + 2) + '\n');
const L = require(path.join(D, 'round15', 'checks', '_load.cjs'));
const html = require(path.join(D, 'round29', 'checks', 'collage', '_tc.cjs'))(L, keywords);
fs.writeFileSync(path.join(HERE, 'topiccloud.base.html'), html);
const pkg = fs.readFileSync(path.join(process.cwd(), 'portal', 'package.json'));
writeJson('base.json', { portal_head: at, package_json_sha256: crypto.createHash('sha256').update(pkg).digest('hex') });
console.log(`OK: captures at BASE ${at.slice(0, 8)} -- TopicCloud ${tc.length} chars, function block ${e + 2 - s} chars, render ${html.length} chars`);
