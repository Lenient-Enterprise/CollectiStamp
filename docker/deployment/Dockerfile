FROM python:3.10-slim

# Configurar entorno de producción
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1


# Instalar dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
    git libpq-dev gcc libc-dev gcc g++ make libffi-dev python3-dev build-essential rsync sqlite3 libsqlite3-dev && \
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
ENV $(cat /app/collecti_stamp/.env | xargs)

# Instalar dependecias de Python
RUN pip install -r requirements.txt

# Configurar la aplicación
RUN python manage.py collectstatic --no-input
RUN mkdir /app/static
RUN rsync -av --progress /app/staticfiles/ /app/static/
RUN rsync -av --progress static/ /app/static/
RUN rm -rf /app/staticfiles
RUN python manage.py makemigrations
RUN python manage.py migrate


# Copiar los archivos estáticos al contenedor
RUN rsync -av --progress static/ /app/static/

# Eliminar el directorio "static"
RUN rm -rf static

CMD ["gunicorn", "-w", "5", "collecti_stamp.wsgi", "--timeout=500", "-b", "0.0.0.0:5000"]