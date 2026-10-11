# **SOTN / Train4Life**

# **Recruitment, Intake & Routing Platform**

PRODUCT REQUIREMENTS DOCUMENT  |  Working draft  |  Pre-Hackathon

Status: Live working document. This document separates existing project direction from proposed implementation details and decisions that require a working session with SOTN.

Reading guide: “P0” means needed for a usable pilot, not necessarily required for the hackathon. Proposed workflow rules, endpoints and technical details remain working assumptions until the relevant SOTN decision is made. The conference prototype informs possible functionality but does not lock the look, navigation or screen sequence.

# **1\. Problem**

Special Olympics Tennessee has a large gap between the people currently participating in its programs and the people who could be reached. One barrier is the lack of a centralized system for recruitment, automated intake and participant routing. Interest from prospective athletes, families, coaches, volunteers, schools and community partners is currently handled through manual intake and follow-up processes. Staff must collect information, work out which program or local contact is appropriate, forward the inquiry and keep track of next steps themselves. This takes time, creates repeated handoffs and makes it harder to see which inquiries need attention or whether someone has successfully connected with a program.

The problem is broader than Train4Life. Train4Life is an important initial use case, but the intended product should also help people find their way into other SOTN programs. The project should not recreate scheduling, session attendance, medical screenings or other operational functionality already being developed elsewhere.

## **Current workflow gaps**

| Topic | Details |
| :---- | :---- |
| **Participation gap** | **What we currently know:** There is a large gap between current participation and the number of people SOTN could potentially reach. **Confidence / follow-up:** Identify which populations, communities and areas are least effectively reached. |
| **No automated intake system** | **What we currently know:** SOTN does not currently have a centralized system that automatically captures, organizes and routes incoming interest. **Confidence / follow-up:** Map the current intake paths and determine which can share a common workflow. |
| **Manual processing and follow-up** | **What we currently know:** Staff coordinate information collection, program matching, referrals and next steps manually. **Confidence / follow-up:** Walk through representative inquiries to identify delays, repeated work and missing handoffs. |
| **Fragmented workflows** | **What we currently know:** Information may pass through separate spreadsheets, messages, contacts and program systems rather than one trackable intake pipeline. **Confidence / follow-up:** Confirm the current tools used across programs and who maintains each record. |
| **System boundaries** | **What we currently know:** This product is intended to address recruitment and routing, while operational program systems may continue managing participation after handoff. **Confidence / follow-up:** Confirm which system owns each step and what information needs to be transferred. |

SOTN does not currently have a centralized automated process for capturing, organizing and routing prospective participants and partners. Staff rely on manual collection, processing and follow-up, making it difficult to see which inquiries need attention and whether a referral reached the right destination. The exact volume of delayed or lost inquiries is not yet measured; the pilot should establish that baseline.

# **2\. Context and product decision**

The initial Train4Life discussions included registration, locations, coaches, attendance, assessments, communications and roster administration. The current product direction focuses instead on a shared recruitment and intake layer that can serve Train4Life as well as other Special Olympics Tennessee programs. Operational features should not be assumed to belong to this platform, particularly when another system already handles them or is planned to do so.

The product consists of two linked surfaces: a public intake experience and a staff dashboard. The public side helps an interested person or referrer identify opportunities and submit the right information. The staff side records the inquiry, makes ownership visible and moves each person to a qualified next step. It should be possible to integrate with COE, SEO NOW and other registration systems later, without requiring those integrations to ship the first usable release.

# **3\. Goal, non-goals and product principles**

Goal: Give SOTN a single, accessible entry point and a trackable workflow from initial interest to appropriate program or staff contact, reducing lost referrals and repeated manual handoffs.

* A prospective participant should know what happens after submitting an inquiry.  
* Staff should see new inquiries, determine their status and identify who owns the next action.  
* Routing should be understandable and correctable by staff, not a black-box eligibility decision.  
* The platform should collect only the information needed at the current step and avoid duplicating sensitive records kept in operational systems.  
* Program-specific workflows should be configurable where feasible rather than hard-coded for Train4Life alone.

Non-goals for the first release: full Train4Life session management, athlete health assessments, attendance, sports rosters, coach credential verification, W-9 collection, donor transactions, replacing COE, and real-time data synchronization with external systems. These can be revisited with explicit ownership and priority decisions.

# **4\. Users and jobs to be done**

| Topic | Details |
| :---- | :---- |
| **Prospective athlete** | **Job to be done:** Understand what programs fit; express interest without navigating multiple websites. **Needs / important exceptions:** Plain-language questions, clear explanation of programs, accessible experience, assisted entry when needed. |
| **Parent / guardian / caregiver** | **Job to be done:** Refer or help someone enroll and learn the next step. **Needs / important exceptions:** Distinguish submitter from participant, relationship and contact preference; age and consent rules must be decided. |
| **Coach or volunteer** | **Job to be done:** Identify relevant opportunities and begin required onboarding. **Needs / important exceptions:** Role/location availability, guidance on next steps; screening/credential systems remain external until clarified. |
| **School / teacher / clinician / organization** | **Job to be done:** Refer an individual or ask about a group partnership. **Needs / important exceptions:** Referral source attribution, organizational details, permission to share contact information, handoff visibility. |
| **Venue / facility / community partner** | **Job to be done:** Offer space or partnership and reach the right staff. **Needs / important exceptions:** Type of facility, region, capacity/interests, contact ownership. |
| **Prospective donor** | **Job to be done:** Signal interest in supporting a program. **Needs / important exceptions:** Collect intent and connect to fundraising contacts; do not process donations in MVP. |
| **Area coordinator / director** | **Job to be done:** Review local inquiries and follow up. **Needs / important exceptions:** Assigned queue, filters, history, reminders, correct contact details. |
| **SOTN admin / program lead** | **Job to be done:** Monitor the statewide pipeline and fix stalled handoffs. **Needs / important exceptions:** Cross-region visibility, program settings, reports, access controls and audit history. |

# **5\. Proposed end-to-end experience**

1. A person opens the site through an SOTN link, local campaign, community referral or staff-assisted intake. They select why they are here: participate, refer someone, volunteer/coach, partner or support SOTN.  
2. The intake asks only the relevant questions. At minimum it records the submitter, intended participant or organization where applicable, general interest, location and a reliable contact method. The form explains why information is requested.  
3. The platform proposes a destination using role, interests, program availability and geography. Where information is missing or ambiguous it assigns “needs review” rather than asserting eligibility.  
4. The submitter sees a confirmation and practical next steps. The case receives a unique ID, initial status and responsible queue.  
5. Staff reviews the record, can correct the proposed destination, assign an owner, add notes and record contact attempts.  
6. Once the receiving person or program accepts the handoff, staff marks it routed or connected. Where possible, the ultimate outcome (registered, declined, no response, not eligible) is recorded to close the loop.

## **Important alternative paths**

* A guardian submits an inquiry for an athlete but prefers to be the primary contact.  
* A person has overlapping interests, such as athlete participation and coaching: retain one contact with multiple interests or linked inquiries rather than silently overwriting data.  
* No program is currently available nearby: route to a review queue and communicate that an opening has not been promised.  
* The record already exists: warn staff of a likely duplicate without automatically merging sensitive records.  
* An external registration system cannot receive data: preserve the intake, expose a manual referral path and retry any authorized transfer safely.  
* An applicant requests correction or deletion of data: follow a documented privacy workflow rather than deleting records ad hoc.

# **6\. Detailed product requirements**

Priority definitions: P0 \= necessary for an initial pilot; P1 \= important after the core workflow is reliable; P2 \= later expansion. Priorities are recommendations, not signed-off scope.

## **INT-01  Role-specific entry  \[P0\]**

Present clear starting options for athlete/family, coach/volunteer, referral partner, organization/venue and donor.

Acceptance: User selects one path and sees a relevant form; no forced account creation to express initial interest.

Decision still needed: Which groups will participate in the first pilot?

## **INT-02  Structured forms  \[P0\]**

Capture contact, location, interest, submitter relationship and required program-specific fields. Validate required entries; avoid collecting full medical histories.

Acceptance: Valid record created once; errors are field-specific; a user can review and submit; accessible errors announced to assistive tech.

Decision still needed: Approved field list and consent copy per group.

## **INT-03  Submission acknowledgment  \[P0\]**

Show a confirmation reference, expected next step and contact channel; send email confirmation when consent/contact details permit.

Acceptance: Submission never ends at an unexplained blank page; confirmation does not incorrectly promise acceptance.

Decision still needed: SOTN service-level promise and official contact details.

## **ROU-01  Basic routing  \[P0\]**

Use role/program interest plus region or area to propose a queue or contact. Keep routing rule and reason visible.

Acceptance: Sample cases go to expected queue; unmatched submissions reach triage rather than being discarded.

Decision still needed: Program-to-area map and authoritative owner directory.

## **ROU-02  Manual override  \[P0\]**

Allow authorized staff to reassign an inquiry and record why.

Acceptance: Original assignment, new assignment, timestamp and operator are logged.

Decision still needed: Who may assign across regions?

## **ADM-01  Central triage queue  \[P0\]**

List unassigned and assigned inquiries with submitted date, type, location, owner and status.

Acceptance: Staff can filter by area/type/status and open a record; pending entries are not hidden by default.

Decision still needed: Staff roles and regional permissions.

## **ADM-02  Case detail and history  \[P0\]**

Show submitted information, source, timeline, notes and next task in one record.

Acceptance: Status and owner persist; private notes cannot be seen on the public site; edit history exists.

Decision still needed: Which notes count as sensitive?

## **ADM-03  Status model  \[P0\]**

Track new, needs review, assigned, contacted, referred, closed and optional program-enrolled outcome.

Acceptance: Allowed transitions documented; close reason required for terminal states; reopen supported.

Decision still needed: Vocabulary and definition of a successful referral.

## **ADM-04  Authentication and roles  \[P0\]**

Require staff sign-in, scoped permissions and no public access to applicant records.

Acceptance: Unauthenticated API requests rejected; area staff cannot see unauthorized records; changes are auditable.

Decision still needed: Identity provider and role matrix.

## **DAT-01  Data foundation  \[P0\]**

Maintain contacts, inquiries, interests, programs, locations/areas, assignments, activity events and consent records as separate related entities.

Acceptance: Records have stable IDs, timestamps and validated references; migrations and backups tested.

Decision still needed: Retention and source-of-truth decisions.

## **RES-01  Guided resources  \[P1\]**

Provide role-appropriate information and next-step links after intake.

Acceptance: Staff can update resource destinations without a developer deployment, if feasible.

Decision still needed: Who owns content and accessibility review?

## **COM-01  Staff follow-up reminders  \[P1\]**

Create due-date reminders for cases awaiting action and optionally email staff digests.

Acceptance: Only appropriate staff receive notices; reminder frequency can be tuned; failed deliveries visible.

Decision still needed: SLA, channels and opt-out rules.

## **COM-02  Contact activity  \[P1\]**

Log calls, email attempts and outreach outcome manually, without storing unnecessary content.

Acceptance: Time, channel, outcome and staff member recorded; contact consent respected.

Decision still needed: Is direct email/SMS sending necessary or is tracking enough?

## **ROU-03  Geographic program matching  \[P1\]**

Recommend available programs/area contacts based on county/ZIP and relevant role.

Acceptance: Unsupported area codes fall back to review; staff can explain and correct match.

Decision still needed: Source and update owner for availability/geographic boundaries.

## **REP-01  Pipeline reporting  \[P1\]**

Show submissions, contact rate, routing completion and aging by source, user type, program and region.

Acceptance: Aggregations follow agreed event definitions; filters do not expose personal data unnecessarily.

Decision still needed: Baseline, reporting cadence and comparison cohorts.

## **INTG-01  Documented integration contract  \[P1\]**

Define versioned API/export formats for authorized receiving systems, without assuming production interoperability.

Acceptance: Data mapping, authentication, failure behavior and sample payloads are documented; no unapproved transfer.

Decision still needed: SEO NOW and COE mapping and approvals.

## **EXT-01  External system sync  \[P2\]**

Send or reconcile records with downstream program systems when integration ownership is agreed.

Acceptance: Retries, duplicate prevention, reconciliation and ownership conflicts tested.

Decision still needed: Receiving APIs, authoritative IDs and agreements.

## **EXP-01  Expanded workflows  \[P2\]**

Consider facility applications, group referrals, advanced donor interest journeys and program-specific qualification paths.

Acceptance: New workflows reuse intake primitives instead of creating unrelated databases.

Decision still needed: Validated demand and staffing capacity.

# **7\. Data model and API implications**

Routes should follow the approved workflow and authorization rules, not determine product scope by themselves. The following is an engineering starting point, not a final API contract. Proposed core tables: person/contact; inquiry; inquiry\_role/interest; organization; program; location/area; routing\_rule; assignment; activity\_event; communication\_preference/consent; resource; integration\_delivery. A submitter and an athlete/participant should be separate entities where the person completing the form is not the subject of the inquiry.

| Topic | Details |
| :---- | :---- |
| **Public intake** | **Candidate operations:** POST /intakes; GET /programs; GET /resources **Notes:** Validate input and rate limit; confirmation returns reference, not sensitive details. |
| **Staff inquiry queue** | **Candidate operations:** GET /admin/intakes; GET /admin/intakes/{id} **Notes:** Pagination/filtering, per-record authorization and audit logging. |
| **Assignment and status** | **Candidate operations:** PATCH /admin/intakes/{id}/assignment; PATCH /admin/intakes/{id}/status **Notes:** Prefer defined transitions and event history to arbitrary overwrites. |
| **Activities** | **Candidate operations:** POST /admin/intakes/{id}/activities **Notes:** Capture follow-up outcome; restrict visibility. |
| **Program directory** | **Candidate operations:** GET /admin/programs; PATCH /admin/programs/{id} **Notes:** Editable only by authorized staff; may be deferred if data imported initially. |
| **Reporting** | **Candidate operations:** GET /admin/reports/pipeline **Notes:** Aggregate counts and aging, with privacy limits. |
| **Integration** | **Candidate operations:** POST /integrations/{target}/deliveries or scheduled export **Notes:** Only after receiver contracts and legal authority are confirmed. |

Suggested stack from the engineering team overview: Next.js/React for public and admin interfaces; FastAPI/Python for authenticated endpoints and routing services; PostgreSQL for relational records; object storage for approved resources. Background jobs may support reminders and delivery retries. The framework selection is a current direction, not evidence that the application architecture or hosting has already been approved.

# **8\. Success metrics and measurement plan**

The primary outcome is a completed handoff to an appropriate program or staff member, not simply a submitted form. The team should capture baseline performance during the pilot before committing to improvement targets. Each metric needs an event definition, a reporting owner and a review cadence.

| Topic | Details |
| :---- | :---- |
| **North-star: connected referral rate** | **Definition / instrument:** Inquiries with documented successful connection to receiving program or coordinator / qualifying submitted inquiries, cohort-based. **Pilot target status:** Baseline first; target proposed after 4–6 weeks of observation. |
| **Time to first staff action** | **Definition / instrument:** Median and 90th percentile hours from submission to first logged meaningful outreach or disposition. **Pilot target status:** Set SLA with SOTN; no invented target. |
| **Routing completion rate** | **Definition / instrument:** Inquiries assigned to a valid owner within agreed window / submitted inquiries eligible for routing. **Pilot target status:** Track weekly by region and user type. |
| **Stalled inquiry rate** | **Definition / instrument:** Open inquiries without action for longer than service-level threshold / all open inquiries. **Pilot target status:** Threshold must be defined with staff. |
| **Form completion rate** | **Definition / instrument:** Completed submissions / sessions that begin an intake path, segmented by path and device. **Pilot target status:** Instrument starts and abandonment points; consent-aware analytics. |
| **Staff effort per inquiry** | **Definition / instrument:** Estimated active handling minutes and number of handoffs, measured in workflow study. **Pilot target status:** Compare before/after with a small staff sample. |
| **Successful downstream enrollment** | **Definition / instrument:** Number or share confirmed registered by receiving program, when observable. **Pilot target status:** Secondary until integration or manual reconciliation exists. |
| **Data quality** | **Definition / instrument:** Share of records with valid contact, location and role fields; duplicate flag rate. **Pilot target status:** Set thresholds after intake form testing. |
| **Accessibility and reliability** | **Definition / instrument:** Task success in usability sessions; critical accessibility issues; failed form submission and notification rates. **Pilot target status:** Define release gates with design and engineering. |

Measurement safeguards: segment by referral source, geography, user type and program; compare rates rather than total signups alone; exclude test data; measure cohorts consistently; do not assume missing downstream data represents failed enrollment. Obtain consent and approval for any analytics that collect personal or sensitive information.

# **9\. Accessibility, privacy and operational quality**

* Aim for WCAG 2.2 AA in the public and staff interfaces; validate with assistive technology and actual target users rather than relying only on automated checks.  
* Keep language concrete, navigation predictable and multi-step flows short; provide large targets, clear progress, plain-language errors and accessible confirmation states.  
* Avoid claiming a user is eligible based solely on automated answers. Route borderline cases for human review.  
* Define data minimization, legal basis/consent, guardianship rules, information sharing, retention and deletion before accepting live referrals. Determine whether any PHI is processed and whether HIPAA-related obligations apply with counsel.  
* Use transport encryption, managed secrets, role-based authorization, audit trails, back-ups, incident response and safeguards against spam/duplicate submissions.  
* Establish who maintains program information and staff directories. Routing quality will decline rapidly if contacts and offerings are stale.

# **10\. Scope and release sequence**

| Topic | Details |
| :---- | :---- |
| **Current: pre-hackathon setup** | **Deliverable / activity:** Repository is set up. The conference mockup/prototype was delivered. Significant backend implementation is anticipated during the hackathon; it is not yet a completed milestone. The prototype is a functional reference, not an approved visual design or exact flow. **Exit condition / dependency:** Agree on first pilot journey, provisional entities and interface assumptions before building routes that rely on unresolved SOTN policy decisions. |
| **Discovery / requirements** | **Deliverable / activity:** SOTN workflow interviews, exact form fields, contact directory, permissions matrix, routing decisions, draft events and reporting definitions. **Exit condition / dependency:** SOTN approves one end-to-end pilot journey and accepts responsibility for the first queue. |
| **M0: pilot foundation** | **Deliverable / activity:** Data model, staff auth, program/area records, public form and submission acknowledgement. **Exit condition / dependency:** Form generates traceable record, basic privacy review complete, test workflow passes. |
| **M1: operational pilot** | **Deliverable / activity:** Triage dashboard, statuses, ownership, assignment override and activity logging. **Exit condition / dependency:** A real referral can be submitted, reviewed, assigned, contacted and closed without spreadsheets. |
| **M2: quality and measurement** | **Deliverable / activity:** Reminders, resources, reporting, accessibility fixes, usability review. **Exit condition / dependency:** Baseline metrics stable and staff can identify stalled referrals. |
| **M3: interoperability** | **Deliverable / activity:** Approved API contract and potentially external integrations, broader programs and richer matching. **Exit condition / dependency:** Other system owners agree to interfaces, security and source-of-truth rules. |

Current stage (October 2026): pre-hackathon setup. The project repository has been set up, and the team anticipates substantial backend development during the hackathon. The July 2026 conference mockup and clickable prototype deliverable is complete. It can inform the functionality being implemented, but it is not a specification for the production visual design or an exact user-flow blueprint. The implementation should be driven by confirmed user requirements and SOTN workflow decisions. Dates and engineering estimates for subsequent milestones remain to be determined.

# **11\. Trade-offs and recommended decisions**

| Topic | Details |
| :---- | :---- |
| **Public accounts** | **Recommended initial choice:** No account required for expressing initial interest. **Reason / consequence:** Reduces friction; needs secure method if applicants later need to edit submissions. |
| **Matching engine** | **Recommended initial choice:** Rules-based suggestion plus staff override. **Reason / consequence:** Easier to explain and maintain than automated qualification; depends on accurate area and program data. |
| **Contact model** | **Recommended initial choice:** Store a person separately from one or more inquiries and relationships. **Reason / consequence:** Supports caregivers, repeat submissions and overlapping interests. |
| **Program directory** | **Recommended initial choice:** Curated and staff-maintained initially. **Reason / consequence:** Avoid building a large content management system before routing works. |
| **Outreach** | **Recommended initial choice:** Activity tracking before direct automated messaging. **Reason / consequence:** Can test workflow value without immediate SMS, deliverability, cost and consent complexity. |
| **Integration** | **Recommended initial choice:** Document contracts and manual handoff first. **Reason / consequence:** Avoid being blocked by unresolved SEO NOW / COE responsibilities. |
| **Pilot users** | **Recommended initial choice:** Choose one or two high-volume paths with SOTN. **Reason / consequence:** More useful than incomplete support for every population on launch. |

# **12\. Dependencies and risks**

| Topic | Details |
| :---- | :---- |
| **Ownership overlap with SEO NOW / COE** | **Consequence:** Duplicate development or conflicting records. **Mitigation:** Agree system boundaries, handoff fields and system of record before integration work. |
| **No agreed routing rules** | **Consequence:** Engineering builds arbitrary logic; users routed incorrectly. **Mitigation:** Use real historical cases in a routing workshop and require staff override. |
| **Staff capacity and adoption** | **Consequence:** Dashboard becomes another inbox nobody checks. **Mitigation:** Assign pilot queue owner, define service-level process and test with staff. |
| **Sensitive personal/health data** | **Consequence:** Privacy exposure, legal risk and exclusion of vulnerable participants. **Mitigation:** Minimize initial fields, review permissions and consent with SOTN / VUMC. |
| **Unreliable outcome visibility** | **Consequence:** Metrics undercount successful enrollment. **Mitigation:** Treat connected referral as observable near-term outcome; manual reconciliation if needed. |
| **Changing program offerings** | **Consequence:** Outdated recommendations and referrals. **Mitigation:** Make the program directory operationally owned and regularly reviewed. |

# **13\. Decisions to resolve with SOTN**

1\. Which intake journeys should the pilot support? For each, walk through a recent real example and agree on required fields, consent, guardian involvement, confirmation text and the first staff handoff.

2\. How should inquiries be routed and resolved? Confirm program and regional coverage, qualification criteria, no-match cases, owners, escalation rules and the meaning of each status, including what counts as successfully connected.

3\. What should staff be allowed to see and do? Confirm statewide versus area access, assignments, notes, outreach history, exports, deletion requests and who approves access.

4\. Where does this platform hand off to existing systems? Confirm SEO NOW, Train4Life and COE boundaries, who maintains program and contact directories, what data can be transferred and who owns the resulting participant record.

5\. What makes the pilot ready for live use? Agree on privacy and accessibility review, first pilot cohort, support ownership, baseline measurement, response expectations and functional sign-off.

# **14\. Decision register**

| Topic | Details |
| :---- | :---- |
| **Product boundary** | **Current status:** Working direction: broader SOTN intake/routing, not operational T4L. **Required decision:** SOTN and SEO NOW jointly approve separation. |
| **Pilot programs and user groups** | **Current status:** Not selected. **Required decision:** Select first two journeys and areas. |
| **Eligibility and routing rules** | **Current status:** Concept only. **Required decision:** Document criteria, exceptions and responsible reviewers. |
| **Admin permissions** | **Current status:** Roles identified, access not specified. **Required decision:** Approve permissions matrix. |
| **Mandatory form fields** | **Current status:** Examples exist, not approved. **Required decision:** Approve fields, consent and retention. |
| **Metrics targets** | **Current status:** Proposed instrumentation, no reliable baseline. **Required decision:** Baseline then agree quantitative targets. |
| **Integration obligations** | **Current status:** SEO NOW / COE interfaces discussed, not confirmed. **Required decision:** Document integration owners, sequence and data contracts. |
| **Hosting and operations** | **Current status:** Suggested tech stack, deployment decision absent. **Required decision:** Confirm hosting, identity, incident and support owner. |

