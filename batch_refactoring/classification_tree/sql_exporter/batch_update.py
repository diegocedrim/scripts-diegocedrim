from py2neo import Graph
import io, re


def clear(sql):
    return re.sub(r"\s+", " ", sql) + "\n"


def export(f):
    query = """
        match (b:Batch) return b order by b.hash_id
    """
    tx = graph.begin()
    cursor = tx.run(query)
    batch_id = 1
    for record in cursor:
        sql = """
          update batch_tree_batch set 
            size = %s,
            is_cross_type = %s,
            is_cross_commit = %s,
            open_source = %s,
            classification_id = %s,
            heuristic_id = %s,
            classification_level = '%s'
          where 
            id = %s
          ;\n"""
        batch_id += 1
        f.write(clear(sql % (
            record["b"]["size"],
            record["b"]["is_cross_type"],
            record["b"]["is_cross_commit"],
            record["b"]["open_source"],
            "(select id from batch_tree_batchclassification where name = '%s')" % record["b"]["classification"],
            "(select id from batch_tree_synthesisheuristic where name = '%s')" % record["b"]["type"],
            record["b"]["classification_level"],
            record["b"]["hash_id"],
        )))
    tx.commit()


graph = Graph(password="boil2.eat")
with io.open("sql/batch_update.sql", "w", encoding="utf8") as out:
    export(out)
