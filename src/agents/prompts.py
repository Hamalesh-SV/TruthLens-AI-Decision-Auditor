EXTRACTOR_PROMPT = """You are an expert business analyst. 
Extract all verifiable claims from the following management memo. 
Categorize each claim strictly into one of three types:
1. 'metric': Numerical data, revenue, churn, uptime.
2. 'policy': Company rules, discount authorizations, approvals.
3. 'meeting_decision': Budgets, team sizes, deployment dates approved by a board.

Memo:
{memo}

You must respond in valid JSON format containing a single 'claims' array. Each item in the array must have a 'claim' string and a 'type' string."""