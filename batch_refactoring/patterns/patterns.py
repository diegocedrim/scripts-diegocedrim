import csv


class Batch:

    def __init__(self):
        self.refs = set()
        self.removes = set()

    def add(self, ref):
        self.refs.add(ref["ref_type"])
        if ref["interference"] == "Removed":
            self.removes.add(ref["smell"])
            all_smells.add(ref["smell"])


    def __repr__(self):
        return "Batch(refs:%s,removes:%s)" % (list(self.refs), list(self.removes))

batches = {}
all_smells = set()
groups = {}
removals = {}

with open("all_batchs.csv") as batchs_file:
    reader = csv.DictReader(batchs_file, delimiter=";", quotechar="\"")
    for row in reader:
        b_id = row["batch_id"]
        batch = batches.get(b_id, Batch())
        batch.add(row)
        batches[b_id] = batch

for key in batches:
    if batches[key].removes:
        group_key = list(batches[key].refs)
        group_key.sort()
        group_key = tuple(group_key)
        groups[group_key] = groups.get(group_key, 0) + 1

        removal = removals.get(group_key, {})
        for smell in batches[key].removes:
            removal[smell] = removal.get(smell, 0) + 1
        removals[group_key] = removal
        # print key, batches[key]

for k in groups:
    print k, groups[k], removals[k]

print all_smells


with open("patterns.csv", "w") as out:
    all_smells = list(all_smells)
    all_smells.sort()
    fieldnames = ['batch', 'occurrences'] + all_smells
    writer = csv.DictWriter(out, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    for k in groups:
        row = removals[k]
        row['batch'] = ", ".join(k)
        row['occurrences'] = groups[k]
        writer.writerow(row)
        # print k, groups[k], removals[k]