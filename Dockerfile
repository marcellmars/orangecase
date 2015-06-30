FROM librarian/motw

MAINTAINER Marcell Mars "https://github.com/marcellmars"

RUN  echo 'Acquire::http::Proxy "http://172.17.42.1:3142";' >> /etc/apt/apt.conf.d/01proxy

ADD build_orangecase.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/build_orangecase.sh
RUN /usr/local/bin/build_orangecase.sh

ADD dnsmasq.local /etc/dnsmasq.d/local
ADD orangecase.conf /etc/supervisor/conf.d/
ADD isnipdom.py /usr/local/bin/isnipdom.py

ENV DISPLAY :0

ENTRYPOINT /usr/local/bin/supervisord
