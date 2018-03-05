import csv, re


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1).title()


def read_interesting_interferences(filename, interference):
    interferences = set()
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            interferences.add((row["batch"], row["smell"], interference))
    return interferences


def main():
    intro = read_interesting_interferences("summaries/element_based_introduced.csv", "introduction")
    rems = read_interesting_interferences("summaries/element_based_removed.csv", "removal")
    interesting = intro.union(rems)

    source = "interferences/element_based-samples.csv"
    destination = "filtered_samples/element_based-samples_filtered.csv"
    with open(source) as rawfile, open(destination, "w") as filteredfile:
        reader = csv.DictReader(rawfile, delimiter=";")

        header = ["batch", "smell", "interference", "batch_id", "element", "refactorings"]
        writer = csv.DictWriter(filteredfile, fieldnames=header, delimiter=";")
        writer.writeheader()
        for row in reader:
            key = (row["batch"], convert(row["smell"]), row["interference"])
            if key in interesting:
                writer.writerow(row)


main()
