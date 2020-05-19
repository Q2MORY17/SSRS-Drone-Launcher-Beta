import os
import sys

import flask
import pytest
from unittest.mock import MagicMock, call

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../../python")

import python.dronelauncher_python

app = flask.Flask(__name__)


@pytest.fixture()
def dl():
    print('\n*********Start*********')
    dl = python.dronelauncher_python
    orig_launch_speed = dl.launch_speed_manual  # = 12
    dl.rc = MagicMock()
    yield dl
    dl.launch_speed_manual = orig_launch_speed
    print('\n**********End**********')


def test_function_launch_backwards_with_valid_speed(dl):
    # WHEN
    return_value = dl.function_launch_backwards()

    # THEN
    dl.rc.BackwardM2.assert_called_with(dl.address_2, dl.launch_speed_manual)
    assert return_value == ('', 204)


# Test fails because no handling for invalid input speed
def test_function_launch_backwards_with_invalid_speed(dl):
    # WHEN
    dl.launch_speed_manual = 30000
    return_value = dl.function_launch_backwards()

    # THEN
    dl.rc.BackwardM2.assert_called_with(dl.address_2, 30000)
    assert return_value != ('', 204)


def test_function_launch_forwards_with_valid_speed(dl):
    # WHEN
    return_value = dl.function_launch_forwards()

    # THEN
    dl.rc.ForwardM2.assert_called_with(dl.address_2, dl.launch_speed_manual)
    assert return_value == ('', 204)


# Test fails because no handling for invalid input speed
def test_function_launch_forwards_with_invalid_speed(dl):
    # WHEN
    dl.launch_speed_manual = 999
    return_value = dl.function_launch_forwards()

    # THEN
    dl.rc.ForwardM2.assert_called_with(dl.address_2, 999)
    assert return_value != ('', 204)


def test_function_launch_stop(dl):
    # WHEN
    return_value = dl.function_launch_stop()

    # THEN
    dl.rc.ForwardM2.assert_called_with(dl.address_2, 0)
    assert return_value == ('', 204)


def test_function_launch_position_encoders_not_ready(dl):
    # GIVEN
    dl.encoders_ready = 0

    # WHEN
    return_value = dl.function_launch_position()

    # THEN
    assert return_value == ('', 403)


invalid_data_over_boundary = {112, -1}


@pytest.mark.parametrize("invalid_data", invalid_data_over_boundary)
def test_function_launch_position_encoders_ready_with_invalid_value(dl, invalid_data):
    # Creates a flask request context
    # GIVEN
    dl.encoders_ready = 1

    # WHEN
    with app.test_request_context('/app_launch_position', data={'launch_position': invalid_data}):
        # THEN
        assert dl.function_launch_position() == ('', 400)


def test_function_launch_position_encoders_ready_launch_position_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    app_client = dl.app.test_client()
    dl.rc.ReadEncM2.return_value = (1, 2, 2)
    dl.rc.ReadBuffers.return_value = (0, 0, 0x80)

    # WHEN
    response = app_client.post('/app_launch_position', content_type='multipart/form-data',
                               data={'launch_position': '0'})

    # THEN
    assert response.status_code == 204
    calls = [call(dl.address_2, -dl.launch_speed_pulses_slow, 2, 1),
             call(dl.address_2, 0, 0, 0),
             call(dl.address_2, dl.launch_speed_pulses_slow, 2188, 0),
             call(dl.address_2, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(calls)
    assert dl.rc.SpeedDistanceM2.call_count == 4


def test_function_launch_position_encoders_ready_launch_position_higher_than_zero(dl):
    # GIVEN
    dl.encoders_ready = 1
    app_client = dl.app.test_client()
    dl.rc.ReadEncM2.return_value = (1, 4, 2)
    dl.rc.ReadBuffers.return_value = (0, 0, 0x80)

    # WHEN
    response = app_client.post('/app_launch_position', content_type='multipart/form-data',
                               data={'launch_position': '10'})

    # THEN
    assert response.status_code == 204
    calls = [call(dl.address_2, -dl.launch_speed_pulses_slow, 4, 1),
             call(dl.address_2, 0, 0, 0),
             call(dl.address_2, dl.launch_speed_pulses_slow, 3519, 0),
             call(dl.address_2, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(calls)
    assert dl.rc.SpeedDistanceM2.call_count == 4


def test_function_launch_position_encoders_ready_launch_position_max(dl):
    # GIVEN
    dl.encoders_ready = 1
    app_client = dl.app.test_client()
    dl.rc.ReadEncM2.return_value = (1, -1.5, 2)
    dl.rc.ReadBuffers.return_value = (0, 0, 0x80)

    # WHEN
    response = app_client.post('/app_launch_position', content_type='multipart/form-data',
                               data={'launch_position': '111'})

    # THEN
    assert response.status_code == 204
    calls = [call(dl.address_2, dl.launch_speed_pulses_slow, 1.5, 1),
             call(dl.address_2, 0, 0, 0),
             call(dl.address_2, dl.launch_speed_pulses_slow, 16991.5, 0),
             call(dl.address_2, 0, 0, 0)]
    dl.rc.SpeedDistanceM2.assert_has_calls(calls)
    assert dl.rc.SpeedDistanceM2.call_count == 4
