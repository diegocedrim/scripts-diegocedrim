import json
import csv


def get_fieldnames(elements):
    headers = ["kind", "element"]
    metrics = elements[0]["metricsValues"].keys()
    metrics.sort()
    headers += metrics + ["smells_count","smells"]
    return headers

with open("meyer_control_results/meyer_control_smells.json") as f:
    elements = json.loads(f.read())

with open('out.csv', 'w') as csvfile:
    fieldnames = get_fieldnames(elements)
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    for clazz in elements:
        smells = []
        for s in clazz["smells"]:
            smells.append(s["name"])
        for method in clazz["methods"]:
            for s in method["smells"]:
                smells.append(s["name"])
        clazz["smells_count"] = len(smells)
        clazz["smells"] = ",".join(list(set(smells)))
        clazz["element"] = clazz["fullyQualifiedName"]
        for mv in clazz["metricsValues"]:
            clazz[mv] = str(clazz["metricsValues"][mv]).replace(".",  ",")
        keys = clazz.keys()
        for k in keys:
            if k not in fieldnames:
                del clazz[k]

        writer.writerow(clazz)