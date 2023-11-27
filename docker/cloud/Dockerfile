FROM python:3.10-alpine
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install system dependencies
RUN apk add --no-cache git postgresql-dev gcc libc-dev
RUN apk add --no-cache gcc g++ make libffi-dev python3-dev build-base

RUN pip install gunicorn
RUN pip install psycopg2
RUN pip install ipdb
RUN pip install ipython
RUN pip install whitenoise

RUN git clone -b feature/actions https://github.com/Lenient-Enterprise/CollectiStamp.git /app

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

WORKDIR /app/collecti_stamp

RUN python manage.py collectstatic --noinput --verbosity 3

ENTRYPOINT [ "gunicorn", "collecti_stamp.wsgi"]