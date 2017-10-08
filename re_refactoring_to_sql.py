import csv


with open('data/re-refactored.csv') as input:
    reader = csv.DictReader(input, delimiter=';', quotechar='"')
    for row in reader:
        sql = "update refactoring set re_refactored = 1, time_to_re_refactor = %s where id = %s;"
        print sql % (row["version_until_next_refactoring"], row["id"])
