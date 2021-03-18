import unittest
import markdown

import tufte

class TestMarginNoteExtension(unittest.TestCase):

    def test_block(self):
        text = """\
->
This is an inline test block.

It has multiple blocks within it.<-
"""
        md = markdown.Markdown(extensions=[tufte.MarginNoteExtension(use_random_note_id=False)], output_format='html5')
        output = md.convert(text)
        expected = """\
<p>
<label class="margin-toggle" for="note_0">&#8853</label>
<input checked="1" class="margin-toggle" id="note_0" type="checkbox">
<aside class="marginnote">
<p>This is an inline test block.</p>
<p>It has multiple blocks within it.</p>
</aside>
</p>"""
        #print(output)
        #print(' ')
        #print(expected)
        self.assertEqual(output, expected)

    def test_paragraph_to_div(self):
        text = """This

It
"""
        md = markdown.Markdown(extensions=[tufte.ParagraphToDivExtension()])
        output = md.convert(text)
        self.assertEqual(output, '<div class="p">This</div>\n<div class="p">It</div>')

    def test_inline_note(self):
        text = "a ->b<- c"
        md = markdown.Markdown(extensions=[tufte.MarginNoteExtension(use_random_note_id=False)], output_format='html5')
        output = md.convert(text)
        expected = """\
<p>
a <label class="margin-toggle" for="note_0">&#8853</label>
<input checked="1" class="margin-toggle" id="note_0" type="checkbox">
<aside class="marginnote">
<p>b</p>
</aside>
 c
</p>"""
        self.assertEqual(output, expected)

    def test_inline_multiblock_note(self):
        text = """hello there ->this is an

inline note<- that spans blocks"""
        md = markdown.Markdown(extensions=[tufte.MarginNoteExtension(use_random_note_id=False)], output_format='html5')
        output = md.convert(text)
        expected = """\
<p>
hello there <label class="margin-toggle" for="note_0">&#8853</label>
<input checked="1" class="margin-toggle" id="note_0" type="checkbox">
<aside class="marginnote">
<p>this is an</p>
<p>inline note</p>
</aside>
 that spans blocks
</p>"""
        self.assertEqual(output, expected)

    def test_inline_note_with_markdown(self):
        text = """hello there ->this is **an**

inline note

- with
- a
- list
<- that spans blocks"""
        md = markdown.Markdown(extensions=[tufte.MarginNoteExtension(use_random_note_id=False)], output_format='html5')
        output = md.convert(text)
        expected = """\
<p>
hello there <label class="margin-toggle" for="note_0">&#8853</label>
<input checked="1" class="margin-toggle" id="note_0" type="checkbox">
<aside class="marginnote">
<p>this is <strong>an</strong></p>
<p>inline note</p>
<ul>
<li>with</li>
<li>a</li>
<li>list
</li>
</ul>
</aside>
 that spans blocks
</p>"""
        self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()
