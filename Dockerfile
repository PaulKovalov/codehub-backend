FROM python:3.7-alpine
WORKDIR /code
ENV PYTHONUNBUFFERED 1
ENV DJANGO_LOG_LEVEL INFO
ENV SECRET_KEY t&rup!*2)&2q97y34ce3&w26+#266!+sbpo\=^b4z$cj(ua^n0x
ENV DEBUG True
ENV DB_ENGINE django.db.backends.postgresql
ENV DB_NAME codehub
ENV DB_HOST localhost
ENV DB_PORT 5432
ENV DB_USER postgres
ENV DB_PASSWORD password123
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["manage.py", "run"]
