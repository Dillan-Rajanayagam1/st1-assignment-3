# Stage 7 Testing and Verification Record

Group/tutorial: [Tue 1:30 - 3:30 Group 5]  
Members/cohorts: Dillan Rajanayagam (Dillan-Rajanayagam1, UG), Kyle Carasig (KhenZ07, UG), Andy Lieu (Andy-Lieu, UG), Kamalpreet Singh (kamal824, UG)
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement                         | Positive test                                                        | Negative test                                                     | Key assertion                                                                        |
|-------------------------------------|----------------------------------------------------------------------|-------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| FR-01 Register patient              | Register a patient with a valid ID and name                          | Register a patient with an empty name                             | Valid patient is saved; invalid patient raise ValueError                             |
| FR-05 Prevent practitioner conflict | Book two appointments with different  practitioners at the same time | Book two appointments with the same practitioner at the same time | Different practitioners are accepted; conflicting booking is rejected                |
| FR-06 Cancel appointment | Cancel an existing SCHEDULED appointment | Cancel an appointment ID that does not exist | Existing appointment becomes CANCELLED; unknown ID raises LookupError and nothing changes |
| FR-07 Retain cancelled history | Cancel an appointment and retrieve it again | Retrieve an appointment ID that was never created | Cancelled appointment is still stored with CANCELLED status; an unknown ID raises LookupError through the service |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement:  Weak/unclear  Why: It always passes and doesn't check SmartCare behaviour

`assert appointment is not None`
Judgement: Weak/unclear  Why: It only checks that an object is exists, not that its details are correct

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: Strong for stated behaviour  Why: It checks the exact cancellation status, assuming the cancellation requirements are met

`assert len(results) > 0`
Judgement: Weak/unclear  Why: It checks that something was returned but not whether the correct appointment was found

`assert data_store.find_appointment('A1') is appointment`
Judgement: Strong for stated behaviour  Why: It checks that the exact appointment object is retrieved. It doesn't prove correct field values

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract: 

| Input                                   | Expected Result                                                         | Supporting Contract                                                    |
|-----------------------------------------|-------------------------------------------------------------------------|------------------------------------------------------------------------|
| Blank Patient ID                        | Reject registration or booking                                          | Patient ID must be valid                                               |
| Whitespace-only patient name            | Reject the patient                                                      | Name must contain valid text                                           |
| Same Practitioner and same time         | Reject second booking                                                   | Practitioner cannot have conflicting appointments                      |
| Same Practitioner and different time    | Accept booking                                                          | Different booking times do not clash                                   |
| Different Practitioner and same time    | Accept booking                                                          | Conflict rule only applies to the practitioner, not every appointment  |
| Cancelled appointment                   | Keep history and allow the practitioner to be booked again at that time | Cancelled appointments are recorded but are not longer active bookings |
| Cancel an already cancelled appointment | Raise ValueError; status stays CANCELLED | Appointment.cancel only allows SCHEDULED to CANCELLED |
| Cancel a COMPLETED appointment, or create one with an unsupported status | Raise ValueError; status unchanged | Appointment.cancel guard and AppointmentStatus validation |
| Cancel an unknown appointment ID | Raise LookupError | Service lookups report absence with LookupError and must not modify other appointments |

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate                         | What is wrong                                                        | Rewritten test intention                                                             |
|-----------------------------------|----------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| 1. assert True                    | Does not test any behaviour                                          | Verify that registering a valid patient stores the expected patient details          |
| 2. assert appointment is not None | Does not check appointment correctness                               | Verify the appointment has the correct patient, practitioner, time and inital status |
| 3. assert appointment is not None | Repeats a weak assertion and may pass even if the operation is wrong | Verify cancellation changes the appointment status to cancelled                      |
| 4. SMS notification is expected   | SMS functionality is not in the SmartCare requirements               | Test the required booking result without assuming notifications exist                |
| 5. SMS notification is expected   | Invents a feature and may depend on an unsupported external service  | Verify that an invalid booking is rejected and no appointment is added               |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
100% code coverage means every line of code was used during testing, but it doesn't prove that the code works correctly. Tests may use weak assertions, fail to check important outcomes or ignore invalid inputs. For example, a test that executes the booking function and only asserts True could achieve coverage without checking whether the appointment was actually booked correctly. Good verification needs meaningful assertions that compare the actual result with the expected behaviour.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| FR-01 | Valid patient can be registered | TEST-01 | Positive | tests/test_booking_and_cancellation.py::test_register_valid_patient | Patient is stored with matching ID and name | Passed | Student-authored |
| FR-01 | Blank or whitespace-only name is rejected | TEST-02 | Negative | tests/test_booking_and_cancellation.py::test_blank_patient_name_rejected | ValueError; no patient stored | Passed | Student-authored |
| FR-05 | Practitioner cannot have two SCHEDULED appointments at the same time | TEST-03 | Negative | tests/test_booking_and_cancellation.py::test_same_practitioner_same_time_rejected | Second booking raises ValueError; store keeps only the first | Passed | Student-authored |
| FR-05 | Different practitioners can be booked at the same time | TEST-04 | Positive | tests/test_booking_and_cancellation.py::test_different_practitioner_same_time_allowed | Both appointments are stored | Passed | Student-authored |
| FR-06 | Scheduled appointment can be cancelled | TEST-05 | Positive | tests/test_booking_and_cancellation.py::test_cancel_changes_status | Stored appointment becomes CANCELLED | Passed (domain transition through the stored object) | Student-authored |
| FR-06 | Unknown appointment cannot be cancelled | TEST-06 | Negative | tests/test_booking_and_cancellation.py::test_cancel_unknown_appointment_rejected | LookupError; existing appointment unchanged | Passed after cancel_appointment was implemented (issue #2); was an expected failure at the first Stage 7 run | Student-authored |
| FR-07 | Cancelled appointment stays in history | TEST-07 | Positive | tests/test_booking_and_cancellation.py::test_cancelled_appointment_retained | Same object still retrievable with its details and CANCELLED status | Passed | Student-authored |
| FR-05, FR-06 | Supplied foundation checks | Supplied | Mixed | tests/test_starter.py (8 tests) | Registration, booking, duplicates, conflict and domain cancellation guard | Passed | Supplied |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| TEST-01 | FR-01 | Valid patient registration succeeds | Positive | Register a patient with valid details | Stored patient is the same object with matching ID and name | Checks stored values and identity |
| TEST-02 | FR-01 | Invalid name is rejected | Boundary | Register a patient with a whitespace-only name | ValueError; patient list stays empty | Tests the whitespace boundary and unchanged state |
| TEST-03 | FR-05 | Conflicting booking rejected | Negative | Book the same practitioner and time twice | ValueError; only the first appointment is stored | Checks no partial booking is added |
| TEST-04 | FR-05 | Non-conflicting booking accepted | Positive | Book different practitioners at the same time | Both bookings stored | Checks the conflict rule is not too broad |
| TEST-05 | FR-06 | Cancellation updates status | Positive | Cancel an existing appointment | Stored appointment status is CANCELLED | Checks the actual status on the stored object |
| TEST-06 | FR-06 | Unknown appointment rejected | Negative | Cancel an unknown ID through the service | LookupError; existing appointment stays SCHEDULED | Checks error type and unchanged state |
| TEST-07 | FR-07 | Cancelled history is retained | Positive | Cancel, then retrieve the appointment | Same object retrievable, details unchanged, status CANCELLED | Checks retention, not only the status change |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| TEST-01 | Fresh store and PatientService | Register patient P9 | store.find_patient('P9') is the returned patient; ID and name match | Checks the actual stored object, not just that something exists |
| TEST-02 | Fresh store and PatientService | Register with name '   ' | pytest.raises(ValueError); list_patients() == [] | Checks validation and unchanged state |
| TEST-03 | Two patients, practitioner D1, first booking at 09:00 | Book D1 again at 09:00 | pytest.raises(ValueError); list_appointments() == [first] | Checks conflict rejection and no mutation |
| TEST-04 | Two patients, practitioners D1 and D2 | Book D1 and D2 at the same time | list_appointments() == [first, second] | Ensures same time alone is not rejected |
| TEST-05 | Booked appointment A1 | appointment.cancel() | find_appointment('A1').status is CANCELLED | Checks the required state change on the stored object |
| TEST-06 | Booked appointment A1 | cancel_appointment('A9') | pytest.raises(LookupError); A1 still SCHEDULED | Checks the service contract's exception and unchanged state |
| TEST-07 | Booked appointment A1 | Cancel, then find_appointment('A1') | Returns the same object; list unchanged; patient and time unchanged | Checks retention, not just cancellation |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| TEST-08 | Patient accepts valid details (trimmed ID and name) | tests/test_domain.py::test_patient_valid_details | Passed |
| TEST-09 | Patient rejects blank, whitespace-only or None name | tests/test_domain.py::test_patient_blank_name_rejected (3 cases) | Passed |
| TEST-10 | Practitioner accepts valid details | tests/test_domain.py::test_practitioner_valid_details | Passed |
| TEST-11 | Appointment starts SCHEDULED with its details | tests/test_domain.py::test_appointment_initial_status | Passed |
| TEST-12 | Cancelling a SCHEDULED appointment makes it CANCELLED | tests/test_domain.py::test_appointment_cancel | Passed |
| TEST-13 | Repeated cancellation raises ValueError and keeps CANCELLED | tests/test_domain.py::test_repeated_cancel | Passed |
| TEST-14 | Cancelling a COMPLETED appointment raises ValueError and keeps COMPLETED | tests/test_domain.py::test_invalid_status_transition | Passed |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| TEST-15 | Service books a valid appointment with expected details | FR-05 booking contract | tests/test_booking_and_cancellation.py::test_service_books_appointment | Passed |
| TEST-16 | Service rejects practitioner conflict | FR-05 | tests/test_booking_and_cancellation.py::test_same_practitioner_same_time_rejected (shared with TEST-03) | Passed |
| TEST-17 | Service accepts different practitioners at same time | FR-05 | tests/test_booking_and_cancellation.py::test_different_practitioner_same_time_allowed (shared with TEST-04) | Passed |
| TEST-18 | Service cancels and returns the same stored object | FR-06 | tests/test_booking_and_cancellation.py::test_service_cancel | Passed after cancel_appointment was implemented (issue #2); was an expected failure at the first Stage 7 run |
| TEST-19 | Service rejects a blank cancellation ID with ValueError | FR-06 | tests/test_booking_and_cancellation.py::test_service_cancel_blank_id | Passed after cancel_appointment was implemented (issue #2); was an expected failure at the first Stage 7 run |
| TEST-20 | Service keeps the cancelled appointment retrievable | FR-07 | tests/test_booking_and_cancellation.py::test_service_retains_cancelled_history | Passed after cancel_appointment was implemented (issue #2); was an expected failure at the first Stage 7 run |

The four service-cancellation tests first used a strict xfail marker that expected NotImplementedError. When cancel_appointment was implemented (issue #2) the marker was removed and all four now pass.

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| Patient registration | Empty or whitespace-only patient ID | ValueError | TEST-21 (tests/test_domain.py::test_patient_empty_id_rejected) |
| Patient registration | Whitespace-only name | ValueError; nothing stored | TEST-02 |
| Booking | Same practitioner, same time | ValueError; only first booking stored | TEST-03 |
| Booking | Same practitioner, different time | Accepted; both stored | TEST-22 (tests/test_booking_and_cancellation.py::test_same_practitioner_different_time_allowed) |
| Booking | Different practitioner, same time | Accepted; both stored | TEST-04 |
| Cancellation | Cancelled appointment | Record retained and slot can be rebooked | TEST-07, test_cancelled_appointment_allows_rebooking |
| Cancellation | Unknown appointment ID | LookupError; nothing changed | TEST-06 |
| Status | Unsupported status value | ValueError | TEST-23 (tests/test_domain.py::test_unsupported_status_value_rejected) |
| Status | Cancel then cancel again | ValueError; stays CANCELLED | TEST-13 |
| Status | Cancel a COMPLETED appointment | ValueError; stays COMPLETED | TEST-14 |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: FR-05 - Prevent practitioner conflict
Acceptance criterion: A practitioner cannot have two active appointments at the same time
Behaviour to test: The service rejects a second appointment for the same practitioner and time without adding it to the appointment store
Human-first test idea/categories:
Positive: Different practitioners at same time
Negative: Same practitioner and same time
Boundary: Same practitioner at different time
State: Cancelled appointment should not block a new booking

Prompt and purpose: Generate pytest tests for SmartCare's appointment service. Use the requirement that one practitioner cannot have two active appointments at the same time. Include a conflicting booking, a different practitioner at the same time, and a cancelled appointment case. Do not invent notifications, payment features or other requirements.

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: Same practitioner/time rejected 
- What it claims to verify: Prevents double booking
- Requirement trace: FR-05
- Assertion quality: Strong if state and exception are checked
- Human critique: Must confirm exact exception and unchanged state
- Decision: Modify
- Reason: The test should check that the system raises the correct exception when the same practitioner is booked at the same time
- Final test reference if accepted/modified: test_same_practitioner_same_time_rejected
- Actual verification result: Complete

- Copilot test idea/candidate: Different practitioner/time accepted
- What it claims to verify: Allows valid concurrent bookings
- Requirement trace: FR-05
- Assertion quality: Strong if both appointments retrieved
- Human critique: Prevents restrictive logic
- Decision: Accept
- Reason: Accept because the test checks the system allows two appointments at the same time when it's two different practitioners
- Final test reference if accepted/modified: test_different_practitioner_same_time_allowed
- Actual verification result: Complete

- Copilot test idea/candidate: Cancelled appointment allows new booking
- What it claims to verify: Cancelled booking no longer active
- Requirement trace: FR-05
- Assertion quality: Strong if replacement booking succeeds
- Human critique: Require cancellation status
- Decision: Modify
- Reason: The test should also confirm that the original appointment status changes to cancelled before checking that a new booking can be made
- Final test reference if accepted/modified: test_cancelled_appointment_allows_rebooking
- Actual verification result: Complete

- Copilot test idea/candidate: SMS notification on booking
- What it claims to verify: Sends notification
- Requirement trace: No requirement
- Assertion quality: Not relevant
- Human critique: Invented functionality
- Decision: Reject
- Reason: SMS notifications are not included in the SmartCare requirements
- Final test reference if accepted/modified: None
- Actual verification result: Not Run

- Copilot test idea/candidate: assert True after booking
- What it claims to verify: Booking succeeds
- Requirement trace: FR-05
- Assertion quality: Weak
- Human critique: Does not verify any booking outcome
- Decision: Reject
- Reason: assert True always passes and doesn't confirm that the appointment was created or contains correct details 
- Final test reference if accepted/modified: None
- Actual verification result: Not Run

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? assert appointment is not None looks convincing because it confirmed that an appointment object existed. It did not check whether the appointment contained the correct patient, practitioner, time or status
Why was it weak? The test could pass even if the appointment was created with incorrect details 
How did you strengthen it? Assert the expected appointment ID, patient, practitioner, time and status. Check that the service raise the expected exception and that the appointment count stays unchanged
Accepted / modified / rejected test decisions and evidence: Modify the test

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| python3 -m pytest | SmartCare_Starter/project | a41e607a768fcbc7e6e8365d39fa6f64d73e3505 | 44 | 0 (4 xfailed) | No failures. The 4 xfailed tests are the service-cancellation tests. | Unresolved: AppointmentService.cancel_appointment is still a Stage 6 TODO (issue #2), not a product defect in tested code | All 8 starter tests, 16 Stage 6 lookup tests and 20 new Stage 7 tests pass |
| python3 -m pytest | SmartCare_Starter/project | ab00f6b0a91eaa6c192bdf992b69f7e8a1b33c15 (PR #7), rerun on main at 6a9ee19 | 59 | 0 | No failures | None | Rerun after cancel_appointment was implemented: 8 starter, 16 lookup, 11 cancellation and 24 Stage 7 tests pass; the 4 former xfail tests now pass |

Individual test runs and changed-order independence evidence: `python3 -m pytest tests/test_domain.py` (11 passed); `python3 -m pytest tests/test_booking_and_cancellation.py` (9 passed, 4 xfailed); `python3 -m pytest tests/test_booking_and_cancellation.py tests/test_domain.py tests/test_starter.py tests/test_services.py` in reversed file order (44 passed, 4 xfailed). Every test builds its own fresh SmartCareDataStore, so no test depends on another.
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: FR-05 links to TEST-03. A local check temporarily removed the SCHEDULED condition from has_practitioner_conflict; test_cancelled_appointment_allows_rebooking then failed because a cancelled appointment blocked the slot. The change was reverted and the suite passed again. This shows the tests can fail for the right reason; it does not prove every conflict case, such as overlapping durations, which are not part of the requirements.

## K What the Suite Still Does Not Prove

What does your test suite still not prove? It doesn't prove that SmartCare is completely free of bugs or that every possible situation has been tested
Coverage if used: Not measured
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? Service cancellation is only covered by expected-failure tests until issue #2 is done. Invalid date/time input (seconds, timezones) at the service level, query and listing behaviour (Stage 9) and the console menu are not tested. Restart persistence (FR-10) is retired, so it is not tested. Code coverage doesn't prove correctness because a test can execute a line without checking whether the result is correct.
Optional fixtures/parametrisation used and why, if any: Could be used to reuse new SmartCare data and test invalid inputs without copying test code

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| FR-02 patient search (https://github.com/Dillan-Rajanayagam1/st1-assignment-3/issues/1) | feature/patient-lookup | https://github.com/Dillan-Rajanayagam1/st1-assignment-3/pull/3 | No another-member review recorded | None recorded | Merged (fc2c292); Stage 6 tests retained in this run |
| Practitioner lookup (https://github.com/Dillan-Rajanayagam1/st1-assignment-3/issues/4) | feature/practitioner-lookup | https://github.com/Dillan-Rajanayagam1/st1-assignment-3/pull/5 | Dillan requested; verbal only | None recorded | Merged (220d739); Stage 6 tests retained in this run |
| Stage 7 domain, booking and cancellation tests | feature/stage7-tests | https://github.com/Dillan-Rajanayagam1/st1-assignment-3/pull/6 | Dillan requested; he merged it but left no written review or approval | None recorded | Merged by Dillan (fd112f9); 44 passed, 4 xfailed on main |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| Dillan Rajanayagam | Tutorial activities, traceability and test-design tables, Copilot test-design review and formative answers; merged PR #6 | Commits b14fa1b, f5421ce, eaec5f1; merge fd112f9 |
| Kamalpreet Singh | Wrote tests/test_domain.py and tests/test_booking_and_cancellation.py (20 tests plus 4 expected-failure cancellation tests), ran the regression and order checks, corrected the record to match the code and results | https://github.com/Dillan-Rajanayagam1/st1-assignment-3/pull/6, commit a41e607 |
| Kyle Carasig | [TO FILL or not applicable] | |
| Andy Lieu | [TO FILL or not applicable] | |

## N Formative Questions

1. What question does verification answer?
Verification answers the question "Are we building this right?" Verification is checking if the code, design, and data meets specific requirements

2. What question does validation answer?
Validation answers "Are we building the right product?" It checks that the software meets the users' actual needs and the intended requirements, not just that it matches its specification.

3. What is a unit test?
A unit test is a piece of code that tests the smallest piece of software program (e.g. a single function or method) in isolation to make sure it works as intended

4. What is a pytest fixture?
A pytest fixture is a reusable function designed to set up an environment, prepare test data, or manage external resources before the test runs, and cleans them up after it finishes

5. What is parametrisation in pytest?
Parametrisation in pytest is a feature that allows you to run a single test function multiple times with different sets of data

6. What is regression testing?
Regression testing is the process of rerunning software tests after code changes, bug fixes, or updates to ensure that existing features still work as intended and that no new bugs are introduced

7. What does code coverage tell us, and what does it not prove?
Code coverage tells you which part of your source code were executed during testing, but it doesn't prove that your software works correctly or is free of bugs

8. What makes an assertion weak?
An assertion is weak if it can pass even when the required behaviour is wrong. Examples are assert True, checking only that a result is not None, or checking len(results) > 0 instead of the exact object, value, status or exception.

9. What is the appropriate role of GitHub Copilot as a test assistant?
GitHub Copilot can suggest test cases, draft test code and point out edge cases. Every suggestion must be checked against the requirements and the actual code, weak or invented tests rejected, and the tests actually run. Copilot does not decide what is correct.

10. What is the Stage 7 engineering rule?
Every test must trace to a requirement or documented contract, use a meaningful assertion, and be verified by actually running it

## O Stage Completion

Tested Stage 7 main SHA: fd112f9b7c298d9a572b7daba932bf441628d863 (merge of PR #6)
Full-suite result: 44 passed, 4 xfailed with `python3 -m pytest` from SmartCare_Starter/project, on the feature branch at a41e607 and again on main at fd112f9
Unresolved defects and effect on baseline: None after issue #2. cancel_appointment was implemented in the cancellation PR and the four former expected-failure tests were turned into normal passing tests (59 passed).
Clean working tree and integration evidence: Kamalpreet Singh pulled main at fd112f9 and reran the full suite: 44 passed, 4 xfailed. PR #6 was merged by another member (Dillan) but without a written review or approval on GitHub; this is recorded as a process gap.
Stage 8 handover status: Stage 7 tests are integrated on main and issue #2 is resolved, so the full suite passes with no expected failures. Ready for Stage 8 preparation.
All tutorial/formative responses and traceability/Copilot decisions complete: Yes, with the record corrected to match the actual tests and results.
