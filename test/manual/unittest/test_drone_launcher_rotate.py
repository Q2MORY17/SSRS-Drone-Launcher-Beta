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

def test_function_rotation_right(self):
    # GIVEN
    self.rc.ForwardM2 = MagicMock(return_value=True)


    # WHEN
    returnValue = self.function_rotation_right()

    # THEN
    self.rc.ForwardM2.assert_called_with(self.address, self.rotation_speed_manual)
    assert returnValue == ('', 204)


def test_function_rotation_left(self):
    # GIVEN
    self.rc.BackwardM2 = MagicMock(return_value=True)

    # WHEN
    returnValue = self.function_rotation_left()

    # THEN
    self.rc.BackwardM2.assert_called_with(self.address, self.rotation_speed_manual)
    assert returnValue == ('', 204)


def test_function_rotation_right_with_invalid_speed(self):
    # GIVEN
    self.rc = MagicMock()

    # WHEN
    self.rotation_speed_manual = 16
    returnValue = self.function_rotation_right()

    # THEN
    self.rc.ForwardM2.assert_called_with(self.address, 16)
    assert returnValue != ('', 204)


def test_function_rotation_left_with_invalid_speed(self):
    # GIVEN
    self.rc = MagicMock()

    # WHEN
    self.rotation_speed_manual = 16000
    returnValue = self.function_rotation_left()

    # THEN
    self.rc.BackwardM2.assert_called_with(self.address, 16000)
    assert returnValue != ('', 204)


def test_function_rotation_position_encoders_not_ready(self):
    # GIVEN
    self.encoders_ready = 0

    # WHEN
    returnValue = self.function_rotation_position()

    # THEN
    assert returnValue == ('', 403)


invalid_data_over_boundary = {181, -181}


@pytest.mark.parametrize("invalid_data", invalid_data_over_boundary)
def test_function_roatation_position_encoders_ready_with_invalid_value(self, invalid_data):

    # GIVEN
    self.encoders_ready = 1

    # WHEN
    with app.test_request_context('app_rotation_position', data={'rotation_position': invalid_data}):
        
    # THEN
     assert self.function_rotation_position() == ('', 400)



def test_function_rotation_position_encoders_ready_rotation_position_zero(self):
    
    # GIVEN
    self.encoders_ready = 1
    app_client = self.app.test_client()
    self.rc = MagicMock()
    self.rc.ReadEncM2.return_value = (3, 5, 7)


    # WHEN
    response = app_client.post('/app_rotation_position', content_type='multipart/form-data',
                               data={'rotation_position': '0'})

    # THEN
    assert response.status_code == 204
    calls = [call(128, -16000, 5, 1),
             call(128, 0, 0, 0)]
    self.rc.SpeedDistanceM2.assert_has_calls(calls)
    assert self.rc.SpeedDistanceM2.call_count == 2


def test_function_rotation_position_encoders_ready_rotation_position_higher_than_zero(self):
   
    # GIVEN
    self.encoders_ready = 1
    app_client = self.app.test_client()
    self.rc = MagicMock()
    self.rc.ReadEncM2.return_value = (2, 7, 3)

    # WHEN
    response = app_client.post('/app_rotation_position', content_type='multipart/form-data',
                               data={'rotation_position': '120'})

    # THEN
    assert response.status_code == 204
    calls = [call(128, 16000, 316659, 1),
             call(128, 0, 0, 0)]
    self.rc.SpeedDistanceM2.assert_has_calls(calls)
    assert self.rc.SpeedDistanceM2.call_count == 2


def test_function_rotation_position_encoders_ready_rotation_position_max(self):
    
    # GIVEN
    self.encoders_ready = 1
    app_client = self.app.test_client()
    self.rc = MagicMock()
    self.rc.ReadEncM2.return_value = (7, -8, 1)

    # WHEN
    response = app_client.post('/app_rotation_position', content_type='multipart/form-data',
                               data={'rotation_position': '180'})

    # THEN
    assert response.status_code == 204
    calls = [call(128, 16000, 475008, 1),
             call(128, 0, 0, 0)]

    self.rc.SpeedDistanceM2.assert_has_calls(calls)
    assert self.rc.SpeedDistanceM2.call_count == 2


def test_function_rotation_stop(self):
    
    # GIVEN
    self.rc.ForwardM2 = MagicMock(return_value=True)

    # WHEN
    returnValue = self.function_rotation_stop()

    # THEN
    self.rc.ForwardM2.assert_called_with(self.address, 0)
    assert returnValue == ('', 204)
