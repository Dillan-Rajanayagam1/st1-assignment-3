"""Stage 7 service tests for registration, booking and cancellation."""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


WHEN = datetime(2026, 10, 1, 9)

# Service cancellation (issue #2) is still a Stage 6 TODO. These tests
# are written now and expected to fail with NotImplementedError. They
# are strict, so they will report a failure once cancel_appointment is
# implemented, which tells the team to remove this marker.
NEEDS_SERVICE_CANCELLATION = pytest.mark.xfail(
    raises=NotImplementedError,
    strict=True,
    reason='AppointmentService.cancel_appointment not implemented (issue #2)',
)


def setup_services() -> tuple[
    SmartCareDataStore,
    PatientService,
    PractitionerService,
    AppointmentService,
]:
    """Create a fresh store, two patients and two practitioners."""
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    patients.register_patient('P1', 'Alex Example')
    patients.register_patient('P2', 'Sam Example')
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    practitioners.register_practitioner('D2', 'Morgan Example', 'General')
    return (
        data_store,
        patients,
        practitioners,
        AppointmentService(data_store),
    )


def test_register_valid_patient() -> None:
    """TEST-01: a registered patient is stored with matching details."""
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    patient = service.register_patient('P9', 'Jordan Example')

    assert data_store.find_patient('P9') is patient
    assert patient.patient_id == 'P9'
    assert patient.name == 'Jordan Example'


def test_blank_patient_name_rejected() -> None:
    """TEST-02: a whitespace-only name is rejected and nothing is stored."""
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    with pytest.raises(ValueError):
        service.register_patient('P9', '   ')

    assert data_store.list_patients() == []


def test_service_books_appointment() -> None:
    """TEST-15: a valid booking is stored with the expected details."""
    data_store, _, _, appointments = setup_services()

    appointment = appointments.book_appointment('A1', 'P1', 'D1', WHEN)

    assert data_store.find_appointment('A1') is appointment
    assert appointment.patient.patient_id == 'P1'
    assert appointment.practitioner.practitioner_id == 'D1'
    assert appointment.date_time == WHEN
    assert appointment.status is AppointmentStatus.SCHEDULED


def test_same_practitioner_same_time_rejected() -> None:
    """TEST-03 / TEST-16: a conflicting booking is rejected, store unchanged."""
    data_store, _, _, appointments = setup_services()
    first = appointments.book_appointment('A1', 'P1', 'D1', WHEN)

    with pytest.raises(ValueError):
        appointments.book_appointment('A2', 'P2', 'D1', WHEN)

    assert data_store.list_appointments() == [first]


def test_different_practitioner_same_time_allowed() -> None:
    """TEST-04 / TEST-17: different practitioners may share a time."""
    data_store, _, _, appointments = setup_services()

    first = appointments.book_appointment('A1', 'P1', 'D1', WHEN)
    second = appointments.book_appointment('A2', 'P2', 'D2', WHEN)

    assert data_store.list_appointments() == [first, second]
    assert second.practitioner.practitioner_id == 'D2'


def test_same_practitioner_different_time_allowed() -> None:
    """TEST-22: the same practitioner may be booked at another time."""
    data_store, _, _, appointments = setup_services()
    later = datetime(2026, 10, 1, 10)

    first = appointments.book_appointment('A1', 'P1', 'D1', WHEN)
    second = appointments.book_appointment('A2', 'P2', 'D1', later)

    assert data_store.list_appointments() == [first, second]


def test_cancel_changes_status() -> None:
    """TEST-05: the domain transition changes the stored object's status."""
    data_store, _, _, appointments = setup_services()
    appointment = appointments.book_appointment('A1', 'P1', 'D1', WHEN)

    appointment.cancel()

    assert data_store.find_appointment('A1').status is (
        AppointmentStatus.CANCELLED
    )


def test_cancelled_appointment_retained() -> None:
    """TEST-07: a cancelled appointment stays stored with its details."""
    data_store, _, _, appointments = setup_services()
    appointment = appointments.book_appointment('A1', 'P1', 'D1', WHEN)

    appointment.cancel()

    assert appointments.find_appointment('A1') is appointment
    assert data_store.list_appointments() == [appointment]
    assert appointment.patient.patient_id == 'P1'
    assert appointment.date_time == WHEN


def test_cancelled_appointment_allows_rebooking() -> None:
    """A cancelled slot can be rebooked and the old record is kept."""
    data_store, _, _, appointments = setup_services()
    original = appointments.book_appointment('A1', 'P1', 'D1', WHEN)
    original.cancel()
    assert original.status is AppointmentStatus.CANCELLED

    replacement = appointments.book_appointment('A2', 'P2', 'D1', WHEN)

    assert replacement.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [original, replacement]


@NEEDS_SERVICE_CANCELLATION
def test_service_cancel() -> None:
    """TEST-18: the service cancels and returns the same stored object."""
    _, _, _, appointments = setup_services()
    appointment = appointments.book_appointment('A1', 'P1', 'D1', WHEN)

    result = appointments.cancel_appointment('A1')

    assert result is appointment
    assert appointment.status is AppointmentStatus.CANCELLED


@NEEDS_SERVICE_CANCELLATION
def test_cancel_unknown_appointment_rejected() -> None:
    """TEST-06: an unknown ID raises LookupError and changes nothing."""
    _, _, _, appointments = setup_services()
    appointment = appointments.book_appointment('A1', 'P1', 'D1', WHEN)

    with pytest.raises(LookupError):
        appointments.cancel_appointment('A9')

    assert appointment.status is AppointmentStatus.SCHEDULED


@NEEDS_SERVICE_CANCELLATION
def test_service_cancel_blank_id() -> None:
    """TEST-19: a blank ID raises ValueError and changes nothing."""
    _, _, _, appointments = setup_services()
    appointment = appointments.book_appointment('A1', 'P1', 'D1', WHEN)

    with pytest.raises(ValueError):
        appointments.cancel_appointment('   ')

    assert appointment.status is AppointmentStatus.SCHEDULED


@NEEDS_SERVICE_CANCELLATION
def test_service_retains_cancelled_history() -> None:
    """TEST-20: after service cancellation the record is still retrievable."""
    data_store, _, _, appointments = setup_services()
    appointment = appointments.book_appointment('A1', 'P1', 'D1', WHEN)

    appointments.cancel_appointment('A1')

    assert appointments.find_appointment('A1') is appointment
    assert data_store.list_appointments() == [appointment]
    assert appointment.status is AppointmentStatus.CANCELLED
