"""
Source: https://github.com/andrewstephens75/gensite/blob/dev/gensite/markdown_extensions/tufte_aside.py
"""
# Markdown extension that allows Tufte-style asides (in conjuction with
# the tufte.css
# Supported syntax:
# ->[This is a margin note. It will be placed next to the main text]
# +->[This is a side note. It will be placed next the main text with a reference number]


from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.blockprocessors import BlockProcessor
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree
import re

# SIDENOTEPATTERN = r'\+\-\>' + BRK   # matches +->[side note]

class MarginNoteProcessor(BlockProcessor):
    RE_FENCE_START = r'^\-\>'
    RE_FENCE_END = r'<-\s*$'  # last non-blank line, e.g, '!!!\n  \n\n'

    def test(self, parent, block):
        return re.match(self.RE_FENCE_START, block)

    def run(self, parent, blocks):
        original_block = blocks[0]
        blocks[0] = re.sub(self.RE_FENCE_START, '', blocks[0])

        # Find block with ending fence
        for block_num, block in enumerate(blocks):
            if re.search(self.RE_FENCE_END, block):
                # remove fence
                blocks[block_num] = re.sub(self.RE_FENCE_END, '', block)
                # render fenced area inside a new div
                e = etree.SubElement(parent, 'div')
                e.set('style', 'display: inline-block; border: 1px solid red;')
                self.parser.parseBlocks(e, blocks[0:block_num + 1])
                # remove used blocks
                for i in range(0, block_num + 1):
                    blocks.pop(0)
                return True  # or could have had no return statement
        # No closing marker!  Restore and do nothing
        blocks[0] = original_block
        return False  # equivalent to our test() routine returning False

class MarginNoteExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(MarginNoteProcessor(md.parser), 'box', 175)
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
