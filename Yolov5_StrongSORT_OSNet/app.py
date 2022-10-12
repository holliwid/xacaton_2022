import video
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QAction, \
    qApp, QFileDialog
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import subprocess

class QImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.w = None

        # параметры окна
        self.resize(1300, 800)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.CreateUI()
        self.setWindowTitle("Детектор")

    #Создание кнопок взаимодействия
    def CreateUI(self):
        _translate = QtCore.QCoreApplication.translate

        self.loadFileButton = QtWidgets.QPushButton(self)
        self.loadFileButton.resize(150, 40)
        self.loadFileButton.setText(_translate("Form", "Открыть видео"))
        self.loadFileButton.clicked.connect(self.RunCommand)
        self.loadFileButton.move(0,0)

        # self.showGraphicButton = QtWidgets.QPushButton(self)
        # self.loadFileButton.resize(150, 40)
        # self.showGraphicButton.setText(_translate("Form", "Показать график"))
        # self.showGraphicButton.clicked.connect(self.ShowGraphic)
        # self.showGraphicButton.move(0,30)

        self.openVideos = QtWidgets.QPushButton(self)
        self.openVideos.resize(150, 40)
        self.openVideos.setText(_translate("Form", "Открыть таблицу"))
        self.openVideos.clicked.connect(self.OpenVideo)
        self.openVideos.move(100,100)

    #Выбор видоса и запуск нейронки
    def RunCommand(self):
        filename = QFileDialog.getOpenFileName()
        path = f"./data/video/{filename[0].split('/')[-1]}"
        print(">>Selected file name: "+path)
        # Создать папку
        folderName = f"example{len(next(os.walk('runs/track'))[1]) + 1}"
        os.popen(f"mkdir ./runs/track/{folderName}")

        import pathlib
        path_1 = str(pathlib.Path(__file__).parent.resolve())
        project_path = f"{path_1}/runs/track/{folderName}"
        path = f"{path_1}/data/video/{filename[0].split('/')[-1]}"

        # Прогон нейронки и создание трёх подпапок
        print(">>Neural network is running!")
        currentCommand = "python track.py --yolo-weights best_DIMA_200m.pt --strong-sort-weights osnet_x0_25_msmt17.pt --img 640 --source " + path + " --save-txt --save-conf --project " + project_path + " --save-vid --name human --classes 0"
        print(">>Current command: " + currentCommand)
        t1 = subprocess.Popen(currentCommand )
        
        currentCommand = "python track.py --yolo-weights best_DIMA_200m.pt --strong-sort-weights osnet_x0_25_msmt17.pt --img 640 --source " + path + " --save-txt --save-conf --project " + project_path + " --save-vid --name jacket --classes 1"
        print(">>Current command: " + currentCommand)
        t2 = subprocess.Popen(currentCommand)

        currentCommand = "python track.py --yolo-weights best_DIMA_200m.pt --strong-sort-weights osnet_x0_25_msmt17.pt --img 640 --source " + path + " --save-txt --save-conf --project " + project_path + " --save-vid --name pants --classes 2"
        print(">>Current command: " + currentCommand)
        t3 = subprocess.Popen(currentCommand)

        process = []
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

    @pyqtSlot()
    def OpenVideo(self):
        self.window().close()
        if self.w is None:
            self.w = video.Form_video()
            self.w.show()
        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    imageViewer = QImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())