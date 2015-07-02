from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
from IPython.qt.inprocess import QtInProcessKernelManager
from IPython.lib import guisupport

from PyQt4 import QtGui, QtCore

import sys

APPNAME = "sniplog"

class Js2Py(QtCore.QObject):
    sent = QtCore.pyqtSignal(str)

    @QtCore.pyqtSlot(str)
    def sendToPython(self, s):
        self.sent.emit(s)

class Snipdom(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)


        self.hsplit = QtGui.QSplitter()
        self.setCentralWidget(self.hsplit)

        kernel_manager = QtInProcessKernelManager()
        kernel_manager.start_kernel()
        self.kernel = kernel_manager.kernel
        self.kernel.gui = 'qt4'

        self.control = RichIPythonWidget(gui_completion="droplist")

        self.kernel.shell.push({'snipdom': self})

        kernel_client = kernel_manager.client()
        kernel_client.start_channels()

        self.control.kernel_manager = kernel_manager
        self.control.kernel_client = kernel_client

        self.vsplit = QtGui.QSplitter()
        self.vsplit.setOrientation(QtCore.Qt.Vertical)

        self.vsplit.addWidget(self.control)
        self.hsplit.addWidget(self.vsplit)

        self.sendButton = QtGui.QPushButton("send")
        #self.sendButton.clicked.connect(self.sendcode)
        self.vsplit.addWidget(self.sendButton)

        self.bridge = Js2Py()
        self.bridge.sent.connect(self.codeFromJs)

        #lab = QtGui.QLabel(kernel.shell.history_manager.get_range(start=-1).next()[2])

    def codeFromJs(self, code):
        self.control.input_buffer = code

if __name__=='__main__':
    if len(sys.argv) == 1:
        app = QtGui.QApplication(sys.argv)
        app.setApplicationName(APPNAME)
        main = Snipdom()
        main.show()

        def stop():
            app.exit()

        main.onclose = stop

        main.control.exit_requested.connect(stop)
        guisupport.start_event_loop_qt4(app)
