from tree.decorators import singleton
from tree.tree import Tree
from tree.utils import generate_default_tree


@singleton
class DBTree(Tree):
    def __init__(self):
        super().__init__()
        self.tree = generate_default_tree(self.tree)
