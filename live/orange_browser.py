from PyQt5.Qt import (Qt,
                      QApplication,
                      QThread,
                      QUrl,
                      QImage,
                      QPainter,
                      QTimer,
                      QWebSettings,
                      pyqtSignal)
from PyQt5 import QtWebKitWidgets as QtWebKit
import cherrypy
import time
import sys
import os
import uuid

APPNAME = "orange_browser"
AGENT_URL = "http://www.useragentstring.com/"
RANDOM_URL = "https://www.random.org/integers/?num=1&min=100&max=999&col=1&base=10&format=plain&rnd=new"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONF = {'/static': {'tools.staticdir.on': True,
                    'tools.staticdir.dir': os.path.join(CURRENT_DIR, 'static'),
                    'tools.staticdir.content_types': {'html': 'application/octet-stream',
                                                      'png': 'image/png'
                                                      }}}


class WebPage(QtWebKit.QWebPage):
    def userAgentForUrl(self, url):
        return USER_AGENT


class ThreadedServer(QThread):
    foo_signal = pyqtSignal(str)
    shutdown_signal = pyqtSignal()
    screenshot_signal = pyqtSignal(str)

    def __init__(self, host='0.0.0.0', port=9919):
        QThread.__init__(self)
        self.host = host
        self.port = port

    @cherrypy.expose
    def index(self, url=AGENT_URL):
        self.foo_signal.emit(url)
        return "Random number there!"

    @cherrypy.expose
    def screenshot(self):
        f_name = "{}.png".format(uuid.uuid4())
        file_name = ("/tmp/live/static/{}".format(f_name))
        self.screenshot_signal.emit(file_name)
        while not os.path.exists(file_name):
            time.sleep(0.15)
        return '<img src="static/{0}" alt="{0}">'.format(f_name)
        #cherrypy.response.headers['Content-Type'] = "image/png"
        #return open(file_name).read()

    @cherrypy.expose
    def shutdown(self):
        self.shutdown_signal.emit()
        return "Shutdown!"

    def run(self):
        cherrypy.server.socket_host = self.host
        cherrypy.server.socket_port = self.port
        cherrypy.config.update({'engine.autoreload.on': False})
        cherrypy.quickstart(self, config=CONF)


class OrangeBrowser(QtWebKit.QWebView):
    def __init__(self, parent=None):
        super(OrangeBrowser, self).__init__(parent)

        # settings for web page screenshots etc.
        self.setPage(WebPage())
        wp = self.page().settings()
        wp.setAttribute(QWebSettings.AutoLoadImages, True)
        wp.setAttribute(QWebSettings.JavascriptEnabled, True)
        self.page().mainFrame().setScrollBarPolicy(Qt.Vertical,
                                                   Qt.ScrollBarAlwaysOff)

        self.load_status = None
        self.page().mainFrame().loadStarted.connect(self.load_started)
        self.page().mainFrame().loadFinished.connect(self.load_finished)

        cherry_server = ThreadedServer()
        cherry_server.foo_signal.connect(self.open_url)
        cherry_server.shutdown_signal.connect(self.shutdown)
        cherry_server.screenshot_signal.connect(self.screenshot)
        cherry_server.start()
        self.setUrl(QUrl(RANDOM_URL))

    def load_started(self):
        print("started")
        self.load_status = "started"
        QTimer.singleShot(10000, self.load_finished)

    def load_finished(self, ok=False):
        print("finished")
        self.load_status = "finished"

    def open_url(self, url):
        print(url)
        self.stop()
        self.setUrl(QUrl(url))

    def screenshot(self, file_name):
        while self.load_status == "started":
            time.sleep(0.15)

        self.page().setViewportSize(self.page().mainFrame().contentsSize())
        image = QImage(self.page().viewportSize(),
                       QImage.Format_ARGB32)
        painter = QPainter(image)
        self.page().mainFrame().render(painter)

        painter.end()
        image.save(file_name)

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
        main.resize(1024, 768)
        main.move(0, 0)
        main.show()

        def stop():
            app.exit()

        main.onclose = stop
        app.exec_()
