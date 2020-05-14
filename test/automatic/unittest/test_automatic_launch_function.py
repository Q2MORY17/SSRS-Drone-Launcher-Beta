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
    return_value = dl.function_launch()
    assert return_value == ('', 403)


def test_encoders_ready_launch_increment_higher_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()
    dl.rc.ReadEncM2.return_value = (1, -2)   # launch_actual = -2, launch_increment= 2

    # WHEN
    return_value = dl.function_launch()

    # THEN
    assert return_value == ('', 204)
    callsM2 = [call(dl.address_2, dl.launch_speed_pulses_slow, 2, 1),
               call(dl.address_2, 0, 0, 0),
               call(dl.address_2, dl.launch_speed_pulses_slow, dl.launch_connect, 0),
               call(dl.address_2, 0, 0, 0),
               call(dl.address_2, 0, 0, 0)]
    dl.rc.SpeedAccelDistanceM2.assert_called_with(dl.address_2, dl.launch_acceleration, dl.launch_speed_pulses, 18810, 0)
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 5


def test_encoders_ready_launch_increment_lower_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()
    dl.rc.ReadEncM2.return_value = (1, 10)   # launch_actual = 10, launch_increment= -10

    # WHEN
    return_value = dl.function_launch()

    # THEN
    assert return_value == ('', 204)
    callsM2 = [call(dl.address_2, -dl.launch_speed_pulses_slow, 10, 1),
               call(dl.address_2, 0, 0, 0),
               call(dl.address_2, dl.launch_speed_pulses_slow, dl.launch_connect, 0),
               call(dl.address_2, 0, 0, 0),
               call(dl.address_2, 0, 0, 0)]
    dl.rc.SpeedAccelDistanceM2.assert_called_with(dl.address_2, dl.launch_acceleration, dl.launch_speed_pulses, 18810, 0)
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 5


def test_encoders_ready_launch_increment_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    dl.rc = MagicMock()
    dl.rc.ReadEncM2.return_value = (1, 0)   # launch_actual = 0, launch_increment= 0

    # WHEN
    return_value = dl.function_launch()

    # THEN
    assert return_value == ('', 204)
    callsM2 = [call(dl.address_2, dl.launch_speed_pulses_slow, 0, 1),
               call(dl.address_2, 0, 0, 0),
               call(dl.address_2, dl.launch_speed_pulses_slow, dl.launch_connect, 0),
               call(dl.address_2, 0, 0, 0),
               call(dl.address_2, 0, 0, 0)]
    dl.rc.SpeedAccelDistanceM2.assert_called_with(dl.address_2, dl.launch_acceleration, dl.launch_speed_pulses, 18810, 0)
    dl.rc.SpeedDistanceM2.assert_has_calls(callsM2)
    assert dl.rc.SpeedDistanceM2.call_count == 5
