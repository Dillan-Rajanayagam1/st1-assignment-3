"""Stage 9 tests for the interactive console workflow."""

import pytest

from smartcare.console import parse_status, run_menu
from smartcare.domain import AppointmentStatus


def run_script(lines):
    """Run the menu with scripted input and return the printed output."""
    inputs = iter(lines)
    output = []

    def fake_input(prompt):
        try:
            return next(inputs)
        except StopIteration:
            raise EOFError from None

    run_menu(fake_input, output.append)
    return output


SETUP = [
    '1', 'P1', 'Alex Example',
    '1', 'P2', 'Sam Example',
    '2', 'D1', 'Taylor Example', 'General',
    '2', 'D2', 'Morgan Example', 'General',
    '5', 'A1', 'P1', 'D1', '2026-10-01 09:00',
]


def test_full_menu_workflow():
    output = run_script(SETUP + [
        '3', 'P1',
        '4', 'D1',
        '5', 'A2', 'P2', 'D1', '2026-10-01 09:00',
        '5', 'A3', 'P2', 'D2', '2026-10-01 09:00',
        '6', 'A1',
        '7', 'A1',
        '5', 'A4', 'P2', 'D1', '2026-10-01 09:00',
        '8', 'D1', '',
        '8', 'D1', 'scheduled',
        '0',
    ])

    assert 'P1: Alex Example' in output
    assert 'D1: Taylor Example, General' in output
    assert ('Error: Practitioner already has a SCHEDULED appointment '
            'at this time') in output
    assert 'Booked A3: P2 with D2, 2026-10-01 09:00, scheduled' in output
    assert 'Cancelled A1: P1 with D1, 2026-10-01 09:00, cancelled' in output
    assert 'A1: P1 with D1, 2026-10-01 09:00, cancelled' in output
    assert 'Booked A4: P2 with D1, 2026-10-01 09:00, scheduled' in output
    all_index = output.index('A4: P2 with D1, 2026-10-01 09:00, scheduled')
    assert output[all_index - 1] == 'A1: P1 with D1, 2026-10-01 09:00, cancelled'
    assert output[-1] == 'Goodbye. Session-only data is lost on exit.'


def test_invalid_inputs_recover_and_state_is_unchanged():
    output = run_script(SETUP + [
        '1', 'P1', 'Duplicate',
        '3', 'P9',
        '3', '   ',
        '5', 'A2', 'P1', 'D1', '01/10/2026 9am',
        '5', 'A2', 'P1', 'D1', '2026-02-30 09:00',
        '8', 'D1', 'booked',
        '9',
        '6', 'A1',
        '6', 'A1',
        '8', 'D1', '',
        '0',
    ])

    errors = [line for line in output if line.startswith('Error:')]
    assert len(errors) == 7
    assert 'Unknown choice; enter a number from the menu' in output
    assert 'Error: Use date/time format YYYY-MM-DD HH:MM' in output
    assert 'Error: Invalid calendar date/time; use YYYY-MM-DD HH:MM' in output
    assert 'Cancelled A1: P1 with D1, 2026-10-01 09:00, cancelled' in output
    listed = [line for line in output if line.startswith('A')]
    assert listed[-1] == 'A1: P1 with D1, 2026-10-01 09:00, cancelled'
    assert not any(line.startswith('A2:') for line in output)
    assert output[-1] == 'Goodbye. Session-only data is lost on exit.'


def test_end_of_input_exits_cleanly():
    output = run_script([])

    assert output[-1] == 'Goodbye. Session-only data is lost on exit.'


@pytest.mark.parametrize(
    'text, expected',
    [
        ('', None),
        ('  ', None),
        ('Scheduled', AppointmentStatus.SCHEDULED),
        ('cancelled', AppointmentStatus.CANCELLED),
        (' completed ', AppointmentStatus.COMPLETED),
    ],
)
def test_parse_status(text, expected):
    assert parse_status(text) is expected


def test_parse_status_rejects_unknown_value():
    with pytest.raises(ValueError):
        parse_status('booked')
