import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../python")

import pytest
from unittest.mock import MagicMock, call

import python.infotiv_launcher


@pytest.fixture()
def launcher():
    print('\n*********Start*********')
    launcher = python.infotiv_launcher.Launcher()
    yield launcher
    print('\n**********End**********')


def test_encoders_ready_check_encoders_not_ready(launcher):
    # GIVEN
    launcher.encoders_ready = 0

    # WHEN
    return_value = launcher.encoder_ready_check()

    # THEN
    assert return_value == 0


def test_set_launch_position_encoders_not_ready(launcher):
    with pytest.raises(Exception) as err:
        launcher.encoders_ready = 0
        launcher.set_launch_position(1)
    assert err.match('Encoder Not Ready')


@pytest.mark.parametrize("invalid_data", [(-1), 112])
def test_set_launch_position_encoders_ready_launch_position_invalid_type_of_error(launcher, invalid_data):
    with pytest.raises(Exception, match='out of bounds') as err:
        launcher.set_launch_position(invalid_data)
    assert err.type is ValueError


@pytest.mark.parametrize("invalid_data", [(-1), 112])
def test_set_launch_position_encoders_ready_launch_position_invalid_message(launcher, invalid_data):
    with pytest.raises(ValueError) as err:
        launcher.set_launch_position(invalid_data)
    err.match('out of bounds')


def test_set_launch_position_encoders_ready_launch_position_zero(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    launcher.rc = MagicMock()
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

    launcher.rc = MagicMock()
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

    launcher.rc = MagicMock()
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

    launcher.rc = MagicMock()
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

    launcher.rc = MagicMock()
    launcher.rc.ReadEncM1.return_value = (1, 2)     # pitch increment = 354998

    # WHEN
    launcher.max_pitch()

    # THEN

    calls = [call(launcher.address, launcher.pitch_speed_pulses, 354998, 1),
             call(launcher.address, 0, 0, 0)]
    launcher.rc.SpeedDistanceM1.assert_has_calls(calls)
    assert launcher.rc.SpeedDistanceM1.call_count == 2


def test_max_pitch_higher_than_zero_increment(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    launcher.rc = MagicMock()
    launcher.rc.ReadEncM1.return_value = (1, 355020)    # pitch increment = -20

    # WHEN
    launcher.max_pitch()

    # THEN

    calls = [call(launcher.address, -launcher.pitch_speed_pulses, 20, 1),
             call(launcher.address, 0, 0, 0)]
    launcher.rc.SpeedDistanceM1.assert_has_calls(calls)
    assert launcher.rc.SpeedDistanceM1.call_count == 2