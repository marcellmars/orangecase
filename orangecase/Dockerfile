FROM alpine:latest

MAINTAINER Marcell Mars "https://github.com/marcellmars"

RUN mkdir -p /var/cache/apk
RUN ln -s /var/cache/apk /etc/apk/cache
COPY apk /var/cache/apk
RUN setup-apkcache
RUN apk cache download
RUN echo @testing http://nl.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories
RUN apk --update add qt5-qtbase-dev qt5-qtwebkit-dev qt5-qtsvg-dev xvfb python3 build-base binutils python3-dev supervisor git libx11-dev libxtst-dev libpng-dev x11vnc@testing
RUN pip3 install cherrypy ipython pygments pyzmq

COPY build_orangecase.sh /usr/local/bin/build_orangecase.sh
COPY PyQt-gpl-5.4.2.tar.gz /tmp/
COPY sip-4.16.8.tar.gz /tmp/
RUN chmod +x /usr/local/bin/build_orangecase.sh
RUN /usr/local/bin/build_orangecase.sh

ADD dnsmasq.local /etc/dnsmasq.d/local
ADD orangecase.conf /etc/supervisor/conf.d/
ADD isnipdom.py /usr/local/bin/isnipdom.py
ADD supervisord.conf /etc/supervisord.conf

COPY fonts.conf /root/.fonts.conf

ENV DISPLAY :0
ENTRYPOINT /usr/bin/supervisord -c /etc/supervisord.conf