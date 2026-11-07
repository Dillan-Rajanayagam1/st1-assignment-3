"""Stage 8 regression tests for defects F8-01 and F8-02."""

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


def make_services() -> tuple[SmartCareDataStore, AppointmentService]:
    """Create one store with two patients and two practitioners."""
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    patients.register_patient('P1', 'Alex Example')
    patients.register_patient('P2', 'Sam Example')
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    practitioners.register_practitioner('D2', 'Morgan Example', 'General')
    return store, AppointmentService(store)


def test_f8_01_practitioner_conflict_rule() -> None:
    """FR-05 / AC-04.1 and AC-04.2: only the same practitioner conflicts."""
    store, service = make_services()
    first = service.book_appointment('A1', 'P1', 'D1', WHEN)

    with pytest.raises(ValueError):
        service.book_appointment('A2', 'P2', 'D1', WHEN)
    assert store.list_appointments() == [first]

    other = service.book_appointment('A3', 'P2', 'D2', WHEN)
    assert store.list_appointments() == [first, other]


def test_f8_02_cancelled_appointment_still_found() -> None:
    """FR-06/07/08, AC-05.2: a cancelled appointment stays findable."""
    store, service = make_services()
    appointment = service.book_appointment('A1', 'P1', 'D1', WHEN)

    result = service.cancel_appointment('A1')

    assert result is appointment
    assert appointment.status is AppointmentStatus.CANCELLED
    assert store.list_appointments() == [appointment]
    assert store.find_appointment('A1') is appointment
    assert service.find_appointment('A1') is appointment

    with pytest.raises(ValueError):
        service.cancel_appointment('A1')
    assert appointment.status is AppointmentStatus.CANCELLED
