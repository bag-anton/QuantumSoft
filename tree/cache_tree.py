from anytree import search

from .decorators import singleton
from .node import Node
from .tree import Tree


@singleton
class CachedTree(Tree):
    def __init__(self):
        super().__init__()

    def find_children(self, parent_id):
        return search.findall(self.tree, lambda node: node.parent_id == parent_id)

    def find_parent(self, node_id):
        search.findall(self.tree, lambda node: node.id == node_id)

    def add_node(self, node: Node):
        children = self.find_children(node.id)
        self.create_node(node.parent_id, node.value, node.id, children)
