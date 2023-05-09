FROM python:3.11.2

WORKDIR /

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY files /files
COPY bin /bin
COPY lib /lib
COPY scripts /scripts
COPY src /src

ENV PYTHONUNBUFFERED=1
ENV FILES_DIR_PATH=/files/

ENTRYPOINT [ "/scripts/run" ]
CMD ["crawler", "post", "habr", "--output", "crawler_output", "--logs", "crawler_logs"]
