# Non-Functional Requirements (NFR) Specification
## Domain & SSL Certificate Expiry Alert System
**Problem Statement #47 | Developer Tools & IT Operations**  
**Course:** Software Engineering Lab (UE22CS351A) | PES University — Department of CSE  
**Project Category:** Individual Project Submission — Folder 1 (RE)  

---

## 1. Overview of Non-Functional Requirements

Non-Functional Requirements (NFRs) specify the operational criteria, performance targets, quality attributes, and security constraints under which the **Domain & SSL Certificate Expiry Alert System** must function. In strict accordance with the lab problem statement guidelines, two core NFRs (**NFR-001** and **NFR-002**) are defined with quantitative metrics and verifiable acceptance criteria.

---

## 2. Requirements Table

| Requirement ID | Type / Category | Priority | Description | Acceptance Criteria | Rationale |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **NFR-001** | Performance & Scalability | **High** | The monitoring engine shall scan an inventory of at least 1,000 domains and SSL/TLS endpoints concurrently in under 3 minutes (≤ 180 seconds) without exceeding 2 GB of memory allocation or 50% CPU load on a standard 4-core worker node. | **Pass:** Automated benchmark with 1,000 live mock/simulated endpoints completes in ≤ 180 seconds with concurrency pool, achieving 99.9% scan completion rate under normal network conditions.<br>**Fail:** Audit pipeline exceeds 180 seconds, worker experiences thread exhaustion, or memory consumption exceeds 2 GB limit. | Guarantees that daily batch audits complete within narrow operational maintenance windows without degrading server resources or delaying critical alerts. |
| **NFR-002** | Security & High Availability | **High** | The system shall protect all stored webhook secrets, notification credentials, and API tokens using AES-256-GCM encryption at rest, enforce Role-Based Access Control (RBAC) via OAuth2/OIDC with TLS 1.3 in transit, and maintain 99.95% system uptime for the alerting and monitoring background service. | **Pass:** Automated vulnerability and penetration tests confirm secrets cannot be retrieved in plaintext from the database; unauthenticated API calls return HTTP 401/403; alert dispatch service uptime exceeds 99.95% per month (max allowable downtime ≤ 21.6 minutes).<br>**Fail:** Plaintext storage of API keys/secrets discovered; privilege escalation allows unauthorized users to modify escalation policies. | Protects enterprise infrastructure credentials from unauthorized leakage and guarantees reliable, continuous alerting during mission-critical operational incidents. |

---

## 3. In-Depth Operational Specifications & Verification Strategies

### 3.1 NFR-001: Performance & Scalability

#### 3.1.1 Quantitative Metrics & Benchmarks
- **Target Inventory Size:** $\ge 1,000$ active domain & SSL endpoints.
- **Maximum Execution Duration:** $\le 180$ seconds (3 minutes) for a complete daily batch run.
- **Average Scan Latency per Endpoint:** $\le 150\text{ ms}$ over asynchronous non-blocking sockets.
- **Memory Ceiling:** $\le 2\text{ GB}$ RSS memory total across all worker processes.
- **CPU Ceiling:** $\le 50\%$ cumulative CPU utilization on a standard 4-core worker instance.
- **Completion Rate:** $\ge 99.9\%$ of endpoints successfully audited or categorized into retry queues.

#### 3.1.2 Architectural Realization
- **Asynchronous Event Loop:** Utilizes Python `asyncio` / epoll I/O multiplexing to handle up to 200 concurrent socket connections without blocking worker threads.
- **Worker Concurrency Pool:** Employs 4 worker processes partitioned with 50 concurrent connection slots each, yielding 200 simultaneous probes.
- **Non-blocking WHOIS Throttling:** Enforces domain-registry token-bucket rate limiters so queries do not trigger HTTP 429 penalties.

#### 3.1.3 Verification & Testing Method
- **Test ID:** `TC-PERF-001`
- **Tooling:** Locust / JMeter combined with mock TLS/WHOIS responders.
- **Execution Procedure:**
  1. Populate database with 1,000 mock domain records mapped to high-speed test servers.
  2. Trigger scheduled audit job and capture timestamps `T_start` and `T_end`.
  3. Monitor CPU, resident set size (RSS) memory, and network throughput at 1-second intervals using Prometheus / OS metrics.
  4. Verify:
     $$\text{Total Duration} = T_{\text{end}} - T_{\text{start}} \le 180\text{ seconds}$$
     $$\text{Peak Memory} \le 2048\text{ MB}$$
     $$\text{Peak CPU} \le 50\%$$

---

### 3.2 NFR-002: Security & High Availability

#### 3.2.1 Quantitative Metrics & Constraints
- **Encryption Standard:** AES-256-GCM (Galois/Counter Mode) with authenticated encryption and unique IVs for all stored third-party credentials.
- **Transit Encryption:** TLS 1.3 mandatory for all API endpoints, disabling deprecated ciphers (SSLv3, TLS 1.0, TLS 1.1).
- **Authentication:** OAuth2 with PKCE / JWT signed with RS256; token lifetime $\le 60\text{ minutes}$.
- **Service Availability Target:** $99.95\%$ uptime per calendar month.
  - Maximum Allowable Monthly Downtime:
    $$\text{Downtime}_{\text{max}} = 30 \times 24 \times 60 \times (1 - 0.9995) = 21.6\text{ minutes/month}$$

#### 3.2.2 Architectural Realization
- **Secrets Management:** Envelope encryption pattern where database-stored secrets (Slack tokens, PagerDuty keys, SMTP passwords) are encrypted using a Master Key stored in HashiCorp Vault or environment keyrings.
- **Role-Based Access Control (RBAC):** Strict role boundaries:
  - `ROLE_SYSADMIN`: Domain CRUD, notification settings, manual scans.
  - `ROLE_SECURITY_OFFICER`: Compliance audit exports, viewing cryptographic posture, receiving Tier-3 escalations.
  - `ROLE_VIEWER`: Read-only access to dashboard statistics.
- **High Availability (HA) Failover:** Distributed leader election via Redis Redlock locks. The primary scheduler holds a heartbeating lease; if the primary fails, the standby instance acquires the lock within 5 seconds and resumes task scheduling without duplicate dispatch.

#### 3.2.3 Verification & Testing Method
- **Test IDs:** `TC-SEC-001`, `TC-HA-001`
- **Execution Procedure (Security):**
  1. Inspect raw PostgreSQL database dumps to confirm all credentials and tokens are ciphertext (`AES-256-GCM`).
  2. Attempt API calls with forged, expired, or missing JWT tokens $\rightarrow$ verify HTTP 401 Unauthorized.
  3. Attempt administrative updates using `ROLE_VIEWER` credentials $\rightarrow$ verify HTTP 403 Forbidden.
- **Execution Procedure (Availability):**
  1. Run simulated crash-stop tests by terminating the primary scheduler container under load.
  2. Measure failover transition latency to secondary replica ($\le 5\text{ seconds}$).
  3. Validate continuous uptime tracking over 30 days via synthetic monitoring probes.
