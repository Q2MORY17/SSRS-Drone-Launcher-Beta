import os
import sys
import pytest
from unittest.mock import MagicMock, call
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../python")
import python.infotiv_launcher
from python.infotiv_launcher import RotationCMD


@pytest.fixture()
def launcher():
    print('\n*********Start*********')
    launcher = python.infotiv_launcher.Launcher()
    launcher.rc = MagicMock()
    yield launcher
    print('\n**********End**********')


# ---------------------------------------------------------------------------------
# -------------------------set_rotation_position-----------------------------------
# ---------------------------------------------------------------------------------
def test_encoders_ready_check_encoders_not_ready(launcher):
    # GIVEN
    launcher.encoders_ready = 0

    # WHEN
    return_value = launcher.encoder_ready_check()

    # THEN
    assert return_value == 0


def test_set_rotation_position_encoders_not_ready(launcher):
    # GIVEN
    with pytest.raises(Exception) as err:
        launcher.encoders_ready = 0
    # WHEN
        launcher.set_rotation_position(1)
    # THEN
    assert err.match('Encoder Not Ready')


@pytest.mark.parametrize("invalid_data", [(-1), 131])
def test_set_rotation_position_invalid_data_type_error(launcher, invalid_data):
    # GIVEN
    with pytest.raises(Exception, match='out of bounds') as err:
        launcher.encoders_ready = 1
    # WHEN
        launcher.set_rotation_position(invalid_data)
    # THEN
    assert err.type is ValueError


@pytest.mark.parametrize("invalid_data", [(-1), 131])
def test_set_rotation_position_invalid_data_message(launcher, invalid_data):
    # GIVEN
    with pytest.raises(ValueError) as err:
        launcher.encoders_ready = 1
    # WHEN
        launcher.set_rotation_position(invalid_data)
    # THEN
    err.match('out of bounds')


def test_set_rotation_position_zero_increment_negative(launcher):
    # GIVEN
    launcher.encoders_ready = 1
    launcher.rc.ReadEncM2.return_value = (1, 2, 2)

    # WHEN
    launcher.set_rotation_position(0)

    # THEN
    calls = [call(launcher.address, -launcher.rotation_speed_pulses, 2, 1), call(launcher.address, 0, 0, 0)]
    launcher.rc.SpeedDistanceM2.assert_has_calls(calls)
    assert launcher.rc.SpeedDistanceM2.call_count == 2


def test_set_rotation_position_higher_than_zero_increment_positive(launcher):
    # GIVEN
    launcher.encoders_ready = 1
    launcher.rc.ReadEncM2.return_value = (1, 4, 2)

    # WHEN
    launcher.set_rotation_position(1)

    # THEN
    calls = [call(launcher.address, launcher.rotation_speed_pulses, 2634, 1), call(launcher.address, 0, 0, 0)]
    launcher.rc.SpeedDistanceM2.assert_has_calls(calls)
    assert launcher.rc.SpeedDistanceM2.call_count == 2


def test_set_rotation_position_max_increment_positive(launcher):
    # GIVEN
    launcher.encoders_ready = 1
    launcher.rc.ReadEncM2.return_value = (1, -1.5, 2)

    # WHEN
    launcher.set_rotation_position(130)

    # THEN
    calls = [call(launcher.address, launcher.rotation_speed_pulses, 343056.5, 1), call(launcher.address, 0, 0, 0)]
    launcher.rc.SpeedDistanceM2.assert_has_calls(calls)
    assert launcher.rc.SpeedDistanceM2.call_count == 2


# ---------------------------------------------------------------------------------
# -------------------------rotation_control----------------------------------------
# ---------------------------------------------------------------------------------
def test_rotation_control_right(launcher):
    # GIVEN
    launcher.rc = MagicMock()
    # WHEN
    launcher.rotation_control(RotationCMD(1))
    # THEN
    launcher.rc.ForwardM1.assert_called_with(launcher.address_2, launcher.rotation_speed_manual)
    launcher.rc.ForwardM2.assert_called_with(launcher.address_2, launcher.rotation_speed_manual)
    launcher.rc.BackwardM1.assert_not_called()


def test_rotation_control_left(launcher):
    # GIVEN
    launcher.rc = MagicMock()
    # WHEN
    launcher.rotation_control(RotationCMD(2))
    # THEN
    launcher.rc.BackwardM1.assert_called_with(launcher.address_2, launcher.rotation_speed_manual)
    launcher.rc.BackwardM2.assert_called_with(launcher.address_2, launcher.rotation_speed_manual)
    launcher.rc.ForwardM1.assert_not_called()


def test_rotation_control_stop(launcher):
    # GIVEN
    launcher.rc = MagicMock()
    # WHEN
    launcher.rotation_control(RotationCMD(3))
    # THEN
    launcher.rc.ForwardM1.assert_called_with(launcher.address_2, 0)
    launcher.rc.ForwardM2.assert_called_with(launcher.address_2, 0)
    launcher.rc.BackwardM1.assert_not_called()
