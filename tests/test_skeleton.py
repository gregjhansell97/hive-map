#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from hive_map.skeleton import fib

__author__ = "gregjhansell97"
__copyright__ = "gregjhansell97"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
