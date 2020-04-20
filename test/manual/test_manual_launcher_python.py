import os
import sys

import flask
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../python")

from unittest.mock import MagicMock

import python.dronelauncher_python
app = flask.Flask(__name__)
@pytest.fixture()
def dl():
    print('\n*********Start*********')
    dl = python.dronelauncher_python
    yield dl
    print('\n**********End**********')


def test_function_launch_backwards_with_valid_speed(dl):
    # GIVEN
    dl.rc.BackwardM2 = MagicMock(return_value=True)

    # WHEN
    returnValue = dl.function_launch_backwards()

    # THEN
    dl.rc.BackwardM2.assert_called_with(dl.address_2, dl.launch_speed_manual)
    assert returnValue == ('', 204)


def test_function_launch_forwards_with_valid_speed(dl):
    # GIVEN
    dl.rc.ForwardM2 = MagicMock(return_value=True)

    # WHEN
    returnValue = dl.function_launch_forwards()

    # THEN
    dl.rc.ForwardM2.assert_called_with(dl.address_2, dl.launch_speed_manual)
    assert returnValue == ('', 204)


def test_function_launch_stop(dl):
    # GIVEN
    dl.rc.ForwardM2 = MagicMock(return_value=True)
    # WHEN
    returnValue = dl.function_launch_stop()
    # THEN
    dl.rc.ForwardM2.assert_called_with(dl.address_2, 0)
    assert returnValue == ('', 204)


def test_function_launch_position_encoders_not_ready(dl):
    # GIVEN
    dl.encoders_ready = 0
    # WHEN
    returnValue = dl.function_launch_position()
    # THEN
    assert returnValue == ('', 403)

invalid_data_over_boundary={112,-1}
@pytest.mark.parametrize("invalid_data",invalid_data_over_boundary)
def test_function_launch_position_encoders_ready_with_large_value(dl,invalid_data):
    #Creates a flask request context
    # GIVEN
    dl.encoders_ready = 1
    # WHEN
    with app.test_request_context('/app_launch_position',data={'launch_position': invalid_data}):
        # THEN
        assert dl.function_launch_position() == ('', 400)