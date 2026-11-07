# Stage 9 activities and evidence
 ## the part is been done by me 
Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: Tue 1:30 - 3:30 Group 5
Members and responsibilities: Kamalpreet Singh (kamal824, UG) — queries, service listing, interactive menu, tests, README and this record; Dillan Rajanayagam (Dillan-Rajanayagam1, UG), Kyle Carasig (KhenZ07, UG) and Andy Lieu (Andy-Lieu, UG) — review and their own contributions in section H.
Stage 8 integrated SHA, command, working directory and actual result: a644dc6e25af3b77b220727280ec82cdc3793af9 (merge of PR #9); `python3 -m pytest -q` in project/ → 61 passed.

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity | Required session/domain state | Needed for lookup and booking; held by Patient in the shared store (FR-01, FR-02) |
| Appointment history | Required session/domain state | Cancelled appointments are retained and must stay findable and listable (FR-07, FR-08) |
| Temporary menu choice | Transient | Only selects the next action; no requirement needs it after the action runs |
| Practitioner specialty | Required session/domain state | Part of practitioner registration and shown on lookup (FR-03) |
| Debug print output | Transient | Console output only; not part of the domain or the store |
| Appointment status | Required session/domain state | Drives cancellation rules, conflict checks and status filtering |

What is intentionally lost on exit? Everything. The store lives only in memory for one run of the program, so patients, practitioners and appointments (including history) are lost when the menu exits. Restart persistence (FR-10) is retired and no saving was added.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | appointment: Appointment | tuple[datetime, str] | Returns (date_time, appointment_id); no validation, no side effects | Appointment's read-only properties |
| select_appointments | appointments: list[Appointment], practitioner_id: str, status: AppointmentStatus or None | New list[Appointment] holding the same objects | Pure: filters by practitioner and optional status, orders with the named key, never mutates the source or performs I/O | Appointment.practitioner and Appointment.status |
| Service listing | practitioner_id: str, status: AppointmentStatus or None | New ordered list | Validates the ID through the store (ValueError), raises LookupError for an unknown practitioner and ValueError for a non-enum status, then calls select_appointments on store.list_appointments() | SmartCareDataStore.find_practitioner / list_appointments |
| Console | Text typed by the user | Printed messages | Reads input, converts text (date/time, status), calls services, prints results or `Error: ...` and keeps the menu running | parse_date_time, format_appointment and the three services |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: IDs are trimmed, non-blank and case-sensitive strings validated by the domain classes. An appointment holds the actual registered Patient and Practitioner objects, not copies or IDs, so the query compares appointment.practitioner.practitioner_id and returns those same Appointment objects. date_time is a local minute-precision datetime and status is an AppointmentStatus member; the console converts text to these types before calling a service.

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | A domain object performs console I/O | Appointment only enforces the SCHEDULED → CANCELLED rule; the console reads input and calls the service |
| Service prints/reads the menu | Workflow code is tied to the console | Services take typed values and return objects or raise errors; only console.py reads and prints |
| Query sorts its source in place | The pure query mutates its input and changes the store's list order | select_appointments returns a new list with sorted(); the source list is untouched |
| Store prints Appointment saved | The store mixes storage with output | The store only adds, finds and lists; the console reports success |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: `.sort()` reorders the source list in place and returns None. `sorted()` leaves the source order unchanged and returns a new list, so `result is not appointments`, while each element is the same Appointment object. Mutation check: record the source IDs and statuses before the call and assert they are equal afterwards; test_select_returns_new_list_and_leaves_source_unchanged does this, and a deliberate in-place sort inside select_appointments made it fail.

Score-example prediction and explanation of passing the named key: sorting `[('Bo', 7), ('Al', 9), ('Cy', 7)]` with a key that returns the score gives `[('Bo', 7), ('Cy', 7), ('Al', 9)]`; equal scores keep their original order because Python's sort is stable. The function is passed by name (`key=appointment_sort_key`) without calling it, so sorted() calls it once per item. A named key can be reused and tested on its own, and adding the appointment ID as the second value breaks equal-time ties so the order does not depend on insertion order.

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: Cancellation changes the status of the same stored Appointment to CANCELLED and keeps it; deletion would remove the record and lose history, which FR-07 forbids. Checks: after cancelling, find_appointment returns the same object; the default listing (no status) still includes the cancelled appointment in date/time order; and a SCHEDULED filter excludes it while still listing the practitioner's other scheduled appointments.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: The query stays a module-level pure function with explicit inputs instead of a store method, so it can be tested with plain lists and never touches shared state. The service owns validation (unknown practitioner, invalid status) so the query does not need to raise errors. run_menu takes optional input and output functions, defaulting to input and print, so the full menu can be tested with scripted input without changing how it runs for a user. No new classes, storage or dependencies were added.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| Query: a practitioner's appointments (QRY) | Appointments for D1 and D2 | select_appointments (queries.py) | Only D1's appointments | test_select_isolates_practitioner_and_orders_with_id_tie_break |
| Query: optional status filter (QRY) | D1 with SCHEDULED and CANCELLED | select_appointments with each enum value or None | None = all statuses; each enum returns only that status | test_select_status_filter (4 cases) |
| Query: ordering (QRY) | Two D1 appointments at 09:00, one at 10:00 | appointment_sort_key | Date/time, then appointment ID | test_sort_key_is_date_time_then_id; tie-break assertion above |
| Service listing: empty, unknown, invalid (QRY) | Known practitioner with no bookings; unknown ID; blank ID; text instead of enum | AppointmentService.list_practitioner_appointments | [] ; LookupError ; ValueError ; ValueError, store unchanged | test_service_known_practitioner_without_matches_returns_empty_list, …_unknown_…, …_invalid_practitioner_id_…, …_invalid_status_… |
| Pure function (FP) | Store list | select_appointments | New list, source order and objects unchanged, no I/O | test_select_returns_new_list_and_leaves_source_unchanged |
| Named key and repeatability (FP) | Same input twice; already-sorted input; empty list | appointment_sort_key / select_appointments | Same order every time, always a new list | test_select_repeated_calls_and_empty_or_sorted_input, test_named_key_gives_same_order_as_sorted |
| Full menu workflow (UI) | Scripted menu input | run_menu (console.py) | Register, find, book, conflict rejected, other practitioner booked, cancel, find, freed slot rebooked, list all and scheduled, exit | test_full_menu_workflow |
| Invalid-input recovery (UI) | Duplicate, unknown and blank IDs, bad and impossible dates, bad status, unknown choice, repeated cancel | run_menu error handling | `Error: ...` and the menu continues; no partial records | test_invalid_inputs_recover_and_state_is_unchanged |
| FR-05, FR-06/07/08 | Booking and cancellation through the menu | Existing services | Conflict rejected; cancelled appointment still found and listed | Both console tests; test_service_lists_all_statuses_and_keeps_cancelled_history |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: A registered practitioner with no matching appointments is a valid query and returns an empty list; an unregistered ID is unknown and raises LookupError; a blank or non-string ID, or a status that is not an AppointmentStatus, is invalid and raises ValueError. The console converts typed status text to the enum with parse_status (blank means all) and rejects anything else before calling the service. Results contain the same stored Appointment objects, checked with `is`. Every rejected action raises before any store change, and the tests compare the store's list before and after.

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| Practitioner isolation | queries.py select_appointments | D2's B1 never appears in D1's list; every item's practitioner is D1 | Passed | project/tests/test_queries.py |
| Every status and default all | queries.py | None → A1, A2, A3; SCHEDULED → A1, A3; CANCELLED → A2; COMPLETED → [] | Passed | test_select_status_filter |
| Equal-time ID tie-break | appointment_sort_key | A1 and A2 at 09:00 list as A1, A2 although A2 was booked first | Passed | test_select_isolates_practitioner_and_orders_with_id_tie_break |
| Named-key reuse | appointment_sort_key | sorted(..., key=appointment_sort_key) gives the same order as the query | Passed | test_named_key_gives_same_order_as_sorted |
| Repeated calls, empty and already-sorted input | select_appointments | Same order each call; a new list each time, including for [] | Passed | test_select_repeated_calls_and_empty_or_sorted_input |
| Unchanged source order and fields | select_appointments | Source IDs and statuses equal before and after; results are the stored objects | Passed | test_select_returns_new_list_and_leaves_source_unchanged |
| Known-empty / unknown / invalid service cases | services.py list_practitioner_appointments | [], LookupError, ValueError for blank/None IDs and a text status; store unchanged | Passed | test_queries.py service tests |
| Retained history | services.py | Cancelled A2 is listed and is the same object returned by find_appointment | Passed | test_service_lists_all_statuses_and_keeps_cancelled_history |
| Full suite | project/ | `python3 -m pytest -q` | 89 passed (61 earlier + 28 new) | Stage 9 commit, section H |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: select_appointments uses only its arguments, builds its result with a generator and sorted(), and returns a new list. It reads no global or store, has no print or input, and calls no method that changes an Appointment. appointment_sort_key only reads two properties. The same input always gives the same output.
What the tests do and do not establish: They show correct filtering, ordering, tie-breaking, error types, retained history and that the source list is not changed for the cases tested. Deliberately breaking the tie-break, the default status filter or the in-place rule made tests fail. They do not prove behaviour for every possible input, timing or large data, and they test the menu through scripted input rather than a person typing at a terminal.

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | test_full_menu_workflow script: register P1, P2, D1, D2; book A1 (P1, D1, 2026-10-01 09:00); find P1 and D1; book A2 for D1 at the same time; book A3 for D2; cancel A1; find A1; book A4 for D1 at 09:00; list D1 (all, then scheduled); exit | Conflict rejected; D2 booked; A1 cancelled and still found; freed slot rebooked; listing shows cancelled A1 then A4 | As expected; final message "Goodbye. Session-only data is lost on exit." | project/tests/test_console.py |
| UI-02 invalid-input recovery | test_invalid_inputs_recover_and_state_is_unchanged: duplicate patient P1, unknown P9, blank ID, `01/10/2026 9am`, `2026-02-30 09:00`, status `booked`, choice 9, cancel A1 twice | Seven `Error:` messages and one unknown-choice message; menu continues | As expected; the first cancel succeeds, A2 is never created, the final listing shows only cancelled A1 | project/tests/test_console.py |
| Automated service workflow | test_queries.py build_store fixture: book A3, A2 (cancelled), A1 for D1 and B1 for D2 through the services | Listing returns A1, A2, A3 with cancelled A2 retained | As expected | project/tests/test_queries.py |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: Section B (interface decisions and contract table) and the implementation with its tests were written before Copilot was consulted.
Actual prompt/context supplied: Kamalpreet Singh, Microsoft Copilot Chat, 7 November 2026. The prompt stated the query, service and console requirements (pure new list, practitioner and optional status filter with default all, date/time then ID ordering through appointment_sort_key, [] / LookupError / ValueError cases, console recovery) and pasted queries.py, list_practitioner_appointments, parse_status and run_menu. It asked for correctness risks, responsibility violations, weak tests and over-engineering ranked Critical, Important or Optional, without new frameworks or claims that tests ran. A first attempt that only gave the repository link was refused by Copilot because it could not read the source.
Actual response: Copilot found no purity, ordering, filtering or layering violation and listed seven findings: 1 Critical, 4 Important and 2 Optional, summarised in the table below.

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| Invalid practitioner IDs may raise LookupError instead of ValueError | SmartCareDataStore.find_practitioner calls required_text, which raises ValueError for blank, whitespace-only and non-string IDs before any lookup | Critical (Copilot) | Reject: Copilot could not see the store; the code shows the risk does not occur | No change | test_service_invalid_practitioner_id_raises_value_error passes for '', '   ' and None; test_service_unknown_practitioner_raises_lookup_error passes for 'D9' |
| Status filter uses `is` instead of equality | Enum members are singletons; `AppointmentStatus('scheduled') is AppointmentStatus.SCHEDULED` is True | Important (Copilot) | Modify: the identity check is correct and matches the project's existing style, but a test of a text-converted status is useful evidence | Added test_service_accepts_status_converted_from_text | New test passes |
| Service status validation should be tested for non-console callers | The service raises ValueError for any non-enum status; the existing test used only the text 'scheduled' | Important | Accept the test suggestion | Added 123 as a second case to test_service_invalid_status_raises_value_error | Both cases pass and the store is unchanged |
| Appointment-ID tie-break may be under-tested | test_select_isolates_practitioner_and_orders_with_id_tie_break books A2 before A1 at 09:00 and expects A1, A2 | Important | Reject: already covered | No change | Removing the ID from the key made 4 tests fail during verification |
| Empty results vs unknown practitioner may be under-tested | D3 is registered with no appointments while D1 and D2 have bookings → []; D9 → LookupError | Important | Reject: already covered by separate tests | No change | Both tests pass |
| Nested helper functions in run_menu add indirection | Each helper is a few lines and is exercised through the menu tests | Optional | Reject as over-engineering for this size; Copilot itself rated it non-defective | No change | test_full_menu_workflow and test_invalid_inputs_recover_and_state_is_unchanged cover every helper |
| Passing practitioner.practitioner_id instead of the input ID gives no benefit | The stored ID is trimmed; the raw input may contain spaces | Optional | Reject: the claim is wrong | No change | Temporarily passing the raw input made test_service_lists_all_statuses_and_keeps_cancelled_history fail for ' D1 '; reverted |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: Patient, Practitioner and Appointment still validate their own data and Appointment alone changes status. SmartCareDataStore only adds, finds and lists. AppointmentService validates the listing request and delegates filtering and ordering to the pure query in queries.py, which does no I/O and changes nothing. Only console.py reads input and prints, and it reaches the domain only through the services.

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? Making the menu testable without moving console code into the services. Passing input and output functions into run_menu kept all I/O in console.py while letting the tests run the whole workflow against one shared store.
2. Which Copilot suggestion did you reject as over-engineering, and why? Splitting run_menu's small nested helpers into separately addressable functions. Each helper is a few lines that read input, call one service and print a result, and the menu tests already exercise every option, so extra functions would add structure without fixing any defect or improving the evidence.
3. How did you prove cancelled appointments remain retrievable and listable in the same session? test_service_lists_all_statuses_and_keeps_cancelled_history checks that cancelled A2 appears in the default listing and is the same object as find_appointment('A2'), and test_full_menu_workflow cancels A1, finds it again and lists it before the new A4 booking in the same session.

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? It uses only its arguments, returns a new list and has no I/O or hidden state. Sorting the source in place, printing, or reading a global store would break purity.
2. Which explicit inputs are needed, and why avoid a global store? The list of appointments, the practitioner ID and an optional status. Passing them explicitly keeps the function testable with plain lists and stops it depending on or changing shared state.
3. How can a new list reuse Appointment objects safely? The new list holds references to the same Appointment objects. That is safe because the query never changes them; the objects' own methods still guard any state change.
4. Why use a named key, and what breaks equal-time ties? A named key is reusable, testable on its own and clearer than an inline lambda. Adding the appointment ID after the date/time breaks equal-time ties.
5. How do default and explicit status filters differ? The default (None) includes every status, including cancelled history. An explicit AppointmentStatus returns only appointments with that status.
6. How do empty, unknown practitioner and invalid filter cases differ? A known practitioner with no matches returns an empty list; an unknown practitioner raises LookupError; a blank ID or non-enum status raises ValueError.
7. Which console errors recover, and how is unchanged state checked? ValueError and LookupError from bad IDs, duplicates, bad dates, bad status and illegal transitions are caught, printed as `Error: ...` and the menu continues. Tests check that no partial record is created and that later actions still work.
8. What is data integrity for registered participants, conflicts and history? Appointments refer to actual registered participants, a practitioner cannot have two SCHEDULED appointments at one time, and cancelled appointments are kept with their history.
9. What is Copilot's review role, and who verifies findings? Copilot suggests possible problems after the human design and tests exist. The developer checks every finding against requirements, code and test runs, and decides to accept, modify or reject it.
10. How do pure functions and OOP responsibilities work together? Domain classes and services keep the rules and shared state; pure functions such as select_appointments handle filtering and ordering on the data they are given, so each part can be tested on its own.

## H. Review, completion and common handover

Issues and bounded branches: No separate issues were created; the work was done on one bounded branch, feature/stage09, with commit 702f471 ("Final stage 09"), deleted after merge.
PR/diff and another-member human reviewer: https://github.com/Dillan-Rajanayagam1/st1-assignment-3/pull/10. No other member reviewed the PR before it was merged by the author (kamal824); this is a recorded process gap.
Review responses and Copilot comparison: Section E
Integrated common Stage 9 SHA: 911438106f9ea1b94a4c5a32c245f1618d5f85a2 (merge of PR #10)
Full regression command, working directory, actual count/result and evidence: Kamalpreet Singh ran `git switch main`, `git pull`, then `python3 -m pytest -q` in project/ on the merged main → 89 passed. `python3 main.py --interactive` starts the menu and exits cleanly with 0.
README run instructions and scope/limitations: project/README.md (commands, menu options and limitations) and the root README.md group index
Unresolved issues and support/action: No open code issues; all starter TODOs are complete. Process gap: PR #10 had no another-member review before merge. Other members still need to pull main, rerun the suite and add their contribution notes. Owner: Kamalpreet Singh.
UG common candidate / PG future branch plan: All members are UG, so the integrated Stage 9 SHA is the common candidate protected for Stage 12. Stages 10 and 11 are PG-only and not applicable.

- [x] Query contracts, purity, new lists and named-key ordering verified.
- [x] Service empty/unknown/invalid cases and cancellation history verified.
- [x] Every console command and invalid-input recovery demonstrated.
- [x] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [x] Reflections and ten formative responses completed.
- [x] README updated; earlier code/tests/records preserved.
- [x] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
