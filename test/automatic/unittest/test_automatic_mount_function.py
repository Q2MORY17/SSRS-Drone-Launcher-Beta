import os
import sys

import flask
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/../python")

from unittest.mock import MagicMock

import python.dronelauncher_python
app = flask.Flask(__name__)
