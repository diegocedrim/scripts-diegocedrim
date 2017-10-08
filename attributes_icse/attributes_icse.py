import json


attributes = {
    "complexity": ["Cyclomatic", "Essential", "CountPath", "MaxNesting"],
    "coupling": ["CountClassCoupled", "CountInput", "CountOutput"],
    "inheritance": ["MaxInheritanceTree", "CountClassDerived", "CountClassBase"],
    "size": ["CountLineCode", "CountLineComment", "CountStmt", "CountDeclClass",
            "CountDeclInstanceVariable", "CountDeclInstanceMethod"],
    "cohesion": ["PercentLackOfCohesion"]
}


def resource_pairs(refactoring):
    before = refactoring["resourcesBefore"]
    after = refactoring["resourcesAfter"]

    if len(before) == len(after) == 1:
        return [(before[0], after[0])]

    pairs = []
    for before_rsc in before:
        name = before_rsc["resource"]["name"]
        other_half = None
        for after_rsc in after:
            if after_rsc["resource"]["name"] == name:
                other_half = after_rsc
                break
        if other_half is not None:
            pairs.append((before_rsc, other_half))
    return pairs


def load_refactorings():
    with open("results_no_null.json") as r:
        refs = json.loads(r.read())
    return refs


def measure_impact(pair, attr_name, metrics_to_consider=1):
    metrics = attributes[attr_name]
    metrics_to_consider = min(len(metrics), metrics_to_consider)
    measures_before = pair[0]["measures"][0]
    measures_after = pair[1]["measures"][0]
    improved = 0
    worsen = 0
    for metric_name in metrics:
        val_before = measures_before.get(metric_name, None)
        val_after = measures_after.get(metric_name, None)
        if val_before is None or val_after is None:
            continue
        if val_after > val_before:
            worsen += 1
        elif val_after < val_before:
            improved += 1

    if worsen >= metrics_to_consider:
        return "negative"
    if improved >= metrics_to_consider:
        return "positive"
    return "neutral"


query = """
insert into refs_and_attributes (refactoring_id, attribute, impact, resource_id_from, resource_id_to, type)
values (%s, '%s', '%s', %s, %s, '%s');
"""

metrics_to_consider = 2
i = 0
all_refs = load_refactorings()
for ref in all_refs:
    i += 1
    print "#", ref["id"]
    rsc_pairs = resource_pairs(ref)
    for pair in rsc_pairs:
        id_from = pair[0]["resource"]["id"]
        id_to = pair[1]["resource"]["id"]
        for attribute in attributes.keys():
            impact = measure_impact(pair, attribute, metrics_to_consider)
            line =  query % (ref["id"], attribute, impact, id_from, id_to, str(metrics_to_consider) + "-metrics")
            line = line.replace("\n", " ")
            print line
    # if i == 10:
    #     exit()
