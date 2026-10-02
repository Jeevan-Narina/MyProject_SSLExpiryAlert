# Domain & SSL Certificate Expiry Alert System
**Assigned Topic:** Problem Statement #47 | Developer Tools & IT Operations  

---

## 1. Project Overview & Objective

The **Domain & SSL Certificate Expiry Alert System** is an automated IT operations utility developed to eliminate critical service outages caused by lapsed domain registrations and expired X.509 SSL/TLS certificates. The system conducts automated daily audits via non-blocking TLS handshakes and WHOIS/RDAP queries, continuously computing remaining validity lifetimes and routing alerts across a structured **multi-tier escalation ladder** (Tier 1: SysAdmin, Tier 2: SysAdmin Lead, Tier 3: Security Officer).

### Key Highlights
- **High-Performance Scanning:** Audits an inventory of 1,000+ domains and endpoints in under 3 minutes using asynchronous worker pools (**NFR-001**).
- **Multi-Tier Escalation Ladder:** Automated notification progression across SMTP Email, Slack, Teams Webhooks, and PagerDuty (**FR-003**).
- **Enterprise Security:** AES-256-GCM encryption of stored credentials, OAuth2/OIDC RBAC access control, and 99.95% system availability (**NFR-002**).

---

## 2. Individual Project Repository Directory Structure

As specified in the lab submission guidelines, the repository is structured into dedicated modular folders for each milestone:

```text
.
├── 1-RE/                                # Folder 1: Requirements Engineering (Completed)
│   ├── README.md                        # Master Requirements Specification, RTM & Core Use Case Flow
│   ├── functional_requirements.md       # Dedicated 5 Functional Requirements (FR-001 to FR-005)
│   ├── non_functional_requirements.md   # Dedicated 2 Non-Functional Requirements (NFR-001 & NFR-002)
│   └── use_case_diagram.drawio          # Standalone UML Use-Case Diagram (Draw.io XML)
│
├── 2-Architectural-Diagram/             # Folder 2: Architectural Specification (Completed)
│   ├── README.md                        # Multi-Tier Microservice & Worker Architecture Specification
│   ├── system_architecture.drawio       # High-Level System Architecture Diagram (Draw.io XML)
│   └── data_flow_architecture.drawio    # End-to-End Audit & Escalation Data Flow Pipeline (Draw.io XML)
│
├── 3-Project-Creational-Screenshots/    # Folder 3: Project Creational Screen Shots in GitHub & Jira Tool
│   └── README.md                        # (Pending Lab 3 Phase)
│
├── 4-SRS-and-WBS/                       # Folder 4: SRS and Work Breakdown Steps (WBS)
│   └── README.md                        # (Pending Lab 4 Phase)
│
├── 5-GitHub-Copilot-Code/               # Folder 5: GitHub Copilot Generated Code & Repository Link
│   └── README.md                        # (Pending Lab 5 Phase)
│
├── 6-Software-Testing-Vibe-Coding/      # Folder 6: Software Testing Tools & Bug Fixes
│   └── README.md                        # (Pending Lab 6 Phase)
│
├── 47_SE_Lab1_SE_Problem_Statements.pdf # Official Lab Problem Statement Reference
├── Git Hub Project Submission Details.docx # Official Submission Guidelines
└── README.md                            # Main Project Master Index (This File)
```

---

## 3. Completed Milestones

### Milestone 1: Requirements Engineering (RE)
**Location:** [`1-RE/`](./1-RE/) | [Detailed Master Specification](./1-RE/README.md)
- **Functional Requirements Document:** [`functional_requirements.md`](./1-RE/functional_requirements.md) — Exactly 5 fully specified FRs (**FR-001** through **FR-005**) with ID, Type, Description, Priority, Pass/Fail Acceptance Criteria, and Rationale.
- **Non-Functional Requirements Document:** [`non_functional_requirements.md`](./1-RE/non_functional_requirements.md) — Dedicated **NFR-001** (Performance: 1,000 domains in < 3 min) and **NFR-002** (Security & HA: AES-256, RBAC, 99.95% uptime) with benchmark metrics and verification methods.
- **Requirements Traceability Matrix (RTM Table):** Full bidirectional matrix linking requirements to architecture modules, use cases, and verification test case IDs.
- **UML Use-Case Modeling:**
  - Stakeholders & Actors: SysAdmin (Primary), Security Officer (Secondary), Audit Scheduler Daemon, External Endpoints & Registries, External Notification Gateways.
  - Stereotypes: Explicitly includes `«include»` (UC-04 includes UC-07; UC-01/02/05/08 include UC-09) and `«extend»` (UC-05 extends UC-03; UC-06 extends UC-04).
  - Editable Draw.io diagram: [`use_case_diagram.drawio`](./1-RE/use_case_diagram.drawio).
- **Formal Use-Case Flow Specification:** Complete 1-page standard specification for core use case `UC-03 / UC-04` detailing Preconditions, Postconditions, Main Success Scenario, and Alternate Flows (TLS Timeout, WHOIS Rate Limiting, Unacknowledged Escalation).

### Milestone 2: Architectural Diagram & System Design
**Location:** [`2-Architectural-Diagram/`](./2-Architectural-Diagram/) | [Detailed Architecture Document](./2-Architectural-Diagram/README.md)
- **High-Level Tiered Architecture:**
  1. Presentation & Client Tier (React / Vite Web Dashboard & CLI)
  2. API Gateway & Security Tier (FastAPI, OAuth2 / JWT RBAC, Rate Limiter)
  3. Core Orchestration Engine (Cron Scheduler Daemon, Task Dispatcher, Escalation Rule Engine)
  4. Task Broker & Asynchronous Queue Tier (Redis / Celery, Dead Letter Queue)
  5. Asynchronous Worker Pool (TLS Handshake Worker, WHOIS/RDAP Worker, DNS Resolver)
  6. Persistence, State & Secrets Tier (PostgreSQL, AES-256 Vault, Compliance Ledger)
  7. Multi-Tier Escalation Notification Subsystem (Tier 1: SysAdmin, Tier 2: Lead, Tier 3: Security Officer)
  8. External Target Infrastructure (Public Endpoints, ICANN Registrars, Notification APIs)
- **Editable Draw.io Diagrams:**
  - System Subsystems & Components: [`system_architecture.drawio`](./2-Architectural-Diagram/system_architecture.drawio)
  - End-to-End Data Flow & Lifecycle: [`data_flow_architecture.drawio`](./2-Architectural-Diagram/data_flow_architecture.drawio)
- **Design Patterns Applied:** Producer-Consumer, Strategy Pattern (Notification Channels), State Pattern (Escalation Lifecycle), Circuit Breaker & DLQ.

---

## 4. Upcoming Individual Submission Milestones

| Folder # | Deliverable | Description | Status |
| :---: | :--- | :--- | :---: |
| **Folder 1** | **RE (FR, NFR, RTM Table, Use-Case)** | Requirements engineering, traceability matrix, and UML diagram | **Completed** |
| **Folder 2** | **Architectural Diagram** | System architecture, component models, and data flow pipelines | **Completed** |
| **Folder 3** | **Project Creational Screen Shots** | GitHub repository setup, branch protection, and Jira Kanban/Scrum board setup | Planned |
| **Folder 4** | **SRS and Work Breakdown Steps** | Complete Software Requirements Specification (IEEE 830) and Work Breakdown Structure (WBS) | Planned |
| **Folder 5** | **GitHub Copilot Generated Code** | Copilot prompt logs, generated implementation scripts, and repository code links | Planned |
| **Folder 6** | **Software Testing Tools & Vibe Coding**| Testing suite execution, bug fixes via vibe coding, patches, and retest evidence | Planned |
