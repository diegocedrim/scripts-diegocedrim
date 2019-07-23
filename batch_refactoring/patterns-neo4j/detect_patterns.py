import json
from collections import Counter
from json import JSONEncoder
import csv


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Refactoring:
    def __init__(self):
        self.type = None
        self.smells_before = None
        self.smells_after = None
        self.ref_id = None
        self.element = None

    def __repr__(self):
        return "Refactoring(%s, %s, %s)" % (self.type, self.smells_before, self.smells_after)


class Interference:
    def __init__(self):
        self.introduced = 0
        self.removed = 0


class BatchSlice:
    def __init__(self, sequence):
        self.sequence = sequence  # tuple of ordered refactoring types
        self.occurrences = 0
        self.interferences = {}

    def introduction(self, smell):
        interference = self.interferences.get(smell, Interference())
        interference.introduced += 1
        self.interferences[smell] = interference

    def removal(self, smell):
        interference = self.interferences.get(smell, Interference())
        interference.removed += 1
        self.interferences[smell] = interference


def load_batches(filename, only_single_commit=False):
    batches = {}
    with open(filename) as f:
        data = json.loads(f.read())
        for row in data:
            is_cross = row["batch"]["is_cross_commit"]
            if is_cross and only_single_commit:
                continue
            refactorings = batches.get(row["batch"]["hash_id"], [])
            ref = Refactoring()
            ref.type = row["refactoring"]["type"]
            ref.smells_before = row["smells_before"]
            ref.smells_after = row["smells_after"]
            ref.ref_id = row["refactoring"]["hash_id"]
            ref.element = row["batch"]["element"]
            refactorings.append(ref)
            batches[row["batch"]["hash_id"]] = refactorings
    return batches


def slices(refactorings):
    for i in range(2, len(refactorings) + 1):
        ref_slice = refactorings[:i]
        sequence = tuple(sorted([r.type for r in ref_slice]))
        yield sequence, ref_slice[0].smells_before, ref_slice[-1].smells_after


def slices_not_repeated(refactorings):
    sequence_set = set([r.type for r in refactorings])
    sequence = tuple(sorted(list(sequence_set)))
    yield sequence, refactorings[0].smells_before, refactorings[-1].smells_after


def sliding_slices(refactorings):
    n = len(refactorings)
    for slice_size in range(2, n + 1):
        for i in range(0, n):
            ref_slice = refactorings[i:i+slice_size]
            if len(ref_slice) != slice_size:
                continue
            # sequence = tuple([r.type for r in ref_slice])
            sequence_set = set([r.type for r in refactorings])
            sequence = tuple(sorted(list(sequence_set)))
            yield sequence, ref_slice[0].smells_before, ref_slice[-1].smells_after


def sliding_slices_no_set(refactorings):
    n = len(refactorings)
    for slice_size in range(2, n + 1):
        for i in range(0, n):
            ref_slice = refactorings[i:i+slice_size]
            if len(ref_slice) != slice_size:
                continue
            # sequence = tuple([r.type for r in ref_slice])
            sequence = compress_sequence([r.type for r in ref_slice])
            # print [r.type for r in ref_slice], sequence
            yield sequence, ref_slice[0].smells_before, ref_slice[-1].smells_after, ref_slice


# converte de MM, MM, MM, RM, RM => MM{3}, RM{2}
def compress_sequence(ref_types):
    compressed = []
    current = ref_types[0]
    count = 0
    for ref in ref_types:
        if current != ref:
            aggregated = current
            if count > 1:
                aggregated = "%s{n}" % current
            compressed.append(aggregated)
            count = 0
            current = ref
        count += 1
    aggregated = current
    if count > 1:
        aggregated = "%s{n}" % current
    compressed.append(aggregated)
    return tuple(compressed)


def changes(smells_before, smells_after):
    before = Counter(smells_before)
    after = Counter(smells_after)
    introductions = set()
    removals = set()

    for smell, count in before.iteritems():
        if after[smell] > count:
            introductions.add(smell)
        if after[smell] < count:
            removals.add(smell)

    for smell, count in after.iteritems():
        if before[smell] > count:
            removals.add(smell)
        if before[smell] < count:
            introductions.add(smell)

    return list(introductions), list(removals)


def load_batches_project():
    with open("batches/project_by_batch_id.csv") as f:
        project_by_batch_id = {}
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            project_by_batch_id[int(row["b.hash_id"])] = row["p.name"]
        return project_by_batch_id


def print_impact(impact):
    for i in impact:
        print i
        print json.dumps(impact[i], indent=4, cls=MyEncoder, sort_keys=True)
        print ""


def interferences(batches):
    # key => tuple of ordered refactoring types
    # value => {occurrences: X,
    impact = {}
    samples = []
    total = len(batches)
    current = 0
    project_by_batch_id = load_batches_project()
    for hash_id, refactorings in batches.iteritems():
        current += 1
        print "Processing %s/%s" % (current, total)
        for sequence, before, after, ref_slice in sliding_slices_no_set(refactorings):
            # computes the smell introductions and removals of the slice
            introductions, removals = changes(before, after)

            batch_slice = impact.get(sequence, BatchSlice(sequence))
            seq_key = ", ".join(sequence)
            refs = [r.ref_id for r in ref_slice]

            batch_slice.occurrences += 1
            # register the introductions and removals
            for smell in introductions:
                sample = {
                    "batch": seq_key,
                    "smell": smell,
                    "interference": "introduction",
                    "refactorings": refs,
                    "batch_id": hash_id,
                    "element": refactorings[0].element,
                    "project": project_by_batch_id[hash_id]
                }
                samples.append(sample)

                batch_slice.introduction(smell)

            for smell in removals:
                sample = {
                    "batch": seq_key,
                    "smell": smell,
                    "interference": "removal",
                    "refactorings": refs,
                    "batch_id": hash_id,
                    "element": refactorings[0].element,
                    "project": project_by_batch_id[hash_id]
                }
                samples.append(sample)

                batch_slice.removal(smell)

            impact[sequence] = batch_slice
    cleanup(impact)
    return impact, samples


# delete all sequences with less than 10 occurrences
def cleanup(impact):
    to_delete = []
    for k, v in impact.iteritems():
        if v.occurrences < 10:
            to_delete.append(k)
    for k in to_delete:
        del impact[k]


def detect(batches_filename, alias, only_single=False):
    bs = load_batches(batches_filename, only_single)
    ints, samples = interferences(bs)
    with open("interferences/%s.json" % alias, "w") as out:
        data = json.dumps(ints.values(), indent=4, cls=MyEncoder, sort_keys=True)
        out.write(data)
    with open("interferences/%s-samples.csv" % alias, "w") as samplefile:
        header = ["project", "batch", "smell", "interference", "batch_id", "element", "refactorings"]
        writer = csv.DictWriter(samplefile, fieldnames=header, delimiter=";")
        writer.writeheader()
        writer.writerows(samples)



# detect("batches/batch_and_smells_scope_based.json", "scope_based", True)
detect("batches/batch_and_smells_element_based.json", "element_based", True)
# detect("batches/batch_and_smells_version_based.json", "version_based", True)
