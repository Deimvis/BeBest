FROM python:3.11.2

WORKDIR /

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY bebest /bebest

ENV PYTHONUNBUFFERED=1
ENV FILES_DIR_PATH=/files/

WORKDIR /bebest
ENTRYPOINT [ "gunicorn", "bebest.wsgi:application" ]
CMD ["--bind", "0.0.0.0:8000"]
