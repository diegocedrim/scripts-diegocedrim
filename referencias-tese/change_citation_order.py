import re, json


def is_comment(line):
    line = line.strip()
    return len(line) > 0 and line[0] == "%"


def find_multiple_citations(line):
    return [i for i in re.findall("\\cite{(.*?)}", line) if "," in i]


def dedup(citation_list):
    clean = []
    for cite in citation_list:
        if cite not in clean:
            clean.append(cite)
    return clean


def correct_citation(citation, ordering):
    keys = [i.strip() for i in citation.split(",")]
    compond = [(ordering[key],key) for key in keys]
    compond.sort()
    compond = dedup(compond)
    return ", ".join([key for i, key in compond])


def correct_citation_ordering(citation_map, lines, filename):
    for line in lines:
        if is_comment(line):
            continue
        citations = find_multiple_citations(line)
        for cite in citations:
            correct = correct_citation(cite, citation_map)
            if cite != correct:
                print "%s) %s => %s" % (filename, cite, correct)


def main():
    files = [
        "thesis-cedrim.tex",
        "chapters/chapter-1.tex",
        "chapters/chapter-2.tex",
        "chapters/chapter-3.tex",
        "chapters/chapter-4.tex",
        "chapters/chapter-5.tex",
        "chapters/chapter-6.tex",
        "chapters/chapter-7.tex",
        "appendix.tex"
    ]

    path = "/Users/diego/Documents/puc/tese/thesis-cedrim/"

    with open("ordem.json") as j:
        citation_map = json.load(j)

    for filename in files:
        with open(path + filename) as f:
            correct_citation_ordering(citation_map, f.readlines(), filename)


main()