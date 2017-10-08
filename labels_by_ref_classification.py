import issues
import re
import refactorings

labels_found = {}


def add_refs_type(label, refs):
    for ref in refs:
        t = ref["classification"]
        k = (label,t)
        labels_found[k] = labels_found.get(k, 0) + 1

for issue in issues.issues():
    labels = issue["labels"]
    refs = refactorings.find_by_issue_url(issue["url"])
    for label in labels:
        label = label["name"].lower().strip(":")
        add_refs_type(label, refs)

keys = labels_found.keys()
keys.sort()
for key in keys:
    label = key[0]
    if not re.match("v\d.*", label):
        print "%s,%s,%s" % (key + (labels_found[key],))
