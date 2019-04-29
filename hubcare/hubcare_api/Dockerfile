FROM python:3-alpine
ENV PYTHONUNBUFFERED 1
ARG URL_COMMIT
ENV URL_COMMIT=$URL_COMMIT
ARG URL_COMMUNITY
ENV URL_COMMUNITY=$URL_COMMUNITY
ARG URL_ISSUE
ENV URL_ISSUE=$URL_ISSUE
ARG URL_PULL_REQUEST
ENV URL_PULL_REQUEST=$URL_PULL_REQUEST
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt && apk add bash
COPY . /code/
CMD bash -c "python3 manage.py makemigrations && \
             python3 manage.py migrate --run-syncdb && \
             python3 manage.py runserver 0.0.0.0:$PORT"