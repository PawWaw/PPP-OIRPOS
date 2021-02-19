from PyQt5 import QtCore, QtGui, QtWidgets
from scriptRunner import runScripts

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        self.textName = ""
        self.tab = []
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1125, 793)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.openGLWidget = QtWidgets.QOpenGLWidget(self.centralwidget)
        self.openGLWidget.setGeometry(QtCore.QRect(30, 70, 791, 641))
        self.openGLWidget.setObjectName("openGLWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(900, 530, 131, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openFile)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 5, 791, 61))
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setGeometry(QtCore.QRect(900, 620, 131, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.runApp)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1125, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Wybierz plik"))
        self.pushButton_2.setText(_translate("MainWindow", "Start"))

    def runApp(self):
        self.tab = runScripts(self.textName)
        self.label.setText("bsfoinvsdkg")

    def openFile(self):
        self.textName, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(None, "Wybierz obrazek",  "Początkowa nazwa pliku", "Image files (*.jpg *.png)")
        if self.textName:
            self.pushButton_2.setEnabled(True)
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())