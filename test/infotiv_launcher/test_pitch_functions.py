import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../python")
from unittest.mock import MagicMock, call
import python.infotiv_launcher
from python.infotiv_launcher import EncoderError,PitchCMD
import random


# ---------------------------------------------------------------------------------
# ----------------- set_pitch_position --------------------------------------------
# ---------------------------------------------------------------------------------

@pytest.fixture()
def dl():
    print('\n*********Start*********')
    dl = python.infotiv_launcher.Launcher()
    yield dl
    print('\n**********End**********')


def test_encoder_default_value(dl):
    assert dl.encoders_ready == 0,"The default value should be 0"


def test_set_pitch_position_encoder_not_ready(dl):
    # GIVEN
    dl.encoders_ready = 0

    # WHEN
    with pytest.raises(EncoderError) as excinfo:
        pitch_position=random.randint(-100,111)
        dl.set_pitch_position(pitch_position)

    # THEN
    assert "Encoder Not Ready" in str(excinfo.value)


# 91 fails because there is something wrong with one code "pitch_position > self.lift_length should be pitch_position > self.pitch_length"

invalid_position ={-1,91}
@pytest.mark.parametrize("pitch_position",invalid_position)
def test_set_pitch_position_encoder_ready_invalid_position(dl,pitch_position):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()

    # WHEN
    with pytest.raises(ValueError) as excinfo:
        dl.rc.ReadEncM1.return_value = (1, 1, 0)
        dl.rc.ReadEncM2.return_value = (1, 0, 0)
        dl.set_pitch_position(pitch_position)

    # THEN
    assert "out of bounds" in str(excinfo.value)


def test_set_pitch_position_encoder_ready_position_zero_increment_not_less_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()

    # WHEN
    dl.rc.ReadEncM1.return_value = (1, 0, 0)
    dl.set_pitch_position(0)

    # THEN
    callsM1 = [call(0x80, 7000, 0, 1),
               call(0x80, 0, 0, 0)
               ]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)


def test_set_pitch_position_encoder_ready_position_zero_increment_less_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()

    # WHEN
    dl.rc.ReadEncM1.return_value = (1,1,0)
    dl.set_pitch_position(0)

    # THEN
    callsM1 = [call(0x80, -7000, 1, 1),
               call(0x80, 0, 0, 0)
               ]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)


def test_set_pitch_position_encoder_ready_valid_position_not_zero_increment_not_less_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()

    # WHEN
    dl.rc.ReadEncM1.return_value = (1, 0, 0)
    dl.set_pitch_position(45)

    # THEN
    callsM1 = [call(0x80, 7000, 177500, 1),
               call(0x80, 0, 0, 0)
               ]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)


def test_set_pitch_position_encoder_ready_valid_position_not_zero_increment_less_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()

    # WHEN
    dl.rc.ReadEncM1.return_value = (1, 35501, 0)
    dl.set_pitch_position(9)

    # THEN
    callsM1 = [call(0x80, -7000, 1, 1),
               call(0x80, 0, 0, 0)
               ]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)


# ---------------------------------------------------------------------------------
# ----------------- pitch_control --------------------------------------------
# ---------------------------------------------------------------------------------
def test_pitch_control_PitchCMD_up(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()

    # WHEN
    dl.rc.BackwardM1.return_value = True
    dl.pitch_control(PitchCMD(1))

    # THEN
    dl.rc.BackwardM1.assert_called_with(dl.address, dl.pitch_speed_manual)
    dl.rc.ForwardM1.assert_not_called()


def test_pitch_control_PitchCMD_down(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()

    # WHEN
    dl.rc.ForwardM1.return_value = True
    dl.pitch_control(PitchCMD(2))

    # THEN
    dl.rc.ForwardM1.assert_called_with(dl.address, dl.pitch_speed_manual)
    dl.rc.BackwardM1.assert_not_called()


def test_pitch_control_PitchCMD_stop(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()

    # WHEN
    dl.rc.ForwardM1.return_value = True
    dl.pitch_control(PitchCMD(3))

    # THEN
    dl.rc.ForwardM1.assert_called_with(dl.address, 0)
    dl.rc.BackwardM1.assert_not_called()