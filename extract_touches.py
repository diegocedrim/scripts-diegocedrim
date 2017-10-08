from py2neo import Graph

query = "match (r:Refactoring)-[:CHANGED]->(el:Element)-->(s:Smell) return r.type, s.type, count(*) as total order by r.type"
print "ref_name,smell_name,touches"

graph = Graph(password="boil2.eat")
data = graph.data(query)

for row in data:
    print "%s,%s,%s" % (row["r.type"], row["s.type"], row["total"])