from uuid import uuid4

from tree.node import Node


def generate_default_tree(root):
    node1 = Node(uuid4().int, 'node1', parent=root, parent_id=root.id)
    node2 = Node(uuid4().int, 'node2', parent=node1, parent_id=node1.id)
    node3 = Node(uuid4().int, 'node3', parent=node2, parent_id=node2.id)
    node4 = Node(uuid4().int, 'node4', parent=node3, parent_id=node3.id)
    node5 = Node(uuid4().int, 'node5', parent=node4, parent_id=node4.id)
    node6 = Node(uuid4().int, 'node6', parent=node1, parent_id=node1.id)
    node7 = Node(uuid4().int, 'node7', parent=node6, parent_id=node6.id)
    node8 = Node(uuid4().int, 'node8', parent=node7, parent_id=node7.id)
    node9 = Node(uuid4().int, 'node9', parent=node8, parent_id=node8.id)
    node10 = Node(uuid4().int, 'node10', parent=node9, parent_id=node9.id)
    return root
