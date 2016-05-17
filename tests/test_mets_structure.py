import unittest

from pymets import mets_structure


class METSStructureTests(unittest.TestCase):

    def test_invalid_kwarg(self):
        with self.assertRaises(mets_structure.MetsStructureException) as cm:
            mets_structure.MetsBase(**{'invalid_kwarg': 'invalid_value'})

        expected_error = 'Argument invalid_kwarg not valid'
        self.assertEqual(str(cm.exception), expected_error)

    def test_invalid_attribute(self):
        attributes = {
            'TYPE': 'archival information package',
            'OBJID': 'ark:/67531/TEST',
            'INVALID': 'RANDOM'
        }

        with self.assertRaises(mets_structure.MetsStructureException) as cm:
            m = mets_structure.Mets()
            m.set_atts(attributes)

        expected_error = 'Attribute INVALID is not legal in this element!'
        self.assertEqual(str(cm.exception), expected_error)

    def test_invalid_child(self):
        with self.assertRaises(mets_structure.MetsStructureException) as cm:
            m = mets_structure.Mets()
            m.add_child(mets_structure.File())

        expected_error = 'Invalid child type file for parent mets.'
        self.assertEqual(str(cm.exception), expected_error)

    def test_does_not_all_textual_content(self):
        with self.assertRaises(mets_structure.MetsStructureException) as cm:
            m = mets_structure.Mets()
            m.set_content('Texas')

        expected_error = 'Element mets does not allow textual content.'
        self.assertEqual(str(cm.exception), expected_error)

    def test_set_empty_attribute(self):
        attributes = {
            'TYPE': None,
            'OBJID': None,
        }

        m = mets_structure.Mets()
        m.set_atts(attributes)

        self.assertEqual(m.atts, {})


def suite():
    all_tests = unittest.TestSuite()
    all_tests.addTest(unittest.makeSuite(METSStructureTests))

    return all_tests

if __name__ == '__main__':
    unittest.main()
