#!/usr/bin/env python
import unittest

from tests import test_metsdoc, test_mets_structure


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(test_metsdoc.suite())
    test_suite.addTest(test_mets_structure.suite())

    return test_suite

runner = unittest.TextTestRunner()
runner.run(suite())
