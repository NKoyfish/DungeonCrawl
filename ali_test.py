#creating my test for getscore()
from pytest import approx, raises as pytest_raises
import dungeon_crawl as dg
import sys
import os
import builtins
from unittest import mock
from unittest.mock import patch
from time import sleep