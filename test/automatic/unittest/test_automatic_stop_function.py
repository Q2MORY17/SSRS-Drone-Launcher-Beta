import os
import sys

from unittest.mock import MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../../python")

import python.dronelauncher_python as dl


def test_function_stop():
    # GIVEN
    dl.rc = MagicMock()

    # WHEN
    returnValue = dl.function_stop()

    # THEN
    dl.rc.ForwardM1.assert_any_call(dl.address, 0)
    dl.rc.ForwardM2.assert_any_call(dl.address, 0)
    dl.rc.ForwardM1.assert_any_call(dl.address_2, 0)
    dl.rc.ForwardM2.assert_any_call(dl.address_2, 0)
    assert dl.rc.ForwardM1.call_count == 2
    assert dl.rc.ForwardM2.call_count == 2
    assert returnValue == ('', 204)
