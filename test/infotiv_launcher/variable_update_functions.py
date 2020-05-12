import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../python")

import pytest
import python.infotiv_launcher


@pytest.fixture()
def launcher():
    print('\n*********Start*********')
    launcher = python.infotiv_launcher.Launcher()
    yield launcher
    print('\n**********End**********')


@pytest.mark.parametrize("invalid_data", [(-1), (11), (0)])
def test_change_speed_invalid(launcher, invalid_data):
    with pytest.raises(Exception, match='Out of Bounds') as err:
        launcher.change_speed(invalid_data)
        assert err.type is ValueError


@pytest.mark.parametrize("data", [(8), (10)])
def test_change_speed_above_7(launcher, data):
        launcher.change_speed(data)
        actual = data*13400
        assert launcher.launch_speed_pulses == actual

@pytest.mark.parametrize("data", [(1), (3), (7)])
def test_change_speed_below_8(launcher, data):
        launcher.change_speed(data)
        pulse = data * 13400
        actual = (pulse**2)/13400
        assert launcher.launch_acceleration == actual


