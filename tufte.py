"""
Inspired by: https://github.com/andrewstephens75/gensite/blob/dev/gensite/markdown_extensions/tufte_aside.py
"""
# Markdown extension that allows Tufte-style asides (in conjuction with
# the tufte.css
# Supported syntax:
# ->[This is a margin note. It will be placed next to the main text]<-
# +->[This is a side note. It will be placed next the main text with a reference number]<-


from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.blockprocessors import BlockProcessor
from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as etree
import re
import random

class TufteNoteProcessor(BlockProcessor):
    # The only difference between a sidenote and a margin note is the leading `+`.
    RE_SIDENOTE_START = r'\+-\>\['
    RE_NOTE_START = r'\+?-\>\['
    RE_NOTE_END = r'\]<-'

    def __init__(self, md, label_text, use_random_note_id):
        super().__init__(md.parser)
        self.md = md
        self._label_text = label_text
        self._use_random_note_id = use_random_note_id
        self._id_counter = 0

    def test(self, parent, block):
        return re.search(self.RE_NOTE_START, block)

    def run(self, parent, blocks):
        """
        Replace margin / side notes with the full HTML required
        for support in tufte.css.

        Supports standalone or inline notes, and notes can contain markdown.
        """
        is_sidenote = re.search(self.RE_SIDENOTE_START, blocks[0])
        for block_num, block in enumerate(blocks):
            if re.search(self.RE_NOTE_END, block):
                note_id = str(random.random()) if self._use_random_note_id else f"note_{self._id_counter}"
                self._id_counter += 1

                p = etree.SubElement(parent, 'p')
                p.tail = '\n'

                pre_note_content, note_content_start = re.split(self.RE_NOTE_START, blocks[0], maxsplit=1)
                p.text = '\n' + pre_note_content

                # single line notes are a special case since we have to process the middle
                if block_num == 0:
                    note_body, after_note_content = re.split(self.RE_NOTE_END, note_content_start, maxsplit=1)
                    note_blocks = [note_body]
                else:
                    note_last_line, after_note_content = re.split(self.RE_NOTE_END, block, maxsplit=1)
                    note_blocks = [note_content_start] + blocks[1 : block_num] + [note_last_line]

                label = etree.SubElement(p, 'label', {
                    'for': note_id,
                    'class':'margin-toggle' + (' sidenote-number' if is_sidenote else '')
                })
                label.text = self.md.htmlStash.store(self._label_text)
                label.tail = '\n'

                checkbox = etree.SubElement(p, 'input', {
                    'id': note_id,
                    'type': 'checkbox',
                    'class': 'margin-toggle',
                    'checked': '1'
                })
                checkbox.tail = '\n'

                aside = etree.SubElement(p, 'aside', {'class': 'sidenote' if is_sidenote else 'marginnote'})
                aside.tail = '\n' + after_note_content + '\n'

                self.parser.parseBlocks(aside, note_blocks)

                for i in range(0, block_num + 1):
                    blocks.pop(0)
                return

class TufteNoteExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'use_random_note_id' : [True, 'use a random note ID, or start at zero'],
            'label_text': ['&#8853', 'what label text to use when on a small screen']
        }
        super(TufteNoteExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(
            TufteNoteProcessor(
                md,
                self.getConfig('label_text'),
                self.getConfig('use_random_note_id'),
            ),
            'margin_note',
            175
        )

class ParagraphToDivProcessor(Treeprocessor):
    def run(self, root):
        paragraphs = root.findall("p")
        for p in paragraphs:
            p.tag = 'div'
            p.set('class', 'p')

class ParagraphToDivExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.treeprocessors.register(ParagraphToDivProcessor(md.parser), 'ptodiv', 175)
#
#class TufteMargin(Pattern):
#    def handleMatch(self, m):
#        el = etree.Element('span')
#        el.set("class", "marginnote")
#        el.text = m.group(2)
#        return el
#
#class TufteSidenote(Pattern):
#    def handleMatch(self, m):
#        el = etree.Element('span')
#        el.set("class", "sidenote")
#        el.text = m.group(2)
#        return el
#
#class TufteSidenoteTreeProcessor(Treeprocessor):
#    def __init__(self):
#        self.count = 1
#
#    def run(self, root):
#        # etree sucks for modifying the tree mainly because there are no text
#        # nodes, only nodes with tails. Here I remove all children of the parent
#        # and add them back one-by-one, inserting the required labels
#        # and checkboxs where needed
#        parents = root.findall(".//span[@class='sidenote']/..")
#        self.count = 1
#        for p in parents:
#            children = list(p)
#            for c in children:
#                p.remove(c)
#
#            for c in children:
#                if (c.tag == 'span') and (c.get('class', "") == 'sidenote'):
#                    id = "sidenote" + str(self.count)
#                    self.count = self.count + 1
#                    p.append(etree.Element("label", {"for" : id, "class" : "margin-toggle sidenote-number"}))
#                    p.append(etree.Element("input", {"type": "checkbox", "id": id, "class" : "margin-toggle", "checked": 1}))
#                p.append(c)
#
#class TufteAsideExtension(Extension):
#    """ Extenstion to build Tufte-style margin notes
#        ->[This is a margin note that will go in the margin] """
#    def extendMarkdown(self, md, md_globals):
#
#        tufte_magin_tag = TufteMargin(MARGINNOTEPATTERN)
#        tufte_sidenote_tag = TufteSidenote(SIDENOTEPATTERN)
#        turfe_sidenote_tree = TufteSidenoteTreeProcessor()
#        md.inlinePatterns.add('tufte_margin', tufte_magin_tag, '_begin')
#        md.inlinePatterns.add('tufte_sidenote', tufte_sidenote_tag, '_begin')
#        md.treeprocessors.add('tufte_sidenote_tree', turfe_sidenote_tree, '_end')
