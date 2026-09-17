# FENCE_PROBES -- the four arms of the opal-data-49financial fence, run for real (EN-f-2, ledger leg L3)

**Author:** `0.9.0_WK_LGIC_ENFORCE~1`, task order `LGIC_ENFORCE.TO-EN-f-2`. **Bucket:** `opal-data-49financial`. **Object:** `_code/POLICY_BLOCK.json`.
**Instrument:** `aws s3api get-object --debug` through `.tools/aws` (Git Bash), once per principal. Each probe role was
assumed with `aws sts assume-role` and its caller printed with `sts get-caller-identity` before the read. No policy
simulation was used. The request id is the S3 response's `x-amz-request-id` header, read from the `--debug` stream.
**Fence live since:** the leg L2 apply, completed 2026-09-15T08:17:25Z.

```json
{
  "probes": [
    {
      "role": "mdpf-49f-fenceprobe-role",
      "kind": "probe",
      "action": "s3:GetObject",
      "object": "_code/POLICY_BLOCK.json",
      "result": "ALLOWED",
      "evidence": "x-amz-request-id C5WFQFQPTWGXTD8N; ETag \"ebb90267ebf2ff5d575008bdb2bc72ad\"; caller arn:aws:sts::313476888478:assumed-role/mdpf-49f-fenceprobe-role/enf2-probe; at 2026-09-15T08:20:28Z"
    },
    {
      "role": "mdpf-cot-fenceprobe-role",
      "kind": "probe",
      "action": "s3:GetObject",
      "object": "_code/POLICY_BLOCK.json",
      "result": "DENIED",
      "evidence": "x-amz-request-id BYP7EENM7APP44CC; error: An error occurred (AccessDenied) when calling the GetObject operation: User: arn:aws:sts::313476888478:assumed-role/mdpf-cot-fenceprobe-role/enf2-probe is not authorized to perform: s3:GetObject on resource: \"arn:aws:s3:::opal-data-49financial/_code/POLICY_BLOCK.json\" with an explicit deny in a resource-based policy; caller arn:aws:sts::313476888478:assumed-role/mdpf-cot-fenceprobe-role/enf2-probe; at 2026-09-15T08:20:42Z"
    },
    {
      "role": "mdpf-fenceprobe-role",
      "kind": "probe",
      "action": "s3:GetObject",
      "object": "_code/POLICY_BLOCK.json",
      "result": "DENIED",
      "evidence": "x-amz-request-id CHXCAFYPDN6KRAHR; error: An error occurred (AccessDenied) when calling the GetObject operation: User: arn:aws:sts::313476888478:assumed-role/mdpf-fenceprobe-role/enf2-probe is not authorized to perform: s3:GetObject on resource: \"arn:aws:s3:::opal-data-49financial/_code/POLICY_BLOCK.json\" with an explicit deny in a resource-based policy; caller arn:aws:sts::313476888478:assumed-role/mdpf-fenceprobe-role/enf2-probe; at 2026-09-15T08:20:59Z"
    },
    {
      "role": "Andrew_Berman",
      "kind": "exempt",
      "action": "s3:GetObject",
      "object": "_code/POLICY_BLOCK.json",
      "result": "ALLOWED",
      "evidence": "x-amz-request-id FKEX87SAV4D5EX39; ETag \"ebb90267ebf2ff5d575008bdb2bc72ad\"; caller arn:aws:iam::313476888478:user/Andrew_Berman; at 2026-09-15T08:21:10Z"
    }
  ]
}
```
