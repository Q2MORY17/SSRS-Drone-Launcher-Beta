import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../../python")
from unittest.mock import MagicMock, call
import python.dronelauncher_python

#DONE
@pytest.fixture()
def dl():
    print('\n*********Start*********')
    dl = python.dronelauncher_python
    yield dl
    print('\n**********End**********')


def test_function_standby_encoders_not_ready(dl):
    assert dl.function_standby() == ('', 403)

def test_function_standby_encoders_ready_all_increment_not_less_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()

    # WHEN
    dl.rc.ReadEncM1.return_value=(1,0,0)
    dl.rc.ReadEncM2.return_value=(1,0,0)
    return_value = dl.function_standby()

    # THEN
    assert return_value== ('', 204)

    callsM1 = [call(0x80, 7000, 0, 1),
               call(0x80, 0, 0, 0),
               call(0x81, 420, 0, 1),
               call(0x81, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4

    callsM2 = [call(0x80, 16000, 0, 1),
               call(0x80, 0, 0, 0),
               call(0x81, 2500, 0, 1),
               call(0x81, 0, 0, 0),
               call(0x81, 2500, 8000, 0),
               call(0x81, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 6

def test_function_standby_encoders_ready_all_increment_less_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()

    # WHEN
    dl.rc.ReadEncM1.return_value=(1,1,0)
    dl.rc.ReadEncM2.return_value=(1,2,0)
    return_value = dl.function_standby()

    # THEN
    assert return_value== ('', 204)

    callsM1 = [call(0x80, -7000, 1, 1),
               call(0x80, 0, 0, 0),
               call(0x81, -420, 1, 1),
               call(0x81, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4

    callsM2 = [call(0x80, -16000, 2, 1),
               call(0x80, 0, 0, 0),
               call(0x81, -2500, 2, 1),
               call(0x81, 0, 0, 0),
               call(0x81, 2500, 8000, 0),
               call(0x81, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 6



def test_function_standby_encoders_ready_pitch_and_lift_increment_not_less_than_zero_and_rotate_and_launch_less_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()

    # WHEN
    dl.rc.ReadEncM1.return_value = (1,0,0)
    dl.rc.ReadEncM2.return_value = (1,2,0)
    return_value = dl.function_standby()

    # THEN
    assert return_value == ('', 204)

    callsM1 = [call(0x80, 7000, 0, 1),
               call(0x80, 0, 0, 0),
               call(0x81, 420, 0, 1),
               call(0x81, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4
    callsM2 = [call(0x80, -16000, 2, 1),
               call(0x80, 0, 0, 0),
               call(0x81, -2500, 2, 1),
               call(0x81, 0, 0, 0),
               call(0x81, 2500, 8000, 0),
               call(0x81, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 6


def test_function_standby_encoders_ready_pitch_and_lift_increment_less_than_zero_and_rotate_and_launch_not_less_than_zero(
            dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()

    # WHEN
    dl.rc.ReadEncM1.return_value = (1,1,0)
    dl.rc.ReadEncM2.return_value = (1,0,0)
    return_value = dl.function_standby()

    # THEN
    assert return_value == ('', 204)

    callsM1 = [call(0x80, -7000, 1, 1),
               call(0x80, 0, 0, 0),
               call(0x81, -420, 1, 1),
               call(0x81, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4
    callsM2 = [call(0x80, 16000, 0, 1),
               call(0x80, 0, 0, 0),
               call(0x81, 2500, 0, 1),
               call(0x81, 0, 0, 0),
               call(0x81, 2500, 8000, 0),
               call(0x81, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 6