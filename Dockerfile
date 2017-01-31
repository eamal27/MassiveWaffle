FROM ubuntu:trusty

EXPOSE 8000
RUN apt-get update && apt-get install -y \
    git \
    python3-pip && \
    git clone https://github.com/jipson7/MassiveWaffle.git && \
    cd MassiveWaffle && \
    pip3 install -r requirements.txt && \
    python3 -m nltk.downloader vader_lexicon

CMD /MassiveWaffle/docker-run.sh

