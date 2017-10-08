import json

with open("/Users/diego/Downloads/academico__smells.json") as f:
    elements = json.loads(f.read())

smells = []
for clazz in elements:
    for s in clazz["smells"]:
        s["element"] = clazz["fullyQualifiedName"]
        smells.append(s)
    for method in clazz["methods"]:
        for s in method["smells"]:
            s["element"] = method["fullyQualifiedName"]
            smells.append(s)
print json.dumps(smells, indent=4)