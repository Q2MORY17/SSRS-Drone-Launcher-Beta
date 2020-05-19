import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../python")
from unittest.mock import MagicMock
import python.infotiv_launcher


# ---------------------------------------------------------------------------------
# ------------------------ Standby-------------------------------------------------
# ---------------------------------------------------------------------------------
@pytest.fixture()
def launcher():
    print('\n*********Start*********')
    launcher = python.infotiv_launcher.Launcher()
    yield launcher
    print('\n**********End**********')

def test_standby(launcher):
    # GIVEN
    launcher.set_pitch_position = MagicMock()
    launcher.set_rotation_position = MagicMock()
    launcher.set_lift_position = MagicMock()
    launcher.set_launch_position = MagicMock()

    # WHEN
    launcher.standby()

    # THEN
    launcher.set_pitch_position.assert_called_with(0)
    launcher.set_rotation_position.assert_called_with(0)
    launcher.set_lift_position.assert_called_once_with(0)
    launcher.set_launch_position.assert_called_with(0)


def test_prepare_launch_function_calls_with_correct_parameters(launcher):
    # GIVEN
    launcher.set_pitch_position = MagicMock()
    launcher.set_rotation_position = MagicMock()
    launcher.set_lift_position = MagicMock()
    launcher.set_launch_position = MagicMock()

    # WHEN
    launcher.prepare_launch()

    # THEN
    launcher.set_pitch_position.assert_called_with(launcher.pitch_ready)
    launcher.set_rotation_position.assert_called_with(launcher.rotation_ready)
    launcher.set_lift_position.assert_called_once_with(launcher.lift_ready)
    launcher.set_launch_position.assert_called_with(0)
