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

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: [complete]
Acceptance criterion: [quote]
Behaviour to test: [complete]
Human-first test idea/categories: [complete]
Prompt and purpose: [complete or link]

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: [complete]
- What it claims to verify: [complete]
- Requirement trace: [complete]
- Assertion quality: [complete]
- Human critique: [complete]
- Decision: [Accept / Modify / Reject]
- Reason: [complete]
- Final test reference if accepted/modified: [link or not retained]
- Actual verification result: [complete; do not claim an unrun test passed]

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? [response]
Why was it weak? [response]
How did you strengthen it? [response]
Accepted / modified / rejected test decisions and evidence: [link actual decisions in H]

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

Individual test runs and changed-order independence evidence: [commands, results, links]
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? [response]
Coverage if used: [result or not used]
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? [response]
Optional fixtures/parametrisation used and why, if any: [response or not used]

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| [complete] | [complete] | [complete] |

## N Formative Questions

1. What question does verification answer?
[Verification answers the question "Are we building this right?" Verification is checking if the code, design, and data meets specific requirements]

2. What question does validation answer?
[Validation answers the questions "Is the data acceptable and safe to use?" Validation is the process of checking and verifying data to ensure it meets correct rules, formats, and constraints before the code is executed.]

3. What is a unit test?
[A unit test is a piece of code that tests the smallest piece of software program (e.g. a single function or method) in isolation to make sure it works as intended]

4. What is a pytest fixture?
[A pytest fixture is a reusable function designed to set up an environment, prepare test data, or manage external resources before the test runs, and cleans them up after it finishes]

5. What is parametrisation in pytest?
[Parametrisation in pytest is a feature that allows you to run a single test function multiple times with different sets of data ]

6. What is regression testing?
[Regression testing is the process of rerunning software tests after code changes, bug fixes, or updates to ensure that existing features still work as intended and that no new bugs are introduced]

7. What does code coverage tell us, and what does it not prove?
[Code coverage tells you which part of your source code were executed during testing, but it doesn't prove that your software works correctly or is free of bugs]

8. What makes an assertion weak?
[An assertion is weak if it can be easily bypassed, handles error incorrectly, or test conditions that are prone to changing]

9. What is the appropriate role of GitHub Copilot as a test assistant?
[response]

10. What is the Stage 7 engineering rule?
[response]

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
