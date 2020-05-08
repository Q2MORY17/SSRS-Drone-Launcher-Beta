import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../../python")

import pytest
import python.dronelauncher_python

@pytest.fixture()
def dl():
    print('/n--- Start ---')
    dl = python.dronelauncher_python
    yield dl
    print('/n--- End ---')

def test_function_home(dl): #Line 421 in dronelauncher_python
