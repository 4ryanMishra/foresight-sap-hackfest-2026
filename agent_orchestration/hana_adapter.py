import os
import json
import datetime
from typing import Dict, Any, List, Optional

try:
    from hdbcli import dbapi
except ImportError:
    dbapi = None

class HanaPersistenceAdapter:
    """
    SAP HANA Cloud Persistence Adapter for FORESIGHT Operational State.
    Uses SAP's official Python hdbcli for direct database access to Hackfest-DB / HACKEFEST0115.
    
    Configuration is environment-driven. Zero hardcoded or printed credentials.
    """
    def __init__(self):
        self.host = os.environ.get("HANA_HOST")
        self.port = int(os.environ.get("HANA_PORT", "443"))
        self.user = os.environ.get("HANA_USER")
        self.password = os.environ.get("HANA_PASSWORD")
        self.schema = os.environ.get("HANA_SCHEMA", "HACKEFEST0115")
        
        self.is_configured = bool(self.host and self.user and self.password and dbapi is not None)

    def _get_connection(self):
        if not self.is_configured:
            raise RuntimeError("HANA Cloud connection is NOT CONFIGURED or hdbcli is not installed.")
        return dbapi.connect(
            address=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            currentSchema=self.schema,
            encrypt=True,
            sslValidateCertificate=False
        )

    def health_check(self) -> Dict[str, Any]:
        """
        Runs database connectivity check without printing or revealing credentials.
        """
        status = {
            "configured": self.is_configured,
            "reachable": False,
            "schema": self.schema,
            "test_query_passed": False,
            "error": None
        }
        if not self.is_configured:
            status["error"] = "Missing HANA_HOST / HANA_USER / HANA_PASSWORD or hdbcli module."
            return status

        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM DUMMY")
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if row and row[0] == 1:
                status["reachable"] = True
                status["test_query_passed"] = True
        except Exception as e:
            status["error"] = str(e)
            
        return status

    def init_schema(self):
        """
        Idempotent schema initialization in HANA Cloud (HACKEFEST0115).
        Creates tables if they do not already exist.
        """
        if not self.is_configured:
            return

        conn = self._get_connection()
        cursor = conn.cursor()

        tables = {
            "RECOVERY_CASE": """
                CREATE COLUMN TABLE RECOVERY_CASE (
                    CASE_ID VARCHAR(64) PRIMARY KEY,
                    DISRUPTION_ID VARCHAR(64),
                    STATUS VARCHAR(32),
                    SUPPLIER_ID VARCHAR(64),
                    MATERIAL_ID VARCHAR(64),
                    SHORTAGE_QTY INT,
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "DISRUPT_EVENT": """
                CREATE COLUMN TABLE DISRUPT_EVENT (
                    EVENT_ID VARCHAR(64) PRIMARY KEY,
                    CASE_ID VARCHAR(64),
                    EVENT_TYPE VARCHAR(64),
                    SUPPLIER_ID VARCHAR(64),
                    MATERIAL_ID VARCHAR(64),
                    CONFIDENCE DECIMAL(5,2),
                    DETAILS NCLOB,
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "AGENT_DECISION": """
                CREATE COLUMN TABLE AGENT_DECISION (
                    DECISION_ID VARCHAR(64) PRIMARY KEY,
                    CASE_ID VARCHAR(64),
                    AGENT_NAME VARCHAR(64),
                    ACTION_TYPE VARCHAR(64),
                    TARGET_ID VARCHAR(64),
                    QUANTITY INT,
                    ESTIMATED_COST DECIMAL(15,2),
                    CONFIDENCE DECIMAL(5,2),
                    RATIONALE NCLOB,
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "RECOVERY_PLAN": """
                CREATE COLUMN TABLE RECOVERY_PLAN (
                    PLAN_ID VARCHAR(64) PRIMARY KEY,
                    CASE_ID VARCHAR(64),
                    STATUS VARCHAR(32),
                    TOTAL_COST DECIMAL(15,2),
                    COMMITMENT_RISK DECIMAL(15,2),
                    SLA_IMPACT VARCHAR(128),
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "COMMITMENT": """
                CREATE COLUMN TABLE COMMITMENT (
                    COMMITMENT_ID VARCHAR(64) PRIMARY KEY,
                    CASE_ID VARCHAR(64),
                    PLAN_ID VARCHAR(64),
                    COMMITMENT_TYPE VARCHAR(64),
                    REFERENCE_ID VARCHAR(64),
                    STATUS VARCHAR(32),
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "APPROVAL_EVENT": """
                CREATE COLUMN TABLE APPROVAL_EVENT (
                    APPROVAL_ID VARCHAR(64) PRIMARY KEY,
                    CASE_ID VARCHAR(64),
                    PLAN_ID VARCHAR(64),
                    APPROVER_ID VARCHAR(64),
                    DECISION VARCHAR(32),
                    COMMENTS NCLOB,
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "COMPENSATION_EVENT": """
                CREATE COLUMN TABLE COMPENSATION_EVENT (
                    COMPENSATION_ID VARCHAR(64) PRIMARY KEY,
                    CASE_ID VARCHAR(64),
                    PREVIOUS_PLAN_ID VARCHAR(64),
                    REASON NCLOB,
                    ACTIONS_RELEASED NCLOB,
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
        }

        for table_name, ddl in tables.items():
            try:
                # Check if table exists in HANA sys tables
                cursor.execute(f"SELECT COUNT(*) FROM SYS.TABLES WHERE SCHEMA_NAME = '{self.schema}' AND TABLE_NAME = '{table_name}'")
                exists = cursor.fetchone()[0] > 0
                if not exists:
                    cursor.execute(ddl)
                    conn.commit()
            except Exception as e:
                # Ignore table already exists errors
                pass

        cursor.close()
        conn.close()

    # --- RECOVERY CASE CRUD ---
    def create_recovery_case(self, case_id: str, disruption_id: str, supplier_id: str, material_id: str, shortage_qty: int, status: str = "PROPOSED") -> Dict[str, Any]:
        if not self.is_configured:
            return {"case_id": case_id, "status": status}
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO RECOVERY_CASE (CASE_ID, DISRUPTION_ID, STATUS, SUPPLIER_ID, MATERIAL_ID, SHORTAGE_QTY) VALUES (?, ?, ?, ?, ?, ?)",
            (case_id, disruption_id, status, supplier_id, material_id, shortage_qty)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return self.get_recovery_case(case_id)

    def get_recovery_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        if not self.is_configured:
            return None
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT CASE_ID, DISRUPTION_ID, STATUS, SUPPLIER_ID, MATERIAL_ID, SHORTAGE_QTY, CREATED_AT, UPDATED_AT FROM RECOVERY_CASE WHERE CASE_ID = ?", (case_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return {
                "case_id": row[0],
                "disruption_id": row[1],
                "status": row[2],
                "supplier_id": row[3],
                "material_id": row[4],
                "shortage_qty": row[5],
                "created_at": str(row[6]),
                "updated_at": str(row[7])
            }
        return None

    def update_recovery_case_status(self, case_id: str, status: str):
        if not self.is_configured:
            return
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE RECOVERY_CASE SET STATUS = ?, UPDATED_AT = CURRENT_TIMESTAMP WHERE CASE_ID = ?", (status, case_id))
        conn.commit()
        cursor.close()
        conn.close()

    # --- DISRUPTION EVENT ---
    def create_disruption_event(self, event_id: str, case_id: str, event_type: str, supplier_id: str, material_id: str, confidence: float, details: str):
        if not self.is_configured:
            return
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO DISRUPT_EVENT (EVENT_ID, CASE_ID, EVENT_TYPE, SUPPLIER_ID, MATERIAL_ID, CONFIDENCE, DETAILS) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (event_id, case_id, event_type, supplier_id, material_id, confidence, details)
        )
        conn.commit()
        cursor.close()
        conn.close()

    # --- AGENT DECISION ---
    def save_agent_decision(self, decision_id: str, case_id: str, agent_name: str, action_type: str, target_id: str, quantity: int, estimated_cost: float, confidence: float, rationale: str):
        if not self.is_configured:
            return
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO AGENT_DECISION (DECISION_ID, CASE_ID, AGENT_NAME, ACTION_TYPE, TARGET_ID, QUANTITY, ESTIMATED_COST, CONFIDENCE, RATIONALE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (decision_id, case_id, agent_name, action_type, target_id, quantity, estimated_cost, confidence, rationale)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_agent_decisions(self, case_id: str) -> List[Dict[str, Any]]:
        if not self.is_configured:
            return []
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DECISION_ID, AGENT_NAME, ACTION_TYPE, TARGET_ID, QUANTITY, ESTIMATED_COST, CONFIDENCE, RATIONALE FROM AGENT_DECISION WHERE CASE_ID = ?", (case_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [{
            "decision_id": r[0], "agent_name": r[1], "action_type": r[2], "target_id": r[3],
            "quantity": r[4], "estimated_cost": float(r[5]), "confidence": float(r[6]), "rationale": r[7]
        } for r in rows]

    # --- RECOVERY PLAN ---
    def save_recovery_plan(self, plan_id: str, case_id: str, status: str, total_cost: float, commitment_risk: float, sla_impact: str):
        if not self.is_configured:
            return
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO RECOVERY_PLAN (PLAN_ID, CASE_ID, STATUS, TOTAL_COST, COMMITMENT_RISK, SLA_IMPACT) VALUES (?, ?, ?, ?, ?, ?)",
            (plan_id, case_id, status, total_cost, commitment_risk, sla_impact)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_recovery_plan(self, plan_id: str) -> Optional[Dict[str, Any]]:
        if not self.is_configured:
            return None
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT PLAN_ID, CASE_ID, STATUS, TOTAL_COST, COMMITMENT_RISK, SLA_IMPACT, CREATED_AT, UPDATED_AT FROM RECOVERY_PLAN WHERE PLAN_ID = ?", (plan_id,))
        r = cursor.fetchone()
        cursor.close()
        conn.close()
        if r:
            return {
                "plan_id": r[0], "case_id": r[1], "status": r[2], "total_cost": float(r[3]),
                "commitment_risk": float(r[4]), "sla_impact": r[5], "created_at": str(r[6]), "updated_at": str(r[7])
            }
        return None

    def update_recovery_plan_status(self, plan_id: str, status: str):
        if not self.is_configured:
            return
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE RECOVERY_PLAN SET STATUS = ?, UPDATED_AT = CURRENT_TIMESTAMP WHERE PLAN_ID = ?", (status, plan_id))
        conn.commit()
        cursor.close()
        conn.close()

    # --- COMMITMENT ---
    def create_commitment(self, commitment_id: str, case_id: str, plan_id: str, commitment_type: str, reference_id: str, status: str):
        if not self.is_configured:
            return
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO COMMITMENT (COMMITMENT_ID, CASE_ID, PLAN_ID, COMMITMENT_TYPE, REFERENCE_ID, STATUS) VALUES (?, ?, ?, ?, ?, ?)",
            (commitment_id, case_id, plan_id, commitment_type, reference_id, status)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_commitments(self, case_id: str) -> List[Dict[str, Any]]:
        if not self.is_configured:
            return []
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COMMITMENT_ID, PLAN_ID, COMMITMENT_TYPE, REFERENCE_ID, STATUS FROM COMMITMENT WHERE CASE_ID = ?", (case_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [{
            "commitment_id": r[0], "plan_id": r[1], "commitment_type": r[2], "reference_id": r[3], "status": r[4]
        } for r in rows]

    # --- APPROVAL EVENT ---
    def record_approval_event(self, approval_id: str, case_id: str, plan_id: str, approver_id: str, decision: str, comments: str):
        if not self.is_configured:
            return
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO APPROVAL_EVENT (APPROVAL_ID, CASE_ID, PLAN_ID, APPROVER_ID, DECISION, COMMENTS) VALUES (?, ?, ?, ?, ?, ?)",
            (approval_id, case_id, plan_id, approver_id, decision, comments)
        )
        conn.commit()
        cursor.close()
        conn.close()

    # --- COMPENSATION EVENT ---
    def record_compensation_event(self, compensation_id: str, case_id: str, previous_plan_id: str, reason: str, actions_released: str):
        if not self.is_configured:
            return
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO COMPENSATION_EVENT (COMPENSATION_ID, CASE_ID, PREVIOUS_PLAN_ID, REASON, ACTIONS_RELEASED) VALUES (?, ?, ?, ?, ?)",
            (compensation_id, case_id, previous_plan_id, reason, actions_released)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_compensation_events(self, case_id: str) -> List[Dict[str, Any]]:
        if not self.is_configured:
            return []
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COMPENSATION_ID, PREVIOUS_PLAN_ID, REASON, ACTIONS_RELEASED, CREATED_AT FROM COMPENSATION_EVENT WHERE CASE_ID = ?", (case_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [{
            "compensation_id": r[0], "previous_plan_id": r[1], "reason": r[2], "actions_released": r[3], "created_at": str(r[4])
        } for r in rows]
