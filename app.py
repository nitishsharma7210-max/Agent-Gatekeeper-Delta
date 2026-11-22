import csv
import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
from gatekeeper import ACTIONS, SPENDING_LIMIT, decide_request

APP_DIR = Path(__file__).parent
AGENTS_FILE = APP_DIR / "agents.json"
AUDIT_FILE = APP_DIR / "audit_log.csv"
AUDIT_COLUMNS = [
    "timestamp", "customer", "agent_id", "agent_name",
    "action", "amount_inr", "decision", "rule", "reason"
]


def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_agents():
    if not AGENTS_FILE.exists():
        demo = {
            "AGENT-001": {
                "name": "TravelBuddy Demo",
                "customer": "Demo Customer",
                "active": True,
                "registered_at": now_iso(),
                "revoked_at": "",
                "permissions": ACTIONS,
            }
        }
        save_agents(demo)
        return demo
    try:
        return json.loads(AGENTS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_agents(agents):
    AGENTS_FILE.write_text(
        json.dumps(agents, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def ensure_audit_file():
    if not AUDIT_FILE.exists():
        with AUDIT_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=AUDIT_COLUMNS)
            writer.writeheader()


def write_audit(customer, agent_id, agent_name, action, amount, decision, rule, reason):
    ensure_audit_file()
    row = {
        "timestamp": now_iso(),
        "customer": customer,
        "agent_id": agent_id,
        "agent_name": agent_name,
        "action": action,
        "amount_inr": amount,
        "decision": decision,
        "rule": rule,
        "reason": reason,
    }
    with AUDIT_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=AUDIT_COLUMNS)
        writer.writerow(row)


st.set_page_config(page_title="Agent Gatekeeper | Delta", page_icon="🛫", layout="wide")

if "agents" not in st.session_state:
    st.session_state.agents = load_agents()
ensure_audit_file()

st.title("🛫 Agent Gatekeeper")
st.subheader("Delta Air Lines | AI Agent Permission & Security Prototype")
st.caption("Educational simulation only — not connected to Delta systems and does not book, change, charge, or refund tickets.")

with st.sidebar:
    st.header("Project details")
    enrolment = st.text_input(
        "Enter your full enrolment number",
        placeholder="Enter your actual enrolment number"
    )
    if enrolment.strip():
        st.success(f"Enrolment number: {enrolment.strip()}")
    else:
        st.info("Enrolment number ends in 1. Enter your full number before taking the final screenshot.")
    st.metric("Spending limit", f"₹{SPENDING_LIMIT:,.0f}")
    st.markdown("---")
    st.markdown("**Decision meanings**")
    st.success("ALLOW — permitted by the demo rules")
    st.warning("ASK CUSTOMER — pause for confirmation")
    st.error("BLOCK — not permitted")

agents = st.session_state.agents
audit_count = 0
if AUDIT_FILE.exists():
    try:
        audit_count = max(0, len(pd.read_csv(AUDIT_FILE)))
    except Exception:
        audit_count = 0
active_count = sum(1 for a in agents.values() if a.get("active"))

m1, m2, m3 = st.columns(3)
m1.metric("Registered agents", len(agents))
m2.metric("Active agents", active_count)
m3.metric("Requests in audit log", audit_count)

tab_request, tab_agents, tab_audit, tab_rules = st.tabs(
    ["Check a request", "Agent management", "Audit log", "Rules & about"]
)

with tab_request:
    st.header("Evaluate an AI agent request")
    with st.form("request_form"):
        c1, c2 = st.columns(2)
        with c1:
            customer = st.text_input("Customer name", value="Demo Customer")
            agent_id = st.text_input("Agent ID", value="AGENT-001")
            action = st.selectbox("Requested action", ACTIONS)
        with c2:
            amount = st.number_input(
                "Amount in INR (use 0 for read-only actions)",
                min_value=0.0, value=0.0, step=500.0
            )
            st.caption("The amount is used for booking/payment requests.")
        submitted = st.form_submit_button("Evaluate request", type="primary")

    if submitted:
        customer = customer.strip() or "Customer not provided"
        agent_id = agent_id.strip()
        decision, rule, reason = decide_request(
            st.session_state.agents, agent_id, action, amount
        )
        agent_name = st.session_state.agents.get(agent_id, {}).get("name", "Unknown")
        write_audit(customer, agent_id, agent_name, action, amount, decision, rule, reason)
        st.session_state.last_result = {
            "decision": decision, "rule": rule, "reason": reason,
            "agent_id": agent_id, "action": action, "amount": amount
        }

    if "last_result" in st.session_state:
        result = st.session_state.last_result
        st.markdown("---")
        st.subheader("Decision result")
        if result["decision"] == "ALLOW":
            st.success(f'{result["decision"]} — {result["rule"]}')
        elif result["decision"] == "ASK CUSTOMER":
            st.warning(f'{result["decision"]} — {result["rule"]}')
        else:
            st.error(f'{result["decision"]} — {result["rule"]}')
        st.write(result["reason"])
        if result["decision"] == "ASK CUSTOMER":
            st.info("The request is paused. The prototype has not performed the booking, change, payment or refund.")

with tab_agents:
    st.header("Register an agent")
    with st.form("register_form"):
        new_id = st.text_input("New agent ID", placeholder="Example: AGENT-002")
        new_name = st.text_input("Agent name", placeholder="Example: SkyPlanner")
        new_customer = st.text_input("Customer who authorizes this agent")
        permissions = st.multiselect(
            "Actions authorized by the customer",
            ACTIONS,
            default=["View fares", "View booking details"]
        )
        register = st.form_submit_button("Register agent")
    if register:
        new_id = new_id.strip()
        if not new_id or not new_name.strip() or not new_customer.strip():
            st.error("Enter an agent ID, agent name and customer name.")
        elif new_id in st.session_state.agents:
            st.error("That agent ID already exists. Use a unique ID.")
        elif not permissions:
            st.error("Select at least one permission.")
        else:
            st.session_state.agents[new_id] = {
                "name": new_name.strip(),
                "customer": new_customer.strip(),
                "active": True,
                "registered_at": now_iso(),
                "revoked_at": "",
                "permissions": permissions,
            }
            save_agents(st.session_state.agents)
            st.success(f"Registered {new_name.strip()} as {new_id}.")
            st.rerun()

    st.markdown("---")
    st.header("Registered agents")
    if st.session_state.agents:
        for aid, info in st.session_state.agents.items():
            status = "ACTIVE" if info.get("active") else "REVOKED"
            with st.expander(f'{aid} — {info.get("name", "Unnamed")} — {status}'):
                st.write(f'Customer: {info.get("customer", "")}')
                st.write(f'Registered: {info.get("registered_at", "")}')
                st.write(f'Revoked: {info.get("revoked_at") or "Not revoked"}')
                st.write("Permissions: " + ", ".join(info.get("permissions", [])))
                if info.get("active"):
                    if st.button("Revoke this agent", key=f"revoke_{aid}", type="secondary"):
                        st.session_state.agents[aid]["active"] = False
                        st.session_state.agents[aid]["revoked_at"] = now_iso()
                        save_agents(st.session_state.agents)
                        st.success(f"{aid} revoked. The revocation timestamp has been saved.")
                        st.rerun()
    else:
        st.info("No agents registered yet.")

with tab_audit:
    st.header("Audit log")
    st.caption("Every evaluated request is appended to audit_log.csv with a local date/time and the rule that caused the decision.")
    if AUDIT_FILE.exists():
        try:
            log_df = pd.read_csv(AUDIT_FILE)
            if not log_df.empty:
                st.dataframe(log_df.sort_values("timestamp", ascending=False), use_container_width=True)
                st.download_button(
                    "Download audit_log.csv",
                    data=AUDIT_FILE.read_bytes(),
                    file_name="audit_log.csv",
                    mime="text/csv"
                )
            else:
                st.info("No requests recorded yet. Run the test cases to create audit entries.")
        except Exception as exc:
            st.error(f"Could not read audit log: {exc}")

with tab_rules:
    st.header("Eight prototype rules")
    rule_rows = [
        ("R1", "Unknown agent or action outside granted permissions", "BLOCK"),
        ("R2", "Revoked agent", "BLOCK"),
        ("R3", "Registered agent views fares", "ALLOW"),
        ("R4", "Registered agent views booking details", "ALLOW"),
        ("R5", "Booking/payment at or below ₹50,000", "ALLOW"),
        ("R6", "Booking/payment above ₹50,000", "ASK CUSTOMER"),
        ("R7", "Change an existing booking", "ASK CUSTOMER"),
        ("R8", "Request a refund", "ASK CUSTOMER"),
    ]
    st.table(pd.DataFrame(rule_rows, columns=["Rule", "Condition", "Decision"]))
    st.markdown("**Why this prototype?** It demonstrates controlled permissions, explicit customer approval for higher-risk actions, revocation and an auditable decision trail.")
    st.markdown("**Limitations:** This is a local classroom simulation. It does not authenticate real Delta customers, connect to Delta APIs, or execute airline transactions.")
