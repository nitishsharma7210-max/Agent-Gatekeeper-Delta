# PROMPTS.md — AI coding session record

Use these prompts in Google Antigravity. Keep this file accurate: add the date/time and paste or summarize the prompts you actually used. Do not claim you used a prompt unless you did.

## Prompt 1 — Project scaffold
Date/time used: [fill in actual date and time]

"Create a small Python Streamlit classroom prototype called Agent Gatekeeper for Delta Air Lines. It must be a local simulation only, not connect to Delta. Include a dashboard, request evaluation, agent registration/revocation, and a CSV audit log. Show the student's enrolment number, but ask for the full number rather than inventing it."

## Prompt 2 — Decision rules
Date/time used: [fill in actual date and time]

"Implement eight rules: unknown agents are blocked; revoked agents are blocked; authorized registered agents may view fares; authorized registered agents may view booking details; booking/payment at or below ₹50,000 is allowed; booking/payment above ₹50,000 requires customer confirmation; booking changes require customer confirmation; refunds require customer confirmation. Return the decision, rule number and reason."

## Prompt 3 — Persistence and audit
Date/time used: [fill in actual date and time]

"Persist registered agents in agents.json. When an agent is revoked, save the revocation date and time. Append every evaluated request to audit_log.csv with timestamp, customer, agent, action, amount, decision, rule and reason."

## Prompt 4 — Testing
Date/time used: [fill in actual date and time]

"Add or verify six test scenarios: known agent viewing fares; unknown agent; payment above the limit; payment below the limit; revoked agent; and refund request. Show expected and actual results and fix any defects."

## Prompt 5 — Review and explain
Date/time used: [fill in actual date and time]

"Review the project for errors. Explain the application flow, each rule, the agent revocation logic and audit log in beginner-friendly language. Do not add real airline integrations or claim real transactions are performed."

## Student work record
After each Antigravity session, add:
- Actual date and time:
- Prompt used:
- What Antigravity generated or changed:
- What I personally checked, edited or tested:
