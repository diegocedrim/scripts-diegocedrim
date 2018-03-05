from py2neo import Graph
import json


def export_to_json(cursor, filename):
    result = []
    with open(filename, "w") as jsonfile:
        for record in cursor:
            result.append(dict(record))
        result_json = json.dumps(result, indent=4)
        jsonfile.write(result_json)


query = """
match (b:Batch)-[co:COMPOSED_OF]->(r:Refactoring)-->(c:Commit)
where b.type = 'version-based'
with b, co, r

optional match (r)-[:CHANGED]->(eb:Element)-->(sb:Smell)
with b, co, r, collect(sb.type) as smells_before

optional match (r)-[:PRODUCED]->(eb:Element)-->(sb:Smell)
return
    b as batch,
    co as composed_of,
    r as refactoring,
    smells_before,
    collect(sb.type) as smells_after

order by b.hash_id, co.order;
"""

filename = "../batch_refactoring/patterns-neo4j/batches/batch_and_smells_version_based.json"
graph = Graph(password="boil2.eat")
tx = graph.begin()
cursor = tx.run(query)
export_to_json(cursor, filename)
tx.commit()

