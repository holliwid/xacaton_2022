from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import video
import os
import subprocess
import sqlite3
import sys
import css 

class QImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None
        self.resize(1700, 800)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle("Детектор")
        self.width = int(self.frameGeometry().width())
        self.height = int(self.frameGeometry().height())
        print(self.width)
        self.CreateUI()

    #Создание кнопок взаимодействия
    def CreateUI(self):
        _translate = QtCore.QCoreApplication.translate

        button_width = 250
        button_height = 70
        self.loadFileButton = QtWidgets.QPushButton(self)
        self.loadFileButton.setStyleSheet(css.button)
        self.loadFileButton.resize(button_width, button_height)
        self.loadFileButton.setText(_translate("Form", "Открыть видео"))
        self.loadFileButton.clicked.connect(self.RunCommand)
        self.loadFileButton.move(int(self.width / 2 - button_width / 2), int(self.height / 2 - button_height / 2 - 100))

        self.openVideos = QtWidgets.QPushButton(self)
        self.openVideos.setStyleSheet(css.button)
        self.openVideos.resize(button_width, button_height)
        self.openVideos.setText(_translate("Form", "Открыть таблицу"))
        self.openVideos.clicked.connect(self.OpenVideo)
        self.openVideos.move(int(self.width / 2 - button_width / 2), int(self.height / 2 - button_height / 2))

    #Выбор видоса и запуск нейронки
    def RunCommand(self):
        self.filename = QFileDialog.getOpenFileName()
        path = f"./data/video/{self.filename[0].split('/')[-1]}"
        print(">>Selected file name: "+path)

        # Создать папку
        folderName = f"example{len(next(os.walk('runs/track'))[1]) + 1}"
        os.popen(f"mkdir ./runs/track/{folderName}")

        import pathlib
        path_1 = str(pathlib.Path(__file__).parent.resolve())
        project_path = f"{path_1}/runs/track/{folderName}"
        path = f"{path_1}/data/video/{self.filename[0].split('/')[-1]}"

        # Прогон нейронки и создание трёх подпапок
        print(">>Neural network is running!")
        currentCommand = "python track.py --yolo-weights best_DIMA_200m.pt --strong-sort-weights osnet_x0_25_msmt17.pt --img 640 --source " + path + " --save-txt --save-conf --project " + project_path + " --save-vid --name human --classes 0"
        print(">>Current command: " + currentCommand)
        t1 = subprocess.Popen(currentCommand)
        
        currentCommand = "python track.py --yolo-weights best_DIMA_200m.pt --strong-sort-weights osnet_x0_25_msmt17.pt --img 640 --source " + path + " --save-txt --save-conf --project " + project_path + " --save-vid --name jacket --classes 1"
        print(">>Current command: " + currentCommand)
        t2 = subprocess.Popen(currentCommand)

        currentCommand = "python track.py --yolo-weights best_DIMA_200m.pt --strong-sort-weights osnet_x0_25_msmt17.pt --img 640 --source " + path + " --save-txt --save-conf --project " + project_path + " --save-vid --name pants --classes 2"
        print(">>Current command: " + currentCommand)
        t3 = subprocess.Popen(currentCommand)

        #~~~Какая-то магия с процессами~~~
        process = []
        process.append(t1)
        process.append(t2)
        process.append(t3)

        for i in process:
            if i.wait() != 0:
                print('\t \t Идет распознавание')

        currentCommand_script = "python script.py"
        t4 = subprocess.Popen(currentCommand_script)
        process.append(t4)
        self.SendDataToDB()

    def SendDataToDB(self):
        db = sqlite3.connect("reports.db")
        cursor = db.cursor()
        lastExampleID = len(next(os.walk('runs/track'))[1])
        Heat_Human_path = f"runs/track/example{lastExampleID}/Graphics/heat_human.png"
        Heat_Without_Jacket_path = f"runs/track/example{lastExampleID}/Graphics/heat_without_jacket.png"
        Heat_Without_Pants_Jacket_path = f"runs/track/example{lastExampleID}/Graphics/heat_without_pants_jacket.png"
        Heat_Without_Pants_path = f"runs/track/example{lastExampleID}/Graphics/heat_without_pants.png"
        Human_path = f"runs/track/example{lastExampleID}/Graphics/human.png"
        Without_Jacket_path = f"runs/track/example{lastExampleID}/Graphics/without_jacket.png"
        Without_Pants_Jacket_path = f"runs/track/example{lastExampleID}/Graphics/without_pants_jacket.png"
        Without_Pants_path = f"runs/track/example{lastExampleID}/Graphics/without_pants.png"
        Video_Path = f"data/video/{self.filename[0].split('/')[-1]}"
        cursor.execute(f"""
            insert into Reports(
                Heat_Human_path,
                Heat_Without_Jacket_path,
                Heat_Without_Pants_Jacket_path,
                Heat_Without_Pants_path,
                Human_path,
                Without_Jacket_path,
                Without_Pants_Jacket_path,
                Without_Pants_path,
                Video_Path)
            values(
                '{Heat_Human_path}',
                '{Heat_Without_Jacket_path}',
                '{Heat_Without_Pants_Jacket_path}',
                '{Heat_Without_Pants_path}',
                '{Human_path}',
                '{Without_Jacket_path}',
                '{Without_Pants_Jacket_path}',
                '{Without_Pants_path}',
                '{Video_Path}');
        """)
        db.commit()

    @pyqtSlot()
    def OpenVideo(self):
        self.window().close()
        if self.w is None:
            self.w = video.VideoForm()
            self.w.show()
        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

if __name__ == '__main__':
    app = QApplication(sys.argv)
    imageViewer = QImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())