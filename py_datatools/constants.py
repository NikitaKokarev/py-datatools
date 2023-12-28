# -*- coding: utf-8 -*-
""" CONSTANTS OF HELPER FUNCTIONS.
"""
__author__ = 'kokarev.nv'

import re


PREDEFINED_TRUE_ARRAY = ("true", "t", "1", "yes", "y")
PREDEFINED_FALSE_ARRAY = ("false", "f", "0", "no", "n")
VALID_ARRAY_TYPES = (tuple, list, set)
ONLY_NUMBERS_SYMBOLS = re.compile(r'^[0-9]+$')