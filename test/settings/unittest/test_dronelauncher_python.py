import python.dronelauncher_python
import pytest


@pytest.fixture
def dl():
    dl = python.dronelauncher_python
    return dl

def test_comports_closed(dl):
    assert 0 == dl.rc.Open()