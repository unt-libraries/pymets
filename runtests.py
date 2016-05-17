#!/usr/bin/env python
import unittest

from tests import test_metsdoc


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(test_metsdoc.suite())

    return test_suite

runner = unittest.TextTestRunner()
runner.run(suite())
