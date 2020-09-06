import random
import os
from PyQt5.QtWidgets import QDockWidget, QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsLineItem, \
    QGraphicsEllipseItem, QGraphicsTextItem, QLabel, QMessageBox, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QLineF, QRectF
from services.backlink_indexer import BacklinkIndexer


class NotesGraph(QDockWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
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

        node_list = []
        link_index = BacklinkIndexer(parent.project_folder)

        if not os.path.isdir(os.path.join(parent.project_folder, '.notes')):
            label = QGraphicsTextItem('Current project is not a note project')
            self.scene.addItem(label)
        else:
            for files in os.listdir(parent.project_folder):
                if not files.startswith('.'):
                    node = Node(os.path.basename(os.path.normpath(files)))
                    link_index.add(files, node)
                    node.set_screen(parent)
                    node_list.append(node)
                    self.scene.addItem(node)

            for key in link_index.get_links():
                for i2 in link_index.get_links()[key]:
                    for i in node_list:
                        if i.text.toPlainText() == i2:
                            edge = Edge(key, i)
                            self.scene.addItem(edge)
        info_text_title = QGraphicsTextItem("Information")
        info_text_title.setFont(QFont("", weight=QFont.Bold))
        info_text = QGraphicsTextItem(f'Files: {len(node_list)}\n'
                                      f'Links: {len(link_index.get_links())}')
        info_text.setPos(0, 15)
        self.scene.addItem(info_text_title)
        self.scene.addItem(info_text)





class Node(QGraphicsEllipseItem):
    def __init__(self, name, rect=QRectF(0, 0, 20, 20), parent=None):
        QGraphicsEllipseItem.__init__(self, rect, parent)
        self.setX(random.randrange(0, 1000, 1))
        self.setY(random.randrange(0, 300, 1))
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
        self.text.setPos(-float(len(self.text.toPlainText())), -20.0)
        self.text.setParentItem(self)

        self.screen = ''

    def set_screen(self, screen):
        self.screen = screen

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

    def mouseDoubleClickEvent(self, event):
        try:
            file = open(os.path.join(self.screen.project_folder, self.text.toPlainText()), 'r', encoding='utf-8', errors='ignore')

            with file:
                text = file.read()
                self.screen.new_document(title=self.text.toPlainText())
                self.screen.current_editor.setPlainText(text)
                self.screen.current_editor.set_change_name(self.screen.tab_widget, False)
        except FileNotFoundError as error:
            QMessageBox.question(self.screen, 'Error', 'Error occured : ' + str(error), QMessageBox.Close)


class Edge(QGraphicsLineItem):
    def __init__(self, source, dest, parent=None):
        QGraphicsLineItem.__init__(self, parent)
        self.source = source
        self.dest = dest
        self.source.addEdge(self)
        self.dest.addEdge(self)
        self.line_color = QColor(153, 153, 153)
        self.line_color.setAlpha(40)
        self.setPen(QPen(self.line_color, 1.75))
        self.adjust()

    def defocus(self):
        self.setPen(QPen(self.line_color, 1.75))

    def focus(self):
        self.setPen(QPen(QColor("#1976D2"), 1.75))

    def adjust(self):
        self.prepareGeometryChange()
        center = int(self.dest.rect().width() / 2)
        self.setLine(QLineF(self.dest.pos().x() + center, self.dest.pos().y() + center,
                            self.source.pos().x() + center, self.source.pos().y() + center))