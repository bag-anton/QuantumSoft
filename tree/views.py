from anytree import PreOrderIter
from anytree.exporter import DictExporter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from tree.cache_tree import CachedTree
from tree.database_tree import DBTree
from tree.node import Node


class DBTreeView(APIView):
    def post(self, request: Request):
        """
        Copy node to cache
        :param request: {node_id}
        """
        db_tree = DBTree()
        cached_tree = CachedTree()
        exporter = DictExporter()

        if cached_tree.get_node_by_id(request.data['node_id']):
            result = exporter.export(cached_tree.tree)
            return Response(data=result)

        node = db_tree.get_node_by_id(request.data['node_id'])
        cached_tree.add_node(node)

        result = exporter.export(cached_tree.tree)
        return Response(data=result)

    def get(self, request):
        """
        Save changes
        """
        exporter = DictExporter()
        db_tree = DBTree()
        cached_tree = CachedTree()
        for node in PreOrderIter(cached_tree.tree):
            self.save(node, db_tree)
        result = exporter.export(db_tree.tree)
        return Response(data=result)

    def save(self, cached_node: Node, db_tree: DBTree):
        db_node = db_tree.get_node_by_id(cached_node.id)
        if db_node:
            db_node.value = cached_node.value
            if cached_node.is_deleted:
                db_tree.delete_node(db_node.id)
        else:
            db_tree.create_node(
                cached_node.parent_id,
                cached_node.value,
                cached_node.id,
                is_deleted=cached_node.is_deleted,
            )


class CachedTreeView(APIView):
    def post(self, request):
        """
        Create node in cache
        :param request: {parent_id: int, value: str}
        """
        cached_tree = CachedTree()
        cached_tree.create_node(
            parent_id=request.data['parent_id'], value=request.data['value']
        )

        exporter = DictExporter()
        return Response(data=exporter.export(cached_tree.tree))

    def delete(self, request):
        """
        Delete node from cache
        :param request: {node_id: int}
        """
        cached_tree = CachedTree()
        cached_tree.delete_node(request.data['node_id'])

        exporter = DictExporter()
        return Response(data=exporter.export(cached_tree.tree))

    def put(self, request):
        """
        Change value in node
        :param request: {node_id: int, new_value: str}
        """
        cached_tree = CachedTree()
        node = cached_tree.get_node_by_id(request.data['node_id'])
        node.change_node_value(request.data['new_value'])

        exporter = DictExporter()
        return Response(data=exporter.export(cached_tree.tree))


class ResetView(APIView):
    def get(self, request):
        db_tree = DBTree()
        db_tree.reset()
        CachedTree().reset()

        exporter = DictExporter()
        return Response(data=exporter.export(db_tree.tree))
