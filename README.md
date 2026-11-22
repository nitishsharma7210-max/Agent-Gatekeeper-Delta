# Agent Gatekeeper — Delta Air Lines

A classroom prototype that evaluates simulated AI-agent requests and returns ALLOW, ASK CUSTOMER, or BLOCK.

## Important
This is an educational simulation only. It is not affiliated with Delta Air Lines, does not connect to Delta systems, and does not make real bookings, payments, changes, or refunds.

## Features
- Evaluate flight-fare, booking-detail, booking/payment, change, and refund requests.
- Register agents with customer-granted permissions.
- Revoke an agent and save the revocation date/time.
- Record every decision in `audit_log.csv`.
- Show the enrolment number on the dashboard after the student enters the full number.

## Run locally
1. Install Python 3.10 or later.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (optional but recommended).
4. Run `pip install -r requirements.txt`.
5. Run `streamlit run app.py`.
6. Open the local URL shown in the terminal.

## Demo agent
The first launch creates `AGENT-001` (TravelBuddy Demo) for Demo Customer. It is a sample record for testing. You can register additional agents in the Agent management tab.

## Data files
- `agents.json`: registered agents and revocation timestamps.
- `audit_log.csv`: timestamped decision history.

These files are created in the project folder when the app runs.
