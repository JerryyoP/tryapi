FROM debian:latest
RUN apt update && apt upgrade -y
RUN apt install youtube-dl -y
RUN apt install uvicorn -y
RUN apt install git curl python3-pip -y
RUN pip3 install -U pip
RUN pip3 install -U -r requirements.txt
CMD python3 pornhub_relay.py
