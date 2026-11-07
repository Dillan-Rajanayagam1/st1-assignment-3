"""Stage 9 tests for the pure query, named key and service listing."""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.queries import appointment_sort_key, select_appointments
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def build_store():
    """Return a store and service with appointments for D1 and D2.

    D1 has A3 (10:00), A2 (09:00, cancelled) and A1 (09:00); D2 has B1.
    """
    store = SmartCareDataStore()
    PatientService(store).register_patient('P1', 'Alex Example')
    PatientService(store).register_patient('P2', 'Sam Example')
    practitioners = PractitionerService(store)
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    practitioners.register_practitioner('D2', 'Morgan Example', 'General')
    practitioners.register_practitioner('D3', 'Jordan Example', 'General')
    service = AppointmentService(store)
    service.book_appointment('A3', 'P1', 'D1', datetime(2026, 10, 1, 10))
    service.book_appointment('A2', 'P2', 'D1', datetime(2026, 10, 1, 9))
    service.cancel_appointment('A2')
    service.book_appointment('A1', 'P1', 'D1', datetime(2026, 10, 1, 9))
    service.book_appointment('B1', 'P2', 'D2', datetime(2026, 10, 1, 8))
    return store, service


def ids(appointments):
    return [appointment.appointment_id for appointment in appointments]


def test_sort_key_is_date_time_then_id():
    store, _ = build_store()
    appointment = store.find_appointment('A1')

    assert appointment_sort_key(appointment) == (datetime(2026, 10, 1, 9), 'A1')


def test_select_isolates_practitioner_and_orders_with_id_tie_break():
    store, _ = build_store()

    result = select_appointments(store.list_appointments(), 'D1')

    assert ids(result) == ['A1', 'A2', 'A3']
    assert all(a.practitioner.practitioner_id == 'D1' for a in result)


@pytest.mark.parametrize(
    'status, expected',
    [
        (None, ['A1', 'A2', 'A3']),
        (AppointmentStatus.SCHEDULED, ['A1', 'A3']),
        (AppointmentStatus.CANCELLED, ['A2']),
        (AppointmentStatus.COMPLETED, []),
    ],
)
def test_select_status_filter(status, expected):
    store, _ = build_store()

    assert ids(select_appointments(store.list_appointments(), 'D1', status)) == expected


def test_select_returns_new_list_and_leaves_source_unchanged():
    store, _ = build_store()
    source = store.list_appointments()
    before_order = ids(source)
    before_status = [a.status for a in source]

    result = select_appointments(source, 'D1')

    assert result is not source
    assert ids(source) == before_order
    assert [a.status for a in source] == before_status
    assert all(a is store.find_appointment(a.appointment_id) for a in result)


def test_select_repeated_calls_and_empty_or_sorted_input():
    store, _ = build_store()
    source = store.list_appointments()

    first = select_appointments(source, 'D1')
    second = select_appointments(source, 'D1')
    already_sorted = select_appointments(first, 'D1')
    empty = []

    assert ids(first) == ids(second) == ids(already_sorted)
    assert first is not second and already_sorted is not first
    assert select_appointments(empty, 'D1') == []
    assert select_appointments(empty, 'D1') is not empty


def test_named_key_gives_same_order_as_sorted():
    store, _ = build_store()
    source = store.list_appointments()
    d1 = [a for a in source if a.practitioner.practitioner_id == 'D1']

    assert ids(sorted(d1, key=appointment_sort_key)) == ids(
        select_appointments(source, 'D1'),
    )


def test_service_accepts_status_converted_from_text():
    _, service = build_store()

    result = service.list_practitioner_appointments(
        'D1',
        AppointmentStatus('scheduled'),
    )

    assert ids(result) == ['A1', 'A3']


def test_service_lists_all_statuses_and_keeps_cancelled_history():
    store, service = build_store()

    result = service.list_practitioner_appointments(' D1 ')

    assert ids(result) == ['A1', 'A2', 'A3']
    assert result[1] is service.find_appointment('A2')
    assert result[1].status is AppointmentStatus.CANCELLED


def test_service_scheduled_filter_excludes_cancelled_only():
    _, service = build_store()

    result = service.list_practitioner_appointments(
        'D1',
        AppointmentStatus.SCHEDULED,
    )

    assert ids(result) == ['A1', 'A3']


def test_service_known_practitioner_without_matches_returns_empty_list():
    _, service = build_store()

    assert service.list_practitioner_appointments('D3') == []


def test_service_unknown_practitioner_raises_lookup_error():
    store, service = build_store()
    before = store.list_appointments()

    with pytest.raises(LookupError):
        service.list_practitioner_appointments('D9')

    assert store.list_appointments() == before


@pytest.mark.parametrize('bad_id', ['', '   ', None])
def test_service_invalid_practitioner_id_raises_value_error(bad_id):
    _, service = build_store()

    with pytest.raises(ValueError):
        service.list_practitioner_appointments(bad_id)


@pytest.mark.parametrize('bad_status', ['scheduled', 123])
def test_service_invalid_status_raises_value_error(bad_status):
    store, service = build_store()
    before = [a.status for a in store.list_appointments()]

    with pytest.raises(ValueError):
        service.list_practitioner_appointments('D1', bad_status)

    assert [a.status for a in store.list_appointments()] == before
