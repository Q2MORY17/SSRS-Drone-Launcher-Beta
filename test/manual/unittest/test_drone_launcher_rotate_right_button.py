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


def test_function_rotate_right(dl):
    # GIVEN
    dl.rc.ForwardM2 = MagicMock(return_value=True)


    # WHEN
    returnValue = dl.function_rotation_position()

    # THEN
    dl.rc.ForwardM2.assert_called_with(dl.address, dl.rotation_speed_manual)
    assert returnValue == ('', 204)