# Delta Air Lines — Agent Gatekeeper Rules

**Project spending limit: ₹50,000.** This is an illustrative threshold chosen for this classroom prototype, not a real Delta Air Lines policy.

| Rule | Rule | Decision |
|---|---|---|
| R1 | An unknown agent, or an agent attempting an action outside the permissions granted by the customer, is blocked. | BLOCK |
| R2 | A revoked agent is always blocked. | BLOCK |
| R3 | A registered, active and authorized agent may view fares. | ALLOW |
| R4 | A registered, active and authorized agent may view booking details. | ALLOW |
| R5 | A registered, active and authorized agent may make a booking/payment at or below ₹50,000. | ALLOW |
| R6 | A booking/payment above ₹50,000 requires customer confirmation. | ASK CUSTOMER |
| R7 | Changing an existing booking requires customer confirmation. | ASK CUSTOMER |
| R8 | Requesting a refund requires customer confirmation. | ASK CUSTOMER |

## Why these rules?
Read-only actions have lower impact than transactions. A spending threshold allows limited routine activity while requiring confirmation for larger payments. Changes and refunds can materially affect a customer's travel and money, so the prototype pauses them for explicit customer approval. Revocation takes priority over every other rule.

## Decision order
1. Check that the agent exists (R1).
2. Check that the agent is active (R2).
3. Check that the requested action is within the agent's granted permissions (R1).
4. Apply the action-specific rule (R3–R8).

## Scope
This is a proposed classroom prototype. It is not Delta policy and is not connected to Delta's booking or payment systems.
