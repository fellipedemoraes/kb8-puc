FROM python:3.10-alpine AS builder

RUN addgroup -S dockergroup && adduser -S dockeruser -G dockergroup

WORKDIR /code

COPY requirements.txt /code

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R dockeruser:dockergroup /code

USER dockeruser

ENV FLASK_APP run.py
ENV FLASK_DB_TYPE postgres
ENV FLASK_DB_PORT 5432
ENV FLASK_DB_USER postgres
ENV FLASK_DB_NAME postgres
ENV FLASK_DB_PASSWORD secretpass
ENV FLASK_DB_HOST localhost

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
