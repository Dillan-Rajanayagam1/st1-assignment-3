"""Console helpers and a small runnable starting demonstration."""


import re
from collections.abc import Callable
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def parse_date_time(text: str) -> datetime:
    """Parse YYYY-MM-DD HH:MM; raise ValueError for invalid input."""
    if (
        not isinstance(text, str)
        or re.fullmatch(
            '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', text
        ) is None
    ):
        raise ValueError('Use date/time format YYYY-MM-DD HH:MM')
    try:
        return datetime.strptime(text, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError(
            'Invalid calendar date/time; use YYYY-MM-DD HH:MM',
        ) from None


def format_appointment(appointment: Appointment) -> str:
    """Return readable synthetic appointment details without changing
    state.
    """
    return (
        f'{appointment.appointment_id}: '
        f'{appointment.patient.patient_id} with '
        f'{appointment.practitioner.practitioner_id}, '
        f'{appointment.date_time:%Y-%m-%d %H:%M}, {appointment.status.value}'
    )


def run_demo() -> None:
    """Demonstrate supplied registration and booking using synthetic
    records.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner(
        'DR1',
        'Taylor Example',
        'General practice',
    )
    try:
        appointments.book_appointment(
            'A1',
            'P1',
            'DR1',
            parse_date_time('2026-10-01 09:00'),
        )
        print(format_appointment(appointments.find_appointment('A1')))
    except (ValueError, LookupError) as error:
        print(f'Error: {error}')
    print('Session-only data: records are lost on exit.')


MENU = """
SmartCare menu
1. Register patient
2. Register practitioner
3. Find patient
4. Find practitioner
5. Book appointment
6. Cancel appointment
7. Find appointment
8. List practitioner appointments
0. Exit"""


def parse_status(text: str) -> AppointmentStatus | None:
    """Return None for a blank filter, otherwise the matching status.

    Raise ValueError for an unsupported status value.
    """
    value = text.strip().lower()
    if not value:
        return None
    try:
        return AppointmentStatus(value)
    except ValueError:
        raise ValueError(
            'Status must be scheduled, cancelled, completed or blank',
        ) from None


def run_menu(
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> None:
    """Run the register/find/book/cancel/list/exit menu.

    Call services, recover from expected input errors, and keep this
    session's data until exit. Input and output functions can be
    replaced so the workflow can be tested.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    def register_patient() -> None:
        patient = patients.register_patient(
            input_func('Patient ID: '),
            input_func('Patient name: '),
        )
        output_func(f'Registered patient {patient.patient_id}')

    def register_practitioner() -> None:
        practitioner = practitioners.register_practitioner(
            input_func('Practitioner ID: '),
            input_func('Practitioner name: '),
            input_func('Specialty: '),
        )
        output_func(f'Registered practitioner {practitioner.practitioner_id}')

    def find_patient() -> None:
        patient = patients.find_patient(input_func('Patient ID: '))
        output_func(f'{patient.patient_id}: {patient.name}')

    def find_practitioner() -> None:
        practitioner = practitioners.find_practitioner(
            input_func('Practitioner ID: '),
        )
        output_func(
            f'{practitioner.practitioner_id}: {practitioner.name}, '
            f'{practitioner.specialty}',
        )

    def book_appointment() -> None:
        appointment = appointments.book_appointment(
            input_func('Appointment ID: '),
            input_func('Patient ID: '),
            input_func('Practitioner ID: '),
            parse_date_time(input_func('Date/time (YYYY-MM-DD HH:MM): ')),
        )
        output_func(f'Booked {format_appointment(appointment)}')

    def cancel_appointment() -> None:
        appointment = appointments.cancel_appointment(
            input_func('Appointment ID: '),
        )
        output_func(f'Cancelled {format_appointment(appointment)}')

    def find_appointment() -> None:
        appointment = appointments.find_appointment(
            input_func('Appointment ID: '),
        )
        output_func(format_appointment(appointment))

    def list_appointments() -> None:
        practitioner_id = input_func('Practitioner ID: ')
        status = parse_status(
            input_func('Status (scheduled/cancelled/completed, blank = all): '),
        )
        results = appointments.list_practitioner_appointments(
            practitioner_id,
            status,
        )
        if not results:
            output_func('No matching appointments')
        for appointment in results:
            output_func(format_appointment(appointment))

    actions = {
        '1': register_patient,
        '2': register_practitioner,
        '3': find_patient,
        '4': find_practitioner,
        '5': book_appointment,
        '6': cancel_appointment,
        '7': find_appointment,
        '8': list_appointments,
    }
    while True:
        output_func(MENU)
        try:
            choice = input_func('Choice: ').strip()
        except EOFError:
            break
        if choice == '0':
            break
        action = actions.get(choice)
        if action is None:
            output_func('Unknown choice; enter a number from the menu')
            continue
        try:
            action()
        except (ValueError, LookupError) as error:
            output_func(f'Error: {error}')
        except EOFError:
            break
    output_func('Goodbye. Session-only data is lost on exit.')
