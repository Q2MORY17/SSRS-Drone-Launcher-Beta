import os
import sys

import flask
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../../python")

from unittest.mock import MagicMock, call

import python.dronelauncher_python

app = flask.Flask(__name__)


@pytest.fixture()
def dl():
    print('\n*********Start*********')
    dl = python.dronelauncher_python
    yield dl
    print('\n**********End**********')


def test_encoders_not_ready(dl):
    dl.encoders_ready = 0
    return_value = dl.function_mount()
    assert return_value == ('', 403)


def test_encoders_ready_pitch_increment_higher_than_zero_rotation_increment_lower_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()
    dl.rc.ReadEncM1.return_value = (1, 2, 5)  # pitch_actual = 2  #pitch_increment= 354998  #lift_incr= -2
    dl.rc.ReadEncM2.return_value = (1, 1, 8)  # rotation_increment = -1   #launch_increment= -1

    # WHEN
    return_value = dl.function_mount()

    # THEN
    assert return_value == ('', 204)
    callsM1 = [call(128, 7000, 354998, 1),
               call(128, 0, 0, 0),
               call(129, -420, 2, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4
    callsM2 = [call(128, -16000, 1, 1),
               call(128, 0, 0, 0),
               call(129, -2500, 1, 1),
               call(129, 0, 0, 0),
               call(129, 2500, 17000, 0),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 6


def test_encoders_ready_pitch_increment_lower_than_zero_rotation_increment_higher_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()
    dl.rc.ReadEncM1.return_value = (1, 360000, 5)  # pitch_actual = 360000  #pitch_increment= -5000 #lift_incr= -360000
    dl.rc.ReadEncM2.return_value = (1, -1, 8)  # rotation_increment = 1   #launch_increment= 1

    # WHEN
    return_value = dl.function_mount()

    # THEN
    assert return_value == ('', 204)
    callsM1 = [call(128, -7000, 5000, 1),
               call(128, 0, 0, 0),
               call(129, -420, 360000, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4
    callsM2 = [call(128, 16000, 1, 1),
               call(128, 0, 0, 0),
               call(129, 2500, 1, 1),
               call(129, 0, 0, 0),
               call(129, 2500, 17000, 0),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 6


def test_encoders_ready_lift_increment_higher_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()
    dl.rc.ReadEncM1.return_value = (1, -2, 5)  # pitch_actual = -2  #pitch_increment= 355002  #lift_incr= 2
    dl.rc.ReadEncM2.return_value = (1, -10, 8)  # rotation_increment = 10   #launch_increment= 10

    # WHEN
    return_value = dl.function_mount()

    # THEN
    assert return_value == ('', 204)
    callsM1 = [call(128, 7000, 355002, 1),
               call(128, 0, 0, 0),
               call(129, 420, 2, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4
    callsM2 = [call(128, 16000, 10, 1),
               call(128, 0, 0, 0),
               call(129, 2500, 10, 1),
               call(129, 0, 0, 0),
               call(129, 2500, 17000, 0),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 6
