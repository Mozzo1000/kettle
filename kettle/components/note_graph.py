import random
from PyQt5.QtWidgets import QDockWidget, QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsLineItem, \
    QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QLineF, QRectF


class NotesGraph(QDockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Notes graph')
        self.setMinimumHeight(400)
        self.zoom = 0
        self.scene = QGraphicsScene()

        self.brush = QBrush(QColor(133, 63, 191))
        self.pen = QPen(Qt.red)

        self.graphic_view = QGraphicsView(self.scene, self)
        self.graphic_view.setGeometry(0, 0, self.size().width(), self.size().height())
        self.graphic_view.setDragMode(self.graphic_view.ScrollHandDrag)

        self.setWidget(self.graphic_view)

    def mouseDoubleClickEvent(self, event):
        node = Node('Document 1')
        node2 = Node('Document 2')
        node3 = Node('Document 3')
        edge = Edge(node, node2)
        edge2 = Edge(node, node3)
        self.scene.addItem(edge)
        self.scene.addItem(edge2)
        self.scene.addItem(node)
        self.scene.addItem(node2)
        self.scene.addItem(node3)


class Node(QGraphicsEllipseItem):
    def __init__(self, name, rect=QRectF(0, 0, 20, 20), parent=None):
        QGraphicsEllipseItem.__init__(self, rect, parent)
        self.edges = []
        self.setZValue(2)
        self.brush_color = QColor(153, 153, 153)
        self.setBrush(self.brush_color)
        self.setPen(QPen(Qt.NoPen))
        self.setFlags(QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemIsSelectable |
                      QGraphicsItem.ItemSendsGeometryChanges)
        self.text = QGraphicsTextItem(name)
        self.text.setDefaultTextColor(self.brush_color)
        self.text.setPos(0.0 / self.text.textWidth(), -20.0)
        self.text.setParentItem(self)

    def addEdge(self, edge):
        self.edges.append(edge)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange:
            self.setBrush(QColor("#1976D2") if value else self.brush_color)
            self.text.setDefaultTextColor(QColor("#1976D2") if value else self.brush_color)
            for i in range(len(self.edges)):
                self.edges[i].focus() if value else self.edges[i].defocus()

        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edges:
                edge.adjust()

        return QGraphicsItem.itemChange(self, change, value)


class Edge(QGraphicsLineItem):
    def __init__(self, source, dest, parent=None):
        QGraphicsLineItem.__init__(self, parent)
        self.source = source
        self.dest = dest
        self.source.addEdge(self)
        self.dest.addEdge(self)
        self.setPen(QPen(Qt.red, 1.75))
        self.adjust()

    def defocus(self):
        self.setPen(QPen(Qt.red, 1.75))

    def focus(self):
        self.setPen(QPen(QColor("#1976D2"), 1.75))

    def adjust(self):
        self.prepareGeometryChange()
        center = int(self.dest.rect().width() / 2)
        self.setLine(QLineF(self.dest.pos().x() + center, self.dest.pos().y() + center,
                            self.source.pos().x() + center, self.source.pos().y() + center))