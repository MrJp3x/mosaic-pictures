import sys
import methods as meth
from PyQt5.QtWidgets import QTabWidget, QWidget, QFormLayout, QLineEdit, QHBoxLayout, QRadioButton, QLabel, QCheckBox, \
    QApplication, QFileDialog, QPushButton
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *


class tabDemo(QTabWidget):
    def __init__(self, parent=None):
        super(tabDemo, self).__init__(parent)

        self.movie_file_path = None
        self.setWindowTitle('..:: Mosaic Images ::..')
        self.setStyleSheet('background-color:#c0c0c0')
        self.setGeometry(100, 100, 400, 200)
        self.setFixedSize(400, 200)

        self.tab1 = QWidget()
        self.addTab(self.tab1, 'Mosaic Image')
        self.tab1UI()

    def tab1UI(self):
        layout = QFormLayout()
        self.mosaicWidth = QLineEdit()
        self.mosaicHeight = QLineEdit()
        layout.addRow('Mosaic Width', self.mosaicWidth)
        layout.addRow('Mosaic Height', self.mosaicHeight)

        btn = QPushButton(self, text='set file Path')
        layout.addRow('', btn)
        btn.clicked.connect(lambda: self.get_directory_path())
        self.setTabText(1, 'Mosaic Image')
        self.tab1.setLayout(layout)

        runBtn = QPushButton(self, text='Run')
        layout.addRow('', runBtn)
        runBtn.setGeometry(120, 140, 100, 26)
        runBtn.clicked.connect(self.mosaic_image_run)

    def mosaic_image_run(self):
        m = meth.mosaic(self.directory_Path, int(self.mosaicWidth.text()), int(self.mosaicHeight.text()))
        m.show_image()

    def _openFileNameDialog(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "..:: Select File ::..", "",
                                                  "All Files (*);;Jpg Files (*.jpg);;Png file (*.png)",
                                                  options=options)
        if fileName:
            return fileName

    def _openDirectoryDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = str(QFileDialog.getExistingDirectory(self, "..:: Select Directory ::.."))
        if fileName:
            return fileName

    def get_directory_path(self):
        self.directory_Path = self._openDirectoryDialog()

    def get_file_path(self):
        self.movie_file_path = self._openFileNameDialog()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = tabDemo()
    win.show()
    sys.exit(app.exec_())
