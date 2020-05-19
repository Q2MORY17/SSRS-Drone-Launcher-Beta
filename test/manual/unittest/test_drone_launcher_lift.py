import pytest
import os
import sys

import flask


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../../python")

from unittest.mock import MagicMock, call

import python.dronelauncher_python
app = flask.Flask(__name__)


@pytest.fixture()
def self():
    self = python.dronelauncher_python
    return self

def test_function_lift_up(self):
    # GIVEN
    self.rc.ForwardM1 = MagicMock(return_value=True)


    # WHEN
    returnValue = self.function_lift_up()

    # THEN
    self.rc.ForwardM1.assert_called_with(self.address_2, self.lift_speed_manual)
    assert returnValue == ('', 204)

def test_function_lift_down(self):
    # GIVEN
    self.rc.BackwardM1 = MagicMock(return_value=True)

    # WHEN
    returnValue = self.function_lift_down()

    # THEN
    self.rc.BackwardM1.assert_called_with(self.address_2, self.lift_speed_manual)
    assert returnValue == ('', 204)


def test_function_lift_stop(self):
    # GIVEN
    self.rc.ForwardM1 = MagicMock(return_value=True)

    # WHEN
    returnValue = self.function_lift_stop()

    # THEN
    self.rc.ForwardM1.assert_called_with(self.address_2, 0)
    assert returnValue == ('', 204)


def test_function_lift_up_with_invalid_speed(self):
    # GIVEN
    self.rc = MagicMock()

    # WHEN
    self.lift_speed_manual = 127
    returnValue = self.function_lift_up()

    # THEN
    self.rc.ForwardM1.assert_called_with(self.address_2, 127)
    assert returnValue != ('', 204)


def test_function_lift_down_with_invalid_speed(self):
    # GIVEN
    self.rc = MagicMock()

    # WHEN
    self.lift_speed_manual = 127
    returnValue = self.function_lift_down()

    # THEN
    self.rc.BackwardM1.assert_called_with(self.address_2, 127)
    assert returnValue != ('', 204)


def test_function_lift_position_encoders_not_ready(self):
    # GIVEN
    self.encoders_ready = 0

    # WHEN
    returnValue = self.function_lift_position()

    # THEN
    assert returnValue == ('', 403)


invalid_data_over_boundary = {131, -1}


@pytest.mark.parametrize("invalid_data", invalid_data_over_boundary)
def test_function_lift_position_encoders_ready_with_invalid_value(self, invalid_data):
    # GIVEN
    self.encoders_ready = 1

    # WHEN
    with app.test_request_context('app_lift_position', data={'lift_position': invalid_data}):
        # THEN
        assert self.function_lift_position() == ('', 400)


def test_function_lift_position_encoders_ready_lift_position_zero(self):
    # GIVEN
    self.encoders_ready = 1
    app_client = self.app.test_client()
    self.rc = MagicMock()
    self.rc.ReadEncM1.return_value = (3, 5, 7)

    # WHEN
    response = app_client.post('/app_lift_position', content_type='multipart/form-data',
                               data={'lift_position': '0'})

    # THEN
    assert response.status_code == 204
    calls = [call(129, -420, 5, 1),
             call(129, 0, 0, 0)]
    self.rc.SpeedDistanceM1.assert_has_calls(calls)
    assert self.rc.SpeedDistanceM1.call_count == 2


def test_function_lift_position_encoders_ready_lift_position_higher_than_zero(self):
    # GIVEN
    self.encoders_ready = 1
    app_client = self.app.test_client()
    self.rc = MagicMock()
    self.rc.ReadEncM1.return_value = (2, 7, 3)

    # WHEN
    response = app_client.post('/app_lift_position', content_type='multipart/form-data',
                               data={'lift_position': '120'})

    # THEN
    assert response.status_code == 204
    calls = [call(129, 420, 17531, 1),
             call(129, 0, 0, 0)]
    self.rc.SpeedDistanceM1.assert_has_calls(calls)
    assert self.rc.SpeedDistanceM1.call_count == 2


def test_function_lift_position_encoders_ready_lift_position_max(self):
    # GIVEN
    self.encoders_ready = 1
    app_client = self.app.test_client()
    self.rc = MagicMock()
    self.rc.ReadEncM1.return_value = (7, -8, 1)

    # WHEN
    response = app_client.post('/app_lift_position', content_type='multipart/form-data',
                               data={'lift_position': '130'})

    # THEN
    assert response.status_code == 204
    calls = [call(129, 420, 19008, 1),
             call(129, 0, 0, 0)]

    self.rc.SpeedDistanceM1.assert_has_calls(calls)
    assert self.rc.SpeedDistanceM1.call_count == 2

