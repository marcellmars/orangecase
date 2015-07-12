#!/bin/sh

cd /tmp/
tar xvfz sip-4.16.8.tar.gz
cd sip-4.16.8/
python3 configure.py
make
make install

cd /tmp/
tar xvfz PyQt-gpl-5.4.2.tar.gz
cd PyQt-gpl-5.4.2/
python3 configure.py --qmake=/usr/bin/qmake-qt5 --confirm-license
make
make install

cd /tmp/
git clone git://github.com/msanders/autopy.git
cd /tmp/autopy/
python3 setup.py build
python3 setup.py install

