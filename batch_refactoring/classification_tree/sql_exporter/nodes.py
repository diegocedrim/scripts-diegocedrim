from py2neo import Graph
import sys
import sql_tree


def query_and_export(batch_tree, query, heuristic):
    print heuristic, " - computing tree"
    tx = graph.begin()
    cursor = tx.run(query)
    for record in cursor:
        batch_tree.add_batch(record["b"], record["el"], record["p"]["name"])
    tx.commit()
    print heuristic, " - processed"


def version_based(batch_tree):
    query = """
        match (b:Batch)-->(r:Refactoring)-->(el:Element)-->(c:Commit)-->(p:Project)
        where b.type = 'version-based'
        with  b, el, p
        return distinct b, el.name as el, p 
    """
    query_and_export(batch_tree, query, "version-based")


def scope_based(batch_tree):
    query = """
        match (b:Batch)-->(r:Refactoring)-->(el:Element)-->(c:Commit)-->(p:Project)
        where b.type = 'scope-based'
        with  b, el, p
        return distinct b, el.name as el, p 
    """
    query_and_export(batch_tree, query, "scope-based")


def element_based(batch_tree):
    query = """
        match (b:Batch)-->(r:Refactoring)-->(el:Element)-->(c:Commit)-->(p:Project)
        where b.type = 'element-based'
        with  b, el, p
        return distinct b, b.element as el, p 
    """
    query_and_export(batch_tree, query, "element-based")


graph = Graph(password="boil2.eat")
# element_based(6)
b_tree = sql_tree.Tree(all_levels=True)
version_based(b_tree)
element_based(b_tree)
scope_based(b_tree)

exporter = sql_tree.TreeSQLExporter("sql/nodes.sql", b_tree)
exporter.export()
