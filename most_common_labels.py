import issues
import re

labels_found = {}

for issue in issues.issues():
    labels = issue["labels"]
    for label in labels:
        label = label["name"].lower().strip(":")
        labels_found[label] = labels_found.get(label, 0) + 1

for label in labels_found:
    if not re.match("v\d.*", label):
        print label,"\t",labels_found[label]
