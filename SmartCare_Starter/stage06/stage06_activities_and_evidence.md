# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Tue 1:30 - 3:30 Group 5
- Members, GitHub usernames and cohorts:
  - Dillan Rajanayagam — Dillan-Rajanayagam1 — UG
  - Kyle Carasig — KhenZ07 — UG
  - Andy Lieu — Andy-Lieu — UG
  - Kamalpreet Singh — kamal824 — UG
- Repository URL: https://github.com/Dillan-Rajanayagam1/st1-assignment-3
- Starting SHA: dd0d9ec417c73d6fd881f1b8b499aea2b5f960c7 (Add shared SmartCare Assignment 3 starter)

## A Requirement to issue activities

### FR-02 Patient Search

- Title: Find a registered patient by ID
- Context: Patients can already be registered through PatientService, but PatientService.find_patient was an unfinished starter method. Staff need to look up an existing patient by ID before booking or checking appointments, and the lookup must return the record already held in the shared SmartCareDataStore rather than a copy.
- Requirement: FR-02 Patient search. A registered patient can be found by patient ID.
- Acceptance criteria:
  1. A known patient ID returns the same Patient object held in the shared data store.
  2. Surrounding whitespace in the ID is trimmed, and IDs remain case-sensitive.
  3. A blank, whitespace-only or non-string ID raises ValueError.
  4. A valid ID that is not registered raises LookupError.
  5. A failed lookup does not create, replace or change any stored patient.
- Scope: In scope: PatientService.find_patient and focused tests in tests/test_services.py. Out of scope: changes to Patient, SmartCareDataStore, the console menu, name-based search and any new dependency.
- Definition of Done: All acceptance criteria are met; focused tests are added; the original starter tests are unchanged and pass; the full suite has been run with the command, directory, observed result and tested SHA recorded; another member has reviewed the actual diff with human observations recorded before Copilot; feedback is resolved; the PR is merged into main; every member has pulled main and the integrated suite passes.
- Owner: Kyle Carasig (KhenZ07)
- Actual issue link: https://github.com/Dillan-Rajanayagam1/st1-assignment-3/issues/1

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: Cancel a scheduled appointment and retain its history
- Context: Appointments can already be booked and retrieved, but AppointmentService.cancel_appointment is unfinished and raises NotImplementedError. The service must be completed so that a scheduled appointment can be cancelled without deleting its record and without bypassing the guarded Appointment.cancel domain rule.
- Requirement: FR-06 Appointment cancellation and FR-07 Retained history. A scheduled appointment can be cancelled, and the cancelled appointment remains stored and retrievable.
- Acceptance criteria:
  1. Cancelling an existing SCHEDULED appointment changes its status to CANCELLED.
  2. The service returns the same Appointment object held in the data store, not a replacement.
  3. After cancellation the appointment is still stored and can be retrieved by ID with its patient, practitioner and time unchanged.
  4. A valid but unknown appointment ID raises LookupError and changes no records.
  5. A blank, whitespace-only or non-string ID raises ValueError and changes no records.
  6. Cancelling an appointment that is already CANCELLED, or one that is COMPLETED, raises ValueError and leaves its status unchanged.
  7. The status change is made through Appointment.cancel, not by the service setting the status directly.
- Scope: In scope: AppointmentService.cancel_appointment and focused tests in tests/test_services.py. Out of scope: changes to the Appointment state rules, the data store, the console menu, rescheduling, deletion of records and any new dependency.
- Definition of Done: As for FR-02: acceptance criteria met, focused tests added, original starter tests unchanged and passing, full-suite evidence recorded with tested SHA, another-member review of the actual diff with the human-first Copilot comparison, feedback resolved, merged into main, every member pulled main and integrated tests pass.
- Owner: Kyle Carasig (KhenZ07) [TO CONFIRM: change if another member takes this PR]
- Actual issue link: https://github.com/Dillan-Rajanayagam1/st1-assignment-3/issues/2

### Practitioner lookup (third Stage 6 service target)

- Title: Find a registered practitioner by ID
- Context: PractitionerService.find_practitioner is the third unfinished Stage 6 service method and still raises NotImplementedError. Booking and later appointment listing depend on finding the stored practitioner object, so the service lookup needs the same contract as patient lookup.
- Requirement: Supporting criterion for the Stage 6 service targets: a registered practitioner can be found by practitioner ID. It is a supporting service operation over practitioners registered under FR-03; FR-03 itself remains the practitioner-registration requirement.
- Acceptance criteria:
  1. A known practitioner ID returns the same Practitioner object held in the shared data store.
  2. Surrounding whitespace is trimmed, and IDs remain case-sensitive.
  3. A blank, whitespace-only or non-string ID raises ValueError.
  4. A valid ID that is not registered raises LookupError.
  5. A failed lookup does not create, replace or change any stored practitioner.
- Scope: In scope: PractitionerService.find_practitioner and focused tests in tests/test_services.py. Out of scope: changes to Practitioner, the data store, the console menu and any new dependency.
- Definition of Done: Same as FR-02.
- Owner: Kamalpreet Singh (kamal824)
- Actual issue link: https://github.com/Dillan-Rajanayagam1/st1-assignment-3/issues/4

## B Commit quality

| Original example                               | Strong or Weak | Reason                                                                                                                      |
|------------------------------------------------|----------------|-----------------------------------------------------------------------------------------------------------------------------|
| changes                                        | Weak           | It does not say what changed or why, so teammates would need to inspect the diff to understand the commit.                  |
| final version                                  | Weak           | It claims the work is finished but does not describe what was added or fixed, and "final" is unclear and rarely stays true. |
| Add patient search by ID                       | Strong         | It clearly names the feature added and suggests one focused change.                                                         |
| fix stuff                                      | Weak           | It is too vague. It does not identify the problem or what was actually fixed.                                               |
| Prevent cancellation of completed appointments | Strong         | It names a specific behaviour being enforced, so the purpose of the change is clear.                                        |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR includes changes that are not needed for appointment cancellation. Renaming patient fields, restructuring unrelated code and adding a dependency make the change much larger than the linked issue requires, and none of them are covered by its acceptance criteria.
- Responsibility and architecture concerns: Cancellation should use the existing AppointmentService, the shared data store and the Appointment.cancel method, so the Appointment object keeps control of its own state changes. The restructuring would need checking to make sure it does not move these rules into the wrong class or bypass them. The new dependency also needs justification, because the runtime currently uses only the standard library.
- Testing and review concerns: Mixing several kinds of change makes it hard to see which lines implement cancellation and which might introduce unrelated bugs. Renamed fields could break other code that uses them. Passing tests alone would not prove the extra changes are safe or needed. The reviewer should read the actual diff and check cancellation status, same-object return, retained retrieval, invalid and unknown IDs and rejected state changes, while confirming the original tests are unchanged.
- Changes to remove or separate, with reasons: Keep this PR focused on the cancellation service, its tests and directly related evidence. Remove the patient field renaming, the unrelated restructuring and the new dependency. If any of them is genuinely useful, propose it through its own issue and PR so it can be justified, tested and reviewed on its own.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: The review does not say which changed lines were checked, how they meet the acceptance criteria or which tests support the conclusion. It gives no test command, observed result or tested SHA. It is not possible to tell whether invalid inputs, object identity, retained history and class responsibilities were checked, or whether unrelated changes were included.
- Follow-up review question 1: Which changed lines meet each acceptance criterion, and are any criteria not covered?
- Follow-up review question 2: What test command, working directory, observed result and code SHA support the claim that the tests pass?
- Follow-up review question 3: Which tests check invalid and unknown IDs, and do their assertions check the specific exceptions required by the service contract?
- Follow-up review question 4: Which assertions show that cancelling returns the same stored object, changes its status to CANCELLED and leaves it retrievable afterwards?
- Follow-up review question 5: Where do the code and tests show that repeated cancellation, and cancellation of a COMPLETED appointment, raise ValueError without changing the appointment's state?
- Additional questions if useful: Does the diff contain anything outside the linked issue's scope, and were the original starter tests left unchanged?

## E Team workflow agreement

| Practice                            | Team agreement                                                                                                                                                                                                               |
|-------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Branch naming                       | feature/short-description, for example feature/patient-lookup, feature/practitioner-lookup and feature/appointment-cancellation.                                                                                             |
| Commit message convention           | Imperative, specific messages that say what changed, such as "Add patient search by ID". Each commit holds one coherent change; vague messages such as "test" or "changes" are not used for feature work.                    |
| PR size                             | One PR per issue, containing only that issue's implementation, tests and directly related evidence.                                                                                                                          |
| Another-member review requirement   | Every PR is reviewed by at least one member who did not write it. The reviewer reads the actual diff against the requirement, acceptance criteria and tests, and records their own observations before consulting Copilot.   |
| Merge rule                          | Merge into main only when the acceptance criteria are met, the full suite passes, feedback is resolved, the Copilot comparison is recorded and another member has approved. The author does not merge without that approval. |
| Significant Copilot disclosure rule | Significant Copilot help is recorded in the PR and in section H, with its purpose, a summary of the output, our checks and whether we accepted, modified or rejected it.                                                     |

## F Issue and backlog index

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| https://github.com/Dillan-Rajanayagam1/st1-assignment-3/issues/1 | FR-02 Patient search | Kyle Carasig (KhenZ07) | Returns the stored Patient for a known ID; ValueError for blank or invalid IDs; LookupError for an unknown valid ID; no records changed. See section A. | Implemented and merged through PR #3 (merge commit fc2c292). [TO CONFIRM: issue closed] |
| https://github.com/Dillan-Rajanayagam1/st1-assignment-3/issues/2 | FR-06 Appointment cancellation and FR-07 Retained history | Kyle Carasig (KhenZ07) [TO CONFIRM] | Seven criteria in section A: CANCELLED status, same object returned, retained and retrievable, LookupError for unknown, ValueError for invalid IDs and illegal transitions, change made through Appointment.cancel. | Open. Not yet implemented on main; work prepared for feature/appointment-cancellation. [TO UPDATE when merged] |
| https://github.com/Dillan-Rajanayagam1/st1-assignment-3/issues/4 | Practitioner lookup (supporting criterion for the Stage 6 service targets) | Kamalpreet Singh (kamal824) | Returns the stored Practitioner for a known ID; ValueError for blank or invalid IDs; LookupError for an unknown valid ID; no records changed. See section A. | Implemented and merged through PR #5 (merge commit 220d739). Merged before another-member approval was recorded; see section G. |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

### PR #3 — Patient search

- PR link and title: https://github.com/Dillan-Rajanayagam1/st1-assignment-3/pull/3 — Add patient search by ID
- Linked issue and requirement: https://github.com/Dillan-Rajanayagam1/st1-assignment-3/issues/1 — FR-02 Patient search
- Feature branch: feature/patient-lookup
- Changed behaviour: Implemented PatientService.find_patient using the existing shared SmartCareDataStore. The service returns the stored Patient object and raises LookupError when a valid ID is not registered. Blank or invalid ID validation, whitespace trimming and case sensitivity are handled by the existing store. Added focused patient-search tests.
- Meaningful commits: [Add patient search by ID](https://github.com/Dillan-Rajanayagam1/st1-assignment-3/commit/83a94bc8696c85eb53602f2045e42ed7bdaa29ba) — changes smartcare/services.py and tests/test_services.py only.
- Test command, directory and observed result:
  - Directory: SmartCare_Starter/project
  - Command: `..\..\.venv\Scripts\python.exe -m pytest`
  - Observed result: 16 passed in 0.10s (eight patient-search cases and the eight starter tests).
  - Tested code SHA: 83a94bc8696c85eb53602f2045e42ed7bdaa29ba
- Another-member reviewer: Not recorded. The merge commit fc2c292 was made by the PR author 11 minutes after the feature commit, and no approval from another member is linked. [TO FILL: link the review if a member did review on GitHub; otherwise leave this as a recorded process gap.]
- Human observations recorded before Copilot: Not recorded for this PR.
- Requirement, responsibilities, test assertions and unrelated-scope checks: The author inspected the staged diff. It contained only the PatientService.find_patient implementation and docstring and the new patient-search tests. No unrelated files were changed.
- Key feedback: None recorded.
- Author response/change and verification: No changes were requested.
- Reviewer recheck and approval: Not recorded.
- Merge outcome and SHA: Merged into main. Merge commit fc2c292fa1c16c9907650514e1dad7817156b19f.
- Significant Copilot assistance: Copilot gave implementation guidance and drafted the patient-search tests. The author checked them against the diff and the full-suite run (section H).
- Linked issue closure: [TO CONFIRM: issue #1 closed after merge]
- Each member updated main: [TO FILL: each member's name and confirmation that they pulled main]
- Integrated verification after merge: [TO FILL: command, directory, observed result and SHA from a member's run on main at fc2c292 or later]

### PR #5 — Practitioner lookup

- PR link and title: https://github.com/Dillan-Rajanayagam1/st1-assignment-3/pull/5 — Add practitioner lookup by ID
- Linked issue and requirement: https://github.com/Dillan-Rajanayagam1/st1-assignment-3/issues/4 — practitioner lookup supporting criterion (practitioners registered under FR-03)
- Feature branch: feature/practitioner-lookup
- Changed behaviour: Implemented PractitionerService.find_practitioner through the shared SmartCareDataStore, following the same contract as patient lookup. It returns the stored Practitioner object and raises LookupError when a valid ID is not registered. Blank or invalid IDs raise ValueError through the store's existing validation. Added eight focused tests covering stored-object identity, trimmed IDs, case sensitivity, an unknown ID and four invalid inputs.
- Meaningful commits: [Add practitioner lookup by ID](https://github.com/Dillan-Rajanayagam1/st1-assignment-3/commit/c23b72218de8afe7f780116708ea1be3aa9e93b5) — changes smartcare/services.py, tests/test_services.py and this record only.
- Test command, directory and observed result:
  - Directory: SmartCare_Starter/project
  - Command: `python3 -m pytest`
  - Observed result: 24 passed in 0.02s (Python 3.15.1, pytest 8.3.5): eight practitioner-lookup cases, eight patient-search cases and the eight starter tests.
  - Tested code SHA: c23b72218de8afe7f780116708ea1be3aa9e93b5
- Another-member reviewer: Dillan Rajanayagam (Dillan-Rajanayagam1) was requested as reviewer on GitHub. He looked over the change and told the author verbally that it was fine, but no GitHub approval or written review was recorded before merge. This is a recorded process gap.
- Human observations recorded before Copilot: Not recorded for this PR.
- Requirement, responsibilities, test assertions and unrelated-scope checks: The author checked the diff before committing. It contains only the find_practitioner implementation and docstring, the new practitioner tests and this record. The store keeps validation, the service only turns an absent result into LookupError, and no replacement Practitioner is created. The eight starter tests are unchanged.
- Key feedback: Verbal only: the reviewer said the change was fine. No written feedback on GitHub.
- Author response/change and verification: No changes were requested.
- Reviewer recheck and approval: Not recorded on GitHub before merge.
- Merge outcome and SHA: Merged into main by the author. Merge commit 220d739bd60bf338c5a5923097558639d4a0bfca.
- Significant Copilot assistance: None (stated in the PR description).
- Linked issue closure: Issue #4 is linked with "Closes #4" and closes when the PR is merged.
- Each member updated main: Kamalpreet Singh switched to main and pulled the merge commit. [TO FILL: Dillan, Kyle and Andy confirm they pulled main]
- Integrated verification after merge: Kamalpreet Singh, directory SmartCare_Starter/project on main at 220d739bd60bf338c5a5923097558639d4a0bfca, command `python3 -m pytest`, observed result 24 passed in 0.02s.

### PR [TO FILL: number] — Appointment cancellation

- PR link and title: [TO FILL: link] — Cancel appointments through the service and retain history
- Linked issue and requirement: https://github.com/Dillan-Rajanayagam1/st1-assignment-3/issues/2 — FR-06 and FR-07
- Feature branch: feature/appointment-cancellation
- Changed behaviour: Implemented AppointmentService.cancel_appointment. It finds the stored appointment through the existing find_appointment method, so blank or invalid IDs raise ValueError and unknown IDs raise LookupError. It then calls Appointment.cancel, so the domain object enforces the SCHEDULED-only rule, and returns the same stored object. Nothing is deleted. Added eleven focused tests covering same-object return, CANCELLED status, retained retrieval with unchanged details, trimmed IDs, an unknown ID, four invalid inputs, repeated cancellation, cancellation of a COMPLETED appointment, and rebooking the freed practitioner slot while the cancelled record is kept.
- Meaningful commits: [TO FILL: commit link] — Cancel appointments through the service and retain history
- Test command, directory and observed result:
  - Directory: SmartCare_Starter/project
  - Command: `..\..\.venv\Scripts\python.exe -m pytest`
  - Observed result: [TO FILL from your own run]
  - Tested code SHA: [TO FILL]
- Another-member reviewer: [TO FILL: name and GitHub username; must not be the author]
- Human observations recorded before Copilot: [TO FILL]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [TO FILL]
- Key feedback: [TO FILL]
- Author response/change and verification: [TO FILL]
- Reviewer recheck and approval: [TO FILL: link to the approving review]
- Merge outcome and SHA: [TO FILL]
- Significant Copilot assistance: [TO FILL or "none"]
- Linked issue closure: [TO FILL: issue #2 closed]
- Each member updated main: [TO FILL]
- Integrated verification after merge: [TO FILL]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

### Patient-search PR review

- Member and task: Kyle Carasig — review of the patient-search change (issue #1, PR #3)
- Prompt/purpose and relevant issue/diff: Asked Copilot to review the patient-search diff against its linked requirement, acceptance criteria, responsibility boundaries and tests.
- Summary of output: Copilot found no critical or important issues in the supplied code and tests. It concluded that the implementation met the patient-search contract by delegating to the shared store, returning the stored Patient object and raising LookupError when the store returns None. It asked for full-suite execution evidence.
- Human check against actual code, requirements and tests: I inspected the staged implementation and tests before committing. The implementation calls self.data_store.find_patient(patient_id), raises LookupError when the result is None and otherwise returns the same object. The tests check object identity, whitespace trimming, case sensitivity, unknown IDs and invalid inputs. I ran the full suite at the feature commit and it produced 16 passing tests, including the eight starter tests.
- Decision — Accept / Modify / Reject: Accept
- Reason: Keeping the existing delegation pattern keeps the service focused and avoids duplicating the store's validation. No code change was needed. The claim that the tests pass is supported by my own recorded run, not by Copilot's assessment.
- Verification/evidence: Commit 83a94bc8696c85eb53602f2045e42ed7bdaa29ba; directory SmartCare_Starter/project; command `..\..\.venv\Scripts\python.exe -m pytest`; observed result 16 passed in 0.10s.

### Appointment-cancellation PR review

- Member and task: [TO FILL]
- Prompt/purpose and relevant issue/diff: [TO FILL]
- Summary of output: [TO FILL]
- Human check against actual code, requirements and tests: [TO FILL]
- Decision — Accept / Modify / Reject: [TO FILL]
- Reason: [TO FILL]
- Verification/evidence: [TO FILL]

## I Human versus Copilot review comparison

Comparison for the appointment-cancellation PR. The patient-search PR has no human observations recorded before Copilot, so it cannot serve as the required comparison.

- Human reviewer noticed before consulting Copilot: [TO FILL by the reviewer, written before asking Copilot]
- Copilot noticed: [TO FILL]
- Overlap: [TO FILL]
- What did the human reviewer notice that Copilot did not: [TO FILL]
- What did Copilot identify that the human reviewer initially missed: [TO FILL]
- Unsupported or incorrect Copilot suggestion: [TO FILL, or "none identified" with a reason]
- Human judgement accepted, modified or rejected, and why: [TO FILL]
- Which evidence justified merge approval: [TO FILL]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

### Kyle Carasig

- Implementation: Implemented PatientService.find_patient using the shared SmartCareDataStore. The service returns the stored Patient object and raises LookupError when a valid ID is unknown. Commit 83a94bc8696c85eb53602f2045e42ed7bdaa29ba.
- Testing: Added eight patient-search test cases covering stored-object identity, trimmed IDs, case sensitivity, unknown IDs and invalid inputs. Ran the full suite from SmartCare_Starter/project with `..\..\.venv\Scripts\python.exe -m pytest`; observed 16 passed in 0.10s at the feature commit.
- Review: Inspected the staged implementation and test diff before committing, and reviewed it with Copilot (section H).
- Issue refinement: [TO FILL if Kyle wrote issues #1 and #2; otherwise not applicable]
- Design and responsibility discussion: Kept validation and stored-object lookup in SmartCareDataStore. PatientService coordinates the lookup and turns an absent result into LookupError without adding another store.
- Debugging or integration: Pushed feature/patient-lookup and merged PR #3 into main (fc2c292).
- Documentation or team support: Wrote the first version of this Stage 6 record (commit ef23071).

### Dillan Rajanayagam

- Implementation: [TO FILL or not applicable]
- Testing: [TO FILL or not applicable]
- Review: [TO FILL]
- Issue refinement: [TO FILL or not applicable]
- Design and responsibility discussion: [TO FILL or not applicable]
- Debugging or integration: Created the shared group repository and committed the SmartCare starter (dd0d9ec).
- Documentation or team support: [TO FILL or not applicable]

### Andy Lieu

- Implementation: [TO FILL or not applicable]
- Testing: [TO FILL or not applicable]
- Review: [TO FILL]
- Issue refinement: [TO FILL or not applicable]
- Design and responsibility discussion: [TO FILL or not applicable]
- Debugging or integration: [TO FILL or not applicable]
- Documentation or team support: [TO FILL or not applicable]

### Kamalpreet Singh

- Implementation: Implemented PractitionerService.find_practitioner on feature/practitioner-lookup. It delegates to SmartCareDataStore.find_practitioner, so the store's existing validation trims IDs, keeps them case-sensitive and raises ValueError for blank or non-string IDs. The service turns an absent result into LookupError and returns the same stored Practitioner object. No other class was changed.
- Testing: Added eight practitioner-lookup test cases to tests/test_services.py covering stored-object identity, trimmed IDs, case sensitivity, an unknown ID with the store left unchanged, and four invalid inputs ("", whitespace only, None and a number). The full suite, including the eight unchanged starter tests, was run before review (see the practitioner-lookup PR block in section G).
- Review: Checked the PR #5 diff for scope before requesting review. [TO FILL if Kamalpreet reviews another member's PR]
- Issue refinement: Took ownership of the practitioner-lookup supporting criterion and created issue #4 with its acceptance criteria (https://github.com/Dillan-Rajanayagam1/st1-assignment-3/issues/4).
- Design and responsibility discussion: Followed the same pattern as patient lookup so both lookups share one contract. Validation stays in the store and identity stays with the stored object; the service only reports absence as LookupError and does not create a replacement record.
- Debugging or integration: Opened PR #5 linked to issue #4, merged it into main (220d739), then pulled main and ran the integrated suite: 24 passed.
- Documentation or team support: Completed the member details, practitioner-lookup ownership, issue index entry and this contribution record.

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

A high commit count does not necessarily show strong contribution, because work can be split into many small or trivial commits. One coherent commit may deliver a useful, tested behaviour, while many commits may add little value.

For example, the patient-search commit contained the implementation and eight focused test cases. Its value comes from the behaviour it delivered and verified, not from the number of commits. Review, debugging, issue clarification, integration and helping teammates also contribute to a project without always producing many commits. Contribution should therefore be judged by the actual work, its quality and reliability, and the evidence behind it.

## L Stage 6 formative questions

1. What is version control?

Version control records changes to project files over time. It lets a team inspect history, compare versions, recover earlier work and coordinate contributions.

2. Why is a feature branch useful?

A feature branch keeps a focused change separate from main while it is developed, tested and reviewed. This keeps main stable and makes the proposed change easier to inspect.

3. What makes a commit a good engineering commit?

A good engineering commit records one coherent change, avoids unrelated edits and has a meaningful message that says what changed. Related implementation and tests are included together where appropriate. Quality matters more than the number of commits.

4. What is a pull request?

A pull request proposes merging changes from one branch into another. It shows the diff and gives a place to link the requirement, report tests, discuss feedback and obtain review before integration.

5. What is the purpose of code review?

Code review checks whether a change meets its requirement, respects responsibility boundaries, handles errors correctly and has meaningful tests. It also checks readability and unrelated scope, and it spreads understanding of the code across the team.

6. What does a Git diff show?

A Git diff shows the lines added, removed or changed between two versions. For example, `git diff` shows unstaged changes to tracked files, while `git diff --staged` shows the changes staged for the next commit.

7. What is a Definition of Done?

A Definition of Done is the team's agreed standard for when work is complete. For Stage 6, completion means more than writing code: it includes meeting the acceptance criteria, meaningful tests, another-member review, resolved feedback, and appropriate documentation and verification.

8. What is the appropriate role of GitHub Copilot in pull-request review?

Copilot supports review by pointing out possible risks, missing tests and useful questions after the human reviewer has recorded their own observations. Its claims must be checked against the requirements, the code and actual test results. It does not replace human review, approve merges or prove that tests ran.

9. Why should individual contribution not be judged only by commit count?

Commit count does not measure the importance, difficulty or quality of work. It also misses review, debugging, design discussion, issue refinement, integration and mentoring. Contribution should be judged by attributable work, reliability, collaboration and evidence.

10. What is the Stage 6 engineering rule?

Take a focused requirement through a linked issue, feature branch, implementation, meaningful tests, another-member review, resolved feedback, merge and integrated verification. Use Copilot critically and keep evidence for the decisions and results.

## M Completion and handover

- Starting SHA: dd0d9ec417c73d6fd881f1b8b499aea2b5f960c7
- Final Stage 6 code SHA: [TO FILL: main after the cancellation PR is merged]
- Test command: `..\..\.venv\Scripts\python.exe -m pytest`
- Working directory: SmartCare_Starter/project
- Observed result: [TO FILL from your own run on the final Stage 6 code SHA]
- PR and another-member reviewer: PR #3 (no another-member review recorded); PR #5 practitioner lookup (Dillan requested; merged before GitHub approval); [TO FILL: cancellation PR and reviewer]
- Unresolved issue or none: [TO FILL]
- Stage 7 handover status: [TO FILL: ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [TO FILL: SHA of the commit that adds this record; the difference from the tested SHA is evidence-only]

- [ ] Three Stage 6 service targets completed and checked.
- [x] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [x] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.