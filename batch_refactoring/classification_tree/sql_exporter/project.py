from py2neo import Graph
import io, re


def clear(sql):
    return re.sub(r"\s+", " ", sql) + "\n"


def export(f):
    query = """
        match (p:Project) return p order by p.name
    """
    tx = graph.begin()
    cursor = tx.run(query)
    batch_id = 1
    for record in cursor:
        sql = """
          insert into 
            batch_tree_project (
              id, 
              name
          ) values (
            %s, '%s'
          );\n"""
        batch_id += 1
        f.write(clear(sql % (
            batch_id,
            record["p"]["name"]
        )))
    tx.commit()


graph = Graph(password="boil2.eat")
with io.open("sql/project.sql", "w", encoding="utf8") as out:
    export(out)
