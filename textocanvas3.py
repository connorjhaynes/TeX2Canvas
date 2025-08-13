import re # , subprocess
# from playwright.sync_api import sync_playwright, Playwright

# this script assumes that the TeX is formatted as follows (only the order in which commands appear is important, linebreaks don't matter):
# \question ...
# \begin{parts}
#      \part ...
#      \soln{}
# ...
# \end{parts}

# non-functional prototyping things
USE_LATEX2HTML = 0
USE_TEXZILLA = 0

preamble = open("preamble.txt", 'r').read()

def ixIterator(arr, prefix, suffix):
    out = ""
    for i in range(0, len(arr)):
        if i % 2 == 1:
            arr[i] = prefix + arr[i] + suffix
        out += arr[i]
    return out

# replaces macros and things that shouldn't be there with things that should
def Substitute(intext):
    substitutions = {
        r"\\newpage": "",
        r"\\CC": r"\\mathbb{C}",
        r"\\PP": r"\\mathbb{P}",
        r"\\NN": r"\\mathbb{N}",
        r"\\QQ": r"\\mathbb{Q}",
        r"\\RR": r"\\mathbb{R}",
        r"\\ZZ": r"\\mathbb{Z}",
        r"\\begin{tikzpicture}|\\begin{figure}": "<h3 style=\"color:red\"> PICTURE/FIGURE MISSING </h3>",
        r"\\#": r"#",
        r"``": r"&ldquo;",
        r"''": r"&rdquo;",
        r"\\medbreak": r"<br /><br />",
        r"\\_": r"_"
    }

    for i in range(0,len(substitutions)):
        intext = re.sub(list(substitutions)[i], list(substitutions.values())[i], intext)
    return intext

# returns a dictionary whose keys are integers and whose values are pairs (a,b) where a=[question, part1, part2, ...] and b=[solution1, solution2, ...]
def TeX2Dict(intext):
    questionSolnDict: Dict[int, [List[str], List[str]]] = {}

    # break into questions
    intext = re.sub("\\\\begin{parts}|\\\\end{parts}", "", intext)
    qSplit= re.split("\\\\question", intext)
    for i in range(1,len(qSplit)):
        questionSolnDict[i] = [[], []]
        # if contains parts
        pSplit = re.split("\\\\part", qSplit[i])
        if len(pSplit) != 1:
            for j in range(0,len(pSplit)):
                sSplit = re.split("\\\\soln{", (pSplit[j].rstrip())[:-1]) # see comment in the else branch
                
                # if we have part/question text
                questionSolnDict[i][0].append(sSplit[0])
                if j != 0:
                    questionSolnDict[i][1].append(sSplit[1].rstrip())

        # if does not contain parts
        else:
            sSplit= re.split("\\\\soln{", (qSplit[i].rstrip())[:-1]) # this ".rstrip()[:-1]" is a naive and fragile way of removing trailing "}" from "\soln{...}", it needs to be replaced, i know for a fact it is causing issues
            questionSolnDict[i] = [[sSplit[0]], [sSplit[1].rstrip()]]

    return questionSolnDict

# convert question/soln dictionary to html
def Dict2HTML(questionSolnDict):
    expanderQuestionPrefix = "<div class=\"dp-panel-group\">\n<h3 class=\"dp-panel-heading\"> "
    expanderQuestionSuffix = " </h3>\n"
    
    expanderSolnPrefix = "<div class=\"dp-panel-content\">\n<p> "
    expanderSolnSuffix = " </p>\n</div>"

    htmlOut = ""
    if USE_LATEX2HTML == 0:
        for i in range(1,len(questionSolnDict)+1):
            # if parts
            if len(questionSolnDict[i][0]) != 1:
                parts = ""
                solns = ""
                for j in range(1,len(questionSolnDict[i][0])):
                    parts += chr(ord('`') + j) + ") " + questionSolnDict[i][0][j] + "<br /><br />" # this code just puts "(a)" or "(b)" or ... depending on what part it is
                    solns += chr(ord('`') + j) + ") " + questionSolnDict[i][1][j-1] + "<br /><br />"
                    panel = expanderQuestionPrefix + questionSolnDict[i][0][0] + "<br /><br />" + parts + expanderQuestionSuffix + expanderSolnPrefix + solns + expanderSolnSuffix + "</div>\n\n\n\n"
            # if no parts
            else:
                panel = expanderQuestionPrefix + questionSolnDict[i][0][0] + expanderQuestionSuffix + expanderSolnPrefix + questionSolnDict[i][1][0] + expanderSolnSuffix + "</div>\n\n\n\n"
            htmlOut += panel
    else:
        for i in range(1,len(questionSolnDict)+1):
            qTeX = open("q.tex", 'w')
            sTeX = open("s.tex", 'w')
            # if parts
            if len(questionSolnDict[i][0]) != 1:
                qTmp = preamble + questionSolnDict[i][0][0] + "\n\\begin{enumerate}\n"
                sTmp = preamble + "\n\\begin{enumerate}\n"
                for j in range(1,len(questionSolnDict[i][0])):
                    qTmp += "\\item[(" + chr(ord('`') + j) + ")] " + questionSolnDict[i][0][j] + "\n"
                    sTmp += "\\item[(" + chr(ord('`') + j) + ")] " + questionSolnDict[i][1][j-1] + "\n"
                qTmp += "\n\\end{enumerate}\n\\end{document}"
                sTmp += "\n\\end{enumerate}\n\\end{document}"
            # if no parts
            else:
                qTmp = preamble + questionSolnDict[i][0][0] + "\n\\end{document}"
                sTmp = preamble + questionSolnDict[i][1][0] + "\n\\end{document}"

            print(qTmp)
            print(sTmp)
            
            qTeX.write(qTmp)
            sTeX.write(sTmp)
            
            qTeX.close()
            sTeX.close()

            qProc = subprocess.Popen('latex2html q.tex', shell=True)
            qProc.wait()
            sProc = subprocess.Popen('latex2html s.tex', shell=True)
            sProc.wait()

            # below is taken from Playwright's docs
            def run(playwright: Playwright, qors):
                chromium = playwright.chromium
                browser = chromium.launch()
                page = browser.new_page()
                page.goto("file:///home/connorhaynes/Documents/TeXtoCanvas/working/" + qors + "/index.html")
                page.screenshot(path=qors + str(i) + ".png")
                browser.close()

            with sync_playwright() as playwright:
                run(playwright, "q")
                run(playwright, "s")

            subprocess.Popen('rm -rf q', shell=True)
            subprocess.Popen('rm -rf s', shell=True)

            panel = expanderQuestionPrefix + "<img src=\"q" + str(i) + ".png\">" + expanderQuestionSuffix + expanderSolnPrefix + "<img src=\"s" + str(i) + ".png\">" + expanderSolnSuffix + "</div>"
            htmlOut += panel

    return htmlOut

# convert "$...$" and "\[...\]" to "\(...\)" and "\n\n\t\t\(...\)\n\n", respectively
def MM2HTML(intext):
    if USE_TEXZILLA == 1:
        inlinePrefix = "<la-tex display=\"inline\">"
        inlineSuffix = "</la-tex>"
        displayPrefix = "<la-tex display=\"block\">"
        displaySuffix = "</la-tex>"
    else:
        inlinePrefix = "\\("
        inlineSuffix = "\\)"
        displayPrefix = "<br />\\("
        displaySuffix = "\\)<br />"
    tmp = Substitute(intext)
    out = ixIterator(re.split(r"\$", tmp), inlinePrefix, inlineSuffix)
    # out = ixIterator(re.split(r"\\\[|\\\]", tmp), displayPrefix, displaySuffix)
    return out

# prefix = "<head>\n<script type=\"text/javascript\" src=\"./TeXZilla.js\"></script>\n<script type=\"text/javascript\" src=\"./customElement.js\"></script>\n</head>\n<div class=\"dp-panels-wrapper dp-expander-default\">\n"
prefix = "<div class=\"dp-panels-wrapper dp-expander-default\">\n"
suffix = "\n</div>"

with open(r'input.tex', 'r') as f:   
    c = f.read()

if USE_LATEX2HTML == 1:
    print(prefix + Dict2HTML(TeX2Dict(c)) + suffix)
else:
    print(prefix + Dict2HTML(TeX2Dict(MM2HTML(c))) + suffix)

# todo:
# - fix diacritics
# - write something to replace "\emph{...}" with "<i> ... </i>"
# - current fix for removing the trailing curly brace from "\soln{}" is bad
# - implement enumerate and itemize as html lists

# notes:
# - it looks like macros inside of "\text{}" don't render, or at least "\ldots" doesn't
