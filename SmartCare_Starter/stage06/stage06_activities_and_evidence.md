# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: [response]
- Members, GitHub usernames and cohorts: [response]
- Repository URL: [response]
- Starting SHA: [response]

## A Requirement to issue activities

### FR-02 Patient Search

- Title: [Find a registered patient by ID]
- Context: [Patients can already be registered in the shared in-memory
store, but PatientService.find_patient is unfinished. The service needs to retrieve the correct registered patient and report invalid or unknown IDs clearly.]
- Requirement: [FR-02 Patient Search]
- Acceptance criteria: [Searching a patient ID returns the same Patient object held in the data storage]
- Scope: [Implement PatientService.find_patient in services.py and add focused patient-lookup tests in tests/test_services.py. Use the existing shared store and its validation. Do not add name search, fuzzy search, authentication or unrelated refactoring.]
- Definition of Done: [The feature meets the acceptance criteria, and meaningful tests confirm it works. All eight original tests and the new tests pass. The pull request links to this issue and is reviewed and approved by another group member. The human review is recorded before comparing it with copilot's feedback. After the merge, everyone uploads their copy of main, runs the tests, and record the results in the evidence file ]
- Owner: [Dillan Rajanayagam]
- Actual issue link: [https://github.com/Dillan-Rajanayagam1/st1-assignment-3/issues/1]

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: [Cancel a scheduled appointment and retain its history]
- Context: [Appointment can already be booked and retrieved, but AppointmentService.cancel.appointment is unfinished We need to complete the service so scheduled appointment can be cancelled without deleting their records or bypassing the domain rules]
- Requirement: [FR-06 Appointment cancellation and Fr-07 Retaining its history]
- Acceptance criteria: [
    1. Cancelling an existing SCEDULED appointment changes its status to CANCELLED
    2. The service returns the same Appointment object stored in the data storage, not replacement.
]
- Scope: [response]
- Definition of Done: [response]
- Owner: [response]
- Actual issue link: [response]

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | [select] | [response] |
| final version | [select] | [response] |
| Add patient search by ID | [select] | [response] |
| fix stuff | [select] | [response] |
| Prevent cancellation of completed appointments | [select] | [response] |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: [response]
- Responsibility and architecture concerns: [response]
- Testing and review concerns: [response]
- Changes to remove or separate, with reasons: [response]

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: [response]
- Follow-up review question 1: [response]
- Follow-up review question 2: [response]
- Follow-up review question 3: [response]
- Follow-up review question 4: [response]
- Follow-up review question 5: [response]
- Additional questions if useful: [response]

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | [response] |
| Commit message convention | [response] |
| PR size | [response] |
| Another-member review requirement | [response] |
| Merge rule | [response] |
| Significant Copilot disclosure rule | [response] |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| [issue 1] | [response] | [response] | [response] | [response] |
| [issue 2] | [response] | [response] | [response] | [response] |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: [response]
- Linked issue and requirement: [response]
- Feature branch: [response]
- Changed behaviour: [response]
- Meaningful commits: [links]
- Test command, directory and observed result: [response]
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [response]
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

[response]

## L Stage 6 formative questions

1. What is version control?

[response]

2. Why is a feature branch useful?

[response]

3. What makes a commit a good engineering commit?

[response]

4. What is a pull request?

[response]

5. What is the purpose of code review?

[response]

6. What does a Git diff show?

[response]

7. What is a Definition of Done?

[response]

8. What is the appropriate role of GitHub Copilot in pull-request review?

[response]

9. Why should individual contribution not be judged only by commit count?

[response]

10. What is the Stage 6 engineering rule?

[response]

## M Completion and handover

- Starting SHA: [response]
- Final Stage 6 code SHA: [response]
- Test command: [response]
- Working directory: [response]
- Observed result: [response]
- PR and another-member reviewer: [links]
- Unresolved issue or none: [response]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
