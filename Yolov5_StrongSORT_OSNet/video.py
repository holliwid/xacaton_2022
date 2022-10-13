from msilib.schema import CreateFolder
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QAction, \
    qApp, QFileDialog
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import subprocess

#Окно с графиком
class Form(QMainWindow):
    def __init__(self, imagePath):
        super().__init__()
        #self.setGeometry(10, 10, 1500, 300)
        self.path = os.path.dirname(__file__).replace("\\","/") + "/" +imagePath.replace('\\','/')
        self.imageLabel = QLabel(self)
        self.imageLabel.resize(1920,1080)
        #self.imageLabel.move(0,0)
        self.CreateGraphic()
    def CreateGraphic(self):
        image = QImage(self.path)
        self.imageLabel.setPixmap(QPixmap.fromImage(image))

#Кнопка показывания кнопок из /Graphics/
class ReportButton(QPushButton):
    def __init__(self, table, imagePath):
        super().__init__(table)
        self.ImagePath = imagePath
        self.setText(imagePath.split('\\')[-1])
        self.clicked.connect(self.ShowImage)
        self.table = table
    #Вернуть фотку из /Graphics/
    def ShowImage(self):
        self.window1 = Form(self.ImagePath)
        self.window1.show()

class Form_video(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1300, 800)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.CreateUI()
        self.setWindowTitle("Детектор")

    #Создание интерфейса взаимодействия
    def CreateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.tb = Tb(self)

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
        currentCommand = "python track.py --yolo-weights best_DIMA_200m.pt --strong-sort-weights osnet_x0_25_msmt17.pt --img 640 --source " + path + " --save-txt --save-conf --project " + project_path + " --save-vid --classes 0"
        print(">>Current command: " + currentCommand)
        t1 = subprocess.Popen(currentCommand, shell=True)
        
        currentCommand = "python track.py --yolo-weights best_DIMA_200m.pt --strong-sort-weights osnet_x0_25_msmt17.pt --img 640 --source " + path + " --save-txt --save-conf --project " + project_path + " --save-vid --classes 1"
        print(">>Current command: " + currentCommand)
        t2 = subprocess.Popen(currentCommand, shell=True)

        currentCommand = "python track.py --yolo-weights best_DIMA_200m.pt --strong-sort-weights osnet_x0_25_msmt17.pt --img 640 --source " + path + " --save-txt --save-conf --project " + project_path + " --save-vid --classes 2"
        print(">>Current command: " + currentCommand)
        t3 = subprocess.Popen(currentCommand, shell=True)

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

class Tb(QTableWidget):
        def __init__(self, wg):
            self.wg = wg  # запомнить окно, в котором эта таблица показывается
            super().__init__(wg)
            self.setGeometry(10, 10, 1500, 300)
            self.setColumnCount(4)
            self.verticalHeader().hide();
            self.updt() # обновить таблицу
            self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
            
        #Создание таблицы репортов
        def CreateReportList(self):
            reportList = self.cursor.execute("""
                select Reports.Video_Path, Reports.ID from Warnings
                    left join Reports on Warnings.Report_ID = Reports.ID
            """).fetchall()
            row = 0
            for elem in reportList:
                self.setRowCount(self.rowCount() + 1)
                column = 0
                self.setItem(row, column, QTableWidgetItem(str(elem[0]).strip()))
                column += 1
                self.CreateGraphicsButton(elem[1])
                #for t in elem:
                    #self.setItem(row, column, QTableWidgetItem(str(t).strip()))
                    #column += 1
                    #self.CreateGraphicsButton()

        #Создание кнопок для отображения графиков
        def CreateGraphicsButton(self, currentID):
            imagePathList = self.cursor.execute(f"""
                select * from Reports
                    where ID = {currentID}
                """).fetchall()
            imageButtons = []
            j = 0
            for elem in imagePathList:
                i = 0
                j += 1
                for current in elem:
                    if type(current) is int:
                        continue
                    imageButtons.append(ReportButton(self, str(current).strip()))
                    imageButtons[i].resize(100, 25)
                    imageButtons[i].move(120 * (i + 1), 30 * j)
                    i += 1
            self.resizeColumnsToContents() 



        # обновление таблицы
        def updt(self):
            self.clear()
            self.setRowCount(0)
            self.setColumnCount(1)
            self.setHorizontalHeaderLabels([
                'ReportID'
                ])
            self.setCellWidget(0,0, QPushButton())

            import sqlite3
            self.db = sqlite3.connect("reports.db")
            self.cursor = self.db.cursor()
            self.CreateReportList()
            
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    imageViewer = QImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())