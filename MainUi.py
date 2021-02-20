from PyQt5 import QtGui
from scriptRunner import runScripts
from Endpoints import getDataForText, getDataForGraph
import numpy as np
import sys

from matplotlib.backends.qt_compat import QtCore, QtWidgets
if QtCore.qVersion() >= "5.":
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        self.textName = ""
        self.LabelString = ""
        self.tab = []
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1350, 793)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 5, 791, 61))
        self.label.setObjectName("label")
        self.label.setWordWrap(True)

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))

        networks = ("InceptionResnetV2", "InceptionV3", "MobileNet", "MobileNetV2", "ResNet50", "VGG16","VGG19")
        performance = (0,0,0,0,0,0,0)

        self._static_ax = static_canvas.figure.subplots()
        self._static_ax.bar(networks, performance, align='center')

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(29, 79, 1300, 641))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(static_canvas)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setMaximumSize(QtCore.QSize(80, 50))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.runApp)
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setEnabled(True)
        self.pushButton.setMaximumSize(QtCore.QSize(80, 50))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openFile)
        self.horizontalLayout.addWidget(self.pushButton)
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
        tabtemp = getDataForGraph(self.tab)
        self._static_ax.bar(tabtemp[0], tabtemp[1], align='center')
        self._static_ax.figure.canvas.draw()
        self.label.setText(getDataForText(self.tab))

    def openFile(self):
        self.textName, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(None, "Wybierz obrazek",  "Początkowa nazwa pliku", "Image files (*.jpg *.png)")
        if self.textName:
            self.pushButton_2.setEnabled(True)
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    w = QtWidgets.QMainWindow()
    ex.setupUi(w)
    w.show()
    sys.exit(app.exec_())
