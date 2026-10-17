import { chromium } from 'playwright-core'
import { existsSync, readFileSync } from 'node:fs'

const EDGE = ['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', 'C:/Program Files/Microsoft/Edge/Application/msedge.exe'].find(existsSync)
const browser = await chromium.launch({ executablePath: EDGE, headless: true })
for (const mode of ['whole', 'late']) {
  const page = await browser.newPage({ viewport: { width: 940, height: 760 } })
  const errors = []
  page.on('pageerror', (e) => errors.push(String(e)))
  await page.route('https://harness.local/**', (route) => {
    const u = new URL(route.request().url())
    if (u.pathname === '/out/entry.js') return route.fulfill({ body: readFileSync('C:/dev/wk-irpt-dashbd-258/portal/scratch_harness/out/entry.js'), contentType: 'text/javascript' })
    return route.fulfill({ body: '<!doctype html><html><head><meta charset="utf-8"></head><style>[data-slot="dashboard-performance-chart"]{height:300px;width:100%;margin-top:12px}</style><body style="background:#fff"><div id="root"></div><script type="module" src="/out/entry.js"></script></body></html>', contentType: 'text/html' })
  })
  await page.goto(`https://harness.local/?mode=${mode}`)
  await page.waitForTimeout(1500)
  const info = await page.evaluate(() => ({
    breaks: document.querySelector('[data-slot="dashboard-chart-breaks"]')?.textContent ?? null,
    headline: document.querySelector('[data-field="window.totalReturn"]')?.textContent ?? null,
    paths: document.querySelectorAll('.recharts-area-curve').length,
    dots: document.querySelectorAll('.recharts-area-dots circle, circle[r="3"]').length,
  }))
  console.log(mode, JSON.stringify(info), errors.length ? 'ERRORS ' + errors.join('|') : '')
  await page.screenshot({ path: `C:/dev/wk-irpt-dashbd-258/portal/scratch_harness/shot_${mode}.png` })
  await page.close()
}
await browser.close()
