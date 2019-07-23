from py2neo import Graph

graph = Graph(password="boil2.eat")

with open("cleanup") as queries_file:
    queries = [i.strip() for i in queries_file.readlines()]
    for qry in queries:
        print qry
        graph.run(qry)
