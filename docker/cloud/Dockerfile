FROM python:3.11.4-slim-bullseye
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install system dependencies
RUN apt-get update && apk add --no-cache git postgresql-dev gcc libc-dev && apk add --no-cache gcc g++ make libffi-dev python3-dev build-base && pip install gunicorn && pip install psycopg2 && pip install ipdb && pip install ipython

RUN git clone -d feature/deployment-of-application https://github.com/Lenient-Enterprise/CollectiStamp.git /app

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r ./collecti_stamp/requirements.txt

WORKDIR /app/collecti_stamp

RUN python manage.py collectstatic --noinput

ENTRYPOINT [ "gunicorn", "collecti_stamp.wsgi"]