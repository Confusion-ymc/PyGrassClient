FROM python:3.11.4-slim-bullseye

WORKDIR /getGrass

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "run.py"]