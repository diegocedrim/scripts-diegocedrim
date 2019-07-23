from py2neo import Graph
import csv


def source():
    query = """
        match (r:Refactoring)-[:CHANGED]->(e:Element)-->(s:Smell)
        where 
            (r.type = 'Move Method'
             or r.type = 'Pull Up Method'
             or r.type = 'Push Down Method') 
             and s.type = 'FeatureEnvy'
        return r, e, s
    """
    return graph.data(query)


def is_there_feature_envy_after(refactoring_id):
    query = """
        match (r:Refactoring)-[:PRODUCED]->(el:Element)-->(s:Smell)
        where r.hash_id = '%s'
        with collect(s.type) as smells_after
        return ANY(x IN smells_after WHERE x = 'FeatureEnvy') as has
    """ % refactoring_id
    return graph.data(query)[0]["has"]


def commits(refactoring_id):
    query = """
        match (e:Commit)<-[:ENDED_AT]-(r:Refactoring)-[:STARTED_AT]->(s:Commit)-->(p:Project)
        where r.hash_id = '%s'
        return e.hash as hash_after, s.hash as hash_before, p.url as project
    """ % refactoring_id
    return graph.data(query)[0]


def details(refactoring, element, smell):
    parameters = eval(refactoring["parameters"])
    cmts = commits(refactoring["hash_id"])
    row = {
        "refactoring_hash_id": refactoring["hash_id"],
        "type": refactoring["type"],
        "reason_of_FeatureEnvy": smell["reason"],
        "method_before": parameters[0][0],
        "method_after": parameters[2][0],
        "commit_before": cmts["hash_before"],
        "commit_after": cmts["hash_after"],
        "project": cmts["project"],
        "refactoring_viewer_link": "http://diegocedrim.com/batch-validation/refactoring_viewer.php?id=%s" % refactoring["hash_id"],
    }
    return row


def get_link(method, commit, project_url):
    # https://github.com/apache/tomcat/blob/61a2e35b83afbeb96c091728540b9ee06243171d/java/org/apache/tomcat/util/net/NioEndpoint.java
    template = "%s/blob/%s/java/%s.java"
    clazz = method[:method.rfind(".")].replace(".", "/")
    return template % (project_url, commit, clazz)



with open("results.csv", "w") as out:
    header = [
        "refactoring_hash_id",
        "type",
        "reason_of_FeatureEnvy",
        "method_before",
        "method_after",
        "commit_before",
        "commit_after",
        "project",
        "refactoring_viewer_link",
    ]
    writer = csv.DictWriter(out,fieldnames=header)
    writer.writeheader()
    graph = Graph(password="boil2.eat")
    for row in source():
        refactoring = row["r"]
        element = row["e"]
        smell = row["s"]
        candidate = not is_there_feature_envy_after(refactoring["hash_id"])
        if candidate:
            parameters = eval(refactoring["parameters"])
            method_before = parameters[0]
            # print refactoring["hash_id"], refactoring["parameters"]
            csv_row = details(refactoring, element, smell)
            writer.writerow(csv_row)
