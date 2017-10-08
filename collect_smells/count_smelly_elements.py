import json, glob


def count_smells(file_name):
    with open(file_name) as smell_json_file:
        resources = json.loads(smell_json_file.read())
        smelly = set()
        for clazz in resources:
            if len(clazz["smells"]) > 0:
                smelly.add(clazz["fullyQualifiedName"])
            for method in clazz["methods"]:
                if len(method["smells"]) > 0:
                    smelly.add(method["fullyQualifiedName"])
        return len(smelly)

for f in glob.glob("/Users/diego/Downloads/output_ultimos/*.json"):
    print "_".join(f.split("/")[-1].split("_")[:2]), count_smells(f)