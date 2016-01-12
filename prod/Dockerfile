FROM python:2.7
RUN apt-get -qq update && apt-get install -y -qq --no-install-recommends vim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD ../requirements.txt /code/
RUN pip install -r requirements.txt
# RUN pip install -U djangorestframework-jwt
ADD ../. /code/
