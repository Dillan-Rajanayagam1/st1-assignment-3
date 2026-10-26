# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Tue 1:30 - 3:30 Group 5    
- Members, GitHub usernames and cohorts: Andy
- Repository URL: [response]
- Starting SHA: [response]

## A Requirement to issue activities

### FR-02 Patient Search

- Title: [response]
- Context: [response]
- Requirement: [response]
- Acceptance criteria: [response]
- Scope: [response]
- Definition of Done: [response]
- Owner: [response]
- Actual issue link: [response]

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
| changes | [Weak] | [It does not explain what changed or why, so teammates would need to inspect the difference to understand the commit] |
| final version | [Weak] | [It says the work is finished but does not describe what was added or fixed. It is also unclear what "Final" means] |
| Add patient search by ID | [Strong] | [It clearly describes the feature that is added and suggests one focused change] |
| fix stuff | [Weak] | [It is too vague. It does not identify the problem or explain what actually was fixed] |
| Prevent cancellation of completed appointments | [Strong] | [It describes a specific behaviour being enforced, making the purpose of the change clear] |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: [The PR includes changes that are not needed for appointment cancellation. Remaining patient fields, restructuring unrelated code and adding a dependency make the change larger than the linked issue requires]
- Responsibility and architecture concerns: [Cancellation should use the existing service, shared data store and Appointment.cancel method. The Appointment object should control its own state changes. We would check that the restructuring does not move these rules into the wrong class or bypass them. The new dependency also needs justification because Stage 6 is meant to preserve the existing runtime dependencies]
- Testing and review concerns: [Mixing several kinds of changes makes it harder to see which lines implement cancellation and shich might introduce unrelated bugs. Remaining fields could affect other code that uses them. Passing tests alone would not prove that the extra changes are safe or needed. The reviewer should check the actual difference and check cancellation status, same object return, reatined retrival, invalid IDs and rejected state changes, while keeping the original tests intact]
- Changes to remove or separate, with reasons: [Keep this PR focused on the cancellation service, its tests and directly related evidence. Remove the unrealted patient field renaming and code restruturing from this PR. If those changes are genuinely useful, propose them through separate issues and PRs so they can be justified, tested and reviewed indpendently]

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: [The review does not explain which changed lines were checked, how they meet the acceptance criteria, or which tests support the conclusion. It also gives no test command, observed result or tested code SHA. we cannot tell whether invalid inputs, obect identity, retained appointment history and class responsibilities were checked, or whether unrelated changes were included]
- Follow-up review question 1: [Which changed lines meet each acceptance criterion, and are there any criteria that have not been covered]
- Follow-up review question 2: [What test command, working directory, observed result and code SHA support the claim that tests pass?]
- Follow-up review question 3: [Which tests chack invalid and unknown IDs, and do their assertions check the specific exceptions required by the service contracts]
- Follow-up review question 4: [Which assertions show that cancelling an appointment returns the same stored object, changes its status to CANCELLED and leaves it retrievable afterwards?]
- Follow-up review question 5: [Where do the code and tests show that repeated cancelletion and cancellation of a COMPLETED appointment raise ValueError without changing the appointment's state?]
- Additional questions if useful: [response]

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | [Use short, descriptive names such as feeature / patient lookup] |
| Commit message convention | [Write clear messages the describe what changed, such as "Add patient search by ID". Keep each commit focused on a meaningful message and not vague ones] |
| PR size | [Keep each PR focused on one issue, including its implementation, test and related evidence] |
| Another-member review requirement | [Every PR must be reviewed by at least one group member who did not make it. The reviewer check the actual difference against the requirements, acceptance criteria, and tests] |
| Merge rule | [Merge into main only when the acceptance criteria are met, all available tests pass, feedback is resolved, the required copilot comparison is recorded and another member has approved] |
| Significant Copilot disclosure rule | [Record significant copilot help in the PR and section H, including its purpose, output summary, our chhecks and whether we acccepted] |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| [https://github.com/Dillan-Rajanayagam1/st1-assignment-3/issues/1] | [FR 02 patient Search] | [Kyle (KhenZ07)] | [Return the actual stored patient for a known ID. raises ValueError for blank or invalid IDs, raise LookupError for an unknown valid ID] | [done] |
| [https://github.com/Dillan-Rajanayagam1/st1-assignment-3/issues/2] | [FR 06 Appointment Cancellation and FR 07 Retained History] | [Kyle (KhenZ07)] | [response] | [done] |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: [https://github.com/Dillan-Rajanayagam1/st1-assignment-3/pull/3     Add a patient search by ID]
- Linked issue and requirement: [https://github.com/Dillan-Rajanayagam1/st1-assignment-3/issues/1]
- Feature branch: [ feature/patient-lookup]
- Changed behaviour: [Implemented PatientService.find_patient using the existing shared SmartCareDataStore. The service returns the actual stored Patient object and raises LookupError when a valid ID is unknown. Blank/invalid ID validation, whitespace trimming and case sensitivity are delegated to the existing store. Added focused patient-search tests.]
- Meaningful commits: [Add patient search by ID](https://github.com/Dillan-Rajanayagam1/st1-assignment-3/commit/83a94bc8696c85eb53602f2045e42ed7bdaa29ba)]
- Test command, directory and observed result: [ Directory: SmartCare_Starter/project
  Command: ..\..\.venv\Scripts\python.exe -m pytest
  Observed result: 16 passed in 0.10s.
  This included eight patient-search cases and all eight starter tests.
  Tested code SHA: 83a94bc8696c85eb53602f2045e42ed7bdaa29ba]
- Another-member reviewer: [All members]
- Human observations recorded before Copilot: [not recorded]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [The author inspected the staged diff. It contained only the PatientService.find_patient implementation/docstring and the new patient-search tests.]
- Key feedback: [no changes were requested]
- Author response/change and verification: [no changes were requested]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [copilot provided simple implementation guidance to get the ideas, drafted patient search tests]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [Kyle. Completion of all of stage 06]
- Prompt/purpose and relevant issue/diff: [Asked Copilot to review the patient-search PR against its linked requirement, acceptance criteria, responsibility boundaries and tests.]
- Summary of output: [ Copilot found no Critical or Important issues in the supplied code and tests. It concluded that the implementation appeared to satisfy the patient-search contract by delegating to the shared store, returning the stored Patient object and raising LookupError when
  the store returns None.]
- Human check against actual code, requirements and tests: [ I inspected the staged implementation and tests before committing. The implementation calls self.data_store.find_patient(patient_id), raises LookupError when the result is None and otherwise returns the same object.

The tests shown in the diff check object identity, whitespace trimming, case sensitivity, unknown IDs and invalid inputs. I ran the full available test suite at the recorded feature commit. This produced 16 passing tests, including the eight supplied starter tests.]
- Decision — Accept / Modify / Reject: [Accept]
- Reason: [  I accepted the recommendation to retain the existing delegation pattern because it keeps the service focused and avoids duplicating store validation. No code change was needed in response to this review. The request for execution evidence was supported by my recorded local full-suite run, not by Copilot's assessment alone.]
- Verification/evidence: [Implementation/test commit:
  83a94bc8696c85eb53602f2045e42ed7bdaa29ba

  Working directory: SmartCare_Starter/project
  Command: ..\..\.venv\Scripts\python.exe -m pytest
  Observed result: 16 passed in 0.10s.]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [Copilot identified the use of the shared store, direct return of the stored object, LookupError for an absent valid ID and delegation of validation to the existing store. It recognised tests for identity, whitespace trimming, case sensitivity and invalid/unknown IDs. It found no blocking issue and requested full-suite execution evidence.]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [Kyle]
- Implementation: [  Implemented PatientService.find_patient using the existing shared SmartCareDataStore. The service returns the stored Patient object and raises LookupError when a valid ID is unknown.
Commit: 83a94bc8696c85eb53602f2045e42ed7bdaa29ba]
- Testing: [Added eight patient-search test cases covering stored-object identity, trimmed IDs, case sensitivity, unknown IDs and invalid inputs. Ran the full available suite from SmartCare_Starter/project using:
..\..\.venv\Scripts\python.exe -m pytest
Observed result at the feature commit: 16 passed in 0.10s.]
- Review: [Inspected my staged implementation and test diff before committing.]
- Issue refinement: [not applicable]
- Design and responsibility discussion: [The implementation keeps validation and stored-object lookup in SmartCareDataStore. PatientService coordinates lookup and translates an absent result into LookupError without adding another store.]
- Debugging or integration: [Committed and pushed feature/patient-lookup.]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

[A high commit count does not necessarily show strong contributio because commits can be split into many small or trivial changes One coherent commit may deliver a useful, tested behaviour, while many commits may add little value.

For example, my patient-search commit included the implementatio and eight focused test cases. Its value comes from the behaviour delivered and verified, not from the number of commits. Review,debugging, issue clarification, integration and helping teammates also contribute to the project without always producing many commits. Contribution should therefore be judged using actual work, quality, reliability and supporting evidence.]

## L Stage 6 formative questions

1. What is version control?

[Version control records changes to project files over time. It lets a team inspect history, compare versions, recover earlier work and coordinate contributions.]

2. Why is a feature branch useful?

[A feature branch separates a focused change from main while it is being developed, tested and reviewed. This helps keep main stable and makes the proposed change easier to inspect.]

3. What makes a commit a good engineering commit?

[A good engineering commit records one coherent change, avoids unrelated edits and uses a meaningful message explaining what changed. Relevant implementation and tests should be included together where appropriate. Quality matters more than creating many commits.]

4. What is a pull request?

[A pull request proposes merging changes from one branch into another. It exposes the diff and provides a place to link the requirement, report tests, discuss feedback and obtain review before integration.]

5. What is the purpose of code review?

[Code review checks whether a change meets its requirement, respects responsibility boundaries, handles errors correctly and has meaningful tests. It also checks readability and unrelated scope, while sharing understanding among team members.]

6. What does a Git diff show?

[A Git diff shows the lines added, removed or changed between versions. For example, git diff shows unstaged tracked-file changes, while git diff --staged shows changes staged for the next commit.]

7. What is a Definition of Done?

[A Definition of Done is the team's agreed completion standard. For Stage 6, completion involves more than writing code: it includes meeting acceptance criteria, meaningful tests, another-member review, resolved feedback and appropriate documentation and verification.]

8. What is the appropriate role of GitHub Copilot in pull-request review?

[Copilot supports review by identifying possible risks, missing tests and useful questions after the human reviewer records independent observations. Its claims must be checked against requirements, code and actual test results. It does not replace human review, approve merges or prove that tests ran.]

9. Why should individual contribution not be judged only by commit count?

[Commit count does not measure the importance, difficulty or quality of work. It can also overlook review, debugging, design discussion, issue refinement, integration and mentoring. Contribution should be judged using attributable work, reliability, collaboration and evidence.]

10. What is the Stage 6 engineering rule?

[Take a focused requirement through a linked issue, feature branch, implementation, meaningful tests, another-member review, resolved feedback, merge and integrated verification. Use Copilot critically and retain evidence for the decisions and results.]

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
