import csv
from bisect import bisect_left
import json


def clean_single_refs(rerefs):
    for key in rerefs.keys():
        if len(rerefs[key]) < 2:
            del rerefs[key]


def load_rerefs(filename):
    rerefs = {}
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            key = (row["project_name"], row["element"])
            rerefs[key] = rerefs.get(key, []) + [row]
    clean_single_refs(rerefs)
    return rerefs


def load_commits_by_devs():
    commits_by_dev = {}
    with open("rerefs/commits_and_devs.csv") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            key = (row["project_name"], row["author_email"])
            commits_by_dev[key] = commits_by_dev.get(key, []) + [int(row["order"])]
    return commits_by_dev


def index(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    raise ValueError


def worked_between(start_order, end_order, ref):
    commits = commits_by_devs[(ref["project_name"], ref["author_email"])]
    start_index = index(commits, int(start_order))
    end_index = index(commits, int(end_order))
    # TODO: Melhorar Criterio
    # Se abs(end_index - start_index) > 1, devemos checar se o dev trabalhou em
    # outra classe ou nao. Se ele trabalhou na mesma durante o intervalo, entao consideramos
    # parte do mesmo batch e nao acabar com o batch
    return abs(end_index - start_index) > 1


def find_batches(key):
    refs = rerefs[key]
    batches = []
    current_batch = []
    element = refs[0]["element"]
    dev = refs[0]["author_email"]
    order = refs[0]["order"]
    for ref in refs:
        if not (ref["element"] == element and ref["author_email"] == dev and not worked_between(order, ref["order"], ref)):
            if len(current_batch) > 1:
                batches.append(current_batch)
            current_batch = []
            element = ref["element"]
            dev = ref["author_email"]
            order = ref["order"]
        current_batch.append(ref)
    if len(current_batch) > 1:
        batches.append(current_batch)
    return batches


rerefs = load_rerefs("rerefs/refactored_elements.csv")
commits_by_devs = load_commits_by_devs()
# print commits_by_devs[("alibaba/dubbo", "ding.lid@1a56cb94-b969-4eaa-88fa-be21384802f2")]
# exit()
# for i in rerefs:
#     if len(rerefs[i]) > 200:
#         print i, len(rerefs[i])
#         exit()
i = 1
multiple = 0
all_batches = []
for key in rerefs:
    batches = find_batches(key)
    all_batches += batches
    for batch in batches:
        print "Batch", i
        i += 1
        orders = set()
        for ref in batch:
            print ref["element"], ref["author_email"], ref["order"]
            orders.add(ref["order"])
        if len(orders) > 1:
            multiple += 1
        print ""
print len(all_batches)

print json.dumps(all_batches, indent=4)
print "Batches: %s (%s multiples)" % (len(all_batches), multiple)
