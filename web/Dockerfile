FROM continuumio/miniconda

ADD environment.yml .

RUN conda-env create -f ./environment.yml

RUN mkdir -p /usr/app
COPY . /usr/app
WORKDIR /usr/app

ENV PYTHONPATH /usr/app
