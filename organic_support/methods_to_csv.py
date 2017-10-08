import json
import csv


def get_fieldnames(elements):
    headers = ["kind", "class", "element"]
    metrics = ["MethodLinesOfCode", "NumberOfAccessedVariables", "ChangingMethods", "ParameterCount", "ChangingClasses"]
    metrics += ["CyclomaticComplexity", "MaxCallChain", "CouplingIntensity", "MaxNesting", "CouplingDispersion"]
    metrics.sort()
    headers += metrics + ["smells_count","smells"]
    return headers

with open("academico_results/academico_smells.json") as f:
    elements = json.loads(f.read())

with open('sumario_smells.csv', 'w') as csvfile:
    fieldnames = get_fieldnames(elements)
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    for clazz in elements:
        smells = []
        for method in clazz["methods"]:
            for s in method["smells"]:
                smells.append(s["name"])
            method["smells_count"] = len(smells)
            method["smells"] = ",".join(list(set(smells)))
            method["element"] = method["fullyQualifiedName"]
            method["class"] = clazz["fullyQualifiedName"]
            for mv in method["metricsValues"]:
                method[mv] = str(method["metricsValues"][mv]).replace(".",  ",")
            keys = method.keys()
            for k in keys:
                if k not in fieldnames:
                    del method[k]

            if len(smells) > 0:
                writer.writerow(method)