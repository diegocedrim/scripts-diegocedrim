from graphviz import Digraph
from colour import Color
import csv


class Interference(object):
    def __init__(self, batch, percentage):
        self.batch = batch
        self.perc = percentage


def load_patterns(filename):
    patterns = {}
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            smell = row["smell"]
            interference = Interference(row["batch"], row["percentage"])
            ints = patterns.get(smell, [])
            ints.append(interference)
            patterns[smell] = ints
    return patterns


def generate_dotfiles(intros, remvs, prefix=""):
    smells = set(intros.keys() + remvs.keys())
    for smell in smells:
        graph_attr = {"rankdir":"LR"}
        dot = Digraph(comment=smell, engine="dot", format="png", graph_attr=graph_attr)
        dot.attr("node", style='filled', fillcolor="grey", shape="box")
        dot.node(smell)

        if smell in intros:
            interferences = intros[smell]
            for intf in interferences:
                color = reds[int(intf.perc)].hex_l
                dot.attr("node", style='filled', fillcolor=color, shape="box")
                dot.node(intf.batch)
                dot.edge(intf.batch, smell, "%.2f" % (float(intf.perc)/100))

        if smell in remvs:
            interferences = remvs[smell]
            for intf in interferences:
                color = greens[int(intf.perc)].hex_l
                dot.attr("node", style='filled', fillcolor=color, shape="box")
                dot.node(intf.batch)
                dot.edge(smell, intf.batch, "%.2f" % (float(intf.perc)/100))

        dot.save("pictures/%s%s" % (prefix, smell.replace(" ", "")))
        dot.render(cleanup=False)


def generate_singledotfile(intros, remvs, prefix=""):
    smells = set(intros.keys() + remvs.keys())
    graph_attr = {"rankdir": "LR"}
    dot = Digraph(engine="dot", format="pdf", graph_attr=graph_attr)
    for smell in smells:
        dot.attr("node", style='filled', fillcolor="grey", shape="box")
        dot.node(smell)

        if smell in intros:
            interferences = intros[smell]
            for intf in interferences:
                color = reds[int(intf.perc)].hex_l
                dot.attr("node", style='filled', fillcolor=color, shape="box")
                seq = intf.batch + "+"
                dot.node(seq)
                dot.edge(seq, smell, "%.2f" % (float(intf.perc)/100))

        if smell in remvs:
            interferences = remvs[smell]
            for intf in interferences:
                color = greens[int(intf.perc)].hex_l
                dot.attr("node", style='filled', fillcolor=color, shape="box")
                seq = intf.batch + "-"
                dot.node(seq)
                dot.edge(smell, seq, "%.2f" % (float(intf.perc)/100))

    dot.save("pictures/%s" % prefix)
    dot.render(cleanup=False)

reds = list(Color("#FFFFFF").range_to(Color("#FF0000"),100))
greens = list(Color("#FFFFFF").range_to(Color("#00FF00"),100))
introductions = load_patterns("../summaries/element_based_introduced.csv")
removals = load_patterns("../summaries/element_based_removed.csv")
generate_singledotfile(introductions, removals, "eb_")











