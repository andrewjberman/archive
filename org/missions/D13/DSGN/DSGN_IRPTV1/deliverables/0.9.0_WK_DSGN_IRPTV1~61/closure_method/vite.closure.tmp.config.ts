// The one-off, UNCOMMITTED config used to read the build's module graph (DSGN_IRPTV1 IV-e-111). Copy to portal/ root, run, delete.
//   cd portal && CLOSURE_OUT=<abs path>/build_graph.json bun run vite build --configLoader runner --config vite.closure.tmp.config.ts --outDir <abs path>/dist_x
//   python closure.py <build_graph.json> <abs portal root> <print_closure.json> <changed_files.json>   (changed_files.json = git diff --name-only 37aa1247ee HEAD as a JSON list)
//   python controls.py <build_graph.json> <abs portal root> <print_closure.json>
import { mergeConfig, defineConfig, type Plugin } from 'vite'
import { writeFileSync } from 'node:fs'
import base from './vite.config'

const OUT = process.env.CLOSURE_OUT as string

function graphPlugin(): Plugin {
  return {
    name: 'closure-graph',
    apply: 'build',
    generateBundle(_o, bundle) {
      const modules: Record<string, { s: string[]; d: string[] }> = {}
      for (const id of this.getModuleIds()) {
        const info = this.getModuleInfo(id)
        if (!info) continue
        modules[id] = { s: [...info.importedIds], d: [...info.dynamicallyImportedIds] }
      }
      const chunks: Record<string, { facade: string | null; modules: string[]; imports: string[]; dynamicImports: string[] }> = {}
      for (const [name, item] of Object.entries(bundle)) {
        if (item.type !== 'chunk') continue
        chunks[name] = {
          facade: item.facadeModuleId, modules: Object.keys(item.modules),
          imports: item.imports, dynamicImports: item.dynamicImports,
        }
      }
      writeFileSync(OUT, JSON.stringify({ modules, chunks }))
    },
  }
}

export default defineConfig(mergeConfig(base as never, { plugins: [graphPlugin()] }) as never)
