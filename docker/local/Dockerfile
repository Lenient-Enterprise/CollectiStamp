FROM python:3.10-alpine

RUN apk add --no-cache git postgresql-dev gcc libc-dev
RUN apk add --no-cache gcc g++ make libffi-dev python3-dev build-base

RUN pip install gunicorn
RUN pip install psycopg2
RUN pip install ipdb
RUN pip install ipython

WORKDIR /app

RUN git clone -b feature/actions https://github.com/Lenient-Enterprise/CollectiStamp.git /app
RUN pip install -r requirements.txt

WORKDIR /app/collecti_stamp

RUN python manage.py collectstatic

RUN python manage.py makemigrations

RUN python manage.py migrate

CMD ["gunicorn", "-w 5", "collecti_stamp.wsgi", "--timeout=500", "-b 0.0.0.0:5000"]
