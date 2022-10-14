from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import sqlite3
import sys

#Базовое окно с происшествиями
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

#Окно с фоткой графика/варнинга
class ImageForm(QMainWindow):
    def __init__(self, imagePath):
        super().__init__()
        self.path = os.path.dirname(__file__).replace("\\","/") + "/" +imagePath.replace('\\','/')
        print(self.path)
        self.imageLabel = QLabel(self)
        self.imageLabel.resize(1920,1080)
        self.CreateGraphic()
    def CreateGraphic(self):
        image = QImage(self.path)
        self.imageLabel.setPixmap(QPixmap.fromImage(image))

#Кнопка показывания фотографий графиков или варнингов
class ImageButton(QPushButton):
    def __init__(self, parentWindow, imagePath):
        super().__init__(parentWindow)
        self.table = parentWindow
        self.ImagePath = imagePath
        self.setText(imagePath.split('\\')[-1])
        self.clicked.connect(self.ShowImage)
    def ShowImage(self):
        self.window1 = ImageForm(self.ImagePath)
        self.window1.show()

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
            select Reports.Video_Path, Reports.ID from Reports
                left join Warnings on Warnings.Report_ID = Reports.ID
        """).fetchall()
        row = 0
        for elem in reportList:
            self.setRowCount(self.rowCount() + 1)
            print(f"\t{elem[0]}\t{elem[1]}")
            self.setItem(row, 0, QTableWidgetItem(str(elem[0]).strip()))
            row += 1
            self.CreateReportButtons(elem[1], row)

    def CreateReportButtons(self, currentID, currentRow):
        imagePathList = self.cursor.execute(f"""
            select * from Reports
                where ID = {currentID}
            """).fetchall()
        imageButtons = []
        warningButtons = []

        for elem in imagePathList:
            i = 0
            warningButtons.append(WarningButton(self.parentWindow, currentID))
            warningButtons[i].resize(100, 25)
            warningButtons[i].move(220 + 105 * i, 10 + 30 * currentRow)
            for current in elem:
                if type(current) is int:
                    continue
                imageButtons.append(ImageButton(self.parentWindow, str(current).strip()))
                imageButtons[i].resize(100, 25)
                imageButtons[i].move(110 + 105 * (i + 2), 10 + 30 * currentRow)
                i += 1
        self.resizeColumnsToContents()

#Таблица с варнингами
class WarningTable(QTableWidget):
    def __init__(self, reportID):
        super().__init__()
        self.reportID = reportID
        self.setGeometry(10, 10, 200, 300)
        self.setRowCount(0)
        self.setColumnCount(4)
        self.verticalHeader()
        self.setHorizontalHeaderLabels([
            'ReportID',
            'Object_ID',
            'EventDescription',
            'FramePath'
            ])
        self.db = sqlite3.connect("reports.db")
        self.cursor = self.db.cursor()
        self.CreateReportList()
        self.setEditTriggers(QTableWidget.NoEditTriggers)

    def CreateReportList(self):
        reportList = self.cursor.execute(f"""
            select Warnings.Report_ID, Warnings.Object_ID, Events.Description, Warnings.Frame_Path from Reports
                left join Warnings on Warnings.Report_ID = Reports.ID
                left join Events on Warnings.Event_ID = Events.ID
            where Warnings.Report_ID = {self.reportID}
        """).fetchall()
        row = 0
        for elem in reportList:
            column = 0
            self.setRowCount(self.rowCount() + 1)
            for t in elem:
                self.setItem(row, column, QTableWidgetItem(str(t).strip()))
                column += 1
            row += 1
            self.CreateWarningButtons(elem[0], row)

    def CreateWarningButtons(self, currentID, currentRow):
        warningList = self.cursor.execute(f"""
            select * from Warnings
                where ID = {currentID}
            """).fetchall()
        imageButtons = []
        i = 0
        for elem in warningList:
            imageButtons.append(ImageButton(self, elem[4]))
            imageButtons[i].resize(100, 25)
            imageButtons[i].move(550 + 105 * i, 30 * currentRow)
            i += 1
        self.resizeColumnsToContents()

#Кнопка-хуёпка для варнинга-хуярнинга
class WarningButton(QPushButton):
    def __init__(self, parentWindow, ReportID):
        super().__init__(parentWindow)
        self.parentWindow = parentWindow
        self.RepordID = ReportID
        self.setText("Show warnings")
        self.clicked.connect(self.ShowWarningWindow)
    def ShowWarningWindow(self):
        self.window1 = WarningTable(self.RepordID)
        self.window1.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.exit(app.exec_())