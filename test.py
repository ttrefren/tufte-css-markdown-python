import unittest
import markdown

from tufte import MarginNoteExtension, ParagraphToDivExtension

class TestMarginNoteExtension(unittest.TestCase):

    def test_block(self):
        text = """
->
This is an inline test block.

It has multiple blocks within it.
<-"""
        md = markdown.Markdown(extensions=[MarginNoteExtension()])
        output = md.convert(text)
        self.assertEqual(output, 'yes')

    def test_paragraph_to_div(self):
        text = """This

It
"""
        md = markdown.Markdown(extensions=[ParagraphToDivExtension()])
        output = md.convert(text)
        self.assertEqual(output, '<div class="p">This</div>\n<div class="p">It</div>')


if __name__ == '__main__':
    unittest.main()
