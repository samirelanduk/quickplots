from unittest import TestCase
import quickplots

class QuickObjectsTests(TestCase):

    def test_line_imported(self):
        from quickplots.quick import line
        self.assertIs(line, quickplots.line)
