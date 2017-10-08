import json
import csv


def get_fieldnames(elements):
    headers = ["kind", "class", "element"]
    metrics = ["MethodLinesOfCode", "NumberOfAccessedVariables", "ChangingMethods", "ParameterCount", "ChangingClasses"]
    metrics += ["CyclomaticComplexity", "MaxCallChain", "CouplingIntensity", "MaxNesting", "CouplingDispersion"]
    metrics.sort()
    headers += metrics + ["smell", "reason"]
    return headers

with open("meyer_control_results/meyer_control_smells.json") as f:
    elements = json.loads(f.read())

with open('sumario_smells_metodos_com_razao_meyer.csv', 'w') as csvfile:
    fieldnames = get_fieldnames(elements)
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    for clazz in elements:
        for method in clazz["methods"]:
            method["element"] = method["fullyQualifiedName"]
            method["class"] = clazz["fullyQualifiedName"]
            smells = method["smells"]
            for mv in method["metricsValues"]:
                method[mv] = str(method["metricsValues"][mv]).replace(".", ",")
            keys = method.keys()
            for k in keys:
                if k not in fieldnames:
                    del method[k]

            for s in smells:
                method["smell"] = s["name"]
                method["reason"] = s["reason"]

                writer.writerow(method)