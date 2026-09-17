# LIMB_ROOTS_CENSUS.r3 -- round 2's roots census, each row now carrying its init flags

**Cell:** `EN-t-8`, LGIC_ENFORCE round 3 (`LGIC_ENFORCE.TO-EN-t-8-r3.roots-evaluated.md`).
**Worker:** `0.9.0_WK_LGIC_ENFORCE~3`.

**What this is.** Round 2's `LIMB_ROOTS_CENSUS.md` (`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/LIMB_ROOTS_CENSUS.md`,
vintage `2026-09-16T10:15:18Z`) carried 72 root rows -- 68 planned with a committed extract, 4 NOT planned each with a recorded
`terraform plan rc=1` cause -- but no row named the `terraform init` flags it ran with. Round 2's own record
(section 1, "What ran, and how the disk was held") states the flags were UNIFORM across all 72 roots: one root
at a time, `terraform init -input=false` (from the populated `TF_PLUGIN_CACHE_DIR`), then a read-only
`plan -lock=false -input=false -out=<abs scratch path>`, then `show -json`, then that root's `.terraform` removed
before the next root was initialised. This file carries every round-2 row forward UNCHANGED (`extract`,
`plan_sha256`, `reason`) and adds one field, `init_flags`, printing that uniform value per row (A-12).

**Not a re-run of all 72.** A fresh spot re-plan of ONE planned root (`infra/aws/terraform/49f-value-parity`,
`-lockfile=readonly` on init, run in a throwaway copy of that root plus its `../../compdiff` source dependency)
reproduces the committed extract exactly -- see
`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/ROOTS_REPRODUCTION.r3.json` and the full
reduced document beside it in `roots_r3/`. Re-planning all 72 roots again was not attempted: the order's disk bound
(one root's `.terraform` costs ~686 MB against ~7-8 GB free on this box) makes a full 72-root re-run the exact
hazard `LGIC_ENFORCE-S22` names, and the round-2 record already states its init flags in prose -- carrying that
forward per row is a citation of a measured fact, not a re-derivation.

**The 4 NOT-planned roots keep their round-2 cause unchanged** (below), each still carrying `init_flags` for the
init attempt that preceded the failing plan.

```json
{
 "vintage": "2026-09-16T10:15:18Z",
 "roots": [
  {
   "root": "infra/aws/terraform/49f-value-parity",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__49f-value-parity.r2.json",
   "plan_sha256": "d83139429c4e85aa9e6f0777bc25b5f9d26dd535a780f3c7579e57450ca5d8de",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/aaii-v2-bucket-lifecycle",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__aaii-v2-bucket-lifecycle.r2.json",
   "plan_sha256": "b211d819a731cba0181e2f3827e65319dddbdfac06e456f037eddacb72ef0eae",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/astn-pipeline",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__astn-pipeline.r2.json",
   "plan_sha256": "5f986ec1ccf943543c81cd2121474e46cba1748a77c0d022657c42a632d28a82",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/bd-49f-auto-login",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__bd-49f-auto-login.r2.json",
   "plan_sha256": "3fc0975f95a8c73436428f3872a6cf9a551b176bae00e9f9e6e0a0c7511991a8",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/bd-bucket-lifecycle",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__bd-bucket-lifecycle.r2.json",
   "plan_sha256": "b6dd79794f0d5eb1dbac171206ae2fadcb467d3b960dd884c63070d2ed47ce9c",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/bd-pipeline",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__bd-pipeline.r2.json",
   "plan_sha256": "fe9da15434d949db6c45fbf4ee99bc89cedcdbdcdfed56b853fe674224261a39",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/bloomberg-tunnel",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__bloomberg-tunnel.r2.json",
   "plan_sha256": "05d5a8d5a182a3b039abb54a77ca2ece2eda9a06a46cda58a1bc652b78bff3cd",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/c3materialize-b4",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__c3materialize-b4.r2.json",
   "plan_sha256": "66f70324e5bbb0637693c7b0e9a6bbc9742060a9aa88a45f753a237cb6da888d",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/canonical-schwab-ec2",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__canonical-schwab-ec2.r2.json",
   "plan_sha256": "18e35788235ec02903ef586cde052668140c17182ef4235ae9b81c3d995829dd",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/canonical-schwab-si2-schedule",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__canonical-schwab-si2-schedule.r2.json",
   "plan_sha256": "bb4913d93ac88608c10d672f8c46074f3a98e8685c3b3a62f1fe052db75b2d5e",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/consolidation-gold-runner",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__consolidation-gold-runner.r2.json",
   "plan_sha256": "f12ac282f00446f7fb125196fc0655685f86721ccbb79dc01df64754178ca610",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/cot-pipeline",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__cot-pipeline.r2.json",
   "plan_sha256": "a456d5f71d3a01ea17203593fea65708d7675f7480b68b7563b6f0272dbfff95",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/cot-value-parity",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__cot-value-parity.r2.json",
   "plan_sha256": "e3ed2a5279de53fce030b85e22bcdeaca8eb608254a45395eef99dbb27e016ce",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/daily-sprint-generator",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__daily-sprint-generator.r2.json",
   "plan_sha256": "73de3d776275b033b587ff59ff93bdc5b7cca1dc36c6381565be162a1f6d5b75",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/data-refresh",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__data-refresh.r2.json",
   "plan_sha256": "3046a24d79d3ecb1bf8c50bca4b1ba9f2ebf0750ded67a46e3cbf8b0841cb190",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/deck-generation-pipeline",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__deck-generation-pipeline.r2.json",
   "plan_sha256": "e8fb3cc409296a27302dc85baad57d57bcc98566c6a34ee379e5d317ab2c98ac",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/estate-report",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__estate-report.r2.json",
   "plan_sha256": "dec7022229e050fa7d13cd5d25a49f2f35814015e36408d5a3bac21ae40154b6",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/etfs-canon",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__etfs-canon.r2.json",
   "plan_sha256": "def1728ed0b4a8cb526477266349b4d58882f3a82239a9c99a0154fbf22df796",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/etfs-netassets",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__etfs-netassets.r2.json",
   "plan_sha256": "8d6dbccdc4ac4630d0b482033aa02df90a66ddfb7fae47e72d003baa981199b3",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/etfs-positioning",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__etfs-positioning.r2.json",
   "plan_sha256": "98fc602f0bf5a0a856f75df5788062c579bd16c80800308f297f37cd79e567c2",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/etfs-reports",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__etfs-reports.r2.json",
   "plan_sha256": "c259cff2c10372cbeb0aab317dc11a334e7dfa2a35a936424b52debfb3c3c763",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/exec-summary",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__exec-summary.r2.json",
   "plan_sha256": "30b7e1790ba7df79ca31297922e1aac16dc0123a41243ea9f3fadadebc8b8a0a",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/fred-pipeline",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__fred-pipeline.r2.json",
   "plan_sha256": "c5d1e478e42b47136efdb2d39fce943e69cf07ec7700a04ff9de828dca4dac84",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/github-actions-runner",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__github-actions-runner.r2.json",
   "plan_sha256": "02de4fab2bceb2b253b64101153a557e20dec0828d46e42f41dc2e0774f73c54",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/globgrph",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__globgrph.r2.json",
   "plan_sha256": "4634b074a690b368dd24d1ce9d365c9706edbeb42581b84b00649857dfe27d83",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/harvest",
   "planned": false,
   "extract": null,
   "plan_sha256": null,
   "reason": "terraform plan rc=1: e \"aws_lambda_function\" \"chatter_axis_producer\": 124: source_code_hash = filebase64sha256(local.chatter_axis_zip) while calling filebase64sha256(path) local.chatter_axis_zip is \"./.build/chatter-axis-producer.zip\" Call to function \"filebase64sha256\" failed: open .build\\chatter-axis-producer.zip: The system cannot find the path specified..",
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/imo-pipeline",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__imo-pipeline.r2.json",
   "plan_sha256": "1483d4ee977fd86417feee2243320aae2c5fe80eb5c3ef4b75562665c54e224d",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/inf-pipeline",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__inf-pipeline.r2.json",
   "plan_sha256": "074116686f330a2691fe3af01c02f604856d43cb7883c36f166271a1cf263082",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/inf-value-parity",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__inf-value-parity.r2.json",
   "plan_sha256": "8ef8b2b31cc02e7803860d0470fb7b9ff0c14a81a748c3ca46a92a7155a7d4a7",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/investor-reporting/api",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__investor-reporting__api.r2.json",
   "plan_sha256": "c39947f335c8d534e5d542eeb5d86f0cdb6abc57becc8f0053afe244d56c07c6",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/investor-reporting/core",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__investor-reporting__core.r2.json",
   "plan_sha256": "80f682be40c0520b92b4dc32b0e6c37ffacc3a76c097bbba7153eca0fbca30d3",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/investor-reporting/directory",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__investor-reporting__directory.r2.json",
   "plan_sha256": "fa3c4aa40de20c44d88f7b75d241f0d4a7d43b5386166f9dc5b097adab9cea74",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/investor-reporting/export",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__investor-reporting__export.r2.json",
   "plan_sha256": "33588e463c4e61285131146e1d9c1ade1a63bab80d54819927f2fe9d6a855df6",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/investor-reporting/holdings",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__investor-reporting__holdings.r2.json",
   "plan_sha256": "21534508c41bfdc0020e7807bc9e687146590a91292a2643bdc3e13fe3764b0a",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/investor-reporting/intake",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__investor-reporting__intake.r2.json",
   "plan_sha256": "9c3d8239e57e54a55058499b7c1099eec524a989d683842867e4c273c2c18587",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/investor-reporting/narrative",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__investor-reporting__narrative.r2.json",
   "plan_sha256": "63b5517509cdffc27c1a6d60025c24b96dd1cb543d7d60c57e2ec209ecf83ba1",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/investor-reporting/ops",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__investor-reporting__ops.r2.json",
   "plan_sha256": "13ae86cebf182a24404228462c23172651733d15f26a268bdb5695c58f3ffa0d",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/investor-reporting/performance",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__investor-reporting__performance.r2.json",
   "plan_sha256": "220823c046e6a8f3b88f460fd144205e0cd810de68018cb4bfeb4377bf0cf55a",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/investor-reporting/ycharts",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__investor-reporting__ycharts.r2.json",
   "plan_sha256": "2c0f5ac15780f976ef0116ed9422110695a816d9b7de2485237cf12f2def5f02",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/market-overview",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__market-overview.r2.json",
   "plan_sha256": "5692e0d7ad326fcd52dd720f1b08b3054142e6e7a5b0d950b068dbe55d3a33f4",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/mdpf-pipeline",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__mdpf-pipeline.r2.json",
   "plan_sha256": "cc5b37e90213d60f3860a9833bb6cc72d811351013544a3e0e51da607e6e0a82",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/news-pipeline",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__news-pipeline.r2.json",
   "plan_sha256": "606889127a2bf378dd0a74a34ce6cf2678ea895ff17f47b28ee3f6d79fea4973",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/news-v2-bucket-lifecycle",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__news-v2-bucket-lifecycle.r2.json",
   "plan_sha256": "0e93009fcedb001f9ce6f29f03a349aa23a6549d0906f5ee7397e309ced0dac2",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/nfra-agentbus",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__nfra-agentbus.r2.json",
   "plan_sha256": "524fdfea17791f1cb25fc1b837b4be8bb0340f838a5c3f485e8765585fe2a62b",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/nfra-agentbus-alyssa01",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__nfra-agentbus-alyssa01.r2.json",
   "plan_sha256": "c12608e741158803c7b579f3072833c9c88ee8efaf02b1616d11af9d36a24a40",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/nfra-agentbus-port2",
   "planned": false,
   "extract": null,
   "plan_sha256": null,
   "reason": "terraform plan rc=1: 262144), got 1048576 with aws_sqs_queue.sitez_to_laptop, on sqs.tf line 31, in resource \"aws_sqs_queue\" \"sitez_to_laptop\": 31: max_message_size = local.max_message_bytes Error: expected max_message_size to be in the range (1024 - 262144), got 1048576 with aws_sqs_queue.laptop_to_sitez, on sqs.tf line 46, in resource \"aws_sqs_queue\" \"laptop_to_sitez\": 46: max_message_size = local.max_message_bytes",
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/opal-assets",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__opal-assets.r2.json",
   "plan_sha256": "527cff668fca2d4bf21e2d24b5500bc709cab1bdf575d4a6bfaf78a69e349f5d",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/opal-assets-absence",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__opal-assets-absence.r2.json",
   "plan_sha256": "651369148a99988a85a44965c4ff5bfc54d36e8c17181b0f27ebab531d8d8e51",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/opal-gateway",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__opal-gateway.r2.json",
   "plan_sha256": "a19480d1a6738fe09ab6efe11a063752068e055b2d063e352760cbb133eb2bb4",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/opsec",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__opsec.r2.json",
   "plan_sha256": "93779b22b82a3020dc99457345a13fe59b6787b987c56d70582ab8c36db4dd46",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/partner-etl-ops-alerts",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__partner-etl-ops-alerts.r2.json",
   "plan_sha256": "a2f47ec40b0c665bc53edf264277bccfe43b115def9287400ca53db722ad511b",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/partner-firms",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__partner-firms.r2.json",
   "plan_sha256": "02d67d3b3df3cc0f7a743c116019b66d96d2f7ea0d47e481a42fa54ffb8eb0e8",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/partners-api",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__partners-api.r2.json",
   "plan_sha256": "bd25ad77723a926f9eedcd5109f0d754ac1f1805d4a32f8874cdad97b13f4ec1",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/portal-auth",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__portal-auth.r2.json",
   "plan_sha256": "4fce3fd9b1b5d5ff30c4fa53e0b051a2d346a22b3cf4c58f4e6d43edaa9a90a5",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/portal-content",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__portal-content.r2.json",
   "plan_sha256": "509edb6d378a8f3006eb02dd71cb1783df959a46f304911c6da5ecd2c4e03ed1",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/portal-notifications",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__portal-notifications.r2.json",
   "plan_sha256": "6cc862e3c04b48d575db7888402077ea470c2c93795f773c4fc72930733b1fce",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/portfolio-management",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__portfolio-management.r2.json",
   "plan_sha256": "cf227d5e42cd06c525c4cadefb935a827bd2bd7d204dd4aaed931363f745c42e",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/security-ops",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__security-ops.r2.json",
   "plan_sha256": "3825e43256d22c06dfe252f135160c868a5eb5e2171f1a8bd2bdce3ec76b175c",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/security-scanner-pipeline",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__security-scanner-pipeline.r2.json",
   "plan_sha256": "8de7144ee6b67b698316a5cc8b05dc994561a701f8d4be78b6972b5de2001e54",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/seeking-alpha",
   "planned": false,
   "extract": null,
   "plan_sha256": null,
   "reason": "terraform plan rc=1: Error: Missing required argument on main.tf line 168, in module \"news_dedup\": 168: module \"news_dedup\" { The argument \"artifact_key\" is required, but no definition was found. Error: Unsupported argument on main.tf line 171, in module \"news_dedup\": 171: source_dir = \"${local.lambda_base_dir}/seeking-alpha-news-dedup\" An argument named \"source_dir\" is not expected here.",
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/served-guard-49f",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__served-guard-49f.r2.json",
   "plan_sha256": "09739019da2db298cdd1889c05ae7437b65980a4892dff9e5055076a625f67a3",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/served-guard-cot",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__served-guard-cot.r2.json",
   "plan_sha256": "b00385fb7cb1457d56240e1ffd275f96f87db1e804f305fd49e24ad1e7d525ad",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/served-guard-inf",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__served-guard-inf.r2.json",
   "plan_sha256": "3d4ae8a3d032c660c33cc85948777d483f06912b035270f38a2d6477573b0b16",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/shared-infra",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__shared-infra.r2.json",
   "plan_sha256": "812b8efd510603b20024b6a170a75fcf33b04f57bc6ea1cf8a1dfad84aa8e3c1",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/smartx-pipeline",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__smartx-pipeline.r2.json",
   "plan_sha256": "3aa5d0eca59b86de8745d96a00e3274e01a254ad855a63fa63b3f554afcb31c5",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/smartx-v2-bucket-lifecycle",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__smartx-v2-bucket-lifecycle.r2.json",
   "plan_sha256": "23f1e2df55884cd5da200f10508f3f8da093723e65b4ac27cb49651cc6fbfeae",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/terraform-state-bucket-lifecycle",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__terraform-state-bucket-lifecycle.r2.json",
   "plan_sha256": "faf10ecee696eacd0fe00d81cb2efaff5b9c9a96a1afd5833a1f726055671ba9",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/ticket-center",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__ticket-center.r2.json",
   "plan_sha256": "4a6817eee107bf6b26bf610b619c0ee0828ef8aa4b7b455c20a8b7c835dc6f16",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/trade-pipeline",
   "planned": false,
   "extract": null,
   "plan_sha256": null,
   "reason": "terraform plan rc=1: Error: No value for required variable on variables.tf line 1: 1: variable \"jwt_secret\" { The root module input variable \"jwt_secret\" is not set, and has no default value. Use a -var or -var-file command line argument to provide a value for this variable.",
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/website",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__website.r2.json",
   "plan_sha256": "5e6e4631e668acdb662a6d5cad1afba11cb480c65a647755815138ca04b43686",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/yang-pipeline",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__yang-pipeline.r2.json",
   "plan_sha256": "8fb16be56d4cca408b7a3531bd3ee392c6f4d2c4b1e57bd73a9baf2db7cd4954",
   "reason": null,
   "init_flags": "-input=false"
  },
  {
   "root": "infra/aws/terraform/ycharts-pipeline",
   "planned": true,
   "extract": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/infra__aws__terraform__ycharts-pipeline.r2.json",
   "plan_sha256": "f698187b2cddd331ca4af6af65a3b04b8e3a0eb529be772d4333de9b92962552",
   "reason": null,
   "init_flags": "-input=false"
  }
 ],
 "additions": [
  {
   "root": "infra/aws/terraform/49f-value-parity",
   "address": "aws_cloudwatch_event_rule.f49_value_parity_hourly",
   "name": "f49_value_parity_hourly",
   "verdict": "CONFORMANT"
  },
  {
   "root": "infra/aws/terraform/49f-value-parity",
   "address": "aws_cloudwatch_event_target.f49_value_parity_hourly",
   "name": "f49_value_parity_hourly",
   "verdict": "NOT-PRINTED"
  },
  {
   "root": "infra/aws/terraform/49f-value-parity",
   "address": "aws_iam_role.f49_value_parity",
   "name": "f49_value_parity",
   "verdict": "REFUSE"
  },
  {
   "root": "infra/aws/terraform/49f-value-parity",
   "address": "aws_iam_role_policy.f49_value_parity_logs",
   "name": "f49_value_parity_logs",
   "verdict": "REFUSE"
  },
  {
   "root": "infra/aws/terraform/49f-value-parity",
   "address": "aws_iam_role_policy.f49_value_parity_read",
   "name": "f49_value_parity_read",
   "verdict": "REFUSE"
  },
  {
   "root": "infra/aws/terraform/49f-value-parity",
   "address": "aws_iam_role_policy.f49_value_parity_sns",
   "name": "f49_value_parity_sns",
   "verdict": "REFUSE"
  },
  {
   "root": "infra/aws/terraform/49f-value-parity",
   "address": "aws_lambda_function.f49_value_parity",
   "name": "f49_value_parity",
   "verdict": "REFUSE"
  },
  {
   "root": "infra/aws/terraform/49f-value-parity",
   "address": "aws_lambda_permission.f49_value_parity_events",
   "name": "f49_value_parity_events",
   "verdict": "NOT-PRINTED"
  },
  {
   "root": "infra/aws/terraform/aaii-v2-bucket-lifecycle",
   "address": "aws_s3_bucket_lifecycle_configuration.opal_data_aaii_v2",
   "name": "opal_data_aaii_v2",
   "verdict": "NOT-PRINTED"
  },
  {
   "root": "infra/aws/terraform/c3materialize-b4",
   "address": "aws_codebuild_project.sbm",
   "name": "sbm",
   "verdict": "REFUSE"
  },
  {
   "root": "infra/aws/terraform/c3materialize-b4",
   "address": "aws_ecr_lifecycle_policy.sbm",
   "name": "sbm",
   "verdict": "NOT-PRINTED"
  },
  {
   "root": "infra/aws/terraform/c3materialize-b4",
   "address": "aws_ecr_repository.sbm",
   "name": "sbm",
   "verdict": "NOT-PRINTED"
  },
  {
   "root": "infra/aws/terraform/c3materialize-b4",
   "address": "aws_iam_role.build",
   "name": "build",
   "verdict": "CONFORMANT"
  },
  {
   "root": "infra/aws/terraform/c3materialize-b4",
   "address": "aws_iam_role_policy.build",
   "name": "build",
   "verdict": "REFUSE"
  },
  {
   "root": "infra/aws/terraform/etfs-canon",
   "address": "aws_dynamodb_table.etfs_ownership_daily",
   "name": "etfs_ownership_daily",
   "verdict": "REFUSE"
  },
  {
   "root": "infra/aws/terraform/exec-summary",
   "address": "aws_cloudwatch_event_rule.exec_summary_trigger_placeholder",
   "name": "exec_summary_trigger_placeholder",
   "verdict": "REFUSE"
  },
  {
   "root": "infra/aws/terraform/exec-summary",
   "address": "aws_cloudwatch_event_target.exec_summary_trigger_target",
   "name": "exec_summary_trigger_target",
   "verdict": "NOT-PRINTED"
  },
  {
   "root": "infra/aws/terraform/exec-summary",
   "address": "aws_lambda_permission.eventbridge_exec_summary",
   "name": "eventbridge_exec_summary",
   "verdict": "NOT-PRINTED"
  },
  {
   "root": "infra/aws/terraform/github-actions-runner",
   "address": "aws_cloudwatch_log_group.gha_runner",
   "name": "gha_runner",
   "verdict": "REFUSE"
  },
  {
   "root": "infra/aws/terraform/github-actions-runner",
   "address": "aws_iam_instance_profile.gha_runner",
   "name": "gha_runner",
   "verdict": "REFUSE"
  },
  {
   "root": "infra/aws/terraform/github-actions-runner",
   "address": "aws_iam_role.gha_runner",
   "name": "gha_runner",
   "verdict": "REFUSE"
  },
  {
   "root": "infra/aws/terraform/github-actions-runner",
   "address": "aws_iam_role_policy.gha_runner_logs",
   "name": "gha_runner_logs",
   "verdict": "REFUSE"
  },
  {
   "root": "infra/aws/terraform/github-actions-runner",
   "address": "aws_iam_role_policy_attachment.gha_runner_ssm",
   "name": "gha_runner_ssm",
   "verdict": "NOT-PRINTED"
  },
  {
   "root": "infra/aws/terraform/github-actions-runner",
   "address": "aws_instance.gha_runner",
   "name": "gha_runner",
   "verdict": "REFUSE"
  },
  {
   "root": "infra/aws/terraform/globgrph",
   "address": "aws_glue_partition.tool_activity[\"routing\"]",
   "name": "tool_activity",
   "verdict": "NOT-PRINTED"
  },
  {
   "root": "infra/aws/terraform/imo-pipeline",
   "address": "aws_s3_object.prefix_marker[\"qa/.keep\"]",
   "name": "prefix_marker",
   "verdict": "REFUSE"
  },
  {
   "root": "infra/aws/terraform/imo-pipeline",
   "address": "aws_sns_topic_subscription.andrew_email[0]",
   "name": "andrew_email",
   "verdict": "NOT-PRINTED"
  },
  {
   "root": "infra/aws/terraform/inf-pipeline",
   "address": "aws_secretsmanager_secret_version.eclipse_jwt_initial",
   "name": "eclipse_jwt_initial",
   "verdict": "NOT-PRINTED"
  },
  {
   "root": "infra/aws/terraform/market-overview",
   "address": "aws_s3_bucket.market_data_v2",
   "name": "market_data_v2",
   "verdict": "REFUSE"
  },
  {
   "root": "infra/aws/terraform/market-overview",
   "address": "aws_s3_bucket_public_access_block.market_data_v2",
   "name": "market_data_v2",
   "verdict": "NOT-PRINTED"
  },
  {
   "root": "infra/aws/terraform/market-overview",
   "address": "aws_s3_bucket_server_side_encryption_configuration.market_data_v2",
   "name": "market_data_v2",
   "verdict": "NOT-PRINTED"
  },
  {
   "root": "infra/aws/terraform/market-overview",
   "address": "aws_s3_bucket_versioning.market_data_v2",
   "name": "market_data_v2",
   "verdict": "NOT-PRINTED"
  },
  {
   "root": "infra/aws/terraform/portfolio-management",
   "address": "aws_api_gateway_deployment.opal_portal_api",
   "name": "opal_portal_api",
   "verdict": "NOT-PRINTED"
  },
  {
   "root": "infra/aws/terraform/smartx-v2-bucket-lifecycle",
   "address": "aws_s3_bucket_lifecycle_configuration.opal_data_smartx_v2",
   "name": "opal_data_smartx_v2",
   "verdict": "NOT-PRINTED"
  }
 ]
}
```
