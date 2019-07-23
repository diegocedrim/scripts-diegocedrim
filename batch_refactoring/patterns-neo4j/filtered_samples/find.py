import csv
import sys

intros = {}
removals = {}

with open("element_based-samples_filtered.csv") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")
    for row in reader:
        if row["interference"] == "removal":
            destination = removals
        else:
            destination = intros
        key = (row["batch"], row["smell"])
        values = destination.get(key, [])
        values.append(row)
        destination[key] = values

# interference = sys.argv[1]
# smell = sys.argv[2]

interference = "introduction"
smell = "FeatureEnvy"

samples = None
if interference == "removal":
    samples = removals
if interference == "introduction":
    samples = intros

print "Procurando em %s por %s" % (interference, smell)
batch = raw_input("Digite o batch: ")
while samples and batch != "":
    key = (batch, smell)
    if key in samples:
        for row in samples[key]:
            print "Batch id: %s" % row["batch_id"]
            print "Element: %s" % row["element"]
            print "Refactorings:"
            for ref_id in eval(row["refactorings"]):
                print ref_id
            print "-"*50
    batch = raw_input("Digite o batch: ")