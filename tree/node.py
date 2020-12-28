from anytree import NodeMixin


class Node(NodeMixin):
    def __init__(
        self,
        id: int,
        value: str,
        parent_id: int = None,
        parent=None,
        children=tuple(),
        is_deleted=False,
    ):
        super(Node, self).__init__()
        self.id: int = id
        self.parent_id: int = parent_id if parent_id else None
        self.value: str = value
        self.parent = parent
        self.children = children
        self.is_deleted: bool = is_deleted

    def change_node_value(self, value: str):
        if self.is_deleted is True:
            return
        self.value = value

    def mark_as_deleted(self):
        self.is_deleted = True
