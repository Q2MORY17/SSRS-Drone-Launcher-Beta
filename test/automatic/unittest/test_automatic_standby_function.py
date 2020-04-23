import os
import sys

import flask
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../../python")

from unittest.mock import MagicMock

import python.dronelauncher_python
app = flask.Flask(__name__)


@pytest.fixture()
def dl():
    print('\n*********Start*********')
    dl = python.dronelauncher_python
    return dl


def test_function_standby_encoders_not_ready(dl):
    assert dl.function_standby() == ('', 403)


def test_function_standby_encoders_reader_minimum_pitch(dl):
    dl.encoders_ready = 1
    dl.rc = MagicMock()
    dl.rc.ReadEncM1.return_value=(1,0,0)
    dl.rc.ReadEncM2.return_value=(1,3,0)
    return_value = dl.function_standby()
    #assert dl.rc.SpeedDistanceM1.assert_called_with(129, 0, 0, 0)
    assert return_value== ('', 204)
