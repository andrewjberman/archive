// rb15_composite.mjs -- render the DSGN_REBRND RB-s-15 pack page to PNG with system Edge (the ui-smoke instrument's
// browser). Local file only: every non-file: request is ABORTED and counted, so the render proves no egress.
// usage: node rb15_composite.mjs <pack.html> <composite.png> <firstscreen.png>
import { createRequire } from 'node:module'
const require = createRequire('C:/tmp/wk-dsgn-1k/portal/package.json')
const { chromium } = require('playwright-core')

const [html, outFull, outFirst] = process.argv.slice(2)
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const counts = { file: 0, blocked: 0 }
const blocked = []

async function shoot(width, height, out, fullPage) {
  const page = await browser.newPage({ viewport: { width, height } })
  await page.route('**/*', r => {
    const u = r.request().url()
    if (u.startsWith('file:')) { counts.file++; return r.continue() }
    counts.blocked++; blocked.push(u); return r.abort()
  })
  await page.goto('file:///' + html.replace(/^\/c\//, 'C:/'), { waitUntil: 'load' })
  const imgs = await page.evaluate(() => [...document.images].map(i => ({ src: i.getAttribute('src'), ok: i.complete && i.naturalWidth > 0, w: i.naturalWidth, h: i.naturalHeight })))
  const firstScreen = await page.evaluate(() => {
    const el = document.querySelector('.notshown')
    const r = el.getBoundingClientRect()
    return { top: Math.round(r.top), bottom: Math.round(r.bottom), viewportH: window.innerHeight }
  })
  await page.screenshot({ path: out, fullPage })
  console.log(`VIEWPORT: ${width}x${height} fullPage=${fullPage}`)
  console.log(`IMAGES  : ${imgs.filter(i => i.ok).length} of ${imgs.length} loaded`)
  for (const i of imgs) console.log(`  ${i.ok ? 'OK ' : 'BAD'} ${i.src} ${i.w}x${i.h}`)
  console.log(`NOT-SHOWN BOX: top=${firstScreen.top} bottom=${firstScreen.bottom} viewportH=${firstScreen.viewportH} ` +
    `-> ${firstScreen.bottom <= firstScreen.viewportH ? 'WHOLLY ON FIRST SCREEN' : 'SPILLS PAST FIRST SCREEN'}`)
  console.log(`SAVED   : ${out}`)
  await page.close()
}

await shoot(1600, 1000, outFull, true)
await shoot(960, 1080, outFirst, false)
console.log(`REQUESTS: file=${counts.file} non-file-blocked=${counts.blocked}`, blocked.slice(0, 5))
await browser.close()
