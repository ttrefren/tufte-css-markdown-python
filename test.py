import unittest
import markdown

from tufte import MarginNoteExtension, ParagraphToDivExtension

class TestMarginNoteExtension(unittest.TestCase):

    def test_block(self):
        text = """\
->
This is an inline test block.

It has multiple blocks within it.<-
"""
        md = markdown.Markdown(extensions=[MarginNoteExtension(use_random_note_id=False)], output_format='html5')
        output = md.convert(text)
        expected = """\
<label class="margin-toggle" for="note_0">&#8853</label>
<input checked="1" class="margin-toggle" id="note_0" type="checkbox">
<aside class="marginnote">
<p>This is an inline test block.</p>
<p>It has multiple blocks within it.</p>
</aside>"""
        #print(output)
        #print(' ')
        #print(expected)
        self.assertEqual(output, expected)

    def test_paragraph_to_div(self):
        text = """This

It
"""
        md = markdown.Markdown(extensions=[ParagraphToDivExtension()])
        output = md.convert(text)
        self.assertEqual(output, '<div class="p">This</div>\n<div class="p">It</div>')

# TODO in future - implement so that inline will work rather than requiring a newline
#    def test_inline(self):
#        text = "hello there ->this is an inline note<-"
#        md = markdown.Markdown(extensions=[MarginNoteExtension(use_random_note_id=False)], output_format='html5')
#        output = md.convert(text)
#        expected = """\
#hello there <label class="margin-toggle" for="note_0">&#8853</label>
#<input checked="1" class="margin-toggle" id="note_0" type="checkbox">
#<aside class="marginnote">
#<p>this is an inline note</p>
#</aside>"""
#        print(output)
#        print(' ')
#        print(expected)
#        self.assertEqual(output, expected)



if __name__ == '__main__':
    unittest.main()
