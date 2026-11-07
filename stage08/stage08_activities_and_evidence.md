# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Tue 1:30 - 3:30 Group 5
Members and UG/PG cohorts: Dillan Rajanayagam (Dillan-Rajanayagam1, UG), Kyle Carasig (KhenZ07, UG), Andy Lieu (Andy-Lieu, UG), Kamalpreet Singh (kamal824, UG)
Record owner / contribution links for each member: Kamalpreet Singh (record owner, preparation, regression tests, repairs and refactor); other members' contributions in section I

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason:

- "Appointment disappears after cancellation." — Symptom. It describes what a user observed, not why it happened, and it has not been checked against stored state.
- "The data-store removal path is probably being called." — Hypothesis. It proposes a cause that can be tested. In this project it is unlikely, because SmartCareDataStore has no public delete operation; inspecting list_appointments() after cancellation would confirm or reject it.
- "The failing test shows store.find_appointment('A1') returns None." — Evidence. It is a concrete, reproducible result from an executed test.
- "The service layer is badly designed." — Opinion. It names no specific behaviour and cannot be tested as stated, so it does not help locate a defect.
- "Traceback points to smartcare/services.py line 42 in the example." — Evidence of location only. It shows where the failure surfaced; in our run the actual line was services.py:135, where find_appointment raises LookupError. The cause can be elsewhere, here in the data store.

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason:

Scenario: cancelled-history lookup.
- Expected behaviour: after cancellation the same appointment object is CANCELLED, stays in list_appointments() and is still returned by find_appointment (FR-06, FR-07, FR-08, AC-05.2).
- Observed behaviour: after cancelling A1, the appointment is CANCELLED and still in list_appointments(), but store.find_appointment('A1') returns None and AppointmentService.find_appointment('A1') raises LookupError.
- Minimal reproduction: new SmartCareDataStore; register P1 and D1; book A1 for 2026-10-01 09:00; cancel A1; call store.find_appointment('A1') and service.find_appointment('A1').
- Initial hypothesis: cancellation removes the appointment from the store.
- Evidence to inspect: list_appointments() after cancellation (does it still contain A1?), the body of SmartCareDataStore.find_appointment, and Appointment.cancel.
The initial removal hypothesis was later rejected: the object is still in list_appointments(), so the defect is in how the lookup filters records, not in removal.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason:

The test is wrong, not the product. FR-07 requires cancelled appointments to be retained, so a test expecting deletion contradicts the requirement and should be corrected to expect a CANCELLED appointment that is still stored and retrievable. Changing the code to delete records would make the test pass but break FR-07.

A test expecting different practitioners at the same time to conflict does not reflect AC-04.2, which allows a different practitioner to be booked at the same time. That test should also be corrected. Only the same practitioner at the same time with a SCHEDULED appointment is a conflict (AC-04.1). A failing test is a claim about required behaviour that must itself be checked against the requirements.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason:

Smells in the hypothetical 70-line method: a long method with several responsibilities; duplicated status strings (magic values instead of AppointmentStatus); direct manipulation of the stored collection, bypassing the SmartCareDataStore add/find/list boundary; printing mixed with business logic; validation mixed into the workflow; and four nested conditionals that hide the main path.

Small behaviour-preserving refactorings: replace the status strings with the existing AppointmentStatus members; call the store's add/find/list methods instead of touching the collection; move printing to the console layer; use guard clauses to flatten the nesting; and extract a small helper for a repeated check such as the conflict test. Each step is made separately with the tests run after it. No new layers or frameworks are needed.

Classification:
- Rename appt to appointment — refactoring. Only the name changes.
- Extract a repeated conflict helper — refactoring, as long as the same appointments are still rejected and accepted.
- Add rescheduling — feature. It adds new behaviour.
- Restore retained cancellation lookup — repair. It restores required FR-07/FR-08 behaviour that was broken.
- Replace a magic status string with the existing enum — refactoring, if the same statuses still match.

Behaviour that must stay unchanged: the same objects are returned, the same exceptions (ValueError for invalid values, LookupError for unknown IDs) are raised, only SCHEDULED to CANCELLED is allowed, cancelled appointments are retained, the same-practitioner conflict rule is kept, and failed operations change nothing.

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason:

Failure used: tests/test_booking_and_cancellation.py::test_service_retains_cancelled_history on the prepared branch.
- Exception: LookupError: Appointment not found.
- Expected: appointments.find_appointment('A1') returns the same cancelled appointment. Observed: LookupError is raised.
- Test line: tests/test_booking_and_cancellation.py:187, the call to appointments.find_appointment('A1') after cancel_appointment('A1').
- Call path: test → AppointmentService.find_appointment (smartcare/services.py:135 raises LookupError) → SmartCareDataStore.find_appointment, which returned None.
- Requirement: FR-07 retained history, FR-08 lookup, AC-05.2.

Ranked causes and discriminating checks:
1. The store lookup skips cancelled appointments. Check: after cancellation, compare `a in store.list_appointments()` with `store.find_appointment('A1')`; if the object is listed but the lookup returns None, the lookup is filtering it.
2. Cancellation removes the appointment from the store. Check: inspect list_appointments() after cancellation; if A1 is missing, removal is the cause.
3. The service mistranslates a valid result into LookupError. Check: call store.find_appointment('A1') directly; if it returns the object, the service is wrong; if it returns None, the store is wrong.

Evidence: A1 was still in list_appointments() and store.find_appointment('A1') returned None, so cause 1 fitted and causes 2 and 3 were rejected. A traceback shows only where the failure was raised (services.py:135); the faulty decision was in data_store.py, so the traceback alone cannot establish the cause.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason:

Changing code straight away usually treats the place where a failure appears, not its cause. Without first reproducing the failure, stating the expected behaviour from a requirement and checking a hypothesis, an edit may hide the symptom, introduce new defects or change correct behaviour, and there is no evidence that the real problem was fixed.


Classification responses (1–5, each with reason): see the first tutorial response above.
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: see the debugging record response above.
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: see the traceback response above.

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: 0d2540e3d8ae5f342d7c502d52da221a82c3d806 (main after moving project/ to the repository root). Requirements: assignment overview revision 2 (FR-05, AC-04.1/04.2, FR-06/07/08, BR-07, AC-05.2).
- Baseline test command / working directory / observed result / evidence: `python3 -m pytest -q` in project/ → 59 passed.
- Clean preparation SHA if a record-only commit followed Stage 7: 0d2540e3d8ae5f342d7c502d52da221a82c3d806
- Branch and preparer / how teammates obtained this branch: debug/stage08, prepared by Kamalpreet Singh; pushed to GitHub so teammates fetch it with `git fetch` and `git switch debug/stage08` instead of running the tool again.
- Downloaded tool version, source SHA256 and --check outcome: prepare_debugging.py version 1.1, kept outside the repository. --check: preflight PASS; baseline data_store.py SHA256 b4a1993e878c59a9df5e9055320702b2d318c5b6055bb1693a3afc25cd8fd375; both fault signatures verified in a temporary copy, project unchanged.
- --apply and --verify output summaries / artefact references: --apply printed "PREPARED: F8-01 practitioner conflict; F8-02 retained-history lookup" and "Verified expected failures: test_f8_01_conflict; test_f8_02_history (2 failed)". --verify printed "VERIFIED: exactly 2 expected failures; both approved symptom signatures present".
- Bounded diff inspected and recovery location (not committed): git diff --stat showed only project/smartcare/data_store.py changed (find_appointment and has_practitioner_conflict bodies). The backup is in project/.stage8_faults/, which is ignored by .gitignore and not committed.
- Prepared faulty-state commit SHA: 5b95cb111e4b7ffd2363f576df0a0e1101d847a3 ("Prepare stage 08")
- Preparation or recovery issues and resolution, if any: The first --check refused because the project was inside SmartCare_Starter/project; the tool requires project/ at the repository root. The project and stage records were moved to the root in commit 0d2540e, and the Stage 9 record emptied by an earlier update was restored. No --restore was needed.
- Initial prepared full-suite command / result / key failures: `python3 -m pytest -q` in project/ → 8 failed, 51 passed. F8-01: test_starter.py::test_conflict_rule_and_different_practitioner, test_same_practitioner_same_time_rejected (DID NOT RAISE ValueError) and test_different_practitioner_same_time_allowed (ValueError: Practitioner already has a SCHEDULED appointment at this time). F8-02: test_cancel_changes_status (AttributeError: 'NoneType' object has no attribute 'status'), test_cancelled_appointment_retained, test_service_retains_cancelled_history, test_cancelled_appointment_is_retained_with_details (LookupError: Appointment not found) and test_repeated_cancellation_raises_value_error (LookupError instead of ValueError).

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: A second SCHEDULED appointment for practitioner D1 at the same time is accepted, while booking a different practitioner (D2) at that time is rejected with "Practitioner already has a SCHEDULED appointment at this time".
- Expected behaviour and requirement: FR-05 / AC-04.1: a booking for the same practitioner at the same date and time as a SCHEDULED appointment raises ValueError and the store is unchanged. AC-04.2: a different practitioner can be booked at the same time.
- Minimal synthetic reproduction steps: register P1, P2, D1 and D2; book A1 (P1, D1, 2026-10-01 09:00); book A2 (P2, D1, same time) → accepted, store has two appointments; book A3 (P2, D2, same time) → ValueError.
- Meaningful failing test path/name and exact relevant failure: project/tests/test_regressions.py::test_f8_01_practitioner_conflict_rule — "Failed: DID NOT RAISE <class 'ValueError'>" at the second booking for D1.
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: SmartCareDataStore.has_practitioner_conflict compares `appointment.practitioner.practitioner_id != practitioner_id`. The inverted comparison reports a conflict only when the practitioner is different, so it ignores the real conflict and blocks valid bookings. AppointmentService.book_appointment correctly raises ValueError whenever this method returns True, which shows the service is not the cause.
- Smallest justified fix / diff / why other behaviour is preserved: change `!=` to `==` in that one comparison. The exclude-ID, date/time and SCHEDULED conditions are untouched, so cancelled slots stay bookable and booking validation is unchanged.
- Repair SHA / focused verification result: Included in commit "Final stage 08" ea5abca. test_f8_01_practitioner_conflict_rule passes; the three F8-01 tests in the existing suite pass; the F8-02 failures remain until its repair.

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: After cancelling A1, the appointment is CANCELLED and still in store.list_appointments(), but store.find_appointment('A1') returns None and AppointmentService.find_appointment('A1') raises LookupError. A repeated cancellation raises LookupError instead of ValueError.
- Expected behaviour and requirement: FR-06/BR-07: cancellation uses the guarded transition. FR-07/AC-05.2: the same cancelled object is retained. FR-08: it can still be found in the same session. A repeated cancellation raises ValueError without changing state.
- Minimal synthetic reproduction steps: register P1 and D1; book A1; cancel A1; check A1 in list_appointments() (True), store.find_appointment('A1') (None), service.find_appointment('A1') (LookupError).
- Meaningful failing test path/name and exact relevant failure: project/tests/test_regressions.py::test_f8_02_cancelled_appointment_still_found — "AssertionError: assert None is <smartcare.domain.Appointment object …>" where None = store.find_appointment('A1').
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: SmartCareDataStore.find_appointment loops over the stored appointments with the extra condition `appointment.status.value != "cancelled"`, so a cancelled appointment is skipped and None is returned. The appointment is not deleted (it is still in list_appointments()), and Appointment.cancel works correctly (status is CANCELLED). The service correctly turns None into LookupError, which is why the error appears in services.py.
- Smallest justified fix / diff / why other behaviour is preserved: remove the cancelled-status filter so the lookup returns any stored appointment with the trimmed ID. Blank and non-string IDs still raise ValueError, unknown IDs still return None (LookupError in the service), and cancellation still allows only SCHEDULED to CANCELLED.
- Repair SHA / focused verification result: Included in commit "Final stage 08" ea5abca. test_f8_02_cancelled_appointment_still_found passes, including repeated cancellation raising ValueError with status still CANCELLED; full suite 61 passed.

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: [TO FILL by Kamalpreet in your own words, before using Copilot]
Evidence intended to inspect / competing explanation / discriminating check: [TO FILL by Kamalpreet before using Copilot]
Member and saved sequence/time or commit showing this preceded consultation: Kamalpreet Singh; [TO FILL: date/time written, before the Copilot prompt]

### F8-02 human entry
Likely cause and why plausible: [TO FILL by Kamalpreet in your own words, before using Copilot]
Evidence intended to inspect / competing explanation / discriminating check: [TO FILL by Kamalpreet before using Copilot]
Member and saved sequence/time or commit showing this preceded consultation: Kamalpreet Singh; [TO FILL: date/time written, before the Copilot prompt]

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: Kamalpreet Singh, GitHub Copilot Chat in VS Code. [TO FILL: paste the prompt used and a short summary of Copilot's reply]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [TO FILL from Copilot's actual reply]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [TO FILL from Copilot's actual reply]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [TO FILL from Copilot's actual reply]
Final human conclusion and comparison with initial hypothesis: [TO FILL after comparing Copilot's reply with the evidence in C/D]

### F8-02 Copilot review
Actual prompt / output reference and member: Kamalpreet Singh, GitHub Copilot Chat in VS Code. [TO FILL: paste the prompt used and a short summary of Copilot's reply]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [TO FILL from Copilot's actual reply]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [TO FILL from Copilot's actual reply]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [TO FILL from Copilot's actual reply]
Final human conclusion and comparison with initial hypothesis: [TO FILL after comparing Copilot's reply with the evidence in C/D]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | Prepared faulty commit (section B) plus tests/test_regressions.py | `python3 -m pytest -q tests/test_regressions.py` in project/ | test_f8_01_practitioner_conflict_rule failed: DID NOT RAISE ValueError (2 failed) |
| F8-01 after repair | `!=` → `==` in has_practitioner_conflict | same | test_f8_01 passed; test_f8_02 still failed (1 failed, 1 passed); full suite 6 failed, 55 passed, all F8-02 |
| F8-02 before repair | After the F8-01 repair | same | test_f8_02_cancelled_appointment_still_found failed: store.find_appointment('A1') returned None |
| F8-02 after repair | Cancelled-status filter removed from find_appointment | same | 2 passed |
| Full suite after both repairs, before refactor | Both repairs | `python3 -m pytest -q` in project/ | 61 passed (59 earlier tests and 2 regression tests) |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: The F8-01 test requires ValueError for the same practitioner and time and checks that the store still holds only the first appointment, then books a different practitioner at that time and checks both are stored; the inverted comparison fails both halves. The F8-02 test checks the returned object's identity, the CANCELLED status, list membership, store lookup identity and service lookup identity, then that a second cancellation raises ValueError without changing the status; the cancelled-status filter fails the store and service lookups. Earlier starter, Stage 6 and Stage 7 tests are kept unchanged and rerun.
Unrelated failures investigated / resolution: Not applicable. All 8 failures on the prepared branch were traced to F8-01 (3) or F8-02 (5), and all passed after the two repairs.

## H. Refactoring decision and before/after verification

Smell and exact location: Magic status string in project/smartcare/data_store.py, SmartCareDataStore.has_practitioner_conflict: `appointment.status.value == "scheduled"`.
Small proposed structural change / why justified: Compare with the existing enum, `appointment.status is AppointmentStatus.SCHEDULED`. The rest of the project uses the enum; a raw string can drift from the enum value without any error and hides that this is a status rule.
External behaviour to preserve / relevant tests: Only SCHEDULED appointments conflict; cancelled slots can be rebooked; same-practitioner conflict raises ValueError; different practitioners are allowed. Protected by test_regressions.py, test_starter.py::test_conflict_rule_and_different_practitioner and the booking and rebooking tests in test_booking_and_cancellation.py and test_services.py.
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: one line in has_practitioner_conflict, `status.value == "scheduled"` → `status is AppointmentStatus.SCHEDULED` (AppointmentStatus was already imported). The method docstrings removed during preparation were restored. Included in commit "Final stage 08" ea5abca
Focused and full after-refactor commands / working directory / results / evidence: `python3 -m pytest -q tests/test_regressions.py tests/test_starter.py` in project/ → 10 passed; `python3 -m pytest -q` → 61 passed, the same as before the refactor.
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: Accepted. The same 61 tests pass before and after, including conflict, rebooking and cancelled-history checks, so behaviour is preserved and the rule now uses the project's own status type.

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: No separate issues were created; both defects and the refactor are tracked in this record and PR #9; owner Kamalpreet Singh.
Branch / prepared, repair and refactor checkpoints: debug/stage08. Prepared faulty state 5b95cb1; both repairs, the regression tests and the refactor were committed together in ea5abca ("Final stage 08"), so the repair and refactor steps are recorded in sections C, D, G and H rather than as separate commits.
PR link and another member's reviewer identity: https://github.com/Dillan-Rajanayagam1/st1-assignment-3/pull/9; no other member reviewed the PR before merge
Key human feedback, difference from Copilot findings and response/outcome: No human review feedback was recorded on the PR.
Actual review approval / merge evidence: No approval was recorded. PR #9 was merged by the author (kamal824) as merge commit a644dc6e25af3b77b220727280ec82cdc3793af9. This is a recorded process gap.
Integrated code SHA and team pull/retest command / working directory / result: a644dc6e25af3b77b220727280ec82cdc3793af9; Kamalpreet Singh ran `git switch main`, `git pull`, then `python3 -m pytest -q` in project/ → 61 passed. The debug/stage08 branch was then deleted locally and on GitHub.
Evidence-only later SHA / explanation if different: This record was updated with the SHAs above in a later evidence-only commit after a644dc6; the tested code is a644dc6.
Each member's substantive contribution and artefact: Kamalpreet Singh — branch preparation with the tool, regression tests, both repairs, refactor and this record. [TO FILL: Dillan, Kyle and Andy]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [TO FILL after the Copilot review]
2. What evidence changed your group's view? For F8-02 the first idea was that cancellation deleted the appointment. Checking list_appointments() after cancellation showed the object was still stored and CANCELLED, while store.find_appointment returned None. That moved the diagnosis from removal to the lookup filter in data_store.py. For F8-01, booking a different practitioner being rejected showed the comparison was inverted rather than missing.
3. How did regression tests protect the refactoring? The refactor started from 61 passing tests and ended with the same 61 passing. The F8-01 regression and the rebooking tests would fail if the enum comparison matched the wrong statuses, for example if cancelled appointments still blocked a slot, so a passing run shows the conflict rule behaves exactly as before.

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: Reproduce the failure, read the exact error and test line, state the expected behaviour from a requirement, and test a hypothesis with evidence before editing anything.

2. Where should expected behaviour come from during debugging?

Response: From the published requirements and acceptance criteria (revision 2 of the assignment overview), not from what the code currently does or what a test happens to assert.

3. What is a debugging hypothesis?

Response: A specific, testable explanation of a failure that names a likely cause and a check that would confirm or reject it.

4. What is a regression test and why is it retained?

Response: A test that reproduces a fixed defect and is kept in the suite so the same defect cannot return unnoticed in later changes.

5. What is meant by root cause?

Response: The underlying decision in the code that makes the failure happen, as opposed to the place where the failure is observed.

6. What is refactoring?

Response: Changing the internal structure of code to make it clearer or easier to maintain while keeping its external behaviour exactly the same.

7. What is a swallowed exception?

Response: An exception that is caught and ignored, or replaced with a default, so the failure is hidden and the caller never learns that something went wrong.

8. What is a code smell?

Response: A sign in the code that suggests a design or maintenance problem, such as duplication, long methods, magic values or unclear names. It is not itself a defect.

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: As unverified hypotheses. Each suggestion is checked against the requirements, the actual code and a real test run, then accepted, modified or rejected with a reason. Copilot does not replace human diagnosis or review.

10. What is the Stage 8 engineering rule?

Response: Diagnose before you fix: reproduce, form and test a hypothesis, make the smallest supported repair, keep a regression test, refactor only under passing tests, and integrate after human review.

## L. Completion and handover

- [x] Existing project, earlier tests and stage records preserved.
- [x] Passing Stage 7 SHA and safe preparation details recorded.
- [x] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [x] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [x] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [x] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: Tested integrated code a644dc6e25af3b77b220727280ec82cdc3793af9; the following commit only adds evidence to this record.
Unresolved issues or incomplete checks / owner / next action: Human-first hypotheses (E), the Copilot review (F) and reflection 1 are still to be completed by Kamalpreet Singh. PR #9 had no another-member review before merge.
Handover note: Both defects are repaired with regression tests, one refactor is complete and the full suite passes (61). Stage 9 can start after this branch is reviewed, merged and verified on main.
