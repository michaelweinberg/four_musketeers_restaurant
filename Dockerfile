FROM python:3.10.4-slim-bullseye
RUN pip install flask flask-wtf email_validator requests flask-login flask-sqlalchemy
COPY app.py app.py
CMD python app.py

