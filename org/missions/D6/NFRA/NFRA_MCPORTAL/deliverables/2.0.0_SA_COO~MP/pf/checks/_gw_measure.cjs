// MP-pf-8 check helper (the issuer's): loads a rendered Gateway page in a REAL browser (Edge, headless, a viewport of the stated width: emulation, not --window-size, so 390 is really 390)
// and prints `scrollWidth=<n> innerWidth=<n> offenders=<n> ok=<yes|no>`. offenders = elements outside a .gateway-scroll box whose content is wider than their own box.
// usage: node _gw_measure.cjs <playwright-core dir> <html path> <width>
const [, , pwdir, html, width] = process.argv
const { chromium } = require(pwdir)
;(async () => {
  const browser = await chromium.launch({ channel: 'msedge', headless: true })
  const ctx = await browser.newContext({ viewport: { width: Number(width), height: 900 } })
  const page = await ctx.newPage()
  await page.goto('file:///' + html.replace(/^\/+/, ''))
  const r = await page.evaluate(() => {
    const off = []
    for (const e of document.querySelectorAll('body *')) {
      if (e.closest('.gateway-scroll')) continue
      if (e.clientWidth > 0 && e.scrollWidth > e.clientWidth + 1) off.push(e.tagName + '.' + String(e.className).split(' ')[0])
    }
    return { sw: document.documentElement.scrollWidth, iw: window.innerWidth, off: off.length, first: off.slice(0, 3).join(',') }
  })
  console.log('scrollWidth=%d innerWidth=%d offenders=%d ok=%s %s', r.sw, r.iw, r.off, r.sw <= r.iw ? 'yes' : 'no', r.first)
  await browser.close()
})().catch((e) => { console.log('measure failed: ' + (e && e.message ? e.message.split('\n')[0] : e)); process.exit(3) })
