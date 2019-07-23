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


def detect(batches_filename, alias, only_single=False):
    bs = load_batches(batches_filename, only_single)
    with open("sequences/batches_sequence.csv", "a") as f:
        writer = csv.DictWriter(f, fieldnames=["batch_id", "sequence"], delimiter=";")
        writer.writeheader()
        for hash_id, refactorings in bs.iteritems():
            types = [r.type for r in refactorings]
            sequence = ', '.join(compress_sequence(types))
            writer.writerow({
                'batch_id': hash_id,
                'sequence': sequence
            })
            print "update batch_tree_batch set sequence = '%s' where id = %s;" % (sequence, hash_id)


detect("batches/batch_and_smells_scope_based.json", "scope_based")
detect("batches/batch_and_smells_element_based.json", "element_based")
detect("batches/batch_and_smells_version_based.json", "version_based")
