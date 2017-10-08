import csv

refs_by_id = {}
refs_by_url = {}


def load_all():
    with open('data/refactorings_and_issues_complete.csv') as input:
        reader = csv.DictReader(input, delimiter=';', quotechar='"')
        for row in reader:
            refs_by_id[row["ref_id"]] = row
            refs_by_url[row["issue_url"]] = refs_by_url.get(row["issue_url"], []) + [row]


def find_by_issue_url(url):
    return refs_by_url[url]


def all():
    return refs_by_id.values()


load_all()