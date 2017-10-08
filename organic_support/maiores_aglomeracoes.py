import json


with open("./meyer_control_results/meyer_control_agglomeration.json") as f:
    agglomerations = json.loads(f.read())

result = []
for agg in agglomerations:
    elements = []
    for node in agg["nodes"]:
        elements.append(node["resourceFQN"])
    result.append(elements)

print json.dumps(result, indent=4)
