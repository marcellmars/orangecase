import sys
from PyQt4 import (QtGui,
                   QtCore)
from PyQt4 import QtWebKit
import cherrypy

APPNAME = "orange_browser"

class CherryServer(object):
    @cherrypy.expose
    def index(self):
        return "Hello World"

class OrangeBrowser(QtWebKit.QWebView):
    def __init__(self, parent=None):
        super(OrangeBrowser, self).__init__(parent)
        cherrypy.server.socket_host = '127.0.0.1'
        cherrypy.server.socket_port = '9999'
        cherrypy.quickstart(CherryServer())

    def keyPressEvent(self, event):
        if event.modifiers() & QtCore.Qt.ControlModifier:
            if event.key() == QtCore.Qt.Key_Q:
                self.close()

if __name__=='__main__':
    if len(sys.argv) == 1:
        app = QtGui.QApplication(sys.argv)
        app.setApplicationName(APPNAME)
        main = OrangeBrowser()
        main.show()

        #cherrypy.quickstart(Root(), '/', config=CONF)


        def stop():
            app.exit()

        main.onclose = stop
        app.exec_()
