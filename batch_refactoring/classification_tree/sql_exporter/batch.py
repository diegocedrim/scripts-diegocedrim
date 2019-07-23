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
          insert into 
            batch_tree_batch (
              id, 
              size, 
              is_cross_type, 
              open_source, 
              classification_id, 
              heuristic_id
          ) values (
            %s, %s, %s, %s, %s, %s
          );\n"""
        batch_id += 1
        f.write(clear(sql % (
            record["b"]["hash_id"],
            record["b"]["size"],
            record["b"]["is_cross_type"],
            record["b"]["open_source"],
            "(select id from batch_tree_batchclassification where name = '%s')" % record["b"]["classification"],
            "(select id from batch_tree_synthesisheuristic where name = '%s')" % record["b"]["type"],
        )))
    tx.commit()


graph = Graph(password="boil2.eat")
with io.open("sql/batch.sql", "w", encoding="utf8") as out:
    export(out)
