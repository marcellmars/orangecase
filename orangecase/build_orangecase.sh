#!/bin/sh

apt-get update

apt-get -y install iproute build-essential xvfb xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic qt5-default python3-pyqt5 python3-pyqt5.qtwebkit python3-pyqt5.qtsvg x11vnc libxtst-dev libpng-dev zlib1g-dev python3-pip git
pip3 install cherrypy ipython pygments pyzmq
git clone git://github.com/msanders/autopy.git
cd autopy
python3 setup.py build
python3 setup.py install
