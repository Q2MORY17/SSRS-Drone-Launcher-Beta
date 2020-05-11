import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../python")
from unittest.mock import MagicMock, call
import python.infotiv_launcher
from python.infotiv_launcher import EncoderError




# ---------------------------------------------------------------------------------
# ------------------------ Standby-------------------------------------
# ---------------------------------------------------------------------------------
@pytest.fixture()
def dl():
    print('\n*********Start*********')
    dl = python.infotiv_launcher.Launcher()
    yield dl
    print('\n**********End**********')


def test_encoder_default_value(dl):
    assert dl.encoders_ready == 0,"The default value should be 0"


def test_function_standby_encoders_not_ready(dl):
    # GIVEN
    dl.encoders_ready = 0

    # WHEN
    with pytest.raises(EncoderError) as excinfo:
        dl.standby()
    # THEN
    assert "Encoder Not Ready" in str(excinfo.value)


def test_function_standby_encoders_ready_all_increment_not_less_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    assert True == dl.encoder_ready_check()

    # WHEN
    dl.rc = MagicMock()
    dl.rc.ReadEncM1.return_value = (1, 0, 0)
    dl.rc.ReadEncM2.return_value = (1, 0, 0)
    dl.rc.ReadBuffers.return_value=(1,0,0x80)
    dl.standby()

    # THEN
    callsM1 = [call(0x80, 7000, 0, 1),
               call(0x80, 0, 0, 0),
               call(0x81, 420, 0, 1),
               call(0x81, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4
    callsM2 = [ call(128, 16000, 0, 1),
                call(128, 0, 0, 0),
                call(129, 2500, 0, 1),
                call(129, 0, 0, 0),
                call(129, 2500, 2190, 0),
                call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count ==6


def test_function_standby_encoders_ready_all_increment_less_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    assert True == dl.encoder_ready_check()
    dl.rc = MagicMock()

    # WHEN
    dl.rc.ReadEncM1.return_value=(1,1,0)
    dl.rc.ReadEncM2.return_value=(1,2,0)
    dl.rc.ReadBuffers.return_value = (1, 0, 0x80)
    dl.standby()

    # THEN
    callsM1 = [call(0x80, -7000, 1, 1),
               call(0x80, 0, 0, 0),
               call(0x81, -420, 1, 1),
               call(0x81, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4
    callsM2 = [call(128, -16000, 2, 1),
                call(128, 0, 0, 0),
                call(129, -2500, 2, 1),
                call(129, 0, 0, 0),
                call(129, 2500, 2188, 0),
                call(129, 0, 0, 0)
               ]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 6

def test_function_standby_encoders_ready_pitch_and_lift_increment_not_less_than_zero_and_rotate_and_launch_less_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    assert True == dl.encoder_ready_check()
    dl.rc = MagicMock()

    # WHEN
    dl.rc.ReadEncM1.return_value=(1,0,0)
    dl.rc.ReadEncM2.return_value=(1,2,0)
    dl.rc.ReadBuffers.return_value = (1, 0, 0x80)
    dl.standby()

    # THEN
    callsM1 = [call(128, 7000, 0, 1),
                call(128, 0, 0, 0),
                call(129, 420, 0, 1),
                call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4
    callsM2 = [call(128, -16000, 2, 1),
                call(128, 0, 0, 0),
                call(129, -2500, 2, 1),
                call(129, 0, 0, 0),
                call(129, 2500, 2188, 0),
                call(129, 0, 0, 0)
               ]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 6


def test_function_standby_encoders_ready_pitch_and_lift_increment_less_than_zero_and_rotate_and_launch_not_less_than_zero(
            dl):
    # GIVEN
    dl.encoders_ready = 1
    assert True == dl.encoder_ready_check()
    dl.rc = MagicMock()

    # WHEN
    dl.rc.ReadEncM1.return_value=(1,1,0)
    dl.rc.ReadEncM2.return_value=(1,0,0)
    dl.rc.ReadBuffers.return_value = (1, 0, 0x80)
    dl.standby()

    # THEN
    callsM1 = [call(0x80, -7000, 1, 1),
               call(0x80, 0, 0, 0),
               call(0x81, -420, 1, 1),
               call(0x81, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4
    callsM2 = [call(128, 16000, 0, 1),
                call(128, 0, 0, 0),
                call(129, 2500, 0, 1),
                call(129, 0, 0, 0),
                call(129, 2500, 2190, 0),
                call(129, 0, 0, 0)
               ]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 6