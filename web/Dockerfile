FROM continuumio/miniconda

ADD environment.yml .

RUN conda-env create -f ./environment.yml

python -m nltk.downloader stopwords

RUN mkdir -p /usr/app
COPY . /usr/app
WORKDIR /usr/app

ENV PYTHONPATH /usr/app
