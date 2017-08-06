FROM python:2.7

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8888

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8888", "blog.app:create_app()"]
