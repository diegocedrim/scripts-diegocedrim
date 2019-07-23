from py2neo import Graph
import csv
import codecs


def export_to_csv(cursor, filename):
    with codecs.open(filename, "w", "utf-8") as csvfile:
        writer = None
        for record in cursor:
            if writer is None:
                writer = csv.DictWriter(csvfile, fieldnames=list(record.keys()))
                writer.writeheader()
            record = dict(record)
            # print record
            writer.writerow(record)


# query = """
# match (b:Batch) where b.type = 'version-based' return b.size as size order by b.size
# """

query = """
match (b:Batch) return b.type as type, b.size as size order by b.type, b.size
"""

filename = "sizes.csv"
graph = Graph(password="boil2.eat")
tx = graph.begin()
cursor = tx.run(query)
export_to_csv(cursor, filename)
tx.commit()
