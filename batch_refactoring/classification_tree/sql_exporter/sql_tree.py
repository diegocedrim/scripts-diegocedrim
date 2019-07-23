import io
import re


class Node(object):
    COUNTER = 1

    def __init__(self, name, project):
        self.name = name
        self.full_name = None
        self.children = {}
        self.classification = {}
        self.considered_batches = set()
        self.id = Node.COUNTER
        self.project = project
        Node.COUNTER += 1

    def classification_count(self, heuristic, clazz):
        categories = self.classification.get(heuristic, {})
        return categories.get(clazz, 0)

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
        self.batches = {}

    def node_names_generator(self, element, project):
        tokens = element.split(".")
        tokens = [project] + tokens
        for token in tokens:
            yield token

    def add_batch(self, batch, element, project):
        self.batches[batch["hash_id"]] = batch
        node = self.root
        node.add_classification(batch)
        level = 1
        for name_part in self.node_names_generator(element, project):
            if not self.all_levels and level >= self.max_level:
                return
            node = node.get_child(name_part, project)
            node.add_classification(batch)
            level += 1


class TreeSQLExporter(object):
    def __init__(self, filename, tree):
        self.filename = filename
        self.tree = tree
        self.batch_group_id = 1

    def clear(self, sql):
        return unicode(re.sub(r"\s+", " ", sql) + "\n")

    def export_batches_by_heuristic(self, node, heuristic, out):
        batch_ids = node.considered_batches
        group_id = self.batch_group_id
        self.batch_group_id += 1
        sql = """
            insert into batch_tree_batchgroup (
              id, 
              heuristic_id, 
              node_id,
              positive,
              negative,
              neutral
            ) values (
              %s, 
              (select id from batch_tree_synthesisheuristic where name = '%s'),
              %s,
              %s,
              %s,
              %s
            );
        """
        data = (
            group_id,
            heuristic,
            node.id,
            node.classification_count(heuristic, "positive"),
            node.classification_count(heuristic, "negative"),
            node.classification_count(heuristic, "neutral")
        )
        out.write(self.clear(sql % data))
        for batch_id in batch_ids:
            batch = self.tree.batches[batch_id]
            if batch["type"] == heuristic:
                sql = """
                    insert into batch_tree_batchgroup_batches (
                      batchgroup_id, 
                      batch_id
                    ) values (
                      %s,
                      %s
                    );
                """
                out.write(self.clear(sql % (group_id, batch_id)))

    def export_batches(self, node, out):
        self.export_batches_by_heuristic(node, "element-based", out)
        self.export_batches_by_heuristic(node, "version-based", out)
        self.export_batches_by_heuristic(node, "scope-based", out)

    def visit(self, parent, node, out):
        sql = """
            insert into batch_tree_node (
              id, 
              element_name, 
              project_id, 
              parent_id
            ) values (
              %(id)s,
              '%(name)s',
              (select id from batch_tree_project where name = '%(project_name)s'),
              %(parent_id)s
            );
        """
        data = {
            "id": node.id,
            "name": node.name,
            "project_name": node.project if node.project else 'null',
            "parent_id": parent.id if parent else 'null'
        }
        out.write(self.clear(sql % data))
        self.export_batches(node, out)

        for key, child in sorted(node.children.items()):
            self.visit(node, child, out)

    def export(self):
        with io.open(self.filename, "w", encoding="utf8") as out:
            out.write(u"delete from batch_tree_batchgroup_batches;\n")
            out.write(u"delete from batch_tree_batchgroup;\n")
            out.write(u"delete from batch_tree_node;\n")
            self.visit(None, self.tree.root, out)
