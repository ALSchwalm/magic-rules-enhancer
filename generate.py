from docx2python import docx2python
import re
import sys
import pdfkit

def evaluate_rule_type(rule):
    id, _ = rule.split(" ", maxsplit=1)
    if re.fullmatch(r"\d+\.", id):
        num = int(id.strip("."))
        if num < 100:
            return str(num), "section"
        else:
            return str(num), "subsection"
    else:
        if not id.endswith("."):
            return id, "subrule"
        else:
            return id.strip("."), "rule"

def render_rule_text(rule):
    return re.sub(r"rule (\d+(\.\d+([a-z]+)?)?)", r'<a href="#id\1">rule \1</a>', rule)

def render_example(example):
    return f"<div class=\"example\">{example}</div>"

rules = []
terms = []

with docx2python(sys.argv[1], html=True) as docx_content:
    contents = docx_content.text

    intro, contents = contents.split("\nCredits\n", maxsplit=1)
    contents, end = contents.rsplit("\nGlossary\n", maxsplit=1)

    for rule in contents.split("\n\n\n"):
        if not rule.strip():
            continue
        rule, *examples = rule.strip().splitlines()

        id, type = evaluate_rule_type(rule)
        rule = render_rule_text(rule)
        rules.append({
            "text": rule,
            "examples": [render_example(e) for e in examples if e],
            "type": type,
            "id": id
        })

    glossary, _ = end.split("\nCredits\n")
    for term in glossary.split("\n\n\n"):
        if not term.strip():
            continue
        term, *definition = term.strip().splitlines()
        terms.append({
            "term": term,
            "definitions": [render_rule_text(d) for d in definition if d]
        })

with open("output.html", "w") as f:
    f.write('''
    <!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
    <style>
      .pagebreak { page-break-before: always; }
      @font-face {
          font-family: "Times New Roman";
          src: url("https://db.onlinewebfonts.com/t/32441506567156636049eb850b53f02a.eot");
          src: url("https://db.onlinewebfonts.com/t/32441506567156636049eb850b53f02a.eot?#iefix")format("embedded-opentype"),
          url("https://db.onlinewebfonts.com/t/32441506567156636049eb850b53f02a.woff2")format("woff2"),
          url("https://db.onlinewebfonts.com/t/32441506567156636049eb850b53f02a.woff")format("woff"),
          url("https://db.onlinewebfonts.com/t/32441506567156636049eb850b53f02a.ttf")format("truetype"),
          url("https://db.onlinewebfonts.com/t/32441506567156636049eb850b53f02a.svg#Times New Roman")format("svg");

      }
      * {
        font-family: "Times New Roman" !important;
      }
      .subsection { font-size: 1em; font-weight: normal; }
      .rule,.subrule { text-indent: -30px; margin-bottom: 0px; }
      .rule { margin-left: 60px; }
      .subrule { margin-left: 90px; }
      .examples { margin-left: 120px; font-style: italic; }
      .term { font-weight: bold; margin-top: 16px; }
      .defun { margin-top: 0px; margin-bottom: 0px; }
    </style>
  </head>
<body>
    ''')

    for rule in rules:
        text = rule["text"]
        id = rule["id"]
        type = rule["type"]
        html_type = "p"
        if type == "section":
            html_type = "h2"
            f.write('<div class="pagebreak"></div>')
        elif type == "subsection":
            html_type = "h3"
        f.write(f"<{html_type} class=\"{type}\" id=\"id{id}\">{text}</{html_type}>")

        examples = rule["examples"]
        if examples:
            f.write("<div class=\"examples\">")
            for example in examples:
                f.write(example)
            f.write("</div>")

    f.write('<div class="pagebreak"></div>')
    f.write(f"<h2 class=\"section\">Glossary</h2>")
    for term in terms:
        name = term["term"]
        f.write(f"<div class=\"term\">{name}</div>")
        for defun in term["definitions"]:
            f.write(f"<p class=\"defun\">{defun}</p>")
    f.write('''
</body>
</html>
    ''')

options = {
    'page-size': 'Letter',
    'margin-top': '1.2in',
    'margin-right': '1.2in',
    'margin-bottom': '1.2in',
    'margin-left': '1.2in'
}
pdfkit.from_url('output.html', 'out.pdf', options=options)
