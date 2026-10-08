// bb-19 second pass: BA Model tab, wait up to 60 s for "where each input came from" to leave its Loading state. GET only.
import { mkdirSync, writeFileSync } from 'node:fs'
import path from 'node:path'

export async function run(ctx) {
  const { page, opt, OUT, log, settle, setStep, waitForLoaded } = ctx
  const dir = path.join(OUT, 'data', 'ledger')
  mkdirSync(dir, { recursive: true })
  mkdirSync(path.join(OUT, 'shots'), { recursive: true })
  setStep('ledger BA')
  await page.goto(opt.base + '/security-analysis/' + encodeURIComponent('BA_US_Equity'), { waitUntil: 'domcontentloaded', timeout: 30000 })
  await settle(page, 2500)
  await waitForLoaded(page)
  await page.waitForTimeout(2500)
  const b = page.getByRole('button', { name: /^model$/i }).first()
  const t = (await b.count()) ? b : page.getByRole('tab', { name: /^model$/i }).first()
  await t.scrollIntoViewIfNeeded().catch(() => {})
  await t.click({ timeout: 4000 }).catch(() => {})
  const t0 = Date.now()
  const reads = []
  let state = 'ceiling'
  while (Date.now() - t0 < 60000) {
    const r = await page.evaluate(() => ({ ledger: document.querySelectorAll('[data-ledger-class]').length, loading: /Loading where each input came from/.test(document.body.innerText || ''), heading: /Where each input came from/i.test(document.body.innerText || '') }))
    reads.push({ ms: Date.now() - t0, ...r })
    if (r.ledger > 0) { state = 'ledger-drawn'; break }
    if (!r.loading && Date.now() - t0 > 4000) { state = r.heading ? 'heading-without-rows' : 'no-ledger-no-loading'; break }
    await page.waitForTimeout(1000)
  }
  const waited = Date.now() - t0
  const led = await page.evaluate(() => ({ ledger: [...document.querySelectorAll('[data-ledger-class]')].map((li) => ({ cls: li.getAttribute('data-ledger-class'), text: (li.innerText || '').trim() })), still_loading: /Loading where each input came from/.test(document.body.innerText || '') }))
  writeFileSync(path.join(dir, 'ba_model_ledger_wait.json'), JSON.stringify({ state, waited_ms: waited, reads: reads.filter((_, i) => i % 5 === 0 || i === reads.length - 1), ...led }, null, 1))
  log('LEDGER', state, waited, 'ms', JSON.stringify(led).slice(0, 400))
  const target = page.locator('[data-ledger-class]').first()
  if (await target.count()) await target.scrollIntoViewIfNeeded().catch(() => {})
  else await page.getByText(/where each input came from/i).first().scrollIntoViewIfNeeded().catch(() => {})
  const file = 'shots/901-ledger-ba-model-tab-after-wait.png'
  await page.screenshot({ path: path.join(OUT, file), fullPage: false })
  log('CAPTURE', file)
}
