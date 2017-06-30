FROM python:2.7

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8888

CMD ["python", "app.py"]
