import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../../python")

#from unittest.mock import Mock
#mock = Mock()

import pytest
import python.dronelauncher_python

@pytest.fixture()
def dl():
    dl = python.dronelauncher_python
    return dl

def test_comports_closed(dl):
    assert 0 == dl.rc.Open()

def test_function_reset_encoders(dl):
    """Line 440"""

    #GIVEN
    dl.encoders_ready = 1

    #WHEN
    returnValue = dl.function_reset_encoders()

    #THEN
    assert returnValue == ('', 204)
    