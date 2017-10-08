import csv
import sys
import os
import json

def get_agglomerations(ref):
    #diegocedrim_argouml_2e5876b5b6bb4bba332e05f6545c503afb95f6e8_agglomeration.json
    p_name = ref["project"].replace("/", "_")
    agg_file = "%s/%s_%s_agglomeration.json" % (agglomerations_folder, p_name, ref["original_commit"])
    if os.path.isfile(agg_file):
        with open(agg_file) as f:
            content = f.read()
            content = json.loads(content)
            aggs = []
            for agg in content:
                simple = set([i["resourceFQN"] for i in agg["nodes"]])
                aggs.append(simple)
            return aggs
    # print agg_file
    return None

def is_in_agglomeration(ref):
    elements = eval(ref["parameters"])
    agglomerations = get_agglomerations(ref)
    if agglomerations == None:
        # print "No agg file for", ref
        # exit()
        return
    for e in elements:
        for a in agglomerations:
            if e in a:
                return True
    return False


def load_all():
    all_refs = []
    with open('data/all_refs_simplified.csv') as input:
        reader = csv.DictReader(input, delimiter=';', quotechar='"')
        for row in reader:
            all_refs.append(row)
    return all_refs

agglomerations_folder = sys.argv[1]
stats = {True:0, False:0, None:0}
out = file("data/is_in_agglomeration.csv", "w")
# out-10-commits.write("ref_id;is_in_agglomeration\n")
all_refs = load_all()
for i in xrange(len(all_refs)):
    sys.stdout.write("\rRefactoring: %s of %s" % (i,len(all_refs) - 1))
    sys.stdout.flush()
    ref = all_refs[i]
    is_in = is_in_agglomeration(ref)
    stats[is_in] += 1
    if is_in is not None:
        sql = "update refactoring set in_agglomeration = %s where id = %s;\n" % (int(is_in), ref["ref_id"])
        out.write(sql)
print ""
out.close()
print stats
