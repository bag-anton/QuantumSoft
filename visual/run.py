import requests
from PyQt5 import uic, QtWidgets, QtGui


Form, _ = uic.loadUiType("form.ui")

RESET_URL = "http://127.0.0.1:8000/reset"
CACHE_URL = "http://127.0.0.1:8000/cache"
DB_URL = "http://127.0.0.1:8000/db"


class MyQTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, value, is_deleted, id, parent_id):
        super().__init__()
        self.setText(0, value)
        self.is_deleted = is_deleted
        self.id = id
        self.parent_id = parent_id


class Ui(QtWidgets.QMainWindow, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.pushButton_6.clicked.connect(self.restart)
        self.pushButton.clicked.connect(self.get_item_from_db)
        self.pushButton_4.clicked.connect(self.change_node_value)
        self.pushButton_3.clicked.connect(self.delete_node)
        self.pushButton_2.clicked.connect(self.add_node)
        self.pushButton_5.clicked.connect(self.save)

    def save(self):
        db_tree = self.send_request("GET", DB_URL)
        self.fill_widget(self.treeWidget_2, db_tree)

    def add_node(self):
        parent_id = None
        index = self.treeWidget.selectedIndexes()[0] if len(self.treeWidget.selectedIndexes()) else None
        if index:
            node = self.treeWidget.itemFromIndex(index)
            parent_id = node.id
        value = self.textEdit.toPlainText()
        if not value:
            return
        body = {"parent_id": parent_id, "value": value}
        cache_tree = self.send_request("POST", CACHE_URL, body)
        self.fill_widget(self.treeWidget, cache_tree)

    def delete_node(self):
        index = self.treeWidget.selectedIndexes()[0] if len(self.treeWidget.selectedIndexes()) else None
        if index:
            node = self.treeWidget.itemFromIndex(index)
        else:
            return
        node.setForeground(0, QtGui.QBrush(QtGui.QColor("#FF0000")))
        body = {"node_id": node.id}
        cache_tree = self.send_request("DELETE", CACHE_URL, body)
        self.fill_widget(self.treeWidget, cache_tree)

    def change_node_value(self):
        index = self.treeWidget.selectedIndexes()[0] if len(self.treeWidget.selectedIndexes()) else None
        if index:
            node = self.treeWidget.itemFromIndex(index)
        else:
            return
        new_value = self.textEdit.toPlainText()
        body = {"node_id": node.id, "new_value": new_value}
        cache_tree = self.send_request("PUT", CACHE_URL, body)
        self.fill_widget(self.treeWidget, cache_tree)

    def get_item_from_db(self):
        index = self.treeWidget_2.selectedIndexes()[0] if len(self.treeWidget_2.selectedIndexes()) else None
        if index:
            node = self.treeWidget_2.itemFromIndex(index)
        else:
            return
        body = {"node_id": node.id}
        cache_tree = self.send_request("POST", DB_URL, body)
        self.fill_widget(self.treeWidget, cache_tree)

    @staticmethod
    def send_request(method: str, url: str, body: dict = None):
        response = requests.request(method=method, url=url, json=body).json()
        return response

    def restart(self):
        db_tree = self.reset_db()
        self.fill_widget(self.treeWidget_2, db_tree)
        self.fill_widget(self.treeWidget)

    def reset_db(self):
        response = self.send_request('GET', RESET_URL)
        return response

    def fill_item(self, item, value):
        item.setExpanded(True)
        node = MyQTreeItem(value["value"], value["is_deleted"],
                           value["id"], value['parent_id'])
        if value["is_deleted"]:
            node.setForeground(0, QtGui.QBrush(QtGui.QColor("#FF0000")))
        item.addChild(node)

        children = value.get('children', None)
        if children:
            for child in children:
                self.fill_item(node, child)

    def fill_widget(self, widget, value=None):
        widget.clear()
        if value:
            for node in value['children']:
                self.fill_item(widget.invisibleRootItem(), node)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()  # show window
    sys.exit(app.exec_())
