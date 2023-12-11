FROM python:3.10-slim

# Configurar entorno de producción
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Instalar dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
    git libpq-dev gcc libc-dev gcc g++ make libffi-dev python3-dev build-essential rsync && \
    apt-get clean

RUN pip install gunicorn
RUN pip install psycopg2
RUN pip install ipdb
RUN pip install ipython

# Crear directorio de trabajo
WORKDIR /app

# Clonar el repositorio
RUN git clone -b fix/docker https://github.com/Lenient-Enterprise/CollectiStamp.git /app

# Cambiar al directorio del proyecto
WORKDIR /app/collecti_stamp

# Añade el .env
ADD .env /app/collecti_stamp/.env

# Instalar dependecias de Python
RUN pip install -r requirements.txt

# Configurar la aplicación
RUN python manage.py collectstatic --no-input
RUN mkdir /app/static
RUN rsync -av --progress static/ /app/static/
RUN rsync -av --progress staticfiles/ /app/static/
RUN rm -rf static
RUN rm -rf staticfiles

EXPOSE 8000
CMD ["gunicorn", "-w", "5", "collecti_stamp.wsgi", "--timeout=500", "-b", "0.0.0.0:8000"]

