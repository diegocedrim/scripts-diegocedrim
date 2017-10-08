import csv

def load_all():
    all_refs = []
    with open('data/re-refactored.csv') as input:
        reader = csv.DictReader(input, delimiter=',', quotechar='"')
        for row in reader:
            all_refs.append(row)
    return all_refs