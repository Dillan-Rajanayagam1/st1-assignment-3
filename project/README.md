# SmartCare v1.0 (Stage 12 common release)

SmartCare is a small console application for a teaching clinic: staff register synthetic patients and practitioners, book appointments, cancel them while keeping history, and list a practitioner's appointments.

Requirements baseline: SmartCare A3 2026 revision 2, common (UG) scope. Verified with Python 3.13 and 3.15.1 and pytest 8.3.5. Runtime uses only the standard library; pytest is the only development dependency.

From this directory, using a Python environment with the development dependency installed:

```sh
python main.py                 # supplied demonstration
python main.py --interactive   # interactive menu
python -m pytest               # full test suite
```

On macOS use `python3` in place of `python`.

If needed in your approved environment: `python -m pip install -r requirements-dev.txt`.

The demo registers synthetic records and books/finds an appointment. All supplied tests pass. Data exists only in this session and is lost on exit; FR-10 restart persistence is retired. Use synthetic information only.

`domain.py` contains the entities, status and guarded cancellation. `data_store.py` holds three dictionaries through add/find/list methods. The three services share that object. Supplied registration, booking, appointment lookup and conflict checking work. IDs are trimmed, non-blank and case-sensitive. Properties provide read-only identity/appointment state; changes go through domain methods. No special architecture terminology is required.

All starter TODOs are complete. Stage 6 added patient/practitioner lookup and cancellation; Stage 8 repaired the practitioner-conflict and cancelled-history lookup defects; Stage 9 added `queries.py` (`appointment_sort_key` and the pure `select_appointments`), `AppointmentService.list_practitioner_appointments` and the interactive menu in `console.py`. No PG rescheduling or assurance work is included.

Interactive menu: 1 register patient, 2 register practitioner, 3 find patient, 4 find practitioner, 5 book appointment, 6 cancel appointment, 7 find appointment, 8 list a practitioner's appointments (status scheduled, cancelled, completed, or blank for all), 0 exit. Invalid input prints `Error: ...` and the menu continues with the session data unchanged. Listings are ordered by date/time, then appointment ID, and include cancelled appointments unless a status filter is chosen. Cancelling an appointment never deletes it: the same appointment stays stored with CANCELLED status and can still be found and listed for the rest of the session.

Limitations: data exists only for the current session; there is no saving, deletion, rescheduling, authentication or patient-conflict rule.

Service booking accepts IDs and a `datetime` (local, minute precision). Console parser accepts exactly `YYYY-MM-DD HH:MM`. Store lookups return None when absent; service lookups raise LookupError. Invalid values, duplicates, conflicts and illegal transitions raise ValueError. Lists are new containers holding the stored objects. No age, duration, patient-conflict or past-date rules apply.

## Structure and responsibilities

- `smartcare/domain.py` — Patient, Practitioner, Appointment and AppointmentStatus; validation and the guarded SCHEDULED → CANCELLED transition.
- `smartcare/data_store.py` — SmartCareDataStore: one in-memory store with add/find/list operations shared by all services.
- `smartcare/services.py` — registration, lookup, booking with the practitioner-conflict rule, cancellation and practitioner listing.
- `smartcare/queries.py` — pure functions `appointment_sort_key` and `select_appointments` (no I/O, no mutation).
- `smartcare/console.py` — date/time and status parsing, formatting, the demo and the interactive menu (the only place with input/output).
- `tests/` — starter, service, domain, booking/cancellation, regression, query and console tests (89).

## Responsible AI and data

GitHub/Microsoft Copilot was used as a reviewer during Stages 8 and 9; every suggestion was checked against the requirements, code and real test runs, and the decisions are recorded in the stage records. Only synthetic data is used; do not enter real patient information.
