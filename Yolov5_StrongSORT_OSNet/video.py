from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import sqlite3
import sys

#Окно с графиком
class GraphicForm(QMainWindow):
    def __init__(self, imagePath):
        super().__init__()
        self.path = os.path.dirname(__file__).replace("\\","/") + "/" +imagePath.replace('\\','/')
        self.imageLabel = QLabel(self)
        self.imageLabel.resize(1920,1080)
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
    def ShowImage(self):
        self.window1 = GraphicForm(self.ImagePath)
        self.window1.show()

#Окно с происшествиями
class VideoForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1300, 800)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.tb = ReportTable(self)
        self.setWindowTitle("Детектор")

#Таблица с происшествиями
class ReportTable(QTableWidget):
        def __init__(self, parentWindow):
            self.parentWindow = parentWindow
            super().__init__(parentWindow)
            self.setGeometry(10, 10, 200, 300)
            self.setRowCount(0)
            self.setColumnCount(1)
            self.verticalHeader()
            self.setHorizontalHeaderLabels([
                'ReportID'
                ])

            self.db = sqlite3.connect("reports.db")
            self.cursor = self.db.cursor()
            self.CreateReportList()
            self.setEditTriggers(QTableWidget.NoEditTriggers)

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
                    imageButtons.append(ReportButton(self.parentWindow, str(current).strip()))
                    imageButtons[i].resize(100, 25)
                    imageButtons[i].move(110 + 105 * (i + 1), 10 + 30 * j)
                    i += 1
            self.resizeColumnsToContents() 
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.exit(app.exec_())