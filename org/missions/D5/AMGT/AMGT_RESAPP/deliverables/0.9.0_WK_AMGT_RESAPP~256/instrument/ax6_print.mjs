// stage 3: the print GET as the page's own requestPrintPack makes it (GET, bearer), bytes kept as the PDF
import { mkdirSync, writeFileSync } from 'node:fs'
import path from 'node:path'
export async function run(ctx) {
  const { page, opt, OUT, log, settle, setStep } = ctx
  const dir = path.join(OUT, 'data', 'print'); mkdirSync(dir, { recursive: true })
  await page.goto(opt.base + '/security-analysis', { waitUntil: 'domcontentloaded', timeout: 30000 })
  await settle(page, 3000)
  const out = []
  for (const key of ['BA_US_Equity', 'AMD_US_Equity', 'ASML_NA_Equity']) {
    setStep('print ' + key)
    const r = await page.evaluate(async (u) => {
      const t = localStorage.getItem('accessToken'); const t0 = Date.now()
      const resp = await fetch(u, { headers: t ? { Authorization: `Bearer ${t}` } : {} })
      const buf = new Uint8Array(await resp.arrayBuffer())
      let s = ''; for (let i = 0; i < buf.length; i += 0x8000) s += String.fromCharCode.apply(null, buf.subarray(i, i + 0x8000))
      return { status: resp.status, ct: resp.headers.get('content-type'), ms: Date.now() - t0, bytes: buf.length, b64: btoa(s) }
    }, `/api/scoped/amgt/security/${encodeURIComponent(key)}/print`)
    writeFileSync(path.join(dir, key + '.pdf'), Buffer.from(r.b64, 'base64'))
    out.push({ key, status: r.status, content_type: r.ct, ms: r.ms, bytes: r.bytes })
    log('PRINT', key, r.status, r.ct, r.bytes, 'bytes', r.ms, 'ms')
  }
  writeFileSync(path.join(OUT, 'data', 'print', 'print.json'), JSON.stringify(out, null, 1))
}
