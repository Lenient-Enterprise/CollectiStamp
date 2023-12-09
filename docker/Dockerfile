FROM python:3.10-alpine

# Configurar entorno de producción
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Instalar dependencias
RUN apk add --no-cache \
        git \
        postgresql-dev \
        gcc \
        libc-dev \
        g++ \
        make \
        libffi-dev \
        python3-dev \
        build-base

RUN pip install gunicorn
RUN pip install psycopg2
RUN pip install ipdb
RUN pip install ipython

# Crear directorio de trabajo
WORKDIR /app

# Clonar el repositorio
RUN git clone https://github.com/Lenient-Enterprise/CollectiStamp.git /app

# Instalar dependencias Python
RUN pip install -r requirements.txt


# Cambiar al directorio del proyecto
WORKDIR /app/collecti_stamp

# Configurar la aplicación
RUN python manage.py collectstatic --no-input

# Iniciar la aplicación con Gunicorn
# CMD ["gunicorn", "-w", "5", "collecti_stamp.wsgi", "--timeout=500", "-b", "0.0.0.0:5000"]

