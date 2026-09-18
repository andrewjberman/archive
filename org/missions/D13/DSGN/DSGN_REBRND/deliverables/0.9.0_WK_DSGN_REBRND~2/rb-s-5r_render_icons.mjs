/**
 * rb-s-5r_render_icons.mjs -- DSGN_REBRND.TO-RB-s-5 Amendment 1, the touch icon and the 32px read.
 *
 * Renders <portal>/public/favicon.svg with the SAME playwright-core + system Edge that
 * portal/scripts/ui-smoke.mjs uses (no new dependency; playwright-core is resolved from the
 * portal's own node_modules). Nothing is fetched from any network location: the SVG is
 * inlined as a data: URL and the page is built with setContent.
 *
 * Writes:
 *   <portal>/public/apple-touch-icon.png      180x180, the apple-touch-icon
 *   <outdir>/rb-s-5r_favicon_32.png           32x32, the favicon at tab size
 *   <outdir>/rb-s-5r_favicon_32_x8.png        the 32x32 render magnified 8x, nearest-neighbour
 *   <outdir>/rb-s-5r_favicon_context.png      the 16px and 32px renders on a light and a dark tab strip
 *
 * For each PNG it prints its size and a pixel census read back from the written bytes:
 * the share of indigo (#5F3BE3 +-12 per channel), white, and transparent pixels, plus
 * three probe pixels (a corner, the ring left of the mark, the centre).
 *
 * Usage: node rb-s-5r_render_icons.mjs <portal root> <outdir>
 */
import { createRequire } from 'node:module'
import { readFileSync, statSync } from 'node:fs'
import path from 'node:path'

const [portal, outdir] = process.argv.slice(2)
if (!portal || !outdir) {
  console.error('usage: node rb-s-5r_render_icons.mjs <portal root> <outdir>')
  process.exit(2)
}
const require = createRequire(path.join(portal, 'package.json'))
const { chromium } = require('playwright-core')
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'

const svgPath = path.join(portal, 'public', 'favicon.svg')
const svg = readFileSync(svgPath)
const svgUrl = 'data:image/svg+xml;base64,' + svg.toString('base64')
console.log('SOURCE:', svgPath, `(${svg.length} B)`)

const browser = await chromium.launch({ executablePath: EDGE, headless: true })

async function renderAt(size, outPath) {
  const page = await browser.newPage({ viewport: { width: size, height: size }, deviceScaleFactor: 1 })
  await page.setContent(
    `<html><body style="margin:0;background:transparent"><img id="i" src="${svgUrl}" width="${size}" height="${size}" style="display:block"></body></html>`
  )
  await page.waitForFunction(() => document.getElementById('i').complete)
  await page.screenshot({ path: outPath, omitBackground: true, clip: { x: 0, y: 0, width: size, height: size } })
  await page.close()
}

async function census(pngPath) {
  const b64 = readFileSync(pngPath).toString('base64')
  const page = await browser.newPage()
  const r = await page.evaluate(async (src) => {
    const img = new Image()
    img.src = src
    await img.decode()
    const c = document.createElement('canvas')
    c.width = img.naturalWidth
    c.height = img.naturalHeight
    const g = c.getContext('2d')
    g.drawImage(img, 0, 0)
    const d = g.getImageData(0, 0, c.width, c.height).data
    let indigo = 0, white = 0, clear = 0, other = 0
    for (let i = 0; i < d.length; i += 4) {
      const [R, G, B, A] = [d[i], d[i + 1], d[i + 2], d[i + 3]]
      if (A < 16) clear++
      else if (Math.abs(R - 95) <= 12 && Math.abs(G - 59) <= 12 && Math.abs(B - 227) <= 12 && A > 240) indigo++
      else if (R > 240 && G > 240 && B > 240 && A > 240) white++
      else other++
    }
    const px = (x, y) => {
      const i = (Math.floor(y) * c.width + Math.floor(x)) * 4
      return `rgba(${d[i]},${d[i + 1]},${d[i + 2]},${d[i + 3]})`
    }
    const n = c.width * c.height
    return {
      w: c.width, h: c.height, n,
      pct: { indigo: (100 * indigo / n).toFixed(1), white: (100 * white / n).toFixed(1),
             transparent: (100 * clear / n).toFixed(1), antialias: (100 * other / n).toFixed(1) },
      corner: px(0, 0), ring: px(c.width * 0.12, c.height * 0.5), centre: px(c.width * 0.5, c.height * 0.5),
    }
  }, 'data:image/png;base64,' + b64)
  await page.close()
  const bytes = statSync(pngPath).size
  console.log(`PNG   : ${pngPath} ${r.w}x${r.h} (${bytes} B)`)
  console.log(`  PIXELS of ${r.n}: indigo ${r.pct.indigo}% white ${r.pct.white}% transparent ${r.pct.transparent}% antialias ${r.pct.antialias}%`)
  console.log(`  PROBE : corner ${r.corner}  ring(12%,50%) ${r.ring}  centre ${r.centre}`)
  return r
}

const touch = path.join(portal, 'public', 'apple-touch-icon.png')
const f32 = path.join(outdir, 'rb-s-5r_favicon_32.png')
await renderAt(180, touch)
await renderAt(32, f32)
const rTouch = await census(touch)
const r32 = await census(f32)

// 8x nearest-neighbour magnification of the 32px render, so a reader sees tab-size pixels.
{
  const b64 = readFileSync(f32).toString('base64')
  const page = await browser.newPage({ viewport: { width: 256, height: 256 }, deviceScaleFactor: 1 })
  await page.setContent(`<html><body style="margin:0;background:#FFFFFF"><img id="i" src="data:image/png;base64,${b64}" width="256" height="256" style="display:block;image-rendering:pixelated"></body></html>`)
  await page.waitForFunction(() => document.getElementById('i').complete)
  const x8 = path.join(outdir, 'rb-s-5r_favicon_32_x8.png')
  await page.screenshot({ path: x8, clip: { x: 0, y: 0, width: 256, height: 256 } })
  await page.close()
  console.log('SAVED :', x8, '(the 32px render magnified 8x, nearest-neighbour, on white)')
}

// Context strip: the icon at 16px and 32px, beside a tab title, on a light and a dark tab.
{
  const page = await browser.newPage({ viewport: { width: 480, height: 120 }, deviceScaleFactor: 1 })
  const tab = (bg, fg) => `<div style="display:flex;align-items:center;gap:8px;height:60px;padding:0 16px;background:${bg};color:${fg};font:13px Segoe UI,sans-serif">
    <img src="${svgUrl}" width="16" height="16"><span>Opal Invest Dashboard</span>
    <span style="flex:1"></span><img src="${svgUrl}" width="32" height="32"><span>32px</span></div>`
  await page.setContent(`<html><body style="margin:0">${tab('#FFFFFF', '#1F2937')}${tab('#202124', '#E8EAED')}</body></html>`)
  await page.waitForTimeout(300)
  const ctx = path.join(outdir, 'rb-s-5r_favicon_context.png')
  await page.screenshot({ path: ctx, clip: { x: 0, y: 0, width: 480, height: 120 } })
  await page.close()
  console.log('SAVED :', ctx, '(16px and 32px on a light tab strip, then a dark one)')
}

await browser.close()
const ok = rTouch.w === 180 && rTouch.h === 180 && r32.w === 32 && r32.h === 32
  && Number(rTouch.pct.indigo) > 30 && Number(rTouch.pct.white) > 5
console.log('VERDICT:', ok ? 'ICONS-RENDERED' : 'ICONS-SUSPECT')
process.exit(ok ? 0 : 1)
