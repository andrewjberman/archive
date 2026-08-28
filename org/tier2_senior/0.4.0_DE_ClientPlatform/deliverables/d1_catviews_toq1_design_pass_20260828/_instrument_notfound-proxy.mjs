/**
 * 404 front-door for category-views.json, so the `absent_by_scope` branch can be
 * EXHIBITED rather than asserted (TQ1-AC3 says exhibit each view).
 *
 * The repo's category-views-fixture-proxy.mjs deliberately never 404s -- an unknown firm
 * gets a SHAPE, because a 404 there would look identical to "the fixture is not wired up".
 * That is right for its job and wrong for mine: `absent_by_scope` is set ONLY on an HTTP
 * 404 (aum.ts:873), so nothing already in the repo can reach that branch.
 *
 * Scratchpad only -- a capture instrument, never committed.
 *
 *   node notfound-proxy.mjs --port 5176 --vite 5185
 */
import http from 'node:http'

const argv = process.argv.slice(2)
const argOf = (flag, dflt) => {
  const i = argv.indexOf(flag)
  return i >= 0 && argv[i + 1] ? Number(argv[i + 1]) : dflt
}
const PORT = argOf('--port', 5176)
const VITE = argOf('--vite', 5185)
let missed = 0

http
  .createServer((req, res) => {
    const path = req.url ?? '/'
    if (path.includes('category-views.json')) {
      missed += 1
      console.log(`  404 #${missed}  ${path}`)
      res.writeHead(404, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' })
      res.end('{"error":"not found"}')
      return
    }
    const headers = { ...req.headers }
    delete headers.host
    delete headers['accept-encoding']
    // 'localhost', NOT '127.0.0.1' -- vite binds IPv6-only ([::1]) on this box, and an
    // IPv4 literal upstream ECONNREFUSEs while curl to localhost succeeds.
    const up = http.request(
      { host: 'localhost', port: VITE, path, method: req.method, headers },
      r => {
        res.writeHead(r.statusCode ?? 502, r.headers)
        r.pipe(res)
      }
    )
    up.on('error', e => {
      res.writeHead(502, { 'Content-Type': 'text/plain' })
      res.end(`notfound-proxy: vite unreachable on ${VITE}: ${e.message}`)
    })
    req.pipe(up)
  })
  .listen(PORT, () => console.log(`404 proxy http://localhost:${PORT} -> vite ${VITE}`))
