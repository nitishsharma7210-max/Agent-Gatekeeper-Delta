"""Pure decision logic for the Agent Gatekeeper classroom prototype."""

SPENDING_LIMIT = 50000
ACTIONS = [
    "View fares",
    "View booking details",
    "Book flight / make payment",
    "Change booking",
    "Request refund",
]

def decide_request(agents, agent_id, action, amount):
    """Return decision, rule number and explanation. No real airline transaction is made."""
    agent = agents.get(agent_id)

    if agent is None:
        return "BLOCK", "R1", "The agent is not registered."

    if not agent.get("active", False):
        revoked_at = agent.get("revoked_at") or "timestamp unavailable"
        return "BLOCK", "R2", f"The agent's permission was revoked at {revoked_at}."

    if action not in agent.get("permissions", []):
        return "BLOCK", "R1", "This action is outside the permissions granted to this agent."

    if action == "View fares":
        return "ALLOW", "R3", "Registered and active agent; viewing fares is read-only."

    if action == "View booking details":
        return "ALLOW", "R4", "Registered and active agent; viewing booking details is read-only."

    if action == "Book flight / make payment":
        if amount > SPENDING_LIMIT:
            return "ASK CUSTOMER", "R6", (
                f"₹{amount:,.2f} is above the ₹{SPENDING_LIMIT:,.0f} spending limit. "
                "Customer confirmation is required."
            )
        return "ALLOW", "R5", (
            f"₹{amount:,.2f} is within the ₹{SPENDING_LIMIT:,.0f} spending limit."
        )

    if action == "Change booking":
        return "ASK CUSTOMER", "R7", "Changing an existing booking requires customer confirmation."

    if action == "Request refund":
        return "ASK CUSTOMER", "R8", "A refund request requires customer confirmation."

    return "BLOCK", "R1", "The requested action is not recognized."

