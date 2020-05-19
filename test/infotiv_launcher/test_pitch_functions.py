import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../python")
from unittest.mock import MagicMock, call
import python.infotiv_launcher
from python.infotiv_launcher import EncoderError,PitchCMD
import random


@pytest.fixture()
def launcher():
    print('\n*********Start*********')
    launcher = python.infotiv_launcher.Launcher()
    launcher.rc = MagicMock()
    yield launcher
    print('\n**********End**********')


# ---------------------------------------------------------------------------------
# ----------------- set_pitch_position --------------------------------------------
# ---------------------------------------------------------------------------------


def test_encoder_default_value(launcher):
    assert launcher.encoders_ready == 0,"The default value should be 0"


def test_set_pitch_position_encoder_not_ready(launcher):
    # GIVEN
    launcher.encoders_ready = 0

    # WHEN
    with pytest.raises(EncoderError) as excinfo:
        pitch_position=random.randint(-100,111)
        launcher.set_pitch_position(pitch_position)

    # THEN
    assert "Encoder Not Ready" in str(excinfo.value)


@pytest.mark.parametrize("invalid_position", [-1,91])
def test_set_pitch_position_encoder_ready_invalid_position(launcher,invalid_position):
    # GIVEN
    launcher.encoders_ready = 1

    # WHEN
    with pytest.raises(ValueError) as excinfo:
        launcher.set_pitch_position(invalid_position)

    # THEN
    assert "out of bounds" in str(excinfo.value)


def test_set_pitch_position_encoder_ready_position_zero_increment_not_less_than_zero(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    # WHEN
    launcher.rc.ReadEncM1.return_value = (1, 0, 0)
    launcher.set_pitch_position(0)

    # THEN
    callsM1 = [call(launcher.address, launcher.pitch_speed_pulses, 0, 1),
               call(launcher.address, 0, 0, 0)
               ]
    launcher.rc.SpeedDistanceM1.assert_has_calls(callsM1)


def test_set_pitch_position_encoder_ready_position_zero_increment_less_than_zero(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    # WHEN
    launcher.rc.ReadEncM1.return_value = (1,1,0)
    launcher.set_pitch_position(0)

    # THEN
    callsM1 = [call(launcher.address, -launcher.pitch_speed_pulses, 1, 1),
               call(launcher.address, 0, 0, 0)
               ]
    launcher.rc.SpeedDistanceM1.assert_has_calls(callsM1)


def test_set_pitch_position_encoder_ready_valid_position_not_zero_increment_not_less_than_zero(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    # WHEN
    launcher.rc.ReadEncM1.return_value = (1, 0, 0)
    launcher.set_pitch_position(45)

    # THEN
    callsM1 = [call(launcher.address, launcher.pitch_speed_pulses, 177500, 1),
               call(launcher.address, 0, 0, 0)
               ]
    launcher.rc.SpeedDistanceM1.assert_has_calls(callsM1)


def test_set_pitch_position_encoder_ready_valid_position_not_zero_increment_less_than_zero(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    # WHEN
    launcher.rc.ReadEncM1.return_value = (1, 35501, 0)
    launcher.set_pitch_position(9)

    # THEN
    callsM1 = [call(launcher.address, -launcher.pitch_speed_pulses, 1, 1),
               call(launcher.address, 0, 0, 0)
               ]
    launcher.rc.SpeedDistanceM1.assert_has_calls(callsM1)


# ---------------------------------------------------------------------------------
# ----------------- pitch_control --------------------------------------------
# ---------------------------------------------------------------------------------
def test_pitch_control_up(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    # WHEN
    launcher.pitch_control(PitchCMD(1))

    # THEN
    launcher.rc.BackwardM1.assert_called_with(launcher.address, launcher.pitch_speed_manual)
    launcher.rc.ForwardM1.assert_not_called()


def test_pitch_control_down(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    # WHEN
    launcher.pitch_control(PitchCMD(2))

    # THEN
    launcher.rc.ForwardM1.assert_called_with(launcher.address, launcher.pitch_speed_manual)
    launcher.rc.BackwardM1.assert_not_called()


def test_pitch_control_stop(launcher):
    # GIVEN
    launcher.encoders_ready = 1

    # WHEN
    launcher.pitch_control(PitchCMD(3))

    # THEN
    launcher.rc.ForwardM1.assert_called_with(launcher.address, 0)
    launcher.rc.BackwardM1.assert_not_called()