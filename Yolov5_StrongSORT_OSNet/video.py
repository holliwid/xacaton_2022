from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import sqlite3
import sys
import css 



button_width = 250
button_height = 70

#Базовое окно с происшествиями
class VideoForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None
        self.resize(1900, 800)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle("Детектор")

        self.width = int(self.frameGeometry().width())
        self.height = int(self.frameGeometry().height())


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
        self.setStyleSheet(css.button_video)

    def ShowImage(self):
        self.window1 = ImageForm(self.ImagePath)
        self.window1.show()

#Таблица с происшествиями
class ReportTable(QTableWidget):
    def __init__(self, parentWindow):
        self.parentWindow = parentWindow
        super().__init__(parentWindow)
        self.setGeometry(10, 10, 200, 300)
        self.setRowHeight(100, 100) 
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
            warningButtons[i].resize(140, 25)
            warningButtons[i].move(220 + 125 * i, 3 + 30 * currentRow)
            k = 0
            for lol in elem[1:]:

                if k == 0:
                    current = 'Люди'
                elif k == 1:
                    current = 'Без жакета'
                elif k == 2:
                    current = 'Без куртки и штанов'
                elif k == 3:
                    current = 'Без штанов'
                elif k == 4:
                    current = 'Люди'
                elif k == 5:
                    current = 'Без жакета'
                elif k == 6:
                    current = 'Без куртки и штанов'
                elif k == 7:
                    current = 'Без штанов'
                elif k == 8:
                    current = 'Видео'
                k += 1

                if type(current) is int:
                    continue
                imageButtons.append(ImageButton(self.parentWindow, str(lol).strip()))
                imageButtons[i].resize(150, 25)
                imageButtons[i].setText(current)
                imageButtons[i].move(110 + 160 * (i + 2), 3 + 30 * currentRow)
                i += 1
        self.resizeColumnsToContents()

#Таблица с варнингами
class WarningTable(QTableWidget):
    def __init__(self, reportID):
        super().__init__()
        self.reportID = reportID
        self.setGeometry(10, 10, 800, 500)

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
                where Report_ID = {currentID}
            """).fetchall()
        imageButtons = []
        i = 0
        kostil = len(warningList) / 2
        for elem in warningList:
            if i == kostil:
                break
            print(elem)
            imageButtons.append(ImageButton(self, elem[4]))
            imageButtons[i].resize(140, 25)
            imageButtons[i].setText('Фото')
            imageButtons[i].move(700 + 125 * i, 25 * currentRow)
            i += 1
        self.resizeColumnsToContents()

#Кнопка-хуёпка для варнинга-хуярнинга
class WarningButton(QPushButton):
    def __init__(self, parentWindow, ReportID):
        super().__init__(parentWindow)
        self.parentWindow = parentWindow
        self.RepordID = ReportID
        self.setText("Проиcшествия")
        self.clicked.connect(self.ShowWarningWindow)
        self.setStyleSheet(css.button_video)

    def ShowWarningWindow(self):
        self.window1 = WarningTable(self.RepordID)
        self.window1.resize(900, 500)
        self.window1.move(400, 400)
        self.window1.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.exit(app.exec_())