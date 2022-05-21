FROM python:3.10.4-slim-bullseye
RUN pip install --upgrade pip
RUN pip install flask flask-wtf email_validator requests flask-login flask-sqlalchemy flask_login
COPY requirements.txt .
RUN pip3 install -r requirements.txt
WORKDIR /app
COPY app.py /app
COPY templates /app/templates
COPY static /app/static
CMD python app.py

