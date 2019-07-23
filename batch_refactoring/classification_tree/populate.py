from py2neo import Graph
import tree


def query_and_export(query, heuristic, level):
    print heuristic, " - computing tree"
    t = tree.Tree(max_level=level)
    tx = graph.begin()
    cursor = tx.run(query)
    for record in cursor:
        t.add_batch(record["b"], record["el"], record["p"]["name"])
    tx.commit()

    print heuristic, " - exporting tree"
    exporter = tree.TreeHTMLExporter(heuristic + ".html", t, heuristic)
    exporter.export()


def version_based(level):
    query = """
        match (b:Batch)-->(r:Refactoring)-->(el:Element)-->(c:Commit)-->(p:Project)
        where b.type = 'version-based'
        with  b, el, p
        return distinct b, el.name as el, p
    """
    query_and_export(query, "version-based", level)


def scope_based(level):
    query = """
        match (b:Batch)-->(r:Refactoring)-->(el:Element)-->(c:Commit)-->(p:Project)
        where b.type = 'scope-based'
        with  b, el, p
        return distinct b, el.name as el, p
    """
    query_and_export(query, "scope-based", level)


def element_based(level):
    query = """
        match (b:Batch)-->(r:Refactoring)-->(el:Element)-->(c:Commit)-->(p:Project)
        where b.type = 'element-based'
        with  b, el, p
        return distinct b, b.element as el, p
    """
    query_and_export(query, "element-based", level)


graph = Graph(password="boil2.eat")
element_based(8)
# version_based(4)
# scope_based(5)
