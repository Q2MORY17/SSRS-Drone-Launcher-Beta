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
    yield dl
    print('\n**********End**********')


def test_encoders_not_ready(dl):
    dl.encoders_ready = 0
    return_value = dl.function_mount()
    assert return_value == ('', 403)


# def test_stuff(dl):
#     dl.rc.ReadEncM1 = MagicMock()
#     dl.encoders_ready = 1
#     dl.pitch_pulses = 0
#     assert dl.function_mount() == ('', 204)
