import csv


def load_touches(f):
    refs = {}
    with open(f) as file:
        reader = csv.DictReader(file)
        for row in reader:
            refs[(row["ref_name"].lower(),row["smell_name"])] = int(row["touches"])
    return refs

def refs():
    with open("touches/refs.csv") as f:
        refs = {}
        lines = f.readlines()
        for line in lines:
            line = line.split(",")
            refs[line[0].strip().lower()] = int(line[1])
        return refs


def merge(refs_1, refs_2):
    for key in refs_2:
        refs_1[key] = refs_1.get(key, 0) + refs_2[key]
    return refs_1

icse = load_touches("touches/touches_icse.csv")
octopus = load_touches("touches/touches_octopus.csv")
all = merge(icse, octopus)
r = refs()
# print r
for key in all:
    percentual = float(all[key])/r[key[0].lower()]
    print "%s\t%s\t%s\t%s\t%.2f" % (key[0].title(), key[1], all[key], r[key[0].lower()], percentual)
