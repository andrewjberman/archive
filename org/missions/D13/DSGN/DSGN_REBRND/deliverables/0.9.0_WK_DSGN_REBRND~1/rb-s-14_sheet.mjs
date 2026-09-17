// rb14-sheet.mjs -- the side-by-side sheet: one row per IV.3 dimension, the site file's value beside the
// portal file's, with the three portal renders as thumbnails. A render of MEASUREMENTS, not of the site
// (no site render is on record; row DSGN_REBRND-W1-S34). Ran from <WS>/.scratch/; the deliverables copy is
// committed as evidence (comment-only difference).
import { readFileSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
const require = createRequire('C:/tmp/wk-dsgn-1j/portal/package.json')
const { chromium } = require('playwright-core')
const WS = 'C:/tmp/wk-dsgn-1j/'
const OUT = WS + 'org/missions/D13/DSGN/DSGN_REBRND/deliverables/0.9.0_WK_DSGN_REBRND~1/'
const site = JSON.parse(readFileSync(WS + 'design/brand/opalinvest.com.json', 'utf8'))
const p = JSON.parse(readFileSync(WS + 'design/brand/portal-routes.json', 'utf8'))
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
const sw = (hex, label) => `<span class="sw" style="background:${hex}"></span><code>${esc(hex)}</code> ${esc(label || '')}`
const routes = ['/market', '/positioning', '/portfolio-management']
const arr = a => Array.isArray(a) ? a.map(v => v === null ? 'n/a' : v).join(' / ') : a
const d = p.siteDelta
const rows = [
  ['Typeface', `${esc(site.typography.family)}, exclusive, ${arr(site.typography.elementCount)} elements`,
    `${esc(p.typography.family)} ${arr(p.typography.elementCount)} elements; Inter ${p.typography.otherFamilies[0].count} on /market (word cloud)`, d.typeface.measuredComparison],
  ['Numerals', 'brief IV.3: Lato tabular (the site file takes no numeral reading)',
    `Lato, tabular-nums on ${arr(p.typography.numerals.elementsWithDigits)} digit-bearing elements`, d.numerals.measuredComparison],
  ['Canvas', `${sw(site.color.canvas.hex)} DOM share ${arr(site.color.canvas.surfaceSharePct)}%; band ${sw(site.color.darkField.hex)} ${arr(site.color.darkField.surfaceSharePct)}%`,
    `${sw(p.color.canvas.hex)} DOM share ${arr(p.color.canvas.surfaceSharePct)}%, pixel ${arr(p.color.canvas.pixelSharePct)}%; band ${sw(p.color.darkField.hex)} DOM ${arr(p.color.darkField.surfaceSharePct)}%, pixel ${arr(p.color.darkField.pixelSharePct)}%`, d.canvas.measuredComparison],
  ["Navy's role", `${sw(site.color.navy.hex)} ${esc(site.color.navy.role)}, ${arr(site.color.navy.surfaceSharePct)}%`,
    `${sw(p.color.navy.hex)} ${esc(p.color.navy.role)}, pixel ${arr(p.color.navy.pixelSharePct)}%`, d.navyRole.measuredComparison],
  ['Status colours', 'none measured on the site',
    p.color.status.tokens.map(t => `<span class="sw" style="background:hsl(${t.hsl.replace(/ /g, ',')})"></span>${esc(t.name)}`).join(' ') + '<br>rendered /market figures: ' + p.color.status.renderedFigureColours.map(c => sw(c.hex, 'x' + c.textNodes)).join(' '), d.statusColours.measuredComparison],
  ['Chart colours', 'none measured on the site',
    `${p.color.chart.tokens.length} --data-* tokens: ` + p.color.chart.tokens.map(t => `<span class="sw sm" title="${esc(t.name)}" style="background:hsl(${t.hsl.replace(/ /g, ',')})"></span>`).join(''), d.chartColours.measuredComparison],
  ['Loudest colour', `${sw(site.color.accent.hex)} accent at ${arr(site.color.accent.surfaceSharePct)}%`,
    routes.map((r, i) => { const l = Object.values(p.color.loudestChromatic.byRoute)[i]; return l ? `${esc(r)} ${sw(l.hex, l.sharePct + '%')}` : `${esc(r)} n/a` }).join('<br>'), d.loudestColour.measuredComparison],
  ['Radius', site.shape.radiiPx.map(r => `<span class="rad" style="border-radius:${r}px"></span>${r}px`).join(' ') + ' + pill',
    p.shape.radiiPx.map(r => `<span class="rad" style="border-radius:${r}px"></span>${r}px`).join(' ') + ` + pill; 8px on ${arr(p.shape.radius8px.elements)} (on band ${arr(p.shape.radius8px.onBandGround)})`, d.radius.measuredComparison],
  ['Shadows', `${site.shape.shadowCount} drop shadows`,
    `<span class="rad" style="box-shadow:0 10px 15px -3px rgba(0,0,0,.1),0 4px 6px -4px rgba(0,0,0,.1)"></span> ${arr(p.shape.shadowCount)} painting elements (nav rail, a band panel, 4 red glows)`, d.shadows.measuredComparison],
  ['Focus ring', `<span class="btn" style="box-shadow:${site.shape.focusRing}">focus</span> <code>${esc(site.shape.focusRing)}</code>`,
    `<span class="btn" style="box-shadow:${p.shape.focusRing.market}">focus</span> <code>${esc(p.shape.focusRing.market)}</code>`, d.focusRing.measuredComparison],
  ['color-scheme', 'n/a (brief IV.3)', `html ${arr(p.color.colorScheme.html)}; body ${arr(p.color.colorScheme.body)}`, d.colorScheme.measuredComparison],
]
const thumbs = Object.values(p.method.renders).map(r => `<figure><img src="file:///${WS}${r}"><figcaption>${esc(r.split('/').pop())}</figcaption></figure>`).join('')
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
body{font-family:Lato,Arial,sans-serif;margin:24px;background:#fff;color:#111;font-size:13px}
h1{font-size:18px;margin:0 0 4px} p.m{margin:0 0 14px;color:#444}
table{border-collapse:collapse;width:100%} th,td{border:1px solid #ccd;padding:8px;vertical-align:top;text-align:left}
th{background:#eef} td.k{font-weight:700;width:120px} td.c{width:230px;color:#333}
.sw{display:inline-block;width:18px;height:18px;border:1px solid #999;vertical-align:middle;margin-right:3px}
.sw.sm{width:12px;height:12px;margin-right:1px}
.rad{display:inline-block;width:34px;height:24px;background:#dde;border:1px solid #889;vertical-align:middle;margin:0 4px}
.btn{display:inline-block;padding:4px 10px;background:#fff;border:1px solid #889;margin:6px}
code{font-size:11px} figure{display:inline-block;margin:10px 10px 0 0;vertical-align:top} img{width:440px;border:1px solid #ccd} figcaption{font-size:11px}
</style></head><body>
<h1>RB-s-14 side-by-side: design/brand/opalinvest.com.json (site, ${esc(site.captured)}) | design/brand/portal-routes.json (portal, ${esc(p.captured)})</h1>
<p class="m">One row per brief IV.3 dimension. Both columns are rendered from the two files; this sheet is a render of MEASUREMENTS, not of the site (no site render is on record, row DSGN_REBRND-W1-S34). Glyphs render in this sheet's own font. The last column is the file's measuredComparison, not a verdict (RB14-AC4 is graded at L9).</p>
<table><tr><th>Dimension</th><th>Site</th><th>Portal (${routes.join(', ')})</th><th>measuredComparison</th></tr>
${rows.map(r => `<tr><td class="k">${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td><td class="c">${esc(r[3])}</td></tr>`).join('\n')}
</table>${thumbs}</body></html>`
writeFileSync(WS + '.scratch/rb14-sheet.html', html)
const browser = await chromium.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
await page.goto('file:///' + WS + '.scratch/rb14-sheet.html')
await page.waitForTimeout(800)
const imgs = await page.evaluate(() => Array.from(document.images).map(i => i.naturalWidth > 0))
await page.screenshot({ path: OUT + 'rb-s-14_side-by-side_1440.png', fullPage: true })
console.log('SHEET rows', rows.length, 'thumbnails loaded', imgs.filter(Boolean).length, 'of', imgs.length, 'SAVED', OUT + 'rb-s-14_side-by-side_1440.png')
await browser.close()
