import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../python")

import pytest
from unittest.mock import MagicMock, call
import random
import python.infotiv_launcher
from python.infotiv_launcher import LaunchCMD


@pytest.fixture()
def launcher():
    print('\n*********Start*********')
    launcher = python.infotiv_launcher.Launcher()
    launcher.rc = MagicMock()
    yield launcher
    print('\n**********End**********')

# ---------------------------------------------------------------------------------
# ------------------------ set_launch_position ------------------------------------
# ---------------------------------------------------------------------------------

def test_encoders_ready_check_encoders_not_ready(launcher):
    # GIVEN
    launcher.encoders_ready = 0

    # WHEN
    return_value = launcher.encoder_ready_check()

    # THEN
    assert return_value == 0


def test_set_launch_position_encoders_not_ready(launcher):
    # GIVEN
    with pytest.raises(Exception) as err:
        launcher.encoders_ready = 0
    # WHEN
        launcher.set_launch_position(1)
    # THEN
    assert err.match('Encoder Not Ready')


@pytest.mark.parametrize("invalid_data", [(-1), 112])
def test_set_launch_position_encoders_ready_launch_position_invalid_type_of_error(launcher, invalid_data):
    # GIVEN
    with pytest.raises(Exception, match='out of bounds') as err:
        launcher.encoders_ready = 1
    # WHEN
        launcher.set_launch_position(invalid_data)
    # THEN
    assert err.type is ValueError


@pytest.mark.parametrize("invalid_data", [(-1), 112])
def test_set_launch_position_encoders_ready_launch_position_invalid_message(launcher, invalid_data):
    # GIVEN
    with pytest.raises(ValueError) as err:
        launcher.encoders_ready = 1
    # WHEN
        launcher.set_launch_position(invalid_data)
    # THEN
    err.match('out of bounds')


def test_set_launch_position_encoders_ready_launch_position_zero(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    launcher.rc.ReadEncM2.return_value = (1, 2, 2)
    launcher.rc.ReadBuffers.return_value = (0, 0, 0x80)

    # WHEN
    launcher.set_launch_position(0)

    # THEN
    calls = [call(129, -2500, 2, 1),
             call(129, 0, 0, 0),
             call(129, 2500, 2188, 0),
             call(129, 0, 0, 0)]
    launcher.rc.SpeedDistanceM2.assert_has_calls(calls)
    assert launcher.rc.SpeedDistanceM2.call_count == 4


def test_set_launch_position_encoders_ready_launch_position_higher_than_zero(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    launcher.rc.ReadEncM2.return_value = (1, 4, 2)  # launch_actual = 4 ,  launch_increment = -4
    launcher.rc.ReadBuffers.return_value = (0, 0, 0x80)

    # WHEN
    launcher.set_launch_position(1)

    # THEN

    calls = [call(129, -2500, 4, 1),
             call(129, 0, 0, 0),
             call(129, 2500, 2319, 0),
             call(129, 0, 0, 0)]
    launcher.rc.SpeedDistanceM2.assert_has_calls(calls)
    assert launcher.rc.SpeedDistanceM2.call_count == 4


def test_set_launch_position_encoders_ready_launch_position_max(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    launcher.rc.ReadEncM2.return_value = (1, -1.5, 2)
    launcher.rc.ReadBuffers.return_value = (0, 0, 0x80)

    # WHEN
    launcher.set_launch_position(111)

    # THEN

    calls = [call(129, 2500, 1.5, 1),
             call(129, 0, 0, 0),
             call(129, 2500, 16991.5, 0),
             call(129, 0, 0, 0)]
    launcher.rc.SpeedDistanceM2.assert_has_calls(calls)
    assert launcher.rc.SpeedDistanceM2.call_count == 4


def test_stop(launcher):
    # GIVEN
    launcher.rc.ForwardM1 = MagicMock(return_value=True)
    launcher.rc.ForwardM2 = MagicMock(return_value=True)

    # WHEN
    launcher.stop()

    # THEN
    launcher.rc.ForwardM1.assert_any_call(launcher.address, 0)
    launcher.rc.ForwardM2.assert_any_call(launcher.address, 0)
    launcher.rc.ForwardM1.assert_any_call(launcher.address_2,0)
    launcher.rc.ForwardM2.assert_any_call(launcher.address_2, 0)


def test_max_pitch_zero_increment(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    launcher.rc.ReadEncM1.return_value = (1, 355000)    # pitch increment = 0

    # WHEN
    launcher.max_pitch()

    # THEN

    calls = [call(launcher.address, launcher.pitch_speed_pulses, 0, 1),
             call(launcher.address, 0, 0, 0)]
    launcher.rc.SpeedDistanceM1.assert_has_calls(calls)
    assert launcher.rc.SpeedDistanceM1.call_count == 2


def test_max_pitch_higher_than_zero_increment(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    launcher.rc.ReadEncM1.return_value = (1, 2)     # pitch increment = 354998

    # WHEN
    launcher.max_pitch()

    # THEN

    calls = [call(launcher.address, launcher.pitch_speed_pulses, 354998, 1),
             call(launcher.address, 0, 0, 0)]
    launcher.rc.SpeedDistanceM1.assert_has_calls(calls)
    assert launcher.rc.SpeedDistanceM1.call_count == 2


def test_max_pitch_lower_than_zero_increment(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    launcher.rc.ReadEncM1.return_value = (1, 355020)    # pitch increment = -20

    # WHEN
    launcher.max_pitch()

    # THEN

    calls = [call(launcher.address, -launcher.pitch_speed_pulses, 20, 1),
             call(launcher.address, 0, 0, 0)]
    launcher.rc.SpeedDistanceM1.assert_has_calls(calls)
    assert launcher.rc.SpeedDistanceM1.call_count == 2


@pytest.mark.parametrize("test_input, expected", [(12345.6789, 1234.57), (10, 1), (123, 12.3), (0, 0), (-10, -1)])
def test_battery_voltage_decimal_value(launcher, test_input, expected):
    # GIVEN
    launcher.rc.ReadMainBatteryVoltage.return_value = (128, test_input)
    # WHEN
    return_value = launcher.battery_voltage()
    # THEN
    assert return_value == expected

# ---------------------------------------------------------------------------------
# ------------------------ set_launch_variables -----------------------------------
# ---------------------------------------------------------------------------------

def test_set_launch_variables_valid_positions_called(launcher):
    # GIVEN
    launcher.change_pitch = MagicMock()
    launcher.change_rotation = MagicMock()
    launcher.change_lift = MagicMock()

    # WHEN
    pitch_position = random.randint(0, launcher.pitch_length)
    rotation_position = random.randint(0, launcher.rotation_length)
    lift_position = random.randint(0, launcher.lift_length)
    launcher.set_launch_variables(pitch_position, rotation_position, lift_position)

    # THEN
    launcher.change_pitch.assert_called_with(pitch_position)
    launcher.change_rotation.assert_called_with(rotation_position)
    launcher.change_lift.assert_called_with(lift_position)


# ---------------------------------------------------------------------------------
# ------------------------ launch_control------------------------------------------
# ---------------------------------------------------------------------------------
def test_launch_control_LaunchCMD_up(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    # WHEN
    launcher.launch_control(LaunchCMD(1))

    # THEN
    launcher.rc.ForwardM2.assert_called_with(launcher.address_2, launcher.launch_speed_manual)
    launcher.rc.BackwardM2.assert_not_called()


def test_launch_control_LaunchCMD_down(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    # WHEN
    launcher.rc.BackwardM2.return_value = True
    launcher.launch_control(LaunchCMD(2))

    # THEN
    launcher.rc.BackwardM2.assert_called_with(launcher.address_2, launcher.launch_speed_manual)
    launcher.rc.ForwardM2.assert_not_called()


def test_launch_control_LaunchCMD_stop(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    # WHEN
    launcher.rc.ForwardM2.return_value = True
    launcher.launch_control(LaunchCMD(3))

    # THEN
    launcher.rc.ForwardM2.assert_called_with(launcher.address_2, 0)
    launcher.rc.BackwardM2.assert_not_called()
