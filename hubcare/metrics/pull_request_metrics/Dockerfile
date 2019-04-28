FROM python:3-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt && apk add bash
COPY . /code/
CMD bash -c "python3 manage.py makemigrations && \
             python3 manage.py migrate --run-syncdb && \
             python3 manage.py runserver 0.0.0.0:$PORT"