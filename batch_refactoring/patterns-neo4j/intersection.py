# coding:utf8

"""
Interseção dos sumários de cada tipo de batch. Pra cada par em cada tipo de batch, eu salvo
a linha pra gerar plot depois
"""
import csv
import os


def get_files(interference):
    return [
        ("summaries/element_based_%s.csv" % interference, "element-based"),
        ("summaries/scope_based_%s.csv" % interference, "scope-based"),
        ("summaries/version_based_%s.csv" % interference, "version-based")
    ]


def export_csv(filename, pairs):
    with open(filename, "w") as out:
        fields = ["batch", "smell", "element-based", "scope-based", "version-based"]
        writer = csv.DictWriter(out, fieldnames=fields, delimiter=";")
        writer.writeheader()
        for batch_smell, batch_types in pairs.iteritems():
            if len(batch_types) > 1:
                row = {
                    'batch': batch_smell[0],
                    'smell': batch_smell[1]
                }
                for btype in batch_types:
                    row[btype] = 'X'
                writer.writerow(row)


def intersection(interference):
    pairs = {}
    for f, batch_type in get_files(interference):
        with open(f) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                key = (row['batch'], row['smell'])
                ocurrences = pairs.get(key, [])
                ocurrences.append(batch_type)
                pairs[key] = ocurrences
    export_csv("intersections/%s.csv" % interference, pairs)


intersection("introduced")
intersection("removed")
