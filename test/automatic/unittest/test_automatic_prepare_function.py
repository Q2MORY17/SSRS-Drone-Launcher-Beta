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
    orig_pitch_ready = dl.pitch_ready
    orig_rotation_ready = dl.rotation_ready
    orig_lift_ready = dl.lift_ready
    orig_launch_bottom = dl.launch_bottom
    yield dl
    print('\n**********End**********')
    dl.pitch_ready = orig_pitch_ready
    dl.rotation_ready = orig_rotation_ready
    dl.lift_ready = orig_lift_ready
    dl.launch_bottom = orig_launch_bottom


def test_encoders_not_ready(dl):
    dl.encoders_ready = 0
    return_value = dl.function_prepare()
    assert return_value == ('', 403)


def test_all_increment_negative(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()
    dl.pitch_ready = 0
    dl.rotation_ready = 0
    dl.lift_ready = 0

    dl.rc.ReadEncM1.return_value = (1, 2)
    dl.rc.ReadEncM2.return_value = (1, 1)

    # WHEN
    return_value = dl.function_prepare()

    # THEN
    assert return_value == ('', 204)
    callsM1 = [call(128, -7000, 2, 1),
               call(128, 0, 0, 0),
               call(129, -420, 2, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4
    callsM2 = [call(128, -16000, 1, 1),
               call(128, 0, 0, 0),
               call(129, -2500, 1, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 4


def test_all_increment_higher_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()
    dl.rc.ReadEncM1.return_value = (1, -2)
    dl.rc.ReadEncM2.return_value = (1, -10)

    # WHEN
    return_value = dl.function_prepare()

    # THEN
    assert return_value == ('', 204)
    callsM1 = [call(128, 7000, 276113, 1),
               call(128, 0, 0, 0),
               call(129, 420, 19002, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4
    callsM2 = [call(128, 16000, 52787, 1),
               call(128, 0, 0, 0),
               call(129, 2500, 10, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 4


def test_lift_increment_negative(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()
    dl.rc.ReadEncM1.return_value = (1, 360000)
    dl.rc.ReadEncM2.return_value = (1, -1)

    # WHEN
    return_value = dl.function_prepare()

    # THEN
    assert return_value == ('', 204)
    callsM1 = [call(128, -7000, 83889, 1),
               call(128, 0, 0, 0),
               call(129, -420, 341000, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4
    callsM2 = [call(128, 16000, 52778, 1),
               call(128, 0, 0, 0),
               call(129, 2500, 1, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 4


def test_own_invalid_ready_variables(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()
    dl.pitch_ready = 71
    dl.rotation_ready = 11
    dl.lift_ready = 131
    dl.launch_bottom = 1

    dl.rc.ReadEncM1.return_value = (1, 2)
    dl.rc.ReadEncM2.return_value = (1, 1)

    # WHEN
    return_value = dl.function_prepare()

    # THEN
    assert return_value == ('', 204)
    callsM1 = [call(128, 7000, 280053, 1),
               call(128, 0, 0, 0),
               call(129, 420, 19144, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4
    callsM2 = [call(128, 16000, 58054, 1),
               call(128, 0, 0, 0),
               call(129, 2500, 0, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 4


def test_increments_higher_than_max_value(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()
    dl.pitch_ready = 71
    dl.rotation_ready = 11
    dl.lift_ready = 131
    dl.launch_bottom = 1

    dl.rc.ReadEncM1.return_value = (1, 2)
    dl.rc.ReadEncM2.return_value = (1, 1)

    # WHEN
    return_value = dl.function_prepare()

    # THEN
    assert return_value == ('', 204)
    callsM1 = [call(128, 7000, 280053, 1),
               call(128, 0, 0, 0),
               call(129, 420, 19144, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4
    callsM2 = [call(128, 16000, 58054, 1),
               call(128, 0, 0, 0),
               call(129, 2500, 0, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 4


def test_pitch_launch_increments_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()

    dl.rc.ReadEncM1.return_value = (1, 276111)
    dl.rc.ReadEncM2.return_value = (1, 0)

    # WHEN
    return_value = dl.function_prepare()

    # THEN
    assert return_value == ('', 204)
    callsM1 = [call(128, 7000, 0, 1),
               call(128, 0, 0, 0),
               call(129, -420, 257111, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4
    callsM2 = [call(128, 16000, 52777, 1),
               call(128, 0, 0, 0),
               call(129, 2500, 0, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 4


def test_rotation_lift_increments_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()

    dl.rc.ReadEncM1.return_value = (1, 19000)
    dl.rc.ReadEncM2.return_value = (1, 52777)

    # WHEN
    return_value = dl.function_prepare()

    # THEN
    assert return_value == ('', 204)
    callsM1 = [call(128, 7000, 257111, 1),
               call(128, 0, 0, 0),
               call(129, 420, 0, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM1.assert_has_calls(callsM1)
    assert dl.rc.SpeedDistanceM1.call_count == 4
    callsM2 = [call(128, 16000, 0, 1),
               call(128, 0, 0, 0),
               call(129, -2500, 52777, 1),
               call(129, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 4
