from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QAction, \
    qApp, QFileDialog
from PyQt5 import QtWidgets, QtCore
import os
import threading
import subprocess

class QImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.printer = QPrinter()
        self.scaleFactor = 0.0
        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)
        self.setCentralWidget(self.scrollArea)
        self.createActions()
        self.CreateUI()
        self.setWindowTitle("Image Viewer")
        self.resize(800, 600)

    #Создание кнопок взаимодействия
    def CreateUI(self):
        _translate = QtCore.QCoreApplication.translate

        self.loadFileButton = QtWidgets.QPushButton(self)
        self.loadFileButton.setText(_translate("Form", "Открыть видео"))
        self.loadFileButton.clicked.connect(self.RunCommand)
        self.loadFileButton.move(0,0)

        self.showGraphicButton = QtWidgets.QPushButton(self)
        self.showGraphicButton.setText(_translate("Form", "Показать график"))
        self.showGraphicButton.clicked.connect(self.ShowGraphic)
        self.showGraphicButton.move(0,30)

    #Выбор видоса и запуск нейронки
    def RunCommand(self):
        filename = QFileDialog.getOpenFileName()
        path = f"data\\video\\{filename[0].split('/')[-1]}"
        print(">>Selected file name: "+path)
        # Создать папку
        folderName = f"example{len(next(os.walk('runs/track'))[1]) + 1}"
        os.popen(f"mkdir \\runs\\track\\{folderName}")
        project_path = f"{os.path.dirname(__file__)}\\runs\\track\\{folderName}"



        process = []

        # Прогон нейронки и создание трёх подпапок
        print(">>Neural network is running!")
        currentCommand = "python track.py --yolo-weights best_DIMA_200m.pt --strong-sort-weights osnet_x0_25_msmt17.pt --img 640 --source " + path + " --save-txt --save-conf --project " + project_path + " --save-vid --classes 0"
        print(">>Current command: " + currentCommand)
        t1 = subprocess.Popen(currentCommand)
        
        currentCommand = "python track.py --yolo-weights best_DIMA_200m.pt --strong-sort-weights osnet_x0_25_msmt17.pt --img 640 --source " + path + " --save-txt --save-conf --project " + project_path + " --save-vid --classes 1"
        print(">>Current command: " + currentCommand)
        t2 = subprocess.Popen(currentCommand)

        currentCommand = "python track.py --yolo-weights best_DIMA_200m.pt --strong-sort-weights osnet_x0_25_msmt17.pt --img 640 --source " + path + " --save-txt --save-conf --project " + project_path + " --save-vid --classes 2"
        print(">>Current command: " + currentCommand)
        t3 = subprocess.Popen(currentCommand)

        process.append(t1)
        process.append(t2)
        process.append(t3)


        for i in process:
            if i.wait() != 0:
                print('\t \t Идет распознование')


        currentCommand_script = "python script.py"
        os.popen(currentCommand_script)

    #Посмотреть график
    def ShowGraphic(self):
        foldersCount = len(next(os.walk('runs/track'))[1])
        fileName = os.path.dirname(__file__).replace("\\","/") + "/runs/track/exp"+str(foldersCount)+"/tracks/heatmap.png"
        print(fileName)
        if fileName:
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return
            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.scaleFactor = 1.0
            self.scrollArea.setVisible(True)
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()
            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()


    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())
    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())
        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)
        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)
    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value() + ((factor - 1) * scrollBar.pageStep() / 2)))
    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())
    def zoomIn(self):
        self.scaleImage(1.25)
    def zoomOut(self):
        self.scaleImage(0.8)
    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0
    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()
        self.updateActions()
    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.ShowGraphic)
        self.printAct = QAction("&Print...", self, shortcut="Ctrl+P", enabled=False, triggered=self.print_)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)
        self.aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    imageViewer = QImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())