FROM python:3.10.4-slim-bullseye
RUN pip install flask flask-wtf email_validator requests flask-login flask-sqlalchemy
WORKDIR /app
COPY app.py /app
COPY templates /app/templates
CMD python app.py

