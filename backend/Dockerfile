FROM python:3.11.2

WORKDIR /

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY bebest /bebest
COPY scripts/entrypoint /entrypoint

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/entrypoint"]
CMD ["--bind", "0.0.0.0:8000"]
