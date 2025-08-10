# TeX2Canvas
This repository stores Python scripts I wrote in the Summer of 2025 as part of a job writing psets for MATH 3012, Applied Combinatorics, at the Georgia Institute of Technology.

# TeX2Dict
This function parses TeX to extract information relevant to the project. In particular, it separates the TeX input into categories: questions and solutions. A question is a list of strings. For questions that have multiple parts, this list has size equivalent to the number of parts plus one. Any text preceding the parts is at index zero, and the relevant parts are at indexes one through n. Similarly, a solution is a list of string, with the distinction that each part has only one solution, and so this list is of length one less than its corresponding question.
These questions and solutions are stored in a Python dictionary for extraction and formatting.

#Dict2HTML
