"""Tests for Stage 6 service operations."""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def test_find_patient_returns_stored_object():
    store = SmartCareDataStore()
    service = PatientService(store)
    patient = service.register_patient("P1", "Test Patient")

    result = service.find_patient("P1")

    assert result is patient
    assert store.find_patient("P1") is patient
    assert store.list_patients() == [patient]
    assert patient.patient_id == "P1"
    assert patient.name == "Test Patient"


def test_find_patient_trims_surrounding_whitespace():
    store = SmartCareDataStore()
    service = PatientService(store)
    patient = service.register_patient("P1", "Test Patient")

    assert service.find_patient("  P1  ") is patient


def test_find_patient_unknown_id_raises_lookup_error():
    store = SmartCareDataStore()
    service = PatientService(store)
    patient = service.register_patient("P1", "Test Patient")

    with pytest.raises(LookupError):
        service.find_patient("P2")

    assert store.list_patients() == [patient]


def test_find_patient_ids_are_case_sensitive():
    store = SmartCareDataStore()
    service = PatientService(store)
    patient = service.register_patient("P1", "Test Patient")

    with pytest.raises(LookupError):
        service.find_patient("p1")

    assert service.find_patient("P1") is patient


@pytest.mark.parametrize("invalid_id", ["", "   ", None, 123])
def test_find_patient_invalid_id_raises_value_error(invalid_id):
    store = SmartCareDataStore()
    service = PatientService(store)

    with pytest.raises(ValueError):
        service.find_patient(invalid_id)

    assert store.list_patients() == []


def test_find_practitioner_returns_stored_object():
    store = SmartCareDataStore()
    service = PractitionerService(store)
    practitioner = service.register_practitioner(
        "D1",
        "Test Practitioner",
        "General Practice",
    )

    result = service.find_practitioner("D1")

    assert result is practitioner
    assert store.find_practitioner("D1") is practitioner
    assert store.list_practitioners() == [practitioner]
    assert practitioner.practitioner_id == "D1"
    assert practitioner.name == "Test Practitioner"
    assert practitioner.specialty == "General Practice"


def test_find_practitioner_trims_surrounding_whitespace():
    store = SmartCareDataStore()
    service = PractitionerService(store)
    practitioner = service.register_practitioner(
        "D1",
        "Test Practitioner",
        "General Practice",
    )

    assert service.find_practitioner("  D1  ") is practitioner


def test_find_practitioner_unknown_id_raises_lookup_error():
    store = SmartCareDataStore()
    service = PractitionerService(store)
    practitioner = service.register_practitioner(
        "D1",
        "Test Practitioner",
        "General Practice",
    )

    with pytest.raises(LookupError):
        service.find_practitioner("D2")

    assert store.list_practitioners() == [practitioner]


def test_find_practitioner_ids_are_case_sensitive():
    store = SmartCareDataStore()
    service = PractitionerService(store)
    practitioner = service.register_practitioner(
        "D1",
        "Test Practitioner",
        "General Practice",
    )

    with pytest.raises(LookupError):
        service.find_practitioner("d1")

    assert service.find_practitioner("D1") is practitioner


@pytest.mark.parametrize("invalid_id", ["", "   ", None, 123])
def test_find_practitioner_invalid_id_raises_value_error(invalid_id):
    store = SmartCareDataStore()
    service = PractitionerService(store)

    with pytest.raises(ValueError):
        service.find_practitioner(invalid_id)

    assert store.list_practitioners() == []


WHEN = datetime(2026, 10, 1, 9)


def booked_appointment():
    """Return a store, an AppointmentService and one SCHEDULED appointment."""
    store = SmartCareDataStore()
    PatientService(store).register_patient("P1", "Test Patient")
    PractitionerService(store).register_practitioner(
        "D1",
        "Test Practitioner",
        "General Practice",
    )
    service = AppointmentService(store)
    appointment = service.book_appointment("A1", "P1", "D1", WHEN)
    return store, service, appointment


def test_cancel_appointment_returns_same_cancelled_object():
    store, service, appointment = booked_appointment()

    result = service.cancel_appointment("A1")

    assert result is appointment
    assert appointment.status is AppointmentStatus.CANCELLED


def test_cancelled_appointment_is_retained_with_details():
    store, service, appointment = booked_appointment()

    service.cancel_appointment("A1")

    assert store.list_appointments() == [appointment]
    assert service.find_appointment("A1") is appointment
    assert appointment.patient.patient_id == "P1"
    assert appointment.practitioner.practitioner_id == "D1"
    assert appointment.date_time == WHEN


def test_cancel_appointment_trims_surrounding_whitespace():
    store, service, appointment = booked_appointment()

    assert service.cancel_appointment("  A1  ") is appointment
    assert appointment.status is AppointmentStatus.CANCELLED


def test_cancel_unknown_appointment_raises_lookup_error():
    store, service, appointment = booked_appointment()

    with pytest.raises(LookupError):
        service.cancel_appointment("A2")

    assert appointment.status is AppointmentStatus.SCHEDULED
    assert store.list_appointments() == [appointment]


@pytest.mark.parametrize("invalid_id", ["", "   ", None, 123])
def test_cancel_invalid_id_raises_value_error(invalid_id):
    store, service, appointment = booked_appointment()

    with pytest.raises(ValueError):
        service.cancel_appointment(invalid_id)

    assert appointment.status is AppointmentStatus.SCHEDULED


def test_repeated_cancellation_raises_value_error():
    store, service, appointment = booked_appointment()
    service.cancel_appointment("A1")

    with pytest.raises(ValueError):
        service.cancel_appointment("A1")

    assert appointment.status is AppointmentStatus.CANCELLED
    assert store.list_appointments() == [appointment]


def test_cancel_completed_appointment_raises_value_error():
    store, service, _ = booked_appointment()
    completed = Appointment(
        "A2",
        store.find_patient("P1"),
        store.find_practitioner("D1"),
        datetime(2026, 10, 2, 9),
        AppointmentStatus.COMPLETED,
    )
    store.add_appointment(completed)

    with pytest.raises(ValueError):
        service.cancel_appointment("A2")

    assert completed.status is AppointmentStatus.COMPLETED


def test_cancelled_slot_can_be_rebooked_and_history_kept():
    store, service, appointment = booked_appointment()
    service.cancel_appointment("A1")

    replacement = service.book_appointment("A2", "P1", "D1", WHEN)

    assert replacement.status is AppointmentStatus.SCHEDULED
    assert store.list_appointments() == [appointment, replacement]
