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
    assert returnValue == ('', 204)



