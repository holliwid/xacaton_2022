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
import threading
import subprocess

class Form_video(QMainWindow):
    def __init__(self):
        super().__init__()
        
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



        process = []

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
            self.setGeometry(10, 40, 1100, 500)
            self.setColumnCount(4)
            self.verticalHeader().hide();
            self.updt() # обновить таблицу
            # self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
            # self.cellClicked.connect(self.cellClick)  # установить обработчик щелча мыши в таблице

    # обновление таблицы
        def updt(self):
            self.clear()
            self.setRowCount(0);
            self.setHorizontalHeaderLabels(['ID', 'path name', 'Графики', 'Проишествия']) # заголовки столцов
            # self.wg.cur.execute("здесь запрос нужен")
            # rows = self.wg.cur.fetchall()
            # print(rows)
            # i = 0
            # for elem in rows:
            #     self.setRowCount(self.rowCount() + 1)
            #     j = 0
            #     for t in elem: # заполняем внутри строки
            #         self.setItem(i, j, QTableWidgetItem(str(t).strip()))
            #         j += 1
            #     i += 1
            # self.resizeColumnsToContents() 

    # обработка щелчка мыши по таблице
        def cellClick(self, row, col): # row - номер строки, col - номер столбца
            self.wg.idp.setText(self.item(row, 0).text())
            self.wg.type.setCurrentText(self.item(row, 1).text().strip())
            self.wg.img.setText(self.item(row, 2).text().strip())
            self.wg.mark.setText(self.item(row, 3).text())
            self.wg.num.setText(self.item(row, 4).text().strip())
            self.wg.length.setText(self.item(row, 5).text())
            self.wg.width.setText(self.item(row, 6).text())
            self.wg.height.setText(self.item(row, 7).text())
            self.wg.year_of_release.setText(self.item(row, 8).text())
            self.wg.load_capacity.setText(self.item(row, 9).text())
            self.wg.number_of_seats.setText(self.item(row, 10).text())
            self.wg.ctc.setText(self.item(row, 11).text())
            self.wg.under_repair.setChecked(bool(self.item(row, 12).text() == 'True'))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    imageViewer = QImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())