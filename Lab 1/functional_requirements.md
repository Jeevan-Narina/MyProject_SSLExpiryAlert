# Functional Requirements (FR) Specification
## Domain & SSL Certificate Expiry Alert System
**Problem Statement #47 | Developer Tools & IT Operations**  
**Course:** Software Engineering Lab (UE22CS351A) | PES University — Department of CSE  
**Project Category:** Individual Project Submission — Folder 1 (RE)  

---

## 1. Overview of Functional Requirements

The following section details the **5 Functional Requirements (FR-001 to FR-005)** for the **Domain & SSL Certificate Expiry Alert System**. Each requirement is strictly formulated with an **Identifier**, **Target Module**, **Description**, **Priority**, **Pass/Fail Acceptance Criteria**, and operational **Rationale** conforming to PES University CSE Software Engineering Lab standards.

---

## 2. Requirements Table

| Requirement ID | Module / Functional Area | Priority | Description | Acceptance Criteria | Rationale |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **FR-001** | TLS Handshake & Certificate Audit Engine | **High** | The system shall initiate automated TLS handshakes against all registered domain endpoints daily, extract the X.509 certificate validity period (`NotAfter` timestamp), issuer CA, subject alternative names (SANs), and certificate trust chain, and calculate remaining days to expiration. | **Pass:** Valid TLS endpoint returns accurate expiration date within ±1 hour; system successfully records remaining validity days and queues alerts at 30, 15, 7, and 3-day milestones.<br>**Fail:** Certificate expiration is ignored, invalid handshake results are logged as valid, or expired certificate produces no alert queue item. | Ensures continuous visibility into certificate health and prevents unexpected SSL/TLS downtime or browser warning lockouts. |
| **FR-002** | WHOIS / RDAP Registration Audit Engine | **High** | The system shall perform scheduled WHOIS queries and RDAP (Registration Data Access Protocol) lookups for all monitored apex domains daily, parsing domain registrar identity, registration creation date, renewal status, and domain expiration timestamps. | **Pass:** Expiration date parsed accurately from registry responses; renewal reminder alerts queued at 60, 30, 14, and 3 days before expiration.<br>**Fail:** Registrar response parsing errors cause expiration date to be recorded as null without error notification, or domain within 14 days of expiry is skipped. | Prevents loss of domain ownership, malicious registrar drop-catching, and enterprise domain hijacking. |
| **FR-003** | Escalation Ladder & Multi-Channel Alert Engine | **High** | The system shall implement a hierarchical escalation ladder alerting engine that dispatches automated notifications across configured channels (Email, Slack, PagerDuty, Webhook) mapped to remaining expiration urgency: Tier 1 (30 days → SysAdmin), Tier 2 (14 days → SysAdmin Team Lead), and Tier 3 (≤ 3 days or unacknowledged Tier 2 alert for >48h → Security Officer & On-call Pager). | **Pass:** Alerts are dispatched to configured channels at each threshold; unacknowledged Tier 1/2 alerts escalate to Tier 3 within specified time window; webhook delivers valid JSON payload.<br>**Fail:** Alert notifications suppressed, sent to incorrect escalation tier, or fail to re-trigger when previous tier remains unacknowledged. | Guarantees operational redundancy and ensures pending expirations receive immediate attention before critical infrastructure failure. |
| **FR-004** | Inventory Management & Asset Ingestion | **Medium** | The system shall provide administrative interfaces for SysAdmins to perform CRUD operations on monitored domains, subdomains, port mappings, and associated notification targets, supporting both single-entry forms and bulk ingestion via CSV and JSON files. | **Pass:** System successfully parses and registers a batch of 500 valid domains via CSV within 5 seconds with validation; rejects malformed domain syntaxes with descriptive error messages.<br>**Fail:** Duplicate domain names inserted without collision warning, or malformed domain syntax crashes the ingestion pipeline. | Centralizes distributed enterprise assets and allows rapid onboarding of vast multi-cloud domain portfolios. |
| **FR-005** | Compliance Dashboard & On-Demand Audit Trigger | **Medium** | The system shall provide an interactive web dashboard displaying real-time certificate health, expiration timelines, root CA issuer metrics, and compliance status, allowing SysAdmins and Security Officers to trigger on-demand audits and export audit reports in CSV and PDF formats. | **Pass:** On-demand audit executes and refreshes endpoint health state within 10 seconds; dashboard updates live metrics; CSV/PDF report download completes with full audit trail.<br>**Fail:** Dashboard displays stale cached data after manual scan trigger, or unauthorized non-admin users can access sensitive audit logs. | Empowers IT teams with instant verification after certificate renewals and provides auditable artifacts for SOC 2 / ISO compliance. |

---

## 3. Detailed Specifications per Functional Requirement

### 3.1 FR-001: TLS Handshake & Certificate Expiry Audit Engine
- **Primary Actor:** Audit Scheduler Daemon / Worker Pool
- **Inputs:** Target Hostname (FQDN), Port (Default 443, configurable), SNI Header, Connect Timeout (default 5000ms).
- **Processing Logic:**
  1. Open TCP socket with SNI matching the target domain.
  2. Perform TLS 1.2 / TLS 1.3 handshake negotiation.
  3. Retrieve peer X.509 certificate and certificate chain.
  4. Parse ASN.1 structure to extract:
     - `NotAfter` validity timestamp.
     - Issuer Common Name (CN) and Organization (O).
     - Subject Alternative Names (SAN) list.
     - Signature algorithm and public key size (e.g., RSA 2048/4096, ECDSA P-256).
  5. Compute `Days_Remaining = floor((NotAfter - Current_UTC_Time) / 86400)`.
  6. Store audit record in PostgreSQL database.
- **Outputs:** Structured Audit Log Record with Certificate Expiration Date, Status (`VALID`, `EXPIRING_SOON`, `EXPIRED`, `UNREACHABLE`), and Latency.
- **Exception Handling:** If socket connection times out or host is unreachable, retry up to 3 times with exponential backoff before logging `CONNECTION_TIMEOUT` and triggering operational warning.

---

### 3.2 FR-002: WHOIS / RDAP Registration Audit Engine
- **Primary Actor:** Audit Scheduler Daemon / Worker Pool
- **Inputs:** Apex Domain Name (e.g., `example.com`), IANA RDAP Bootstrap URL.
- **Processing Logic:**
  1. Query RDAP endpoint via HTTPS GET for domain metadata.
  2. If RDAP service is unavailable, fallback to Port 43 WHOIS query to the authoritative TLD registry.
  3. Extract registrar entity name, registration creation date, last updated date, and registry expiration date.
  4. Compute `Days_To_Domain_Expiry = floor((Registry_Expiry - Current_UTC_Time) / 86400)`.
  5. Compare remaining days against domain reminder milestones: 60, 30, 14, and 3 days.
- **Outputs:** Domain registration status record with expiration timestamp and registrar details.
- **Exception Handling:** Handles HTTP 429 (Rate Limit) by applying token-bucket throttling and scheduling delayed retries.

---

### 3.3 FR-003: Escalation Ladder & Multi-Channel Alert Engine
- **Primary Actor:** Escalation Rule Engine / Notification Gateway
- **Inputs:** Audit Result Payload (`Days_Remaining`, `Asset_ID`, `Endpoint_FQDN`, `Incident_Status`).
- **Processing Logic:**
  1. Evaluate urgency tier:
     - **Tier 1 (Warning):** `Days_Remaining <= 30` $\rightarrow$ Target: SysAdmin.
     - **Tier 2 (Urgent):** `Days_Remaining <= 14` OR (Tier-1 unacknowledged for > 48h) $\rightarrow$ Target: SysAdmin Lead.
     - **Tier 3 (Critical):** `Days_Remaining <= 3` OR (Tier-2 unacknowledged for > 24h) $\rightarrow$ Target: Security Officer.
  2. Retrieve encrypted channel tokens from Vault (Slack Bot Token, PagerDuty Integration Key, SMTP Host).
  3. Decrypt tokens using AES-256-GCM.
  4. Dispatch formatted notification payloads to enabled channels simultaneously.
- **Outputs:** Outbound webhook/API payloads and delivery receipts recorded in the database.
- **Exception Handling:** Undeliverable notification attempts are redirected to Dead Letter Queue (DLQ) with jittered retries.

---

### 3.4 FR-004: Inventory Management & Asset Ingestion
- **Primary Actor:** SysAdmin
- **Inputs:** Single domain registration form OR multi-line CSV/JSON asset catalog.
- **Processing Logic:**
  1. Validate domain syntax against RFC 1035 / RFC 1123 regex standards.
  2. Check for duplicate domain entries in the database.
  3. Sanitize input strings to prevent SQL/Command injection attacks.
  4. Persist domain records with default escalation policy and notification channel associations.
- **Outputs:** Confirmation response with created asset IDs or validation error report detailing invalid lines in batch.
- **Exception Handling:** Invalid domain formats return HTTP 422 Unprocessable Entity with line-specific error descriptions without corrupting valid entries in the batch.

---

### 3.5 FR-005: Compliance Dashboard & On-Demand Audit Trigger
- **Primary Actor:** SysAdmin / Security Officer
- **Inputs:** User request via Web UI / REST API (`GET /api/v1/dashboard/metrics`, `POST /api/v1/audits/scan/{domain_id}`, `GET /api/v1/reports/export?format=pdf`).
- **Processing Logic:**
  1. Authenticate user JWT and verify RBAC permissions.
  2. For on-demand scans: Inject immediate high-priority job into the Redis task broker.
  3. Worker executes immediate TLS/WHOIS probe and returns real-time results within 10 seconds.
  4. Dashboard updates live charts (Expiration Countdown Histogram, CA Issuer Distribution, Expired vs Healthy Ratio).
  5. For report exports: Generate signed CSV or PDF compliance audit ledger containing full chain validation logs.
- **Outputs:** Real-time JSON telemetry, dynamic UI updates, and downloadable PDF/CSV compliance documents.
- **Exception Handling:** Unauthenticated requests rejected with HTTP 401 Unauthorized; insufficient role privileges rejected with HTTP 403 Forbidden.
