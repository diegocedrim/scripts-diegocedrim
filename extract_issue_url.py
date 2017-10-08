import csv
import re

def get_issue_url(row):
    title_search = re.search('.*#(\d+).*', row["commit_text"])
    if title_search:
        issue_id = title_search.group(1)
        row["issue_id"] = issue_id
    template = "https://api.github.com/repos/%(project)s/issues/%(issue_id)s"
    return template % row

with open('data/refactorings_and_issues.csv') as input, open('data/refactorings_and_issues_complete.csv', 'w') as out:
    reader = csv.DictReader(input, delimiter=';', quotechar='"')
    fieldnames = reader.fieldnames + ["issue_url", "issue_id"]
    writer = csv.DictWriter(out, fieldnames=fieldnames, delimiter=';', quotechar='"')
    writer.writeheader()
    for row in reader:
        issue_url = get_issue_url(row)
        row["issue_url"] = issue_url
        writer.writerow(row)