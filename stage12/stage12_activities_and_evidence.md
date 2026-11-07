# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Tue 1:30 - 3:30 Group 5
Members and UG/PG applicability: Dillan Rajanayagam (Dillan-Rajanayagam1), Kyle Carasig (KhenZ07), Andy Lieu (Andy-Lieu) and Kamalpreet Singh (kamal824); all UG, so the common scope applies and Stages 10–11 are not applicable.


## A Release scope and starting SHA

Release label/version and requirements baseline: SmartCare v1.0, common (UG) release; requirements baseline SmartCare A3 2026 revision 2.
Common starting SHA / branch / applicable members: Main at a99b6fd (Stage 9 record update on top of the Stage 9 code merge 9114381); release branch release/stage12; all four members.
PG starting SHA / branch / applicable members or not applicable: Not applicable — all members are UG, so the PG pathway was not taken.
Working-state review and approved integration: git status was clean on main before branching. The only release changes are the corrections in section H, the README updates and this record, made on release/stage12 and integrated through a pull request.
Protected common candidate and PG differences: The Stage 9 merge 9114381 is the protected common candidate code baseline; there is no PG branch.
Feature freeze / owner / verifier: Feature freeze from the Stage 9 merge: no new features, only release corrections and documentation. Owner and verifier: Kamalpreet Singh.


## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: Release with conditions is not enough here; the right decision is Do not release yet. Passing tests show the code works, but users cannot reproduce it without complete setup instructions, an unreviewed dependency is an unchecked supply-chain and licence risk, and an undocumented limitation can mislead users. All three are quick to fix, so they should be fixed and rechecked before release rather than shipped as conditions.

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | Service, regression and console tests show the cancelled object is retained, found and listed | project/tests/test_services.py, test_regressions.py, test_queries.py, test_console.py at the tested SHA | Kamalpreet Singh | Yes | None |
| Architecture responsibilities are appropriate | Code review in section E; I/O only in console.py, query module pure, domain owns status changes | project/smartcare/ | Kamalpreet Singh | Yes | None |
| Rescheduling is safe — PG only | Not applicable — all members are UG, so the PG pathway was not taken. | — | — | — | — |
| AI use is responsible — common recheck / PG assurance | Stage 8 and 9 Copilot decisions recorded with evidence; final Copilot release check in section E found no blocker | stage08 section F, stage09 section E, section E here | Kamalpreet Singh | Yes | None |
| System is maintainable | pycodestyle and pyflakes report no findings after the section H corrections; focused functions, docstrings and type hints; 89 tests | project/ | Kamalpreet Singh | Yes | None |
| FR-01–03 register/find and validation | test_starter.py, practitioner and patient lookup tests in test_services.py, test_domain.py | project/tests/ | Kamalpreet Singh | Yes | None |
| FR-04–05 booking/conflict rules | test_booking_and_cancellation.py, test_regressions.py::test_f8_01_practitioner_conflict_rule, demo steps A2/A3 | project/tests/, stage12/demo_output.txt | Kamalpreet Singh | Yes | None |
| FR-06–08 cancellation/history/find | Cancellation tests in test_services.py, test_regressions.py::test_f8_02_cancelled_appointment_still_found, demo steps for A1 | project/tests/, stage12/demo_output.txt | Kamalpreet Singh | Yes | None |
| FR-09 and QRY/FP listing/filter/order/purity | test_queries.py (status filters, tie-break, purity, empty/unknown/invalid) | project/tests/test_queries.py | Kamalpreet Singh | Yes | None |
| UI full console sequence and error recovery | test_console.py and the scripted demo run with `python3 main.py --interactive < ../stage12/demo_input.txt` | project/tests/test_console.py, stage12/demo_output.txt | Kamalpreet Singh | Yes | None |
| Session-only scope / FR-10 retired | No saving code; README and the exit message state that data is lost on exit | project/README.md, console.py | Kamalpreet Singh | Yes | Documented limitation |
| PG RES and assurance integration | Not applicable — all members are UG, so the PG pathway was not taken. | — | — | — | — |


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | Python 3.15.1 (macOS) and 3.13.18 (clean venv), pytest 8.3.5 | project/: `python3 -m pytest -q` | [TO FILL: merge SHA of the Stage 12 PR] | 89 passed | Section F fresh-clone run and the PR description |
| Complete PG if applicable | Not applicable — all members are UG, so the PG pathway was not taken. | — | — | — | — |
| Affected focused checks after correction | Python 3.13.18, pytest 8.3.5 | project/: `python3 -m pytest -q tests/test_regressions.py tests/test_services.py` | release/stage12 before merge | 29 passed | Section H |
| Full integrated recheck | Python 3.15.1, pytest 8.3.5 | project/: `python3 -m pytest -q` after `git switch main` and `git pull` | [TO FILL: merge SHA of the Stage 12 PR] | [TO FILL: result on main after merge] | Section I |
Prior assertions preserved / reviewed test diff: The release changes no test assertions; the only test-file change is a blank line. All 89 earlier tests are kept.
Remaining failure / limitation: None failing. Limitations are listed in section G.


## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | Clinic reception staff manage synthetic patients, practitioners and appointments in one session | Stakeholders: reception staff, practitioners, patients | Purpose stated in project/README.md | README |
| Register and find Patient and two Practitioners | P1 Alex Example; D1 General practice; D2 Physiotherapy; find P1 and D2 | FR-01–03 | Registered and found with matching details | demo_output.txt |
| Valid booking | A1: P1 with D1 at 2026-10-01 09:00 | FR-04 | Booked A1, scheduled | demo_output.txt |
| Same practitioner exact-time conflict rejected | A2: P1 with D1 at 09:00 | FR-05 / AC-04.1 | Error: Practitioner already has a SCHEDULED appointment at this time | demo_output.txt |
| Different practitioner same time allowed | A3: P1 with D2 at 09:00 | AC-04.2 | Booked A3 | demo_output.txt |
| Cancel SCHEDULED and retain/find CANCELLED object | Cancel A1, then find A1 | FR-06–08 | Cancelled A1; find shows A1 cancelled | demo_output.txt |
| Invalid/repeated cancellation rejected | Cancel A1 again; cancel unknown A9 | FR-06, BR-07 | Error: Only SCHEDULED appointments may be cancelled; Error: Appointment not found | demo_output.txt |
| Default all-status listing | List D1 with blank status | FR-09 | A4 (08:30, scheduled) then A1 (09:00, cancelled) | demo_output.txt |
| Explicit filtering / empty vs unknown / deterministic order | List D1 scheduled; D9; D2 cancelled; final D1 listing with A1 and A5 both at 09:00 | QRY/FP | Only A4; Error: Practitioner not found; No matching appointments; A4, A1, A5 ordered by time then ID | demo_output.txt |
| Invalid date/status/menu/lookup recovery and continued operation | 01/10/2026 9am; 2026-02-30 09:00; status booked; choice 9; then book A5 | UI-02 | Four error/unknown-choice messages, then A5 booked in A1's freed slot | demo_output.txt |
| Session-only limitation and normal exit | Choice 0 | Session-only scope | Goodbye. Session-only data is lost on exit. | demo_output.txt |
| One meaningful requirement-linked pytest test explained | test_regressions.py::test_f8_02_cancelled_appointment_still_found | FR-07/FR-08 | Asserts the same object is returned, CANCELLED, still listed and found by store and service, and that a second cancel raises ValueError without changing status | project/tests/test_regressions.py |
| Architecture and one actual AI decision / known limitation | Stage 9 Copilot claim that passing the stored practitioner ID had no benefit | Responsibilities | Rejected: using the raw input failed the ' D1 ' test; limitation: session-only data | stage09 section E |
| PG reschedule identity/participants/time and no-op | Not applicable — all members are UG, so the PG pathway was not taken. | — | — | — |
| PG conflict/invalid status/failure non-mutation | Not applicable — all members are UG, so the PG pathway was not taken. | — | — | — |
| PG old slot / current lookup/list ordering / assurance risks | Not applicable — all members are UG, so the PG pathway was not taken. | — | — | — |
Stable demo owner / fresh process / command: Kamalpreet Singh; a fresh process from project/: `python3 main.py --interactive < ../stage12/demo_input.txt`; output saved in stage12/demo_output.txt. The same steps can be typed live in the viva.
PG demonstrations through service/tests or not applicable: Not applicable — all members are UG, so the PG pathway was not taken.


## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | project/smartcare/ | No finding: domain owns validation and status, store only add/find/list, services coordinate, queries pure, console does all I/O | No change |
| PascalCase and snake_case naming | All modules | No finding | No change |
| Useful type hints and meaningful docstrings | All public functions | find_appointment and has_practitioner_conflict lost their docstrings during Stage 8 preparation; restored in Stage 8 | No change in Stage 12 |
| Four-space indentation and imports/layout | main.py, tests/test_booking_and_cancellation.py | pycodestyle: E305 and E302 (missing blank lines) | Fixed; pycodestyle and pyflakes then report nothing |
| Focused methods / duplication / dead or commented code | data_store.py find_appointment | Duplicated ID validation and a linear search left from the Stage 8 fault body, instead of required_text and the dictionary lookup used elsewhere | Fixed (section H); 89 passed |
| Globals / leakage / unnecessary inheritance or frameworks | project/ | No globals, no inheritance beyond Enum, no frameworks | No change |
| No SQLite/persistence/repository ABCs/speculative features | project/ | None present | No change |
| Synthetic data / secrets / dependencies / provenance | Repository files, requirements-dev.txt | Only synthetic IDs and names; no secrets; only pytest 8.3.5 for development; .gitignore excludes .venv, caches and .stage8_faults | No change |
| Significant common Copilot contributions and human verification | stage08 section F, stage09 section E | Copilot reviews in Stages 8 and 9 were checked against code and test runs; correct findings accepted, unsupported ones rejected with evidence | No change |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | Not applicable — all members are UG, so the PG pathway was not taken. | — |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| find_appointment now depends entirely on required_text for the invalid-ID contract (Important) | data_store.find_appointment; FR-08 | required_text raises ValueError for any non-string or blank/whitespace value and returns the trimmed text; the same helper already guards patient and practitioner lookup. test_cancel_invalid_id_raises_value_error ('', '   ', None, 123) passes through this path | Accept as a verification point; no defect | No change; 89 passed |
| Correctness depends on cancelled appointments staying in _appointments (Important) | FR-07/FR-08 | Appointment.cancel only sets the status; the store has no delete/pop/remove code; test_f8_02_cancelled_appointment_still_found and the retained-history tests pass | Accept as a verification point; no defect | No change |
| README could state that cancelled appointments are kept and findable (Optional) | project/README.md | The menu paragraph mentioned listing but not lookup after cancellation | Accept | Added one sentence to project/README.md |
| Blank-line PEP 8 changes are low risk (Optional) | main.py, tests | pycodestyle clean; suite unchanged | Accept | No further change |
Access route or approved equivalent / limitations: Microsoft Copilot Chat, signed in with Kamalpreet's work account, 7 November 2026. Copilot could not see the repository, so the release changes and contract were described in the prompt; it reviewed that description, not the full source.
Available AI evidence and missing evidence honestly disclosed: Copilot evidence exists for Stages 8 and 9 in those records. The Stage 6 and 7 records state that Copilot was not used for those PRs. Final check: the prompt listed the find_appointment change and its contract, the PEP 8 changes and the README changes, and asked for ranked correctness, release-blocker, README and responsible-AI findings; Copilot reported no critical finding or release blocker, two Important verification points and two Optional notes (table above).


## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | project/README.md first paragraph | Kamalpreet Singh | Present; common scope only |
| Out-of-scope capabilities and known limitations | project/README.md, Limitations paragraph | Kamalpreet Singh | Present |
| Confirmed teaching Python version and dependency installation | project/README.md and root README.md | Kamalpreet Singh | Python 3.13 and 3.15.1 verified; `python -m pip install -r requirements-dev.txt` |
| Working directory / demo / interactive / test commands | project/README.md commands block | Kamalpreet Singh | All three commands run from project/ |
| Repository structure and architecture responsibilities | project/README.md, Structure and responsibilities | Kamalpreet Singh | Added for the release |
| Responsible AI summary / synthetic-data rule | project/README.md, Responsible AI and data | Kamalpreet Singh | Added for the release |
| Release label/version and SHA links | project/README.md title (v1.0); root README group index; section K | Kamalpreet Singh | Present |
Root README index and project/README verified: Both READMEs were checked against a fresh clone; the root README links every stage record and the demo files.
Fresh clone or extracted ZIP / candidate identity: Fresh clone of release/stage12 into a new folder before merge; candidate identified by commit SHA.
Verifier and clean environment / actual version: Kamalpreet Singh; new virtual environment, Python 3.13.18, pytest 8.3.5 installed from requirements-dev.txt.
Setup/run/test commands and observed results: `python -m pip install -r requirements-dev.txt` installed pytest 8.3.5; `python main.py` printed the A1 demo line and the session note; `python -m pytest -q` → 89 passed; `python main.py --interactive` showed the menu and exited with 0.
Missing local file or setup gap / remedy and recheck: None found. macOS users need `python3` instead of `python`; this is now stated in both READMEs.


## G Known limitations debt and release notes

Delivered features: Patient and practitioner registration and lookup; booking with the same-practitioner conflict rule; cancellation that keeps history; appointment lookup; practitioner listing with optional status filter and date/time-then-ID ordering; interactive menu with error recovery.
Important fixes: Stage 8: practitioner conflict check inverted (F8-01) and cancelled appointments not found (F8-02), both fixed with regression tests.
Architecture/quality improvements: Status magic string replaced with AppointmentStatus (Stage 8); pure query module (Stage 9); duplicated lookup validation removed and style issues fixed (Stage 12).
Known limitations: Session-only data; local minute-precision times without timezones; no deletion, rescheduling, completion workflow, authentication or patient-conflict rule.
AI-assisted development note: Copilot reviewed the Stage 8 and 9 changes. Its suggestions were accepted, modified or rejected only after checking the code and running the tests, as recorded in those stages.

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| Session-only storage | Data is lost on exit | Low for teaching use | Add persistence only if a future requirement needs it | Accepted; FR-10 is retired |
| Linear scans for conflict checks and listings | Slower with very large data | Low | Use indexes if the data grows | Accepted for teaching scale |
| No appointment completion workflow in the menu | COMPLETED can only be created directly in code/tests | Low | Add a guarded completion operation if required | Accepted; not in the common requirements |
Session-only synthetic data and minute-precision local time: All data is synthetic and exists only for one run; times are naive local datetimes at minute precision.
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: Excluded from this release: production authentication and roles, a patient portal, notifications, billing/insurance and any clinical AI.
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: Single-user console; no concurrency control, timezone policy, operations monitoring or accessibility review; scale is limited to teaching data.
Difference between accepted scope limit and unresolved required behaviour: An accepted scope limit (for example no persistence) is outside the agreed requirements and is documented. Unresolved required behaviour would be a requirement the release fails; none is known.
PG assurance residual risks / owner / status or not applicable: Not applicable — all members are UG, so the PG pathway was not taken.


## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| data_store.find_appointment duplicated validation | Code review: the Stage 8 fault body left a manual check and linear search instead of required_text and the dictionary | Low; behaviour correct, maintainability only | Kamalpreet Singh | Return `self._appointments.get(required_text(appointment_id, 'Appointment ID'))` | 29 focused and 89 full passed | None |
| Style: missing blank lines in main.py and tests/test_booking_and_cancellation.py | pycodestyle E305 and E302 | Low | Kamalpreet Singh | Added the blank lines | pycodestyle clean; 89 passed | None |
Justified no-change conclusion if no defect found: The two corrections were maintainability and style only; no required behaviour was found broken in the release review.
Release blockers still open / status: None open.


## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: [TO FILL: Stage 12 PR link]; reviewed SHA [TO FILL: release branch commit SHA]
Independent reviewer / feedback / response: [TO FILL: teammate name, feedback and response, or state that no independent review took place]
Integration commit / full recheck: [TO FILL: merge SHA of the Stage 12 PR]; full recheck in section C.
Tracked and untracked file inspection / cleanliness: `git status --short` was empty before branching; `git ls-files` shows 25 tracked files plus the Stage 12 additions, with no caches or environments.
Secrets/staff material/caches/tool-metadata exclusion check: .gitignore excludes .venv, __pycache__, .pytest_cache, .env and .stage8_faults; the Stage 8 tool and its backup were never committed; no secrets or staff material are tracked.
Candidate recovery plan / known-good SHA: If a release problem is found, return to the Stage 9 common candidate 9114381 or the tagged release commit with `git switch --detach <SHA>`; no history is rewritten.
Named substantive contributions: Kamalpreet Singh — Stage 6 practitioner lookup and cancellation, Stage 7 tests and record corrections, Stage 8 preparation, diagnosis and repairs, Stage 9 queries, listing, menu and tests, Stage 12 release review. [TO FILL: Dillan, Kyle and Andy]


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: READY WITH DOCUMENTED LIMITATIONS
Approver / date / rationale and evidence: Kamalpreet Singh, [TO FILL: date]. All common requirements have passing tests and a reproducible demo; the README was reproduced from a fresh clone; the limitations in section G are documented.
What risks remain / conditions / owners: Session-only data and the process gaps recorded in Stages 6–9 (PRs merged without another-member approval). Owner: Kamalpreet Singh.
Can the team explain the system: Yes: each stage record links the code, tests and decisions, and the viva preparation table in section N covers the main design points.
Can a change be recovered: Yes: every stage was merged through a pull request with a known SHA, so any change can be found and reverted.
Common decision / PG decision where different: Common decision as above; no PG decision.


## K Final tested release SHA

Exact common tested SHA: [TO FILL: merge SHA of the Stage 12 PR]
Exact PG tested SHA or not applicable: Not applicable — all members are UG, so the PG pathway was not taken.
Final submitted SHA / repository URL: [TO FILL: final submitted SHA] / https://github.com/Dillan-Rajanayagam1/st1-assignment-3
Evidence-only later commit and difference explanation: [TO FILL: if the record is updated after the merge, that commit only adds evidence]
Executable changes after testing and re-verification: None after testing; the final integrated recheck in section C confirms the tested code.
Source ZIP name / SHA correspondence / extracted comparison: [TO FILL: ZIP name, e.g. smartcare_v1.0_<sha>.zip, created with git archive from the submitted commit]


## L Submission package verification

- [ ] Feature freeze and scoped requirements traced.
- [ ] Applicable full regressions, integrated demo and invalid paths verified.
- [ ] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [ ] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [ ] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [ ] project/ source and all accumulated applicable tests included.
- [ ] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [ ] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ ] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [ ] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: [TO CONFIRM with the tutor/unit site]
Deadline/timezone: [TO CONFIRM]
Repository access arrangement: Public repository at the URL above; [TO CONFIRM any extra teaching-team access]
Mixed-candidate upload arrangement: Not applicable — UG-only group.
Oral/video recording/accessibility arrangements: [TO CONFIRM]
Remaining administration or release dependency: Group reflection, confidential peer forms and team viva are submitted separately through the unit's routes.


## M Formative questions

1. What is a release candidate? A specific, tested version of the software, identified by a commit SHA, that the team proposes to release if no blocking problem is found.

2. What is feature freeze and why is it used? A point after which no new features are added, only fixes and documentation, so the candidate stays stable while it is tested and reviewed.

3. What is regression testing in a release context? Rerunning the full test suite on the exact candidate to show that earlier behaviour still works after the final changes.

4. What is a known limitation? A documented gap or restriction the release accepts, such as session-only data, so users are not misled.

5. What is technical debt? The future cost of shortcuts or unfinished design that work now but will need rework later.

6. What are release notes? A short summary of what the release delivers, what was fixed, what changed and what limitations remain.

7. What is software maintenance? Changing software after release to fix defects, adapt to new needs or improve its structure while keeping it working.

8. What is the purpose of the individual demonstration/viva? To show that each member understands and can explain the system, their own contribution and the evidence, not just that the code runs.

9. What should the final responsible-AI check establish before release? That every significant AI contribution was checked by a human against the requirements, code and tests, that no secrets or real data were shared, and that the use is disclosed honestly.

10. What is the main course conclusion about AI and the role of the software engineer? AI can suggest and speed up work, but the software engineer stays responsible for requirements, design, verification and the decision to release.


## N Reflection viva and handover

Strongest evidence SmartCare is ready: 89 passing tests that trace to the requirements, plus a demo run from a fresh clone that covers every menu action and error case.
Weakest area: Process: several PRs were merged without another member's approval, and the Stage 8 hypotheses were recorded after the repairs.
How AI use changed from Stage 1 to Stage 12: Copilot was first treated as a reviewer to check; by Stages 8 and 9 every suggestion was tested against code and real runs, and some were rejected with evidence.
Start doing — engineering and AI use: Ask a teammate to review every PR before merging, and record hypotheses before asking an AI tool.
Stop doing — engineering and AI use: Stop accepting an AI suggestion because it sounds confident without checking it.
Continue doing — engineering and AI use: Continue writing regression tests for every defect and keeping evidence in the stage records.
What worked / caused rework / future delivery improvement: Small branches and PRs worked well. Rework came from late cancellation work blocking Stage 8 and from a folder layout that the Stage 8 tool rejected. Next time, agree the repository layout and finish each stage before starting the next.
One paragraph — If AI can write code why do we still need software engineers: AI can produce code quickly, but it cannot decide what the clinic actually needs, judge which requirement a test should protect, or take responsibility for a release. In this project Copilot ranked the right cause first for both Stage 8 defects, but it also suggested causes with no evidence and called a correct design choice pointless; only checking the code and running the tests showed which was which. Software engineers turn requirements into checks, verify what a tool claims, keep the design maintainable and stand behind the result, and that work becomes more important, not less, as AI writes more of the code.

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | Reception staff need to register synthetic patients and practitioners, book without double-booking a practitioner, and cancel while keeping history. Evidence: project/README.md. |
| Two requirements and acceptance criteria | FR-05/AC-04.1–04.2: same practitioner and time rejected, different practitioner allowed (test_f8_01_practitioner_conflict_rule). FR-07: cancelled appointment retained and findable (test_f8_02_cancelled_appointment_still_found). |
| Domain model and architecture | Patient, Practitioner, Appointment and AppointmentStatus in domain.py; one shared SmartCareDataStore; services coordinate; pure queries; console for I/O. |
| Design trade-off | select_appointments is a pure function rather than a store method, so it is easy to test and cannot change state; the cost is passing the list in explicitly. |
| Meaningful test and its limits / 100 percent coverage | test_f8_02 checks identity, status, retention and repeated cancellation. It does not prove every input; 100 percent coverage would show lines ran, not that behaviour is right. |
| Diagnosed defect and verification | F8-01: `!=` instead of `==` in has_practitioner_conflict; reproduced, Copilot's ranked causes checked, one-line fix, regression test failed before and passed after. |
| Shared store and session-state/query responsibilities | The store holds all objects for one session; services read and change them through the store; queries only read a list they are given. |
| What would break if session-state lookup/query responsibilities changed? | If the query read the store directly it would hide a dependency and become harder to test; if it sorted in place it would change the store's list order for every caller. |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Cancellation only needs one Appointment's state, so Appointment.cancel guards it; a conflict needs all appointments, so the service asks the store. |
| FR-07 retained history test | test_service_lists_all_statuses_and_keeps_cancelled_history: cancelled A2 is still listed and is the same object as find_appointment('A2'). |
| Actual AI change rejected/modified or honestly accepted with verification | Rejected Copilot's Stage 9 claim that passing the stored practitioner ID had no benefit: switching to the raw input made the ' D1 ' test fail. |
| Unresolved limitation / future production work | Session-only data; production would need persistence, authentication, a completion workflow and timezone handling. |
| Personal implementation contribution | Practitioner lookup, cancellation, Stage 8 repairs and refactor, Stage 9 query, listing and menu, Stage 12 corrections. |
| Personal test/review/design/integration contribution | Stage 7 domain and booking tests, Stage 8 regression tests, Stage 9 query and console tests, Copilot reviews in Stages 8–9, and integration of PRs #5, #7, #9 and #10. |
| PG agentic change and rescheduling verification | Not applicable — all members are UG, so the PG pathway was not taken. |
| PG responsible-AI risk/remediation or supported no finding | Not applicable — all members are UG, so the PG pathway was not taken. |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: Not undertaken.
Separate reflection / peer / common team viva evidence links and routing: Submitted separately through the unit's routes; confidential peer forms are not stored in this repository.
No further coding stage. Later corrections use the published assessment process.
