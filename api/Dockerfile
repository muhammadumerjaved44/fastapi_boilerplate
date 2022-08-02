FROM continuumio/miniconda3

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /code