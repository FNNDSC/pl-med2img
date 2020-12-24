# Docker file for med2img ChRIS plugin app, pl-med2img
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build --build-arg UID=$UID -t local/pl-med2img .
#
# In the case of a proxy (located at 192.168.13.14:3128), do:
#
#    export PROXY=http://192.168.13.14:3128
#    docker build --build-arg http_proxy=$PROXY --build-arg UID=$UID -t local/pl-med2img .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-med2img
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-med2img
#
# To debug from within a container:
#
#   docker run  -ti                                                                 \
#               -v $(pwd):/usr/src/med2img                                          \
#               -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing                      \
#               local/pl-med2img med2img.py /incoming /outgoing
#


FROM fnndsc/ubuntu-python3:latest
LABEL MAINTAINER="dev@babymri.org"

ENV APPROOT="/usr/src/med2img"
ENV DEBIAN_FRONTEND=noninteractive VERSION="0.1"
COPY ["med2img", "${APPROOT}"]
COPY ["requirements.txt", "${APPROOT}"]

WORKDIR $APPROOT

RUN apt-get update \
  && apt-get install -y python3-tk \
  && pip install -r requirements.txt

CMD ["med2img.py", "--help"]
