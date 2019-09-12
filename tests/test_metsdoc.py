import unittest
import io

from pymets import metsdoc


class METSDocTests(unittest.TestCase):

    def test_invalid_mets_element(self):
        mets_string = """<?xml version="1.0" encoding="UTF-8"?>
        <mets><metsHDR/></mets>"""

        with self.assertRaises(metsdoc.PymetsException) as cm:
            metsdoc.metsxml2py(io.BytesIO(mets_string.encode('utf-8')))

        expected_error = 'Element "metsHDR" not found in mets dispatch.'
        self.assertEqual(str(cm.exception), expected_error)


def suite():
    all_tests = unittest.TestSuite()
    all_tests.addTest(unittest.makeSuite(METSDocTests))

    return all_tests


if __name__ == '__main__':
    unittest.main()
