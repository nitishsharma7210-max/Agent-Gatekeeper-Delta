# Agent Gatekeeper – Delta Air Lines

**Submitted by:** Nitish Sharma  
**PGD Number:** PGD202571511

## Project Overview
Agent Gatekeeper is an educational prototype designed to demonstrate how AI agents can be securely controlled when accessing airline services.

The system evaluates requests and returns one of three decisions:
- ALLOW
- ASK CUSTOMER
- BLOCK

## Security Features
1. Unknown agents are blocked.
2. Revoked agents are blocked.
3. Authorized agents can view flight fares.
4. Authorized agents can view booking details.
5. Payments up to ₹50,000 are allowed.
6. Payments above ₹50,000 require customer approval.
7. Booking changes require customer approval.
8. Refund requests require customer approval.

## Technology Used
- Python
- Streamlit
- Pandas
- Unit Testing

## Testing
The project includes six automated unit tests and manual testing of authorization, spending limits, unknown agents and revoked agents.

## Limitations
This is an educational demonstration. It is not connected to Delta Air Lines and cannot perform actual bookings, payments or refunds.

## Conclusion
The project demonstrates how an AI Agent Gatekeeper can improve security by checking permissions, controlling sensitive actions and maintaining an audit trail.
