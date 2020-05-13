import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../python")

import python.infotiv_launcher


@pytest.fixture()
def launcher():
    print('\n*********Start*********')
    launcher = python.infotiv_launcher.Launcher()
    yield launcher
    print('\n**********End**********')


@pytest.mark.parametrize("invalid_data", [-1, 91])
def test_change_pitch_invalid_data(launcher, invalid_data):
    with pytest.raises(ValueError) as err:
        launcher.change_pitch(invalid_data)
    assert err.match('Out of Bounds')


@pytest.mark.parametrize("valid_data", [0, 1, 89, 90])
def test_change_pitch_valid_data(launcher, valid_data):
    launcher.change_pitch(valid_data)
    assert launcher.pitch_ready == valid_data


@pytest.mark.parametrize("invalid_data", [-0.01, -1, 130.01, 199])
def test_change_lift_invalid(launcher, invalid_data):
    with pytest.raises(Exception, match='Out of Bounds') as err:
        launcher.change_lift(invalid_data)
        assert err.type is ValueError


@pytest.mark.parametrize("data", [1, 130, 0, 129])
def test_change_lift(launcher, data):
    launcher.change_lift(data)
    assert launcher.lift_ready == data


@pytest.mark.parametrize("invalid_data", [-1, 180.1])
def test_change_rotation_invalid(launcher, invalid_data):
    with pytest.raises(Exception, match='Out of Bounds') as err:
        launcher.change_rotation(invalid_data)
        assert err.type is ValueError


@pytest.mark.parametrize("valid_data", [0.0001, 1.5, 180.0])
def test_change_rotation_valid(launcher, valid_data):
    launcher.change_rotation(valid_data)
    rotation_position_actual = valid_data
    assert launcher.rotation_ready == rotation_position_actual


@pytest.mark.parametrize("invalid_data", [-1, 11, 0])
def test_change_speed_invalid(launcher, invalid_data):
    with pytest.raises(Exception, match='Out of Bounds') as err:
        launcher.change_speed(invalid_data)
        assert err.type is ValueError


@pytest.mark.parametrize("data", [8, 10])
def test_change_speed_above_7(launcher, data):
    launcher.change_speed(data)
    actual = data * 13400
    assert launcher.launch_speed_pulses == actual


@pytest.mark.parametrize("data", [1, 3, 7])
def test_change_speed_below_8(launcher, data):
    launcher.change_speed(data)
    pulse = data * 13400
    actual = (pulse ** 2) / 13400
    assert launcher.launch_acceleration == actual


@pytest.mark.parametrize("invalid_data", [-1, 0, 49])
def test_change_acceleration_invalid(launcher, invalid_data):
    with pytest.raises(Exception, match='Out of Bounds') as err:
        launcher.change_acceleration(invalid_data)
        assert err.type is ValueError


@pytest.mark.parametrize("valid_data", [1, 32, 48])
def test_change_acceleration_valid(launcher, valid_data):
    launcher.change_acceleration(valid_data)
    acceleration_actual = valid_data * 13400
    assert launcher.launch_acceleration == acceleration_actual
