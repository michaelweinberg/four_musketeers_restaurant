
FROM python:3.10.4-slim-bullseye

RUN pip3 install email_validator flask-login 
# install python dependencies


RUN pip install --upgrade pip


COPY requirements.txt .

RUN pip3 install -r requirements.txt


COPY app.py app.py

CMD python app.py



