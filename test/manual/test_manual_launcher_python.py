import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../python")

from unittest.mock import MagicMock

import python.dronelauncher_python as dl


def test_function_launch_backwards_with_valid_speed():
    # GIVEN
    dl.rc.BackwardM2 = MagicMock(return_value=True)

    # WHEN
    returnValue = dl.function_launch_backwards()

    # THEN
    dl.rc.BackwardM2.assert_called_with(dl.address_2, dl.launch_speed_manual)
    assert returnValue == ('', 204)


def test_function_launch_forwards_with_valid_speed():
    # GIVEN
    dl.rc.ForwardM2 = MagicMock(return_value=True)

    # WHEN
    returnValue = dl.function_launch_forwards()

    # THEN
    dl.rc.ForwardM2.assert_called_with(dl.address_2, dl.launch_speed_manual)
    assert returnValue == ('', 204)


def test_function_launch_stop():
    # GIVEN
    dl.rc.ForwardM2 = MagicMock(return_value=True)
    # WHEN
    returnValue = dl.function_launch_stop()
    # THEN
    dl.rc.ForwardM2.assert_called_with(dl.address_2, 0)
    assert returnValue == ('', 204)


def test_function_launch_position_encoders_not_ready():
    # GIVEN
    dl.encoders_ready = 0
    # WHEN
    returnValue = dl.function_launch_position()
    # THEN
    assert returnValue == ('', 403)
