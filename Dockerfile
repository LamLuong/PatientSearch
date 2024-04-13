FROM ubuntu:22.04
WORKDIR /code

COPY ./app /code/app
COPY ./requirements.txt /code/
COPY ./runbackend.sh /code/

RUN apt-get update && apt-get -y upgrade && apt-get install -y python3 python3-pip
RUN apt-get install -y libpq-dev
RUN pip3 install -r requirements.txt

ENV PYTHONPATH=/code/

CMD ["bash", "runbackend.sh"]

# EXPOSE 9981

