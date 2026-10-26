"""Tests for Stage 6 service operations."""

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.services import PatientService


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