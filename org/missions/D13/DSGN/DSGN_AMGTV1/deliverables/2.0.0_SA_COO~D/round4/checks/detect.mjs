// DSGN_AMGTV1 round 4, AV-w-1 AC2 -- the walker's sign-in detector as a pure function (no browser, no AWS).
// Contract: `.claude/skills/ui-walk/signin_detect.mjs` exports `isSignInPage({ path, hasEmail, hasPassword })` -> boolean:
// true on the portal's sign-in route (/login, or a path under /login/) or when both the email and password inputs are
// visible; false otherwise -- a page with only an email field, or a route that merely starts with the letters "login",
// is not the sign-in page.
// usage (repo root): node <this>
import path from 'node:path'
import { pathToFileURL } from 'node:url'
import { execSync } from 'node:child_process'
const root = execSync('git rev-parse --show-toplevel').toString().trim()
const file = path.join(root, '.claude/skills/ui-walk/signin_detect.mjs')
let fn
try { fn = (await import(pathToFileURL(file).href)).isSignInPage } catch (e) { fn = null; console.log('module not loadable:', String(e.message).split('\n')[0]) }
const cases = [
  [{ path: '/login', hasEmail: false, hasPassword: false }, true, 'the sign-in route'],
  [{ path: '/login/', hasEmail: true, hasPassword: true }, true, 'the sign-in route with its form'],
  [{ path: '/security-analysis', hasEmail: true, hasPassword: true }, true, 'the sign-in form on another path'],
  [{ path: '/security-analysis', hasEmail: false, hasPassword: false }, false, 'a signed-in page'],
  [{ path: '/security-analysis', hasEmail: true, hasPassword: false }, false, 'an email field alone'],
  [{ path: '/login-history', hasEmail: false, hasPassword: false }, false, 'a route that only starts with "login"'],
]
let pass = 0
for (const [input, want, name] of cases) {
  let got
  try { got = typeof fn === 'function' ? fn(input) : 'NO FUNCTION' } catch (e) { got = 'THREW ' + e.message }
  const ok = got === want
  if (ok) pass += 1
  console.log(`${ok ? 'CASE PASS' : 'CASE FAIL'} ${name} :: want=${want} got=${got}`)
}
console.log(`SIGN-IN DETECTOR: ${pass} of ${cases.length} cases`)
process.exit(pass === cases.length ? 0 : 1)
