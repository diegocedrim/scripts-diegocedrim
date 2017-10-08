import json


class Batch:

    ID = 1

    def query_last_resource(self, last_ref):
        sql = """
            (select
                r.id
            from
                resource r
                inner join version v on (v.id = r.version_id)
            where
                v.project_id = %s
                and r.name = '%s'
                and v.order = %s)
        """ % (last_ref["project_id"], last_ref["element"], int(last_ref["order"]) + 1)
        return sql

    def __init__(self, batch_list):
        self.data = {}
        self.batch_list = batch_list
        self.data["project_id"] = batch_list[0]["project_id"]
        self.data["resource_name"] = batch_list[0]["element"]
        self.data["initial_resource"] = batch_list[0]["resource_id"]
        self.data["final_resource"] = self.query_last_resource(batch_list[-1])
        self.data["lifespan"] = int(batch_list[-1]["order"]) - int(batch_list[0]["order"]) + 1
        self.data["id"] = Batch.ID
        Batch.ID += 1

    def to_sql(self):
        sql = """
            INSERT INTO batch (id, project_id, lifespan, resource_name, initial_resource, final_resource)
            VALUES (%(id)s, %(project_id)s, %(lifespan)s, '%(resource_name)s', %(initial_resource)s, %(final_resource)s);
        """
        query = (sql % self.data).replace("\n", " ").replace("\t", " ")
        while "  " in query:
            query = query.replace("  ", " ")
        return query.strip()


def load():
    with open("fse_batches.json") as batches_file:
        return json.loads(batches_file.read())

# print len(load())
# exit()
print "delete from batch_refactoring;"
print "delete from batch;"
for batch in load():
    bo = Batch(batch)
    print bo.to_sql()
    current_id = bo.data["id"]
    for ref in batch:
        print "insert into batch_refactoring (batch_id, refactoring_id) values (%s, %s);" % (current_id, ref["ref_id"])

print "delete from batch_refactoring where batch_id in (select id from batch where final_resource is null);"
print "delete from batch where final_resource is null;"
