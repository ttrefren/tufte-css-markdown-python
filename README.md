# tufte-css-markdown-python
markdown-python extensions adding support for sidenotes and margin notes to your markdown website that uses [tufte-css](https://edwardtufte.github.io/tufte-css/) for styling.

Margin notes don't have a number, they just show up on the right side margin.

Margin note syntax: `->[your content here]<-`.

Sidenotes have a superscript number.

Sidenote syntax: `+->[your sidenote here]<-`

Note: I went to some effort to support line breaks in the side/margin notes - out of the box, tufte-css only supports a single paragraph per note, since the body of each note is wrapped in a `<span>` tag and you can't use block level elements like `<p>` inside a span or the browser barfs.

But I like to write long, discursive sidenotes and I needed blank lines, dammit - so my sidenotes are more complicated & require some tweaks to your css, but they support multiple lines. You could do something like this:

```
## My article

hello there ->[this is an

inline note]<- that spans blocks
```

and the html output would be something like this:

```
<h2>My article</h2>
<p>
hello there <label class="margin-toggle" for="note_0">&#8853</label>
<input checked="1" class="margin-toggle" id="note_0" type="checkbox">
<aside class="marginnote">
<p>this is an</p>
<p>inline note</p>
</aside>
 that spans blocks
</p>
```

If you're paying close attention, this is also gross, because `<p>` tags also dislike having block level elements inside them - so there's one more piece of the puzzle, which is a second python-markdown plugin to convert `<p>` tags into `<div class="p">`, and some css to include to make them work right.

## How to use:

This isn't a pip package or anything yet... so I'd say just copy the `tufte.py` file into wherever you want in your project. Then, when you are parsing markdown, include the two extensions like so:

```python
from wherever import tufte

md = markdown.Markdown(extensions=[
    tufte.TufteNoteExtension(),
    tufte.ParagraphToDivExtension()
])

html = md.convert(my_markdown_body)
```

You'll also want to include `tweaks.css` as it copies over the original styles into the `<aside>` and `<div class="p">` elements we're using.
