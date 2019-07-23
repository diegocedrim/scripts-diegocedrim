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
match (b:Batch)-->(r:Refactoring)-->(c:Commit)-->(p:Project)
where b.type = 'element-based'
with p.name as project, b.element as element, b order by p.name, b.element, b.order
with project, element, collect(distinct b) as batches
where size(batches) >= 2
return  project, element, batches
"""

filename = "../icse_ana/batches_per_elements.json"
graph = Graph(password="boil2.eat")
tx = graph.begin()
cursor = tx.run(query)
export_to_json(cursor, filename)
tx.commit()



