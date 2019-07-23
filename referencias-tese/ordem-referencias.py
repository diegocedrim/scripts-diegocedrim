import re, json

def is_comment(line):
    line = line.strip()
    return len(line) > 0 and line[0] == "%"


def find_citations(line):
    cites = re.findall("\\cite{(.*?)}", line)
    citations = []
    for cite in cites:
        if "," in cite:
            citations += [i.strip() for i in cite.split(",")]
        else:
            citations.append(cite.strip())
    return citations


def find_citation_in_file(lines):
    citations = []
    for line in lines:
        line = line.strip()
        if line and not is_comment(line):
            citations += find_citations(line)
    return citations


def numbering(all_citations):
    numbering = {}
    ordered = []
    for citation in all_citations:
        if citation not in ordered:
            ordered.append(citation)

    for i, citation in enumerate(ordered):
        numbering[citation] = i + 1
    return numbering


def generate_new_bib(numbering):
    import bibtexparser

    def authors_list(entry):
        authors = []
        for author in entry["author"].split(" and "):
            if "," in author:
                authors.append(author.split(",")[0])
            else:
                authors.append(author.split(" ")[-1])
        return authors

    def generate_key(entry):
        return str(numbering[entry["ID"]])

    with open('thesis-cedrim.bib') as bibtex_file:

        bibtex_database = bibtexparser.load(bibtex_file)
        for entry in bibtex_database.entries:
            if "key" in entry:
                del entry["key"]
            if "Key" in entry:
                del entry["Key"]
            entry["key"] = generate_key(entry)
        for entry in bibtex_database.entries:
            print entry["title"]
            print entry["author"]
            print entry["year"]
            print entry["key"]
            print ""

    with open('thesis-cedrim-with-keys.bib', 'w') as bibtex_file:
        bibtexparser.dump(bibtex_database, bibtex_file)


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

    all_citations = []
    for filename in files:
        with open(path + filename) as f:
            all_citations += find_citation_in_file(f.readlines())

    for citation, i in numbering(all_citations).iteritems():
        print citation, i
    with open("ordem.json", "w") as out:
        out.write(json.dumps(numbering(all_citations), indent=4))
    generate_new_bib(numbering(all_citations))

main()
