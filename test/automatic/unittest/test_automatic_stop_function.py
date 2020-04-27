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


def test_function_stop(dl):
    # GIVEN
    dl.rc.ForwardM1 = MagicMock(return_value=True)
    dl.rc.ForwardM2 = MagicMock(return_value=True)

    # WHEN
    returnValue = dl.function_stop()

    # THEN
    dl.rc.ForwardM1.assert_any_call(dl.address,0)
    dl.rc.ForwardM2.assert_any_call(dl.address, 0)
    dl.rc.ForwardM1.assert_any_call(dl.address_2,0)
    dl.rc.ForwardM2.assert_any_call(dl.address_2, 0)
    assert dl.rc.ForwardM1.call_count == 2
    assert dl.rc.ForwardM2.call_count == 2
    assert returnValue == ('', 204)