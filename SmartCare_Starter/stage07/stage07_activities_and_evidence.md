# Stage 7 Testing and Verification Record

Group/tutorial: [Tue 1:30 - 3:30 Group 5]  
Members/cohorts: [complete]
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
| FR-06 Cancel appointment            | Cancel an exisiting appointment                                      | Cancel an appointment that doesn't exist                          | Existing appointment is cancelled; missing appointment raises ValueError             |
| FR-07 Retain cancelled history      | Cancel an appointment and retrieve it again                          | Attempt to retrieve an appointment ID that was never created      | Cancelled appointment remains stored with cancelled status; unkown ID is no returned |

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
| Cancel an already cancelled appointment | Reject or return a defined result                                       | Repeated cancellation behaviour needs a documented contract            |
| Update appointment to an invalid status | Reject the transition                                                   | Appointment status must be one of the supported values                 |
| Cancel an unkown appointment            | Raise ValueError                                                        | Service must not modify unrelated appointments                         |

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

| Requirement | Acceptance criterion                                    | Test ID | Test type | Test name / location                          | Expected behaviour                                    | Result / observed status                       | Supplied or student-authored |
|-------------|---------------------------------------------------------|---------|-----------|-----------------------------------------------|-------------------------------------------------------|------------------------------------------------|------------------------------|
| FR-01       | Valid patient can be registered                         | TEST-01 | Positive  | test_register_valid_patient                   | Patient details are stored                            | Patient can be retrieved with matching details | Student-authored             |
| FR-01       | Invalid name is rejected                                | TEST-02 | Negative  | test_blank_patient_name_rejected              | ValueError is raised                                  | Validation Error; no patient stored            | Student-authored             |
| FR-05       | Practitioner cannot have overlapping active appointment | TEST-03 | Negative  | test_same_practitioner_same_time_rejected     | Conflicting appointment is rejected                   | Second booking rejected                        | Student-authored             |
| FR-05       | Different practitioners can be booked at the same time  | TEST-04 | Positive  | test_different_practitioner_same_time_allowed | Both appointments are stored                          | Both bookings accepted                         | Student-authored             |
| FR-06       | Existing appointments can be cancelled                  | TEST-05 | Positive  | test_cancel_changes_status                    | Appointment status becomes cancelled                  | Status becomes cancelled                       | Student-authored             |
| FR-06       | Unknown appointment cannot be cancelled                 | TEST-06 | Negative  | test_cancel_unknown_appointment_rejected      | ValueError is raised                                  | ValueError; no existing appoint changed        | Student-authored             |
| FR-07       | Cancelled appointment stays in history                  | TEST-07 | Positive  | test_cancelled_appointment_retained           | Appointment remains retrievable with cancelled status | Appointment still exists and is cancelled      | Student-authored             |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion                | Positive / Negative / Boundary | Test intention                               | Observable result expected                     | Added evidence beyond supplied tests |
|---------|-------------|-------------------------------------|--------------------------------|----------------------------------------------|------------------------------------------------|--------------------------------------|
| TEST-01 | FR-01       | Valid patient registration succeeds | Positive                       | Register a patient with valid details        | Patient can be retrieved with matching details | Checks stored values                 |
| TEST-02 | FR-01       | Invalid name is rejected            | Negative                       | Register a patient with whitespace only name | Validation Error; no patient stored            | Tests whitespace boundary            |
| TEST-03 | FR-05       | Conflicting booking rejected        | Negative                       | Book same practitioner and time twice        | Second booking rejected                        | Checks conflict rules                |
| TEST-04 | FR-05       | Non conflicting booking accepted    | Positive                       | Book different practitioners at same time    | Both bookings accepted                         | Checks conflict is not too broad     |
| TEST-05 | FR-06       | Cancellation updates status         | Positive                       | Cancel existing appointment                  | Status becomes cancelled                       | Checks actual status                 |
| TEST-06 | FR-06       | Unknown appointment rejected        | Negative                       | Cancel unknown ID                            | Cancel unknown ID                              | Checks error and state               |
| TEST-07 | FR-07       | Cancelled history is retained       | Positive                       | Cancel then retrieve appointment             | Cancel then retrieve appointment               | Checks history behaviour             |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange                                                                   | Act                              | Assert                                      | Why meaningful / why assertion proves criterion |
|---------|---------------------------------------------------------------------------|----------------------------------|---------------------------------------------|-------------------------------------------------|
| TEST-01 | Create patient service and valid patient details                          | Register patient                 | Retrieved patient has expected ID and name  | Checks the actual registration result           |
| TEST-02 | Create patient data with whitespace only name                             | Attempt registration             | ValueError and no patient stored            | Checks validation and unchanged state           |
| TEST-03 | Create two patients, one practitioner and service. Book first appointment | Book second appoint at same time | ValueError; appointment counts stays as one | Checks conflict rejection and no mutations      |
| TEST-04 | Create two practitioners and two appointments at same time                | Book both appointments           | Both are retrievable                        | Ensures same time alone is not rejected         |
| TEST-05 | Create and book appointment                                               | Cancel appointment               | Status equals cancelled value               | Checks the required state change                |
| TEST-06 | Create service with no matching appointment                               | Cancel unknown ID                | ValueError; existing records unchanged      | Checks error handling                           |
| TEST-07 | Create and book appointment                                               | Cancel and retrieve it           | Appointment exists and stays cancelled      | Checks retention, not just cancellation         |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID  | Behaviour                                      | Test file/function               | Result   |
|----------|------------------------------------------------|----------------------------------|----------|
| TEST-08  | Patient accepts valid details                  | test_patient_valid_details       | Complete |
| TEST-09  | Patient rejects blank or whitespace only name  | test_patient_blank_name_rejected | Complete |
| TEST-10  | Practitioner accepts valid details             | test_practitioner_valid_details  | Complete |
| TEST-11  | Appointment starts with booked status          | test_appointment_inital_status   | Complete |
| TEST-012 | Appointment cancellation changes status        | test_appointment_cancel          | Complete |
| TEST-013 | Repeated cancellation follows defined contract | test_repeated_cancel             | Complete |
| TEST-014 | Invalid status transition is rejected          | test_invalid_status_transition   | Complete |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour                                            | Requirement / criterion | Test file/function                          | Result   |
|---------|------------------------------------------------------|-------------------------|---------------------------------------------|----------|
| TEST-15 | Service books a valid appointment                    | FR-05                   | test_service_books_appointment              | Complete |
| TEST-16 | Service rejects practitioner conflict                | FR-05                   | test_service_rejects_confliction            | Complete |
| TEST-17 | Service accepts different practitioners at same time | FR-05                   | test_service_allows_different_practitioners | Complete |
| TEST-18 | Service cancels appointment                          | FR-06                   | test_service_cancel                         | Complete |
| TEST-19 | Service rejects unknown cancellation                 | FR-06                   | test_service_cancel_unknown_id              | Complete |
| TEST-20 | Service keeps cancelled appointment                  | FR-07                   | test_service_retains_cancelled_history      | Complete |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour            | Boundary/invalid input            | Expected result                   | Test ID |
|----------------------|-----------------------------------|-----------------------------------|---------|
| Patient Registration | Empty patient ID                  | Reject Registration               | TEST-21 |
| Patient Registration | Whitespace only name              | Reject Registration               | TEST-02 |
| Booking              | Same practitioner, same time      | Reject second active booking      | TEST-03 |
| Booking              | Same practitioner, different time | Accept                            | TEST-22 |
| Booking              | Different practitioner, same time | Accept                            | TEST-04 |
| Cancellation         | Cancelled appointment             | Retain history                    | TEST-07 |
| Cancellation         | Unknown appointment ID            | Raise ValueError                  | TEST-06 |
| Status               | Unsupported status value          | Reject update                     | TEST-23 |
| Status               | Cancel then cancel again          | Follow documented transition rule | TEST-13 |

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
- Reason: The test should check that the system raises the correct expectation when the same practitioner is booked at the same time
- Final test reference if accepted/modified: test_same_practitioner_same_time_rejected
- Actual verification result: Complete

- Copilot test idea/candidate: Different practitioner/time accepted
- What it claims to verify: Allows valid concurrent bookings
- Requirement trace: FR-05
- Assertion quality: Strong if both appointments retrieved
- Human critique: Prevents restrictive logic
- Decision: Accept
- Reason: Accept because the test checks the system allows two appointments at the same time when it's two different practitioners
- Final test reference if accepted/modified: test_different_practitioner_same_time_accepted
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

| Command          | Working directory | Code SHA | Passed  | Failed   | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|------------------|-------------------|----------|---------|----------|-----------------|------------------------------------------|-----------------------------|
| python -m pytest | project/          |          |         |          |                 |                                          |                            |

Individual test runs and changed-order independence evidence: [commands, results, links]
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: The duplicate booking requirement links to TEST-03. The test should observe rejection of a conflicting booking and unchanged appointment count. 

## K What the Suite Still Does Not Prove

What does your test suite still not prove? It doesn't prove that SmartCare is completely free of bugs or that every possible situation has been tested
Coverage if used: Not measured
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? The system still needs tests for persistence after restarting the program, searching patient records, updating patient information, invalid appointment times, appointment status etc. Code coverage doesn't prove correctness because a test can execute a line without checking whether the result is correct.
Optional fixtures/parametrisation used and why, if any: Could be used to reuse new SmartCare data and test invalid inputs without copying test code

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task                       | Branch                           | PR                             | Reviewer | Key feedback                                                                       | Outcome                                     |
|----------------------------------|----------------------------------|--------------------------------|----------|------------------------------------------------------------------------------------|---------------------------------------------|
| Patient registration and details | feature/patient-registration     | PR1 - Patient Registration     | Dillan   | Check that the valid patient details are saved and missing information is rejected | Changes merged after review                 |
| Appointment booking              | feature/appointment-booking      | PR2 - Appointment Booking      | Dillan   | Duplicate bookings for same practitioner and time are rejected                     | Booking validation reviewed and updated     |
| Appointment Cancellation         | feature/appointment-cancellation | PR3 - Appointment Cancellation | Dillan   | Cancellation update the appointment status without deleting its history            | Cancellation behaviour reviewed and updated |
| Appointment testing              | feature/appointment-tests        | PR4 - Appointment Tests        | Dillan   | Replace weak assertions with checks for actual appointment detials and status      | Test assertions improved following feedback |
| JSON data storage                | feature/json-storage             | PR5 - JSON Storage             | Dillan   | Check that the appointment information is saved and loaded correctly               | Presistence changes reviewed                |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution                                                 | Evidence link |
|--------|---------------------------------------------------------------------|--------------|
| Dillan | Designed tests, change tests to requirements and reviewed assertion |              |

## N Formative Questions

1. What question does verification answer?
Verification answers the question "Are we building this right?" Verification is checking if the code, design, and data meets specific requirements

2. What question does validation answer?
Validation answers the questions "Is the data acceptable and safe to use?" Validation is the process of checking and verifying data to ensure it meets correct rules, formats, and constraints before the code is executed.

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
An assertion is weak if it can be easily bypassed, handles error incorrectly, or test conditions that are prone to changing

9. What is the appropriate role of GitHub Copilot as a test assistant?
GitHub Copilot can help suggest test cases, make test code and find possible edge cases

10. What is the Stage 7 engineering rule?
Every test must trace to a requirement or documented contract, use a meaningful assertion, and be verified by actually running it

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
