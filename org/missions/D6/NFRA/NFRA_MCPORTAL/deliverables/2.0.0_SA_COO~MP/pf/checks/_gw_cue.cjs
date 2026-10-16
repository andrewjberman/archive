// MP-pf-11 check helper (the issuer's): loads a rendered Gateway page in a REAL browser (Edge, headless, viewport emulation) and reads the scroll cue of the Indexes paragraphs.
// prints `indexes=<n> cued=<n> uncued=<n> scrolls=<n> ok=<yes|no>` where
//   cued   = p.gateway-indexes whose computed background-image holds 4 linear-gradient( layers and whose background-attachment reads `local, local, scroll, scroll` (the SAME cue as .gateway-scroll),
//   scrolls = p.gateway-indexes whose content is wider than its box (the long-name paragraphs: the cue is for these).
// ok = at least one paragraph scrolls, every paragraph is cued, and the cue's gradients equal the .gateway-scroll box's (same background-image string).
// usage: node _gw_cue.cjs <playwright-core dir> <html path> <width>
const [, , pwdir, html, width] = process.argv
const { chromium } = require(pwdir)
;(async () => {
  const browser = await chromium.launch({ channel: 'msedge', headless: true })
  const ctx = await browser.newContext({ viewport: { width: Number(width), height: 900 } })
  const page = await ctx.newPage()
  await page.goto('file:///' + html.replace(/^\/+/, ''))
  const r = await page.evaluate(() => {
    const ref = document.querySelector('.gateway-scroll')
    const refImage = ref ? getComputedStyle(ref).backgroundImage : ''
    const ps = Array.from(document.querySelectorAll('p.gateway-indexes'))
    let cued = 0
    let scrolls = 0
    let same = 0
    for (const p of ps) {
      const cs = getComputedStyle(p)
      const layers = (cs.backgroundImage.match(/linear-gradient\(/g) || []).length
      const att = cs.backgroundAttachment.replace(/\s+/g, ' ').trim()
      if (layers === 4 && att === 'local, local, scroll, scroll') cued += 1
      if (cs.backgroundImage === refImage && refImage !== '') same += 1
      if (p.scrollWidth > p.clientWidth + 1) scrolls += 1
    }
    return { n: ps.length, cued, scrolls, same, refLayers: (refImage.match(/linear-gradient\(/g) || []).length }
  })
  const ok = r.n > 0 && r.scrolls > 0 && r.cued === r.n && r.same === r.n && r.refLayers === 4
  console.log('indexes=%d cued=%d uncued=%d scrolls=%d same-as-table-cue=%d ok=%s', r.n, r.cued, r.n - r.cued, r.scrolls, r.same, ok ? 'yes' : 'no')
  await browser.close()
})().catch((e) => { console.log('cue read failed: ' + (e && e.message ? e.message.split('\n')[0] : e)); process.exit(3) })
