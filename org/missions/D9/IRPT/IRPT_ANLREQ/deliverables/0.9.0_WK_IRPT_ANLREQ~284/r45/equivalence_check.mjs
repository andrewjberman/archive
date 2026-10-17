// AR-y-384 equivalence check: the old literal (as origin/DEV 4d4dc68c holds it) and the new literal
// (as the candidate holds it) must give the SAME result on the same strings.
// Run with: bun run equivalence_check.mjs   (from this folder)
// The literal TEXT is asserted to occur in the real files (base via git show, new via disk), so the
// check tests the bytes that are in the repository, not a retyped copy.
import { readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";

const PORTAL = "C:/dev/wk-irpt-anlreq-284/portal";
const BASE = "4d4dc68cae";
const HINT = "src/pages/TicketCenter/__tests__/filing-hint.test.tsx";
const TREE = "src/pages/TicketCenter/__tests__/filing-decision-tree.test.tsx";

const baseText = (p) => execFileSync("git", ["-C", PORTAL, "show", `${BASE}:${p}`], { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 });
const newText = (p) => readFileSync(`${PORTAL}/${p}`, "utf8");

let failed = false;
function report(label, oldRe, newRe, strings) {
  for (const s of strings) {
    const a = s.match(oldRe);
    const b = s.match(newRe);
    const same = (a === null && b === null) || (a !== null && b !== null && a.index === b.index && a[0] === b[0] && a[1] === b[1]);
    if (!same) {
      console.log(`DIFFERENT ${label} ${JSON.stringify(s)}`);
      failed = true;
      return;
    }
  }
  const matched = strings.filter((s) => s.match(newRe) !== null).length;
  console.log(`EQUIVALENT ${strings.length} strings (${label}; ${matched} match, ${strings.length - matched} do not match)`);
}

// ---- literal 1: filing-decision-tree.test.tsx line 299 (no-control-regex) ----
// Old body holds RAW U+0008 bytes (the file as origin/DEV has it); new body holds the escape [\b] (a backspace in a class).
const OLD_TREE = "Did you mean|was not found|Replacement ticker|Type the ticker|\u0008Yes\u0008|\u0008Replace\u0008|\u0008No\u0008";
const NEW_TREE = "Did you mean|was not found|Replacement ticker|Type the ticker|[\\b]Yes[\\b]|[\\b]Replace[\\b]|[\\b]No[\\b]";
const baseTree = baseText(TREE);
const treeNow = newText(TREE);
if (!baseTree.includes("/" + OLD_TREE + "/.test(text)")) throw new Error("old decision-tree literal not found at base");
if (!treeNow.includes("/" + NEW_TREE + "/.test(text)")) throw new Error("new decision-tree literal not found in candidate");
const treeStrings = [
  "x\u0008Yes\u0008y",       // match via the Yes arm
  "\u0008Replace\u0008",     // match via the Replace arm
  "\u0008No\u0008",          // match via the No arm
  "Did you mean ACME1?",     // match via the first arm
  "Yes",                     // no backspace: no match
  "No",                      // no match
  "Replace",                 // no match
  "a\u0008Yes",              // one backspace only: no match
  "\u0008Nope\u0008",        // no match
  "plain text",              // no match
];
report("decision-tree", new RegExp(OLD_TREE), new RegExp(NEW_TREE), treeStrings);

// ---- literal 2: filing-hint.test.tsx line 190 (no-regex-spaces) ----
const OLD_HINT = "const chooseHint = \\(choice: FilingChoice\\) => \\{([\\s\\S]*?)\\n  \\}";
const NEW_HINT = "const chooseHint = \\(choice: FilingChoice\\) => \\{([\\s\\S]*?)\\n {2}\\}";
const baseHint = baseText(HINT);
const hintNow = newText(HINT);
if (!baseHint.includes("SOURCES[2].match(/" + OLD_HINT + "/)")) throw new Error("old filing-hint literal not found at base");
if (!hintNow.includes("SOURCES[2].match(/" + NEW_HINT + "/)")) throw new Error("new filing-hint literal not found in candidate");
const H = "const chooseHint = (choice: FilingChoice) => {";
const hintStrings = [
  H + "\n  }",              // two spaces: match
  H + "\n  x\n  }",         // match on the second newline
  H + "\n  \n  }",          // match with a blank line between
  H + "\n   }",             // three spaces: no match
  H + "\n    }",            // four spaces: no match
  H + "\n}",                // no spaces: no match
  H + "\n\t}",              // tab: no match
  "other text",             // no match
];
report("filing-hint", new RegExp(OLD_HINT), new RegExp(NEW_HINT), hintStrings);

process.exit(failed ? 1 : 0);
