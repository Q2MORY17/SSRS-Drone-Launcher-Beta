import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../python")

from unittest.mock import MagicMock, call
import python.infotiv_launcher
from python.infotiv_launcher import LiftCMD


@pytest.fixture()
def launcher():
    print('\n*********Start*********')
    launcher = python.infotiv_launcher.Launcher()
    yield launcher
    print('\n**********End**********')


# ---------------------------------------------------------------------------------
# ------------------------ set_lift_position --------------------------------------
# ---------------------------------------------------------------------------------

def test_lift_position_with_encoders_not_ready(launcher):
    with pytest.raises(Exception) as err:
        launcher.encoders_ready = 0
        launcher.set_lift_position(0)
    assert err.match('Encoder Not Ready')


def test_that_exception_type_is_value_error_if_more_than_max_value(launcher):
    with pytest.raises(Exception, match='out of bounds') as err:
        launcher.encoders_ready = 1
        invalid_number = launcher.lift_length + 1
        launcher.set_lift_position(invalid_number)
    assert err.type is ValueError


def test_that_exception_type_is_value_error_if_less_than_min_value(launcher):
    with pytest.raises(Exception, match='out of bounds') as err:
        launcher.encoders_ready = 1
        invalid_number = -1
        launcher.set_lift_position(invalid_number)
    assert err.type is ValueError


def test_shows_correct_message_if_value_is_higher_than_max_value(launcher):
    with pytest.raises(ValueError) as err:
        launcher.encoders_ready = 1
        invalid_number = launcher.lift_length + 1
        launcher.set_lift_position(invalid_number)
    err.match('out of bounds')


def test_shows_correct_message_if_value_is_lower_than_min_value(launcher):
    with pytest.raises(ValueError) as err:
        launcher.encoders_ready = 1
        invalid_number = -1
        launcher.set_lift_position(invalid_number)
    err.match('out of bounds')


def test_set_lift_position_zero_increment_negative(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    launcher.rc = MagicMock()
    launcher.rc.ReadEncM1.return_value = (1, 2, 2)

    # WHEN
    launcher.set_lift_position(0)

    # THEN
    calls = [call(launcher.address_2, -launcher.lift_speed_pulses, 2, 1), call(launcher.address_2, 0, 0, 0)]
    launcher.rc.SpeedDistanceM1.assert_has_calls(calls)
    assert launcher.rc.SpeedDistanceM1.call_count == 2


def test_set_lift_position_higher_than_zero_increment_positive(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    launcher.rc = MagicMock()
    launcher.rc.ReadEncM1.return_value = (1, 4, 2)

    # WHEN
    launcher.set_lift_position(1)

    # THEN
    calls = [call(launcher.address_2, launcher.lift_speed_pulses, 142, 1), call(launcher.address_2, 0, 0, 0)]
    launcher.rc.SpeedDistanceM1.assert_has_calls(calls)
    assert launcher.rc.SpeedDistanceM1.call_count == 2


def test_set_lift_position_max_increment_positive(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    launcher.rc = MagicMock()
    launcher.rc.ReadEncM1.return_value = (1, -1.5, 2)

    # WHEN
    launcher.set_lift_position(130)

    # THEN
    calls = [call(launcher.address_2, launcher.lift_speed_pulses, 19001.5, 1), call(launcher.address_2, 0, 0, 0)]
    launcher.rc.SpeedDistanceM1.assert_has_calls(calls)
    assert launcher.rc.SpeedDistanceM1.call_count == 2


# ---------------------------------------------------------------------------------
# --------------------------- lift_control ----------------------------------------
# ---------------------------------------------------------------------------------

def test_lift_control_right(launcher):

    launcher.rc = MagicMock()

    launcher.lift_control(LiftCMD(1))

    launcher.rc.ForwardM1.assert_called_with(launcher.address_2, launcher.lift_speed_manual)
    launcher.rc.ForwardM1.assert_called_with(launcher.address_2, launcher.lift_speed_manual)
    launcher.rc.BackwardM1.assert_not_called()


def test_lift_control_left(launcher):

    launcher.rc = MagicMock()

    launcher.lift_control(LiftCMD(2))

    launcher.rc.BackwardM1.assert_called_with(launcher.address_2, launcher.lift_speed_manual)
    launcher.rc.BackwardM1.assert_called_with(launcher.address_2, launcher.lift_speed_manual)
    launcher.rc.ForwardM1.assert_not_called()


def test_lift_control_stop(launcher):

    launcher.rc = MagicMock()

    launcher.lift_control(LiftCMD(3))

    launcher.rc.ForwardM1.assert_called_with(launcher.address_2, 0)
    launcher.rc.ForwardM1.assert_called_with(launcher.address_2, 0)
    launcher.rc.BackwardM1.assert_not_called()
