FROM python:3.11
RUN mkdir /app
WORKDIR /app

COPY source/backend/bot/requirements.txt /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install langchain
RUN pip3 install gigachat

COPY source/backend/ /app


STOPSIGNAL SIGTERM
CMD ["python3",  "run.py"]