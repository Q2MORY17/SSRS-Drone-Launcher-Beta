import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../python")
from unittest.mock import MagicMock
import python.infotiv_launcher





# ---------------------------------------------------------------------------------
# ------------------------ Standby-------------------------------------
# ---------------------------------------------------------------------------------
@pytest.fixture()
def dl():
    print('\n*********Start*********')
    dl = python.infotiv_launcher.Launcher()
    yield dl
    print('\n**********End**********')

def test_standby(dl):
    # GIVEN
    dl.set_pitch_position = MagicMock()
    dl.set_rotation_position = MagicMock()
    dl.set_lift_position = MagicMock()
    dl.set_launch_position = MagicMock()

    # WHEN
    dl.standby()

    # THEN
    dl.set_pitch_position.assert_called_with(0)
    dl.set_rotation_position.assert_called_with(0)
    dl.set_lift_position.assert_called_once_with(0)
    dl.set_launch_position.assert_called_with(0)


def test_prepare_launch_function_calls_with_correct_parameters(dl):
    # Mock all the functions inside prepare_launch
    dl.set_pitch_position = MagicMock()
    dl.set_rotation_position = MagicMock()
    dl.set_lift_position = MagicMock()
    dl.set_launch_position = MagicMock()

    # Use the prepare_launch function to run all the function calls
    dl.prepare_launch()

    # Check if all the functions were called with the correct parameters
    dl.set_pitch_position.assert_called_with(dl.pitch_ready)
    dl.set_rotation_position.assert_called_with(dl.rotation_ready)
    dl.set_lift_position.assert_called_once_with(dl.lift_ready)
    dl.set_launch_position.assert_called_with(0)
