FROM python:3.10-slim

# Configurar entorno de producción
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MODE=deployments


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
ENV $(cat /app/collecti_stamp/.env | xargs)

# Instalar dependecias de Python
RUN pip install -r requirements.txt

# Configurar la aplicación
RUN python manage.py collectstatic --no-input
RUN mkdir /app/static

# Utilizar la variable en una condición para configurar el entorno de desarrollo o despliegue
RUN if [ "$MODE" = "deployment" ]; then \
        rsync -av --progress /app/staticfiles/ /app/static/ && \
        rm -rf /app/staticfiles && \
        python manage.py makemigrations && \
        python manage.py migrate; \
    elif [ "$MODE" = "deployments" ]; then \
        rsync -av --progress staticfiles/ /app/static/ && \
        rm -rf /app/staticfiles; \
    fi

# Copiar los archivos estáticos al contenedor
RUN rsync -av --progress static/ /app/static/

# Eliminar el directorio "static"
RUN rm -rf static

RUN echo "$MODE"

RUN if [ "$MODE" = "deployment" ]; then \
    EXPOSE 8000; \
    ENTRYPOINT ["python3", "manage.py", "runserver", "localhost:8000"]; \
    fi

