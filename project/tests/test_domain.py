"""Stage 7 domain tests for Patient, Practitioner and Appointment."""

from datetime import datetime

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)


WHEN = datetime(2026, 10, 1, 9)


def make_appointment(
    status: AppointmentStatus = AppointmentStatus.SCHEDULED,
) -> Appointment:
    """Create a fresh appointment with synthetic participants."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    return Appointment('A1', patient, practitioner, WHEN, status)


def test_patient_valid_details() -> None:
    """TEST-08: a valid patient keeps trimmed ID and name."""
    patient = Patient('  P1  ', '  Alex Example  ')

    assert patient.patient_id == 'P1'
    assert patient.name == 'Alex Example'


@pytest.mark.parametrize('bad_name', ['', '   ', None])
def test_patient_blank_name_rejected(bad_name) -> None:
    """TEST-09: a blank or whitespace-only patient name is rejected."""
    with pytest.raises(ValueError):
        Patient('P1', bad_name)


def test_patient_empty_id_rejected() -> None:
    """TEST-21: an empty or whitespace-only patient ID is rejected."""
    with pytest.raises(ValueError):
        Patient('', 'Alex Example')
    with pytest.raises(ValueError):
        Patient('   ', 'Alex Example')


def test_practitioner_valid_details() -> None:
    """TEST-10: a valid practitioner keeps ID, name and specialty."""
    practitioner = Practitioner('D1', 'Taylor Example', 'General')

    assert practitioner.practitioner_id == 'D1'
    assert practitioner.name == 'Taylor Example'
    assert practitioner.specialty == 'General'


def test_appointment_initial_status() -> None:
    """TEST-11: a new appointment starts SCHEDULED with its details."""
    appointment = make_appointment()

    assert appointment.status is AppointmentStatus.SCHEDULED
    assert appointment.appointment_id == 'A1'
    assert appointment.patient.patient_id == 'P1'
    assert appointment.practitioner.practitioner_id == 'D1'
    assert appointment.date_time == WHEN


def test_appointment_cancel() -> None:
    """TEST-12: cancelling a SCHEDULED appointment makes it CANCELLED."""
    appointment = make_appointment()

    appointment.cancel()

    assert appointment.status is AppointmentStatus.CANCELLED


def test_repeated_cancel() -> None:
    """TEST-13: a second cancel raises ValueError and keeps CANCELLED."""
    appointment = make_appointment()
    appointment.cancel()

    with pytest.raises(ValueError):
        appointment.cancel()

    assert appointment.status is AppointmentStatus.CANCELLED


def test_invalid_status_transition() -> None:
    """TEST-14: a COMPLETED appointment cannot be cancelled."""
    appointment = make_appointment(AppointmentStatus.COMPLETED)

    with pytest.raises(ValueError):
        appointment.cancel()

    assert appointment.status is AppointmentStatus.COMPLETED


def test_unsupported_status_value_rejected() -> None:
    """TEST-23: a status that is not an AppointmentStatus is rejected."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')

    with pytest.raises(ValueError):
        Appointment('A1', patient, practitioner, WHEN, 'cancelled')
