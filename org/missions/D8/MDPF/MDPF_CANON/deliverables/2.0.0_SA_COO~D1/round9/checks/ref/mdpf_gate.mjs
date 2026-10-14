/**
 * mdpf_gate.mjs -- MDPF_CANON CN-q-1 (cross-adjudication XA-c7cd, ruled LIVE; row MDPF_CANON-D1-S27).
 *
 * THE GAP: the deployed viewer-request function admitted any valid login to every per-firm leaf under
 * /api/general/mdpf/<folder>/ (public-data-router rewrites that prefix to platinum/mdpf/ with no firm check).
 * THE GATE: a non-internal claim may read only the leaf folders its own firm owns.
 *
 *   claim firmId            leaf folders admitted
 *   opal-capital / Dev      every path under the prefix (the page's isInternal() || isDev(), as aggregate_gate.mjs)
 *   49financial             49financial
 *   inflection              inflection
 *   cottonwood              cottonwood
 *   demo                    global   (the page's MDPF_GLOBAL_VIEW_FIRMS: the demo tenant views the aggregate)
 *   no firm (absent / "")   global
 *   any other firmId        none
 *
 * The map is the page's own: ModelPortfolios.tsx effectiveFirmId = internal ? selectedFirmId : (demo -> 'global' :
 * claims.firmId), and every per-firm fetch interpolates that id straight into /api/general/mdpf/{id}/... .
 *
 * THE MATCH IS ON THE PATH THE ORIGIN WILL RESOLVE (as aggregate_gate.mjs): the query is dropped and the path is
 * percent-decoded ONCE, the way S3 decodes a request path into a key. After that one decode, every segment under the
 * prefix must be plain ([A-Za-z0-9._-]), no segment may be "." or "..", and none may be empty except a trailing one:
 * a residual "%" (a double encoding), a backslash, a NUL, a space, a semicolon, "//" and "/../" are all refused for a
 * non-internal claim. The folder must equal an admitted folder EXACTLY (case-sensitive: S3 keys are).
 *
 * TWO PREFIXES ARE GATED: /api/general/mdpf (the served route) and /api/general/json/mdpf (the frozen legacy serve,
 * empty today; the same leak class if it were ever filled). A prefix match is case-insensitive, so a case variant of
 * the prefix is REFUSED for a non-internal claim rather than let through unrecognised.
 *
 * NO IMPORTS, NO TOP-LEVEL SIDE EFFECT: this module loads in the viewer-request function of 25 behaviours; a throw at
 * load, or before the URI test, would refuse every authenticated API path of the portal.
 */

export const MDPF_PASS = "pass";
export const MDPF_DENY = "deny";

const MDPF_PREFIXES = Object.freeze(["/api/general/mdpf", "/api/general/json/mdpf"]);

export const MDPF_FIRM_FOLDERS = Object.freeze({
  "49financial": Object.freeze(["49financial"]),
  inflection: Object.freeze(["inflection"]),
  cottonwood: Object.freeze(["cottonwood"]),
  demo: Object.freeze(["global"]),
});
export const MDPF_NO_FIRM_FOLDERS = Object.freeze(["global"]);

const PLAIN_SEGMENT = /^[A-Za-z0-9._-]+$/;

function decodedPath(uri) {
  const cut = uri.search(/[?#]/);
  const path = cut === -1 ? uri : uri.slice(0, cut);
  try {
    return decodeURIComponent(path);
  } catch {
    return path;
  }
}

// RFC 3986 dot-segment removal on a decoded path ("/a/./b/../c" -> "/a/c"); the form a normalising proxy would hand on.
function withoutDotSegments(p) {
  const out = [];
  for (const s of p.split("/")) {
    if (s === ".") continue;
    if (s === "..") { if (out.length > 1) out.pop(); continue; }
    out.push(s);
  }
  return out.join("/");
}

// null: not an MDPF path. Otherwise { folder, clean }: clean is false for any shape a non-internal claim must not use.
// A path is MDPF if it, or its dot-segment-removed or slash-collapsed form, sits under a gated prefix: a request that
// only becomes an MDPF path after normalisation is still gated, and is refused unless it was already canonical.
export function mdpfRoute(uri) {
  if (typeof uri !== "string") return null;
  const p = decodedPath(uri);
  const forms = [p, withoutDotSegments(p), p.replace(/\/{2,}/g, "/"), withoutDotSegments(p).replace(/\/{2,}/g, "/")];
  for (const prefix of MDPF_PREFIXES) {
    if (!forms.some((f) => { const l = f.toLowerCase(); return l === prefix || l.startsWith(prefix + "/"); })) continue;
    const exact = p.startsWith(prefix) && uri.startsWith(prefix);
    const lower = p.toLowerCase();
    if (!(lower === prefix || lower.startsWith(prefix + "/"))) return { folder: null, clean: false };
    const tail = p.slice(prefix.length);
    const segs = tail === "" ? [] : tail.slice(1).split("/");
    if (segs.length === 0) return { folder: null, clean: false };
    const last = segs.length - 1;
    const plain = segs.every((s, i) =>
      (s === "" && i === last && i > 0) || (PLAIN_SEGMENT.test(s) && s !== "." && s !== ".."));
    return { folder: plain && exact ? segs[0] : null, clean: plain && exact };
  }
  return null;
}

export function admitsAllMdpf(payload) {
  if (!payload || typeof payload !== "object") return false;
  return payload.firmId === "opal-capital" || payload.userType === "Dev";
}

export function mdpfFoldersFor(payload) {
  const firm = payload && typeof payload === "object" ? payload.firmId : undefined;
  if (firm === undefined || firm === null || firm === "") return MDPF_NO_FIRM_FOLDERS;
  if (typeof firm !== "string") return [];
  return Object.prototype.hasOwnProperty.call(MDPF_FIRM_FOLDERS, firm) ? MDPF_FIRM_FOLDERS[firm] : [];
}

export function mdpfGate(uri, payload) {
  const route = mdpfRoute(uri);
  if (route === null) return MDPF_PASS;
  if (!payload || typeof payload !== "object") return MDPF_DENY;
  if (admitsAllMdpf(payload)) return MDPF_PASS;
  if (!route.clean || route.folder === null) return MDPF_DENY;
  return mdpfFoldersFor(payload).includes(route.folder) ? MDPF_PASS : MDPF_DENY;
}
