#!/bin/sh

apt-get update

apt-get -y install iproute build-essential xvfb xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic python-dev qt4-default python-qt4 x11vnc libxtst-dev libpng-dev zlib1g-dev
pip install cherrypy ipython pygments pyzmq autopy
