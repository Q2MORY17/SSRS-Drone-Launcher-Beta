import pytest, os, sys, flask
from unittest.mock import MagicMock, call

#sys.path.insert(0, "../../../python")
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../../python")

import python.dronelauncher_python


app = flask.Flask(__name__)


@pytest.fixture()
def self():
    self = python.dronelauncher_python
    return self

def test_function_pitch_up(self):
    # GIVEN
    self.rc.BackwardM1 = MagicMock(return_value=True)

    # WHEN
    returnValue = self.function_pitch_up()

    # THEN
    self.rc.BackwardM1.assert_called_with(self.address, self.pitch_speed_manual)
    assert returnValue == ('', 204)


def test_function_pitch_down(self):
    # GIVEN
    self.rc.ForwardM1 = MagicMock(return_value=True)

    # WHEN
    returnValue = self.function_pitch_down()

    # THEN
    self.rc.ForwardM1.assert_called_with(self.address, self.pitch_speed_manual)
    assert returnValue == ('', 204)


def test_function_pitch_up_with_invalid_speed(self):
    # GIVEN
    self.rc = MagicMock()

    # WHEN
    self.pitch_speed_manual = 128
    returnValue = self.function_pitch_up()

    # THEN
    self.rc.BackwardM1.assert_called_with(self.address, 128)
    assert returnValue != ('', 204)


def test_function_pitch_down_with_invalid_speed(self):
    # GIVEN
    self.rc = MagicMock()

    # WHEN
    self.pitch_speed_manual = -1
    returnValue = self.function_pitch_down()

    # THEN
    self.rc.ForwardM1.assert_called_with(self.address, -1)
    assert returnValue != ('', 204)


def test_function_pitch_position_encoders_not_ready(self):
    # GIVEN
    self.encoders_ready = 0

    # WHEN
    returnValue = self.function_pitch_position()

    # THEN
    assert returnValue == ('', 403)


invalid_data_over_boundary = {91, -1}
@pytest.mark.parametrize("invalid_data", invalid_data_over_boundary)
def test_function_pitch_position_encoders_ready_with_invalid_value(self, invalid_data):

    # GIVEN
    self.encoders_ready = 1

    # WHEN
    with app.test_request_context('app_pitch_position', data={'pitch_position': invalid_data}):
        
    # THEN
     assert self.function_pitch_position() == ('', 400)



def test_function_pitch_position_encoders_ready_pitch_position_zero(self):
    
    # GIVEN
    self.encoders_ready = 1
    app_client = self.app.test_client()
    self.rc = MagicMock()
    self.rc.ReadEncM1.return_value = (3, 5, 7)


    # WHEN
    response = app_client.post('/app_pitch_position', content_type='multipart/form-data',
                               data={'pitch_position': '0'})

    
    # THEN
    assert response.status_code == 204
    calls = [call(128, -7000, 5, 1),
             call(128, 0, 0, 0)]
    self.rc.SpeedDistanceM1.assert_has_calls(calls)
    assert self.rc.SpeedDistanceM1.call_count == 2


def test_function_pitch_position_encoders_ready_pitch_position_higher_than_zero(self):
   
    # GIVEN
    self.encoders_ready = 1
    app_client = self.app.test_client()
    self.rc = MagicMock()
    self.rc.ReadEncM1.return_value = (2, 7, 3)

    # WHEN
    response = app_client.post('/app_pitch_position', content_type='multipart/form-data',
                               data={'pitch_position': '20'})

    # THEN
    assert response.status_code == 204
    calls = [call(128, 7000, 78881, 1),
             call(128, 0, 0, 0)]
    self.rc.SpeedDistanceM1.assert_has_calls(calls)
    assert self.rc.SpeedDistanceM1.call_count == 2


def test_function_pitch_position_encoders_ready_pitch_position_max(self):
    
    # GIVEN
    self.encoders_ready = 1
    app_client = self.app.test_client()
    self.rc = MagicMock()
    self.rc.ReadEncM1.return_value = (7, -8, 1)

    # WHEN
    response = app_client.post('/app_pitch_position', content_type='multipart/form-data',
                               data={'pitch_position': '90'})

    # THEN
    assert response.status_code == 204
    calls = [call(128, 7000, 355008, 1),
             call(128, 0, 0, 0)]

    self.rc.SpeedDistanceM1.assert_has_calls(calls)
    assert self.rc.SpeedDistanceM1.call_count == 2


def test_function_pitch_stop(self):
    
    # GIVEN
    self.rc.ForwardM1 = MagicMock(return_value=True)

    # WHEN
    returnValue = self.function_pitch_stop()

    # THEN
    self.rc.ForwardM1.assert_called_with(self.address, 0)
    assert returnValue == ('', 204)
