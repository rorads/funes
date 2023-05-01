"""
testing out imports
"""

import utils


def test_import():
    """
    test import
    """
    assert utils.demo_util() is True
    print("test_import passed")


test_import()
