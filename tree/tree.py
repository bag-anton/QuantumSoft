from typing import Optional, Tuple
from uuid import uuid4

from anytree import search

from tree.node import Node


class Tree:
    def __init__(self):
        self.tree = Node(1, 'root')

    def reset(self):
        self.__init__()

    def delete_node(self, node_id: int):
        node = self.get_node_by_id(node_id)
        node.mark_as_deleted()
        for child in node.children:
            self.delete_node(child.id)

    def create_node(
        self,
        parent_id: Optional[int],
        value: str,
        node_id: int = None,
        children: Tuple[Node] = tuple(),
        is_deleted: bool = False,
    ):
        node_id = node_id if node_id else uuid4().int
        parent_node = self.get_node_by_id(parent_id)
        parent_node = parent_node if parent_node else self.tree
        if not parent_node.is_deleted:
            Node(
                node_id,
                value=value,
                parent_id=parent_id,
                parent=parent_node,
                children=children,
                is_deleted=is_deleted,
            )

    def get_node_by_id(self, node_id: int) -> Node:
        return search.find(self.tree, lambda node: node.id == node_id)
