import csv
import sys


def is_next_ref(next, previous):
    if next["project"] != previous["project"]:
        return False
    elements_next = eval(next["parameters"])
    elements_previous = eval(previous["parameters"])
    for e in elements_previous:
        if e in elements_next:
            return True
    return False


def next_refactoring(index):
    ref = all_refs[index]
    for i in xrange(index, len(all_refs)):
        current = all_refs[i]
        if current["project"] != ref["project"]:
            return None
        if current["version_order"] == ref["version_order"]:
            continue
        if is_next_ref(current, ref):
            return current
    return None

def load_all():
    all_refs = []
    with open('data/all_refs_simplified.csv') as input:
        reader = csv.DictReader(input, delimiter=',', quotechar='"')
        for row in reader:
            all_refs.append(row)
    return all_refs

rerefs = set()
out = file("data/re-refactored.csv", "w")
out.write("id;type;classification;version_until_next_refactoring\n")
all_refs = load_all()
for i in xrange(len(all_refs)):
    sys.stdout.write("\rRefactoring: %s of %s" % (i,len(all_refs) - 1))
    sys.stdout.flush()
    ref = all_refs[i]
    next_ref = next_refactoring(i)
    if next_ref != None:
        rerefs.add(all_refs[i]["ref_id"])
        rerefs.add(next_ref["ref_id"])
        how_far = int(next_ref["version_order"]) - int(ref["version_order"])
        out.write("%s;%s;%s;%s;%s\n" % (ref["ref_id"], ref["ref_type"], ref["classification"], how_far, ref["project"]))
out.close()
print len(rerefs)