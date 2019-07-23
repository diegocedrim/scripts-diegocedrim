import io


class Node(object):
    COUNTER = 1

    def __init__(self, name, project):
        self.name = name
        self.children = {}
        self.classification = {}
        self.considered_batches = set()
        self.number = Node.COUNTER
        self.project = project
        Node.COUNTER += 1

    def get_child(self, name, project):
        if name in self.children:
            return self.children[name]
        node = Node(name, project)
        self.children[name] = node
        return node

    def add_classification(self, batch_dict):
        batch_id = batch_dict["hash_id"]
        if batch_id in self.considered_batches:
            return

        batch_class = batch_dict["classification"]
        batch_type = batch_dict["type"]

        self.considered_batches.add(batch_id)
        categories = self.classification.get(batch_type, {})
        categories[batch_class] = categories.get(batch_class, 0) + 1
        self.classification[batch_type] = categories


class Tree(object):
    def __init__(self, max_level=3, all_levels=False):
        self.root = Node("all", None)
        self.max_level = max_level
        self.all_levels = all_levels

    def node_names_generator(self, element, project):
        tokens = element.split(".")
        tokens = [project] + tokens
        for token in tokens:
            yield token

    def add_batch(self, batch, element, project):
        node = self.root
        node.add_classification(batch)
        level = 1
        for name_part in self.node_names_generator(element, project):
            if not self.all_levels and level >= self.max_level:
                return
            node = node.get_child(name_part, project)
            node.add_classification(batch)
            level += 1

    def print_node(self, node, level):
        print "  "*level,node.name, node.classification
        for child in node.children.values():
            self.print_node(child, level + 1)

    def print_tree(self, type):
        self.print_node(self.root, 0)


class TreeHTMLExporter(object):
    def __init__(self, filename, tree, heuristic):
        self.filename = filename
        self.tree = tree
        self.heuristic = heuristic

    def __node_html(self, parent, node, heuristic, f):
        data = {
            "number": node.number,
            "parent_number": parent.number if parent is not None else None,
            "name": node.name,
            "positive": node.classification.get(heuristic, {}).get("positive", 0),
            "neutral": node.classification.get(heuristic, {}).get("neutral", 0),
            "negative": node.classification.get(heuristic, {}).get("negative", 0)
        }

        keys = ["positive", "negative"]
        max_val = max([data[key] for key in keys])
        for key in keys:
            if data[key] == max_val:
                data[key] = "<b>" + str(data[key]) + "</b>"

        if parent:
            dom = """
                   <tr class="treegrid-%(number)s treegrid-parent-%(parent_number)s">
                     <td>%(name)s</td>
                     <td>%(positive)s</td>
                     <td>%(neutral)s</td>
                     <td>%(negative)s</td>
                   </tr>
               """
        else:
            dom = """
                  <tr class="treegrid-%(number)s">
                    <td>%(name)s</td>
                    <td>%(positive)s</td>
                    <td>%(neutral)s</td>
                    <td>%(negative)s</td>
                  </tr>
              """

        f.write(unicode(dom % data))

        for key, child in sorted(node.children.items()):
            self.__node_html(node, child, heuristic, f)

    def export(self):
        with io.open(self.filename, "w", encoding="utf8") as f, open("header.txt") as h, open("footer.txt") as ft:
            f.write(unicode(h.read()))
            self.__node_html(None, self.tree.root, self.heuristic, f)
            f.write(unicode(ft.read()))


class TreeSQLExporter(object):
    def __init__(self, filename, tree):
        self.filename = filename
        self.tree = tree

    def visit(self, parent, node, out):
        data = {
            "number": node.number,
            "parent_number": parent.number if parent is not None else None,
            "name": node.name,
            "positive": node.classification.get(heuristic, {}).get("positive", 0),
            "neutral": node.classification.get(heuristic, {}).get("neutral", 0),
            "negative": node.classification.get(heuristic, {}).get("negative", 0)
        }

        keys = ["positive", "negative"]
        max_val = max([data[key] for key in keys])
        for key in keys:
            if data[key] == max_val:
                data[key] = "<b>" + str(data[key]) + "</b>"

        if parent:
            dom = """
                   <tr class="treegrid-%(number)s treegrid-parent-%(parent_number)s">
                     <td>%(name)s</td>
                     <td>%(positive)s</td>
                     <td>%(neutral)s</td>
                     <td>%(negative)s</td>
                   </tr>
               """
        else:
            dom = """
                  <tr class="treegrid-%(number)s">
                    <td>%(name)s</td>
                    <td>%(positive)s</td>
                    <td>%(neutral)s</td>
                    <td>%(negative)s</td>
                  </tr>
              """

        f.write(unicode(dom % data))

        for key, child in sorted(node.children.items()):
            self.__node_html(node, child, heuristic, f)

    def export(self):
        with io.open(self.filename, "w", encoding="utf8") as out:
            self.visit(None, self.tree.root, out)
