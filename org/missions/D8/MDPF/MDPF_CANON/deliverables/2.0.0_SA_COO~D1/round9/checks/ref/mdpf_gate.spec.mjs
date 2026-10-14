import { describe, test, expect } from "bun:test";
import { MDPF_PASS, MDPF_DENY, mdpfGate } from "../mdpf_gate.mjs";
import { FIRM_BUCKET_MAP, MDPF_GLOBAL_VIEW_FIRMS } from "../../_shared/firm-config.mjs";

const P = "/api/general/mdpf/";
const claim = (firmId, extra = {}) => ({ sub: "u@test", firmId, ...extra });
// the module keeps no firm slug: the partner folders are the keys of the generated FIRM_BUCKET_MAP, the demo tenant is in MDPF_GLOBAL_VIEW_FIRMS
const gate = (uri, payload) => mdpfGate(uri, payload, FIRM_BUCKET_MAP, MDPF_GLOBAL_VIEW_FIRMS);

describe("mdpf_gate: a partner reads its own folder only", () => {
  test("(i) each partner passes on its own leaf, every file", () => {
    for (const [firm, folder] of [["49financial", "49financial"], ["inflection", "inflection"], ["cottonwood", "cottonwood"]]) {
      for (const f of ["aggregate-aua-timeseries.json", "aum-metrics.json", "category-views.json", "category-views-history.json", "account-distribution.json"]) {
        expect(gate(`${P}${folder}/${f}`, claim(firm))).toBe(MDPF_PASS);
      }
    }
  });

  test("(ii) each partner is refused every other folder, global included", () => {
    const firms = ["49financial", "inflection", "cottonwood"];
    for (const a of firms) {
      for (const b of [...firms, "global"]) {
        if (a === b) continue;
        expect(gate(`${P}${b}/aum-metrics.json`, claim(a))).toBe(MDPF_DENY);
      }
    }
  });

  test("(iii) a sibling folder that only starts with the own folder is refused", () => {
    expect(gate(`${P}49financial-old/aum-metrics.json`, claim("49financial"))).toBe(MDPF_DENY);
    expect(gate(`${P}inflectionx/aum-metrics.json`, claim("inflection"))).toBe(MDPF_DENY);
    expect(gate(`${P}globalx/aum-metrics.json`, claim("demo"))).toBe(MDPF_DENY);
  });

  test("(iv) a partner-firm admin is held to its own folder (role and tier do not widen it)", () => {
    const admin = claim("inflection", { role: "admin", firmRole: "admin", tier: "internal" });
    expect(gate(`${P}49financial/aum-metrics.json`, admin)).toBe(MDPF_DENY);
    expect(gate(`${P}inflection/aum-metrics.json`, admin)).toBe(MDPF_PASS);
  });
});

describe("mdpf_gate: internal, demo and no-firm claims", () => {
  test("(v) opal-capital passes every folder, the non-firm folders and the bare prefix", () => {
    for (const t of ["49financial", "inflection", "cottonwood", "global", "_manifests", "archive", "anything"]) {
      expect(gate(`${P}${t}/x.json`, claim("opal-capital"))).toBe(MDPF_PASS);
    }
    expect(gate("/api/general/mdpf", claim("opal-capital"))).toBe(MDPF_PASS);
  });

  test("(vi) a Dev claim passes every folder whatever its firm", () => {
    expect(gate(`${P}inflection/x.json`, claim("49financial", { userType: "Dev" }))).toBe(MDPF_PASS);
    expect(gate(`${P}global/x.json`, claim("demo", { userType: "Dev" }))).toBe(MDPF_PASS);
  });

  test("(vii) the demo tenant reads global and nothing else", () => {
    expect(gate(`${P}global/aum-metrics.json`, claim("demo"))).toBe(MDPF_PASS);
    for (const t of ["49financial", "inflection", "cottonwood", "_manifests", "archive"]) {
      expect(gate(`${P}${t}/aum-metrics.json`, claim("demo"))).toBe(MDPF_DENY);
    }
  });

  test("(viii) a claim with no firm (absent, empty, null) reads global and nothing else", () => {
    for (const payload of [{ sub: "u" }, claim(""), claim(null), claim(undefined)]) {
      expect(gate(`${P}global/aum-metrics.json`, payload)).toBe(MDPF_PASS);
      for (const t of ["49financial", "inflection", "cottonwood", "_manifests"]) {
        expect(gate(`${P}${t}/aum-metrics.json`, payload)).toBe(MDPF_DENY);
      }
    }
  });

  test("(ix) an unknown, prototype-key, non-string or case-variant firm reads nothing, global included", () => {
    for (const firm of ["bd", "__proto__", "constructor", "toString", "hasOwnProperty", 49, {}, [], " inflection", "Inflection", "INFLECTION"]) {
      expect(gate(`${P}global/aum-metrics.json`, claim(firm))).toBe(MDPF_DENY);
      expect(gate(`${P}inflection/aum-metrics.json`, claim(firm))).toBe(MDPF_DENY);
      // a firm id that is only a prototype key or a variant must not read the folder of its own name either
      if (typeof firm === "string" && firm.trim() !== "") expect(gate(`${P}${encodeURIComponent(firm)}/aum-metrics.json`, claim(firm))).toBe(MDPF_DENY);
    }
  });
});

describe("mdpf_gate: only the MDPF prefixes are gated", () => {
  test("(x) a non-MDPF path passes whatever the claim, and a near-miss prefix is not MDPF", () => {
    for (const u of ["/api/general/etfs/x.json", "/api/general/positioning/x.json", "/api/general/json/market-overview/x.json", "/api/general/mdpfx/inflection/x.json", "/api/general/mdpf-other/x.json", "/api/scoped/partners/x"]) {
      expect(gate(u, claim("49financial"))).toBe(MDPF_PASS);
      expect(gate(u, claim("mockadv"))).toBe(MDPF_PASS);
    }
  });

  test("(xi) the frozen legacy prefix /api/general/json/mdpf is gated the same way", () => {
    expect(gate("/api/general/json/mdpf/inflection/x.json", claim("49financial"))).toBe(MDPF_DENY);
    expect(gate("/api/general/json/mdpf/49financial/x.json", claim("49financial"))).toBe(MDPF_PASS);
    expect(gate("/api/general/json/mdpf/inflection/x.json", claim("opal-capital"))).toBe(MDPF_PASS);
  });

  test("(xii) the bare prefix, with and without a slash, is refused to a non-internal claim", () => {
    for (const u of ["/api/general/mdpf", "/api/general/mdpf/", "/api/general/mdpf//", "/api/general/json/mdpf"]) {
      expect(gate(u, claim("demo"))).toBe(MDPF_DENY);
      expect(gate(u, claim("49financial"))).toBe(MDPF_DENY);
    }
  });
});

describe("mdpf_gate: the path the origin will resolve", () => {
  const own = claim("49financial");
  test("(xiii) traversal, dot and empty segments are refused, plain and percent-encoded", () => {
    for (const u of [
      `${P}49financial/../inflection/x.json`, `${P}./inflection/x.json`, `${P}49financial/./../inflection/x.json`,
      `${P}49financial/%2e%2e/inflection/x.json`, `${P}49financial/%2E%2E/inflection/x.json`, `${P}49financial%2f..%2finflection%2fx.json`,
      `${P}49financial//x.json`, `${P}49financial/sub//x.json`, `${P}/inflection/x.json`,
    ]) {
      expect(gate(u, own)).toBe(MDPF_DENY);
    }
  });

  test("(xiv) an encoded or double-encoded folder name is judged after ONE decode", () => {
    expect(gate(`${P}%69nflection/x.json`, own)).toBe(MDPF_DENY);
    expect(gate(`${P}%2569nflection/x.json`, own)).toBe(MDPF_DENY);
    expect(gate(`${P}%49financial/x.json`, own)).toBe(MDPF_DENY);
    expect(gate(`${P}49financial/%252e%252e/x.json`, own)).toBe(MDPF_DENY);
    expect(gate(`${P}%34%39financial/x.json`, own)).toBe(MDPF_PASS);
  });

  test("(xv) case variants of the folder are refused, and so is a case variant of the prefix", () => {
    expect(gate(`${P}49Financial/x.json`, own)).toBe(MDPF_DENY);
    expect(gate(`${P}Inflection/x.json`, claim("inflection"))).toBe(MDPF_DENY);
    expect(gate("/API/general/mdpf/49financial/x.json", own)).toBe(MDPF_DENY);
    expect(gate("/api/general/MDPF/49financial/x.json", own)).toBe(MDPF_DENY);
    expect(gate("/api/general/%6Ddpf/inflection/x.json", own)).toBe(MDPF_DENY);
  });

  test("(xvi) backslash, NUL, space, tab, semicolon, trailing dot and a unicode slash are refused", () => {
    for (const u of [
      `${P}49financial\\x.json`, `${P}49financial%5cx.json`, `${P}49financial%00/x.json`, `${P}49financial/x.json%00.png`,
      `${P}49financial%20/x.json`, `${P}%2049financial/x.json`, `${P}49financial%09/x.json`, `${P}49financial;/x.json`,
      `${P}49financial./x.json`, `${P}49financial%EF%BC%8Fx.json`, `${P}%E0%A4%A/x.json`, `${P}%/x.json`,
    ]) {
      expect(gate(u, own)).toBe(MDPF_DENY);
    }
  });

  test("(xvii) the query string is not part of the path, and a trailing slash on the own folder is allowed", () => {
    expect(gate(`${P}49financial/aum-metrics.json?folder=inflection`, own)).toBe(MDPF_PASS);
    expect(gate(`${P}inflection/aum-metrics.json?x=/49financial/`, own)).toBe(MDPF_DENY);
    expect(gate(`${P}49financial/`, own)).toBe(MDPF_PASS);
    expect(gate(`${P}inflection/`, own)).toBe(MDPF_DENY);
  });
});

describe("mdpf_gate: robustness", () => {
  test("(xviii) it never throws, and a MDPF uri with a malformed payload is refused", () => {
    for (const [u, p] of [[undefined, {}], [null, null], [123, {}], ["", {}], ["%", {}], [`${P}global/x.json`, undefined], [`${P}global/x.json`, null], [`${P}global/x.json`, "s"], [`${P}global/x.json`, []], [`${P}global/x.json`, 7]]) {
      let r;
      expect(() => { r = mdpfGate(u, p); }).not.toThrow();
      expect([MDPF_PASS, MDPF_DENY]).toContain(r);
    }
    expect(gate(`${P}global/x.json`, null)).toBe(MDPF_DENY);
    expect(gate(`${P}global/x.json`, "s")).toBe(MDPF_DENY);
    expect(gate("/api/general/etfs/x.json", null)).toBe(MDPF_PASS);
    expect(MDPF_PASS).not.toBe(MDPF_DENY);
  });
});

describe("mdpf_gate: the firm map and the global-view list are parameters", () => {
  const U = P;
  test("(xix) mockadv is a key of the generated map, so it reads its own name and not global or a partner folder", () => {
    expect(gate(`${U}mockadv/aum-metrics.json`, claim("mockadv"))).toBe(MDPF_PASS);
    expect(gate(`${U}global/aum-metrics.json`, claim("mockadv"))).toBe(MDPF_DENY);
    expect(gate(`${U}49financial/aum-metrics.json`, claim("mockadv"))).toBe(MDPF_DENY);
  });

  test("(xx) a missing, non-object or array firm map denies every non-internal MDPF request (fail closed) and never throws", () => {
    for (const m of [undefined, null, "str", 7, [], true]) {
      for (const [firm, folder] of [["49financial", "49financial"], ["demo", "global"], [undefined, "global"], ["mockadv", "mockadv"]]) {
        let r;
        expect(() => { r = mdpfGate(`${U}${folder}/x.json`, claim(firm), m, MDPF_GLOBAL_VIEW_FIRMS); }).not.toThrow();
        expect(r).toBe(MDPF_DENY);
      }
      expect(mdpfGate(`${U}inflection/x.json`, claim("opal-capital"), m, MDPF_GLOBAL_VIEW_FIRMS)).toBe(MDPF_PASS);
      expect(mdpfGate("/api/general/etfs/x.json", claim("49financial"), m, MDPF_GLOBAL_VIEW_FIRMS)).toBe(MDPF_PASS);
    }
  });

  test("(xxi) a missing or unusable global-view list means no firm views global; a Set behaves as the array", () => {
    for (const g of [undefined, null, "demo", 7, {}]) {
      expect(mdpfGate(`${U}global/x.json`, claim("demo"), FIRM_BUCKET_MAP, g)).toBe(MDPF_DENY);
    }
    expect(mdpfGate(`${U}global/x.json`, claim("demo"), FIRM_BUCKET_MAP, new Set(MDPF_GLOBAL_VIEW_FIRMS))).toBe(MDPF_PASS);
    expect(mdpfGate(`${U}global/x.json`, claim("demo"), FIRM_BUCKET_MAP, [...MDPF_GLOBAL_VIEW_FIRMS])).toBe(MDPF_PASS);
  });

  test("(xxii) the partner folders come from the map it is given: a synthetic map admits its own keys and no others, a null-prototype map answers no prototype key", () => {
    const syn = Object.freeze({ acme: 1 });
    expect(mdpfGate(`${U}acme/x.json`, claim("acme"), syn, [])).toBe(MDPF_PASS);
    expect(mdpfGate(`${U}49financial/x.json`, claim("49financial"), syn, [])).toBe(MDPF_DENY);
    const np = Object.create(null);
    np.acme = 1;
    expect(mdpfGate(`${U}acme/x.json`, claim("acme"), np, [])).toBe(MDPF_PASS);
    expect(mdpfGate(`${U}constructor/x.json`, claim("constructor"), np, [])).toBe(MDPF_DENY);
    expect(mdpfGate(`${U}__proto__/x.json`, claim("__proto__"), np, [])).toBe(MDPF_DENY);
  });
});
