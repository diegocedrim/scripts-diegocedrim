# remover:
# month, keywords, url, mendeley-groups, file, abstract, arxivid, eprint, mendeley-tags, acmid
import bibtexparser

keys = [
    "month",
    "keywords",
    "url",
    "mendeley-groups",
    "file",
    "abstract",
    "arxivid",
    "eprint",
    "mendeley-tags",
    "acmid",
]

def ajust_title(entry):
    entry["title"] = "{" + entry["title"].title() + "}"


with open('thesis-cedrim.bib') as bibtex_file:
    count = 0
    bibtex_database = bibtexparser.load(bibtex_file)
    for entry in bibtex_database.entries:
        ajust_title(entry)
        for to_remove in keys:
            if to_remove in entry:
                del entry[to_remove]
                count += 1
    print count

with open('thesis-cedrim-clean.bib', 'w') as bibtex_file:
    bibtexparser.dump(bibtex_database, bibtex_file)