# # import pyqtgraph.examples
# # pyqtgraph.examples.run()
#
# from PyQt5 import QtWidgets  # (the example applies equally well to PySide2)
# # import pyqtgraph as pg
#
import pyqtgraph as pg
import numpy as np
#
# # Always start by initializing Qt (only once per application)
# app = QtWidgets.QApplication([])
#
# # Define a top-level widget to hold everything
# w = QtWidgets.QWidget()
#
# # Create some widgets to be placed inside
# btn = QtWidgets.QPushButton('press me')
# text = QtWidgets.QLineEdit('enter text')
# listw = QtWidgets.QListWidget()
# # plot = pg.PlotWidget()
#
# @pyqtSlot()
# def on_click()
#
#
#
# x = np.arange(1000)
# y = np.random.normal(size=(3, 1000))
# plotWidget = pg.plot(title="Three plot curves")
# for i in range(3):
#     plotWidget.plot(x, y[i], pen=(i, 3))  # setting pen=(i,3) automaticaly creates three different-colored pens
#
# # Create a grid layout to manage the widgets size and position
# layout = QtWidgets.QGridLayout()
# w.setLayout(layout)
#
# # Add widgets to the layout in their proper positions
# layout.addWidget(btn, 0, 0)  # button goes in upper-left
# layout.addWidget(text, 1, 0)  # text edit goes in middle-left
# layout.addWidget(listw, 2, 0)  # list widget goes in bottom-left
# layout.addWidget(plotWidget, 0, 1, 3, 1)  # plot goes on right side, spanning 3 rows
#
# # Display the widget as a new window
# w.show()
#
# # Start the Qt event loop
# app.exec_()

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QPushButton, QLineEdit, QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200

        self.plot = None

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QGridLayout()

        btn = QPushButton('press me')

        btn.clicked.connect(self.on_click)

        text = QLineEdit('enter text')
        listw = QListWidget()
        #plot = pg.PlotWidget()

        x = np.arange(1000)
        y = np.random.normal(size=(3, 1000))
        self.plot = pg.plot(title="Three plot curves")
        for i in range(3):
            self.plot.plot(x, y[i], pen=(i, 3))  # setting pen=(i,3) automaticaly creates three different-colored pens


        # button = QPushButton('PyQt5 button', self)
        # button.setToolTip('This is an example button')
        # button.move(100, 70)
        # button.clicked.connect(self.on_click)

        # Add widgets to the layout in their proper positions
        layout.addWidget(btn, 0, 0)  # button goes in upper-left
        layout.addWidget(text, 1, 0)  # text edit goes in middle-left
        layout.addWidget(listw, 2, 0)  # list widget goes in bottom-left
        layout.addWidget(self.plot, 0, 1, 3, 1)  # plot goes on right side, spanning 3 rows

        self.setLayout(layout)

        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        self.plot.centralWidget.items[0].setData(self.plot.centralWidget.items[0].xData, self.plot.centralWidget.items[0].yData + 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
