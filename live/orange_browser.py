import sys
from PyQt4.Qt import (Qt,
                      QApplication,
                      QObject,
                      QThread,
                      QWaitCondition,
                      QUrl,
                      pyqtSignal)
from PyQt4 import QtWebKit
import cherrypy
import time

APPNAME = "orange_browser"
RANDOM_URL = "https://www.random.org/integers/?num=1&min=100&max=999&col=1&base=10&format=plain&rnd=new"


class ThreadedServer(QThread):
    foo_signal = pyqtSignal(str)
    shutdown_signal = pyqtSignal()

    def __init__(self, host='0.0.0.0', port=9919):
        QThread.__init__(self)
        self.host = host
        self.port = port

    @cherrypy.expose
    def index(self):
        self.foo_signal.emit(RANDOM_URL)
        return "Random number there!"

    @cherrypy.expose
    def shutdown(self):
        self.shutdown_signal.emit()
        return "Shutdown!"

    def run(self):
        cherrypy.server.socket_host = self.host
        cherrypy.server.socket_port = self.port
        cherrypy.tree.mount(self, "/", None)
        cherrypy.engine.start()


class OrangeBrowser(QtWebKit.QWebView):
    def __init__(self, parent=None):
        super(OrangeBrowser, self).__init__(parent)
        self.cherry_server = ThreadedServer()
        self.cherry_server.foo_signal.connect(self.open_url)
        self.cherry_server.shutdown_signal.connect(self.shutdown)
        self.cherry_server.start()
        self.setUrl(QUrl("http://127.0.0.1:9919"))

    def open_url(self, url):
        print("foo_signal")
        self.setUrl(QUrl(url))

    def shutdown(self):
        cherrypy.engine.exit()
        stop()

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_Q:
                self.close()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        app = QApplication(sys.argv)
        app.setApplicationName(APPNAME)
        main = OrangeBrowser()
        main.show()

        #cherrypy.quickstart(Root(), '/', config=CONF)

        def stop():
            app.exit()

        main.onclose = stop
        app.exec_()
