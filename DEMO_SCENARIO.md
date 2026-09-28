# FORESIGHT - Demo Scenario & Architecture

## 1. Demo Day Architecture
To maintain absolute transparency with the judges, this section explicitly outlines what is running live and what is simulated during the hackfest demo.

### Live (Executing in SAP BTP & Python Runtime)
*   **SAP CAP OData Services**: Live business logic handling routing, draft choreography, and data persistence.
*   **SAP HANA Cloud Persistence**: Live database storing the Disruption events, Recovery Plans, Commitments, and Audit logs.
*   **SAPUI5 Fiori Inbox**: Live frontend application acting as the enterprise decision console.
*   **Python Agent Runtime**: Live concurrent execution of the agent swarm, graph analysis, and mathematical optimization logic.
*   **SAP Generative AI Hub (if verified)**: Live LLM inference passing through SAP's enterprise proxy.

### Simulated / Mocked (Unless explicitly verified)
*   **The Disruption Event**: Simulated via an HTTP POST request to the CAP backend, rather than waiting for a live external system failure (bypassing the Zero-Trust Reality Engine extension for MVP).
*   **S/4HANA OData Endpoints**: If live practice APIs are unverified or unstable, the `mock-s4hana` adapter will respond with realistic, pre-seeded data for Suppliers, Inventory, and Purchase Orders.
*   **SAP Event Mesh**: If unavailable, pub/sub events are simulated via direct REST calls.
*   **Industrial Dark Pool**: Will be mocked or bypassed for the MVP thin slice.

## 2. Thin Vertical Slice Walkthrough (The Demo Flow)

The demo illustrates the "One Controlled Commitment Gate" principle, where multiple intelligence layers process concurrently before a human makes the final, governed decision.

### Step 1: SEE (The Trigger)
The demo begins with an HTTP POST request simulating an alert that "Supplier X" (a critical component manufacturer) has gone offline. The CAP backend registers a new `Disruption` entity in HANA Cloud.

### Step 2: UNDERSTAND (Impact Analysis)
The Python runtime detects the new `Disruption`. It queries the CAP layer to traverse the Supply Chain Knowledge Graph, mapping the blast radius: determining which BOMs use the component and which current Production Orders are stalled.

### Step 3: COLLABORATE (Parallel Agent Swarm)
The runtime spawns parallel, concurrent reasoning threads (No Waiting Rooms!):
*   **Procurement Agent**: Identifies Supplier Y in the mock S/4 system.
*   **Inventory Agent**: Discovers surplus stock in Plant B.
*   **Logistics Agent**: Calculates the cost to expedite freight from Plant B.
*   **Risk Agent**: Confirms Supplier Y meets compliance thresholds.

### Step 4: SIMULATE (Optimization)
The Python optimization logic evaluates the swarm's findings and formulates a `RecoveryPlan` (e.g., Transfer 30% from Plant B, Purchase 70% from Supplier Y). The plan is scored on `Cost + Service Impact + Operational Risk + Working Capital + Commitment Risk`.

### Step 5: COMMIT (Validation & Human Approval Gate)
The plan is validated against the Commitment Graph to ensure it doesn't violate existing top-tier customer commitments. It is then committed to the CAP backend as a Draft.
The judge assumes the role of a Supply Chain Manager. They open the SAPUI5 app on the Launchpad, view the new `RecoveryPlan` draft, read the AI's explanation, and click "Approve".

### Step 6: EXECUTE & RECOVER (Transaction & Audit)
Upon approval, CAP finalizes the Draft. It triggers an action that tells the S/4HANA Adapter to create the necessary POs and STOs. Finally, an `AuditEvent` is written to HANA Cloud, proving the AI acted within bounds and with human oversight.
