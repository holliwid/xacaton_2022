from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
import os


# command = 'C:\\Users\\nikol\\Yolov5_StrongSORT_OSNet\\venv\\Scripts\\python.exe'
# os.system(command)

class Ui_Form(object):
    def setupUi(self, Form):
        self.loadFileButton = QtWidgets.QPushButton(Form)

        self.runNeuralNetworkButton = QtWidgets.QPushButton(Form)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setGeometry(300, 250, 350, 200)

        self.loadFileButton.setText(_translate("Form", "Открыть файл"))
        self.loadFileButton.clicked.connect(self.pushButton_handler)
        self.loadFileButton.move(0, 0)

        self.runNeuralNetworkButton.setText(_translate("Form", "Запустить нейронную сеть"))
        self.runNeuralNetworkButton.clicked.connect(self.runCommand)
        self.runNeuralNetworkButton.move(0, 100)

    def pushButton_handler(self):
        self.open_dialog_box()

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName()
        self.path = f"\\data\\video\\{filename[0].split('/')[-1]}"
        print(self.path)

    def runCommand(self):
        currentCommand = "python track.py --yolo-weights best_DIMA_200m.pt --strong-sort-weights osnet_x0_25_msmt17.pt --img 640 --source '" + self.path + "' --save-txt --save-conf --save-vid"
        p = os.popen(currentCommand)
        print("Neural network is running!")
        print(currentCommand)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())