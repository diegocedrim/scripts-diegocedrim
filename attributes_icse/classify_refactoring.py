import MySQLdb


def attributes():
    sql = "select distinct attribute from refs_and_attributes"
    query = connection.cursor(MySQLdb.cursors.DictCursor)
    query.execute(sql)
    val = [row["attribute"] for row in query.fetchall()]
    query.close()
    return val


def refactorings():
    sql = "select distinct refactoring_id from refs_and_attributes"
    query = connection.cursor(MySQLdb.cursors.DictCursor)
    query.execute(sql)
    val = [row["refactoring_id"] for row in query.fetchall()]
    query.close()
    return val


def impact_on(attr_name, ref_id, type):
    sql = "select impact from refs_and_attributes where attribute = '%s' and refactoring_id = %s and type = '%s'"
    sql %= (attr_name, ref_id, type)
    query = connection.cursor(MySQLdb.cursors.DictCursor)
    query.execute(sql)
    impacts = set([row["impact"] for row in query.fetchall()])
    if "negative" in impacts:
        return "negative"
    if "positive" in impacts:
        return "positive"
    return "neutral"


def classify(ref_id):
    impacts = {"positive": 0, "negative": 0, "neutral": 0}
    for attr_name in attributes_names:
        impact = impact_on(attr_name, ref_id, type_selected)
        impacts[impact] += 1

    sql = "insert into refs_overall_impact_attrs (refactoring_id, positive, negative, neutral, type) " \
          "values (%s, %s, %s, %s, '%s')"
    sql %= (ref_id, impacts["positive"], impacts["negative"], impacts["neutral"], type_selected)
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.close()
    connection.commit()


connection = MySQLdb.connect(user="root", passwd="root", db="ref_base")
type_selected = "2-metrics"
attributes_names = attributes()
# print attributes()
for ref_id in refactorings():
    classify(ref_id)
    print ref_id
    # exit()