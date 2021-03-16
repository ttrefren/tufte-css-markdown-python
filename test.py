import unittest
import markdown

from tufte import MarginNoteExtension

class TestMarginNoteExtension(unittest.TestCase):

    def test_block(self):
        block = """
->
This is an inline test block.

It has multiple blocks within it.
<-"""
        md = markdown.Markdown(extensions=[MarginNoteExtension()])
        output = md.convert(block)
        self.assertEqual(output, 'yes')

if __name__ == '__main__':
    unittest.main()
