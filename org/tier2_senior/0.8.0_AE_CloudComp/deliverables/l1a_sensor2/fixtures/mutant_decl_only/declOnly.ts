// Declaration-vs-invocation MUTANT fixture (CTO~Z-ordered, 20260725T0922Z).
// A function DECLARATION whose name matches the Query-family token, with NO
// invocation of that hook anywhere. The sensor must:
//   - NOT count `useZzzMutantQuery` as a call site (declaration exclusion),
//   - still count the genuine inner useQuery( call (covered by the tool),
//   - list the declaration as a labeled DEFINITION.
// Expected sensor result on this dir: CLEAN rc=0, surface=1 (covered), 1 DEFINITION.
import { useQuery } from '@tanstack/react-query'

export function useZzzMutantQuery(id: string) {
  return useQuery({ queryKey: ['zzz-mutant', id], queryFn: () => fetch('/x') })
}
