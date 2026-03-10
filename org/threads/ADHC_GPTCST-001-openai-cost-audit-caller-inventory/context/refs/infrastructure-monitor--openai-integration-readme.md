# OpenAI Cost Tracking - Integration Instructions

**File:** `openai_cost_tracker.py`
**Status:** ✅ READY FOR INTEGRATION
**Method:** Real-time CloudWatch activity correlation

---

## How It Works

### 1. Empirical Cost Multiplier (from your CSV data)

**Calculated from Jan 18 - Feb 17, 2026 actual usage:**
```
Total Cost: $2.51
Total API Calls: 933
Cost per Call: $2.51 / 933 = $0.00269 (blended average)
```

**Per-function multipliers:**
- `semantic-news-layer3-curation`: $0.011/call (gpt-4o, 50 clusters)
- `news-trending-analysis`: $0.002/call (mixed models)
- `market-update-generator`: $0.002/call (gpt-4o-mini)

### 2. Real-Time Activity Query

**Queries CloudWatch Logs for each OpenAI Lambda function:**
```python
aws logs filter-log-events \
  --log-group-name /aws/lambda/{function_name} \
  --filter-pattern '"api.openai.com"' \
  --since 24h
```

**Counts actual API calls made TODAY**

### 3. Cost Calculation

```
TODAY's Cost = (API calls in CloudWatch) × (Cost per call multiplier)
```

**Example from Feb 17:**
```
CloudWatch: 1 call from semantic-news-layer3-curation
Cost = 1 × $0.011 = $0.011
Projected daily = $0.013
Projected monthly = $0.38
```

---

## Integration into Infrastructure Monitor Lambda

### Step 1: Import the Module

**In `lambda_function.py`:**

```python
# Add at top
from openai_cost_tracker import get_openai_cost_html

def lambda_handler(event, context):
    """Generate daily infrastructure monitoring email."""

    # Existing sections
    ec2_html = generate_ec2_monitoring()
    lambda_html = generate_lambda_monitoring()
    s3_html = generate_s3_monitoring()

    # NEW: OpenAI cost tracking (queries CloudWatch in real-time)
    openai_html = get_openai_cost_html()

    security_html = generate_security_sweep()

    # Compose email
    email_body = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Daily Infrastructure Report</h1>
        {ec2_html}
        {lambda_html}
        {s3_html}
        {openai_html}      <!-- Real-time OpenAI cost -->
        {security_html}
    </body>
    </html>
    """

    # Send email via SES
    send_email(email_body)
```

### Step 2: Add CloudWatch Logs Permissions (If Not Already Present)

**IAM Role:** `opal-portal-lambda-role` (used by infrastructure-monitor)

**Add policy if needed:**
```json
{
  "Sid": "CloudWatchLogsQuery",
  "Effect": "Allow",
  "Action": [
    "logs:FilterLogEvents",
    "logs:StartQuery",
    "logs:GetQueryResults"
  ],
  "Resource": "arn:aws:logs:us-east-1:313476888478:log-group:/aws/lambda/*"
}
```

### Step 3: Deploy

```bash
cd infra/aws/lambda/infrastructure_monitor

# The file is already there: openai_cost_tracker.py

# Deploy (when ready)
# ... your deployment method ...
```

---

## What It Shows (Based on Real Activity)

**Daily Email Will Show:**

```html
💰 OpenAI API Cost (Real-Time Activity)

Today's Usage (8.5 hours elapsed):
  API Calls (so far): 3
  Cost (so far): $0.0250
  Projected Daily: $0.0705
  Projected Monthly: $2.12

Activity by Function (Today):
  semantic-news-layer3-curation: 1 call → $0.0110
  news-trending-analysis: 2 calls → $0.0038

📊 Model: Real-time CloudWatch activity × empirical cost-per-call
🔢 Multiplier: $0.00269 per call (from 30-day data)
🔄 Updates: Live - actual API calls, not static estimates
📈 Baseline: $0.0823/day (30-day avg for reference)
```

---

## Dynamic Behavior Examples

### Scenario 1: Normal Day
```
CloudWatch detects:
- semantic-news-layer3-curation: 1 call (9:05 AM)
- news-trending-analysis: 5 calls (throughout day)
- market-update-generator: 3 calls

Cost = (1 × $0.011) + (5 × $0.002) + (3 × $0.002) = $0.027
Projected monthly = $0.81
```

### Scenario 2: Heavy Testing Day
```
CloudWatch detects:
- semantic-news-layer3-curation: 10 calls (testing)
- news-trending-analysis: 20 calls
- market-update-generator: 5 calls

Cost = (10 × $0.011) + (20 × $0.002) + (5 × $0.002) = $0.160
Projected monthly = $4.80
Email will show: ⚠️ Higher than baseline
```

### Scenario 3: Quiet Day
```
CloudWatch detects: 0 calls

Cost = $0.00
Email will show: "No OpenAI activity detected today"
Fallback: Shows baseline estimate $0.0823/day
```

---

## Updating the Multiplier (Monthly Maintenance)

**Once a month, recalibrate:**

1. **Export new CSVs from OpenAI dashboard**
2. **Calculate new multiplier:**
   ```python
   import pandas as pd

   cost_df = pd.read_csv('cost_new.csv')
   usage_df = pd.read_csv('usage_new.csv')

   total_cost = cost_df['amount_value'].sum()
   total_calls = usage_df['num_model_requests'].sum()

   new_multiplier = total_cost / total_calls
   print(f"Update COST_PER_API_CALL to: {new_multiplier:.6f}")
   ```

3. **Update `openai_cost_tracker.py`:**
   ```python
   COST_PER_API_CALL = 0.002690  # ← Update this value
   ```

4. **Re-deploy infrastructure-monitor**

**Time:** 5 minutes per month

---

## Verification

**Test that it's working:**

```python
# Run locally
python3 openai_cost_tracker.py

# Should output:
# ✅ Found X API calls today
#    Cost so far: $X.XXXX
#    Projected daily: $X.XXXX
```

**In production (after deployment):**

Check tomorrow's infrastructure email - should show:
- Real API call counts from CloudWatch
- Cost calculated from actual activity
- Different values each day based on activity

---

## Files

**CORRECT FILE (use this):**
- ✅ `infra/aws/lambda/infrastructure_monitor/openai_cost_tracker.py`
  - Queries CloudWatch Logs
  - Counts actual API calls
  - Applies empirical multiplier
  - Returns real-time cost estimate

**OLD FILE (deleted):**
- ❌ `openai_cost_estimate.py` (removed - was static approach)

**WRONG FILE (don't use):**
- ❌ `infra/aws/scripts/analyze_openai_costs.py` (complex CSV-based approach)

---

## Summary

✅ **Implemented:** Real-time CloudWatch correlation with empirical multipliers
✅ **Tested:** Working - found 1 API call today, calculated $0.011 cost
✅ **Committed:** Pushed to DEV branch
✅ **Ready:** Drop into infrastructure_monitor Lambda and deploy

**Integration:** Add 1 line to lambda_function.py:
```python
openai_html = get_openai_cost_html()  # Real-time, not static
```

**That's it!** No CSV uploads, no pandas dependency, just pure CloudWatch query + hardcoded multiplier.
