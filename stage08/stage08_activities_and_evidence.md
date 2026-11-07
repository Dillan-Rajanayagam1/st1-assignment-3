# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [complete]
Members and UG/PG cohorts: [complete]
Record owner / contribution links for each member: [complete]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
    Classification: Symptom.
    Reason: This describes the observed problem but does not explain its cause. It does not establish whether the appointment was removed from storage or simply not returned by a lookup.
- The data-store removal path is probably being called.
    Classification: Hypothesis.
    Reason: This proposes a possible explanation that needs evidence. Our current SmartCareDataStore has no public delete operation, so we must not assume that a removal path exists or was called.
- The failing test shows store.find_appointment('A1') returns None.
    Classification: Evidence. 
    Reason: This reports a specific result from a named operation. It supports investigating lookup behaviour but does not by itself prove that the appointment has been deleted.

- The service layer is badly designed.
    Classification: Opinion.
    Reason: This is a broad judgement without a specific cause, supporting observation or test that could confirm it. A useful hypothesis would identify a particular code decision
   and explain how to check it.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.
    Classification: Evidence within the example.
    Reason: A traceback provides an execution location and call path, but the location where a failure appears may differ from its root cause. Line 42 is illustrative, not a confirmed line from our run.
Response and reason: [complete]

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: [complete]

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: [

    A test that expects cancelled appointments to be deleted is incorrect because it contradicts FR-07, which requires cancelled history to be retained. We should correct the test rather than change the application to delete the appointment. The test should check that the appointment has CANCELLED status, remains in the store and can still be retrieved as the same object. Similarly, a test that expects different practitioners booked at the same time to conflict does not reflect AC-04.2. Different practitioners are allowed to have appointments at the same time. The test should accept this case while checking that a second SCHEDULED appointment for the same practitioner at the same time is rejected. These examples show why a failing test does not automatically mean the application is wrong. We need to compare the test's expectation with the published requirement before deciding whether to change the test or repair the implementation.
]

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: [

    The hypothetical 70-line method combines several responsibilities, including validation, storage access, workflow logic and printing. This makes it harder to understand, test and change. Repeated status strings increase the risk of inconsistent comparisons, while four nested conditionals make the different execution paths difficult to follow. Small refactorings could include extracting genuinely repeated logic into a focused helper, replacing status strings with the existing AppointmentStatus enum and simplifying nested conditions where the same behaviour can be preserved. Storage operations should use the existing SmartCareDataStore interface rather than directly manipulating its collections. Printing should be separated from service workflow logic where its appropriate. These changes should be made individually under passing tests rather than as a broad rewrite. They must preserve which operations succeed or fail, the exceptions raised, stored-object identity, cancellation transitions and unchanged state after rejected operations.

    Classification of the proposed changes:

    - Rename appt to appointment — Refactoring.
    This improves readability without changing behaviour, provided the rename is applied consistently and does not change the public interface.

    - Extract a repeated conflict helper — Refactoring.
    This reduces duplication, provided it preserves exactly which bookings are accepted or rejected and does not introduce a new conflict rule.

    - Add rescheduling — Feature.
    This introduces a new operation rather than improving the structure of existing behaviour.

    - Restore retained cancellation lookup — Repair.
    This fixes incorrect behaviour so that cancelled appointments can be retrieved as required. It is not behaviour-preserving refactoring.

    - Replace a magic status string with the existing enum — Refactoring
    Provided the original comparison was already correct and the change preserves its outcome. If it fixes an incorrect comparison, it should instead be recorded as a repair.

]

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: [complete]

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: [

    Changing code immediately after seeing a failure can lead us to fix the visible symptom rather than the underlying cause. We might also change behaviour that was already correct or make several edits without knowing which one affected the result. A better approach is to reproduce the failure, check the expected behaviour against the requirements and form a testable explanation. We should then inspect evidence that can distinguish possible causes before making the smallest justified repair. Keeping a regression test helps us confirm that the repair addresses the original problem and detect whether it returns during later changes.

]


Classification responses (1–5, each with reason): [complete]
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: [complete]
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: [complete]

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: [complete]
- Baseline test command / working directory / observed result / evidence: [complete]
- Clean preparation SHA if a record-only commit followed Stage 7: [complete]
- Branch and preparer / how teammates obtained this branch: [complete]
- Downloaded tool version, source SHA256 and --check outcome: [complete]
- --apply and --verify output summaries / artefact references: [complete]
- Bounded diff inspected and recovery location (not committed): [complete]
- Prepared faulty-state commit SHA: [complete]
- Preparation or recovery issues and resolution, if any: [complete]
- Initial prepared full-suite command / result / key failures: [complete]

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: [complete]
- Expected behaviour and requirement: [complete]
- Minimal synthetic reproduction steps: [complete]
- Meaningful failing test path/name and exact relevant failure: [complete]
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: [complete]
- Expected behaviour and requirement: [complete]
- Minimal synthetic reproduction steps: [complete]
- Meaningful failing test path/name and exact relevant failure: [complete]
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: [complete]
Evidence intended to inspect / competing explanation / discriminating check: [complete]
Member and saved sequence/time or commit showing this preceded consultation: [complete]

### F8-02 human entry
Likely cause and why plausible: [complete]
Evidence intended to inspect / competing explanation / discriminating check: [complete]
Member and saved sequence/time or commit showing this preceded consultation: [complete]

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

### F8-02 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | [complete] | [complete] | [complete] |
| F8-02 after repair | [complete] | [complete] | [complete] |
| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [An engineer should reproduce the failure, record what happened and compare it with the expected behaviour from the requirements. They should then form a testable hypothesis and inspect evidence before making a change. This helps avoid fixing a symptom while leaving the underlying cause unresolved.]

2. Where should expected behaviour come from during debugging?

Response: [Expected behaviour should come from the published requirements, acceptance criteria and documented contracts. We should not assume that the current implementation, an existing test or an AI suggestion is correct without checking it against those sources.]

3. What is a debugging hypothesis?

Response: [A debugging hypothesis is a possible explanation for an observed failure that can be tested using evidence. It should identify what might be causing the problem and what we could inspect or run to support or reject that explanation.]

4. What is a regression test and why is it retained?

Response: [A regression test checks required behaviour to detect whether later changes break it. When added for a defect, it should fail for the relevant incorrect behaviour and pass after the repair. We retain it so that the same problem can be detected if it returns during future development or refactoring.]

5. What is meant by root cause?

Response: [The root cause is the underlying reason a failure occurs, supported by code or execution evidence. It is different from the visible symptom or the location where an error appears. Identifying it helps us repair the source of the problem rather than hide its effects.]

6. What is refactoring?

Response: [Refactoring improves the internal structure of code without changing its required external behaviour. Examples include clarifying names or extracting genuinely repeated logic into a helper. It should preserve results, exceptions and state changes rather than introduce a feature or fix incorrect behaviour.]

7. What is a swallowed exception?

Response: [A swallowed exception occurs when code catches an exception and ignores or suppresses it without appropriate handling or reporting. This can hide a failure and allow execution to continue as though the operation succeeded, making the problem harder to diagnose.]

8. What is a code smell?

Response: [A code smell is a warning sign that code may be difficult to understand, maintain or change. Examples include duplicated logic, unclear names, deep nesting and methods with too many responsibilities. A smell suggests that improvement may be useful, but it does not prove that the code behaves incorrectly.]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [Copilot-generated diagnoses should be treated as hypotheses rather than confirmed explanations. We should check them against the actual code, requirements, reproduction results and tests. Each significant suggestion should be accepted, modified or rejected with a reason. A convincing explanation remains unverified until evidence supports it.]

10. What is the Stage 8 engineering rule?

Response: [Diagnose before you fix. Reproduce the failure, establish the expected behaviour, record human hypotheses and inspect evidence before making the smallest justified repair. Retain regression tests and carry out refactoring only when the required behaviour is passing its checks.]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
