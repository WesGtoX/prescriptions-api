FROM python:3.10.2

# set work directory
WORKDIR /code

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements-dev.txt /code/requirements-dev.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /code/requirements-dev.txt

# copy project
COPY . /code
