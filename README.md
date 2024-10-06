Magic Rules Enhancer
--------------------

The magic rules enhancer is a script that generates more helpful
versions of the official Magic: The Gathering comprehensive rules
reference documents. The official rules texts contain many internal
references (often expressed as "See rule <number>"). However, these
references are not links, making actually reading the associated
text cumbersome. Additionally, while the official documents have
a kind of table of contents, that table does not actually include any
links or page numbers, making it of limited use.

The magic rules enhancer takes a path to an official Magic
comprehensive rules DOCX file and produces a PDF with very similar
style to the official one, but with added internal links and a
more complete table of contents.

Usage
-----

To generate an enhanced PDF version of the Magic rules, first download
the official DOCX version from the Wizards of the Coast [website](https://magic.wizards.com/en/rules) (e.g. MagicCompRules20240917.docx).
You can then install the requirements (ideally using a virtual environment
or similar) and finally run:

```
python3 enhance.py MagicCompRules20240917.docx
```

This will produce a corresponding `MagicCompRules20240917+.pdf` file. Pre-built
versions of the rules PDF are available under [Releases](https://github.com/ALSchwalm/magic-rules-enhancer/releases).

How it works
------------

The enhancer works in a three step process. First, the raw contents
of the docx are extracted using [docx2python](https://pypi.org/project/docx2python/).
This is used instead of the raw txt format provided by Wizards of
the Coast, because it maintains style information like which
phrases should be italicized. Once this is completed, the contents
are converted to HTML, with associated CSS styling to make the
contents render in a form very similar to the original document.
During this phase, rules references are resolved and converted to
internal hyperlinks within the document. Finally, [pdfkit](https://pypi.org/project/pdfkit/)
is used to convert the HTML to a PDF, while also adding a table
of contents derived from the headings in the HTML.
