import json, csv, re


def load_patterns(filename):
    with open(filename) as f:
        return json.loads(f.read())


def export_to_csv(data, headers, filename):
    with open(filename, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers, delimiter=';')

        writer.writeheader()
        for row in data:
            writer.writerow(row)


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1).title()


def export_to_r(data, filename):
    with open(filename, 'w') as csv_file:
        names = ["batch", "smell", "percentage", "observations", "interferences"]
        writer = csv.DictWriter(csv_file, fieldnames=names, delimiter=';')

        writer.writeheader()
        for row in data:
            r_row = {"batch": ",".join(row["batch"])}
            if r_row["batch"] == "Rename Method":
                continue
            for smell in row:
                if smell == "batch":
                    continue
                r_row["smell"] = convert(smell)
                r_row["percentage"] = int(row[smell]["percentage"]*100)
                r_row["observations"] = row[smell]["occurrences"]
                r_row["interferences"] = row[smell]["interferences"]
                writer.writerow(r_row)


def summary(filename, pattern_type):  # pattern_type = introduced or removed
    data = load_patterns(filename)
    stats = []
    smells_names = set()
    for pattern in data:
        row = {"batch": [", ".join(pattern["sequence"])]}
        occurrences = pattern["occurrences"]
        for smell, interference in pattern["interferences"].iteritems():
            smells_names.add(smell)
            # print interference
            percentage = float(interference[pattern_type])/occurrences
            if percentage >= 0.5 and occurrences > 20 and percentage < 1:
                row[smell] = {
                    "occurrences": occurrences,
                    "interferences": interference[pattern_type],
                    "percentage": percentage
                }
        stats.append(row)

    headers = ["batch"] + sorted(list(smells_names))
    filename = "summaries/" + filename.split("/")[-1][:-5] + "_" + pattern_type + ".csv"
    # export_to_csv(stats, headers, filename)
    export_to_r(stats, filename)


summary("interferences/element_based.json", "introduced")
summary("interferences/element_based.json", "removed")
summary("interferences/scope_based.json", "introduced")
summary("interferences/scope_based.json", "removed")
summary("interferences/version_based.json", "introduced")
summary("interferences/version_based.json", "removed")
