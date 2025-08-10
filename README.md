# TeX2Canvas
This repository stores a Python script I wrote in the Summer of 2025 as part of a job writing problem sets for MATH 3012, Applied Combinatorics, at the Georgia Institute of Technology. The portion of this repository used to implement TeX into Canvas currently follows the below workflow:
```
TeX --> --> Substitute --> MM2HTML --> TeX2Dict --> Dict2HTMl --> Canvas
```
On Linux, this is as simple as downloading the script and placing it in a directory with your TeX, naming your TeX `input.tex`, and running `python3 textocanvas3.py > out.html`.

There is some (inactive) code left in the project from my attempts to implement [TeXZilla](https://fred-wang.github.io/TeXZilla/) and [LaTeX2HTMl](https://www.latex2html.org/), but I was dissatisfied with the performance of both, or at least with my implementation of their functionality. I may return to these later, for now I am looking into [Pandoc](https://pandoc.org/).

As far as I am aware, the above workflow requires the following manual editing:
* Replace any TikZ pictures, figures, etc. with images stored in Canvas
* Replace any `\emph{}` macros with the HTML italics tags
* Replace any diacritics (e.g. `jalape\~nos`) with their HTML counterparts
* Replace any TeX macros contained inside of `\text{}` macros with something different (varies)
* Implement any `enumerate` or `itemize` environments with their HTML counterparts

## Substitute
This function performs simple replacement, attempting to fix some common errors before they occur. Currently, the function performs the following replacements:
```
"\newpage"            --> ""
"\CC"                 --> "\mathbb{C}"
"\PP"                 --> "\mathbb{P}"
"\NN"                 --> "\mathbb{N}"
"\QQ"                 --> "\mathbb{Q}"
"\RR"                 --> "\mathbb{R}"
"\ZZ"                 --> "\mathbb{Z}"
"\begin{tikzpicture}" --> Red "PICTURE/FIGURE MISSING" message
"\#"                  --> "#"
"``"                  --> HTML open quote
"''"                  --> HTML close quote
"\medbreak"           --> 2x HTML line break
```
This function returns the input text with the above replacements applied.

## TeX2Dict
This function parses TeX to extract information relevant to the project. In particular, it separates the TeX input into categories: questions and solutions. Input TeX should be some combination of the following "question formats", disregarding linebreaks and other whitespace characters:
```
\question <QUESTION_CONTENT> \solution{<SOLUTION_CONTENT>}
````
or
```
\question <QUESTION_CONTENT>
  \begin{parts}
    \part <PART_CONTENT>
    \soln{SOLUTION_CONTENT
    \part <PART_CONTENT>
    \soln{SOLUTION_CONTENT}
    ...
  \end{parts}
```
The "content" for any given question, part, or solution, is expected to be a combination of text and TeX macros. The function `TeX2Dict` returns a dictionary whose keys are integers (indexed at one) and whose values are ordered pairs $$(Q, S)$$ where $$Q$$ is a list of strings whose index zero element is `<QUESTION_CONTENT>` and whose other elements are `<PART_CONTENT>`. Similarly, $$S$$ is a list whose elements are `<SOLUTION_CONTENT>`.

Note that for any given `<PART_CONTENT>` with index $$i$$, the index of the corresponding `<SOLUTION_CONTENT>` is $$i-1$$.

## MM2HTML
This function replaces math-mode (MM) content with HTML for use in Canvas. In particular, it replaces `$<INLINE_MATHMODE_CONTENT>$` with `\(<INLINE_MATHMODE_CONTENT>\)` and `\[<DISPLAY_MATHMODE_CONTENT>\]` with `<br />\(<DISPLAY_MATHMODE_CONTENT>\)<br />`. It returns the input text with the aforementioned replacements applied.

## Dict2HTML
This function takes in the dictionary returned by [TeX2Dict] and returns HTML for use in Canvas. In particular, this function wraps each question (meaning one of the question formats detailed in [TeX2Dict]) with an HTML "expander" box, which allows `<QUESTION_CONTENT>` and `<PART_CONTENT>` to be displayed, and `<SOLUTION_CONTENT>` to be displayed in a drop-down box. It does this by wrapping the aforementioned content in the following manner:
```
<div class="dp-panel-group">
<h3 class="dp-panel-heading"> <QUESTION_CONTENT> <FORMATTED_PARTS_CONTENT> </h3>
<div class="dp-panel-content"> <p> <FORMATTED_SOLUTIONS_CONTENT> </p>
</div>
```
These HTML tags implement the expander functionality in Canvas. The `<FORMATTED_PARTS_CONTENT>` and `<FORMATTED_SOLUTIONS_CONTENT>` strings are simply the concatenation of all part and solution content, respectively, with some additional formatting done to prepend alphabetical indexes and introduce linebreaks between the parts and solutions, respectively.

In addition, extra HTML tagging is added to tell Canvas that it needs to render these expander boxes.
