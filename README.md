# TeX2Canvas
This repository stores Python scripts I wrote in the Summer of 2025 as part of a job writing psets for MATH 3012, Applied Combinatorics, at the Georgia Institute of Technology.

# Substitute
This function performs simple replacement, attempting to fix some common errors before they occur. Currently, the function performs the following replacements:
```
"\newpage" --> ""
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

# TeX2Dict
This function parses TeX to extract information relevant to the project. In particular, it separates the TeX input into categories: questions and solutions. Input TeX should be some combination of the following "question formats":
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

# Dict2HTML
