
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from grailkit.dna import DNAFile, DNAError
from grailkit.ui import GApplication


def rchop(thestring, ending):
    if thestring.endswith(ending):
        return thestring[:-len(ending)]

    return thestring


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.dna = None
        self.add_dialog = AddDialog()

        self._init_ui()

    def _init_ui(self):

        self._ui_btn_open = QAction("Open", self)
        self._ui_btn_open.triggered.connect(self.open_file)

        self._ui_btn_create = QAction("Create", self)
        self._ui_btn_create.triggered.connect(self.create_file)

        self._ui_toolbar = QToolBar()
        self._ui_toolbar.setMovable(False)
        self._ui_toolbar.setFloatable(False)

        self._ui_toolbar.addAction(self._ui_btn_open)
        self._ui_toolbar.addAction(self._ui_btn_create)

        self.addToolBar(self._ui_toolbar)

        # left side

        self._ui_entities_list = QListWidget()
        self._ui_entities_list.setStyleSheet("QListWidget {border: none;}")
        self._ui_entities_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self._ui_entities_list.setAttribute(Qt.WA_MacShowFocusRect, False)
        self._ui_entities_list.itemActivated.connect(self.entity_selected)
        self._ui_entities_list.itemClicked.connect(self.entity_selected)

        self._ui_btn_add = QAction("Add", self)
        self._ui_btn_add.triggered.connect(self.add_entity)

        self._ui_entities_toolbar = QToolBar()
        self._ui_entities_toolbar.addAction(self._ui_btn_add)

        self._ui_entities_layout = QVBoxLayout()
        self._ui_entities_layout.setContentsMargins(0, 0, 0, 0)
        self._ui_entities_layout.setSpacing(0)
        self._ui_entities_layout.addWidget(self._ui_entities_list)
        self._ui_entities_layout.addWidget(self._ui_entities_toolbar)

        self._ui_entities_panel = QWidget()
        self._ui_entities_panel.setLayout(self._ui_entities_layout)

        # right side
        self._ui_properties = QTableWidget()
        self._ui_properties.setShowGrid(False)
        self._ui_properties.setColumnCount(2)
        self._ui_properties.horizontalHeader().setVisible(True)
        self._ui_properties.horizontalHeader().setStretchLastSection(True)
        self._ui_properties.verticalHeader().setVisible(False)
        self._ui_properties.setHorizontalHeaderLabels(["Key", "Value"])
        self._ui_properties.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._ui_properties.setSelectionMode(QAbstractItemView.SingleSelection)
        self._ui_properties.setStyleSheet("QTableWidget {border: none;}")
        self._ui_properties.currentItemChanged.connect(self.property_changed)

        self._ui_btn_prop = QAction("Add", self)
        self._ui_btn_prop.triggered.connect(self.add_property)

        self._ui_properties_toolbar = QToolBar()
        self._ui_properties_toolbar.addAction(self._ui_btn_prop)

        self._ui_properties_layout = QVBoxLayout()
        self._ui_properties_layout.setContentsMargins(0, 0, 0, 0)
        self._ui_properties_layout.setSpacing(0)
        self._ui_properties_layout.addWidget(self._ui_properties)
        self._ui_properties_layout.addWidget(self._ui_properties_toolbar)

        self._ui_properties_panel = QWidget()
        self._ui_properties_panel.setLayout(self._ui_properties_layout)

        # main layout
        self._ui_splitter = QSplitter()
        self._ui_splitter.setHandleWidth(1)

        self._ui_splitter.addWidget(self._ui_entities_panel)
        self._ui_splitter.addWidget(self._ui_properties_panel)
        self._ui_splitter.setCollapsible(0, False)
        self._ui_splitter.setCollapsible(1, False)
        self._ui_splitter.setSizes([250, 250])

        self.setCentralWidget(self._ui_splitter)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.setWindowTitle("Grail DNA")
        self.setGeometry(100, 100, 600, 600)

    def _update_list(self):

        for entity in self.dna.entities():
            item = QListWidgetItem()
            item.setText("%d - %s" % (entity.id, entity.name))
            item.id = entity.id

            self._ui_entities_list.addItem(item)

    def _show_properties(self, entity_id):

        props = self.dna.properties(entity_id)

        entity = self.dna._entity(entity_id)
        entity_props = {}

        entity_props['@id'] = entity.id
        entity_props['@name'] = entity.name
        entity_props['@type'] = entity.type
        entity_props['@parent'] = entity.parent_id
        entity_props['@content'] = entity.content
        entity_props['@created'] = entity.created
        entity_props['@modified'] = entity.modified
        entity_props['@search'] = entity.search
        entity_props['@index'] = entity.index

        self._ui_properties.clearContents()
        self._ui_properties.setRowCount(len(props) + len(entity_props))

        index = 0

        for key in entity_props:
            self._ui_properties.setItem(index, 0, QTableWidgetItem(key))
            self._ui_properties.setItem(index, 1, QTableWidgetItem(str(entity_props[key])))
            index += 1

        for key in props:
            self._ui_properties.setItem(index, 0, QTableWidgetItem(key))
            self._ui_properties.setItem(index, 1, QTableWidgetItem(str(props[key])))
            index += 1

    def property_changed(self, item, other):
        print(item)

    def entity_selected(self, item):

        self._show_properties(item.id)

    def add_entity(self):

        self.add_dialog.show()

    def add_property(self):
        pass

    def open_file(self):

        path, ext = QFileDialog.getOpenFileName(self, "Open File...", "", "*")

        if not os.path.isfile(path):
            return

        self._open_dna(path, create=False)

    def create_file(self):

        path, ext = QFileDialog.getSaveFileName(self, "Save file", '', "*")
        file_path = rchop(path, '.grail') + '.grail'

        self._open_dna(file_path, True)

    def _open_dna(self, file_path, create=False):

        try:
            self.dna = DNAFile(file_path, create=create)

            self.setWindowTitle("DNA - %s" % (file_path.split('/')[-1],))
            self._update_list()
        except DNAError:
            QMessageBox.warning(self, "DNA", "Could not open file %s" % (file_path,))


class AddDialog(QDialog):

    def __init__(self, parent=None):
        super(AddDialog, self).__init__(parent)

        self._init_ui()

    def _init_ui(self):

        self.setWindowTitle("Add an entity")
        self.setGeometry(100, 100, 200, 300)


class Generate:

    def __init__(self):
        self.test_dir = "./"

        db_path = os.path.join(self.test_dir, 'entity.grail')
        dna_file = DNAFile(db_path, create=True)

        # settings
        settings = dna_file.create()
        settings.name = "settings"

        settings.set('display.background', '#000000')

        settings.set('display.text.align', 1)
        settings.set('display.text.valign', 1)
        settings.set('display.text.case', 'uppercase')

        settings.set('display.font.family', 'Helvetica')
        settings.set('display.font.size', '32pt')
        settings.set('display.font.weight', 'normal')
        settings.set('display.font.style', 'normal')
        settings.set('display.font.color', '#FFFFFF')

        settings.set('display.shadow.x', 0)
        settings.set('display.shadow.y', 2)
        settings.set('display.shadow.blur', 10)
        settings.set('display.shadow.color', '#000000')

        settings.set('display.padding.left', 10)
        settings.set('display.padding.right', 10)
        settings.set('display.padding.top', 10)
        settings.set('display.padding.bottom', 10)
        settings.set('display.padding.box', 10)

        settings.set('display.composition.x', 0)
        settings.set('display.composition.y', 0)
        settings.set('display.composition.width', 1920)
        settings.set('display.composition.height', 1080)

        settings.set('display.geometry.x', 1920)
        settings.set('display.geometry.y', 0)
        settings.set('display.geometry.width', 1920)
        settings.set('display.geometry.height', 1080)

        settings.set('display.disabled', False)
        settings.set('display.display', 'DISPLAY//2')
        settings.set('display.testcard', False)
        settings.set('display.fullscreen', True)
        settings.update()

        # project
        project = dna_file.create()
        project.name = "Grail Project"
        project.set('author', 'Alex Litvin')
        project.set('description', 'Simple Grail project for testing purposes')
        project.update()

        # cuelist
        for cuelist_index in range(5):
            cuelist = dna_file.create(parent=project.id)
            cuelist.name = "%d'st Cuelist" % (cuelist_index,)
            cuelist.set('color', '#FF0000')
            cuelist.set('description', 'Simple cuelist')
            cuelist.update()

            for cue_index in range(5):
                cue = dna_file.create(parent=cuelist.id)
                cue.name = "Cue %d in list %d" % (cue_index, cuelist_index)
                cue.set('color', '#00FF00')
                cue.set('continue', 0)
                cue.set('wait_pre', 100)
                cue.set('wait_post', 30)
                cue.update()

    def _print_childs(self, db, parent, indent=''):

        for entity in db.entities(filter_parent=parent):

            print('\n' + indent + '@', entity.id, entity.name, entity)

            properties = entity.properties()

            for key in properties:
                print(indent + "-", key, ':', properties[key])

            self._print_childs(db, entity.id, indent+'  ')

# test a dialog
if __name__ == '__main__':

    app = GApplication(sys.argv)
    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
