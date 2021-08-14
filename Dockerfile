# Solely coded by xmysteriousx
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata
# setting the working directory in the container
RUN mkdir ./app
RUN chmod 777 ./app
WORKDIR /app/
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    curl \
    git \
    python3 \
    python3-pip \
    make \
    wget \
    ffmpeg \
    ffmpeg \
    meson \
    libglib2.0-dev \
    libssl-dev \
    libcurl4-openssl-dev \
    asciidoc \
    docbook-xml \
    autoconf \
    libtool \
    automake
# Installing Megacmd
RUN mkdir -p /tmp/ && \
    cd /tmp/ && \
    wget https://mega.nz/linux/MEGAsync/xUbuntu_20.04/amd64/megacmd-xUbuntu_20.04_amd64.deb && \
    # -f ==> is required to --fix-missing-dependancies
    apt -fqqy install ./megacmd-xUbuntu_20.04_amd64.deb && \
    # clean up the container "layer", after we are done
    rm ./megacmd-xUbuntu_20.04_amd64.deb

# Installing megatools
RUN mkdir -p /tmp/ && cd /tmp/ && git clone https://github.com/XMYSTERlOUSX/megatools && cd /tmp/megatools && meson b && ninja -C b && ninja -C b install

# Copying the content of the local src directory to the working directory
COPY . .
RUN pip3 install -r requirements.txt
CMD python3 bot.py
