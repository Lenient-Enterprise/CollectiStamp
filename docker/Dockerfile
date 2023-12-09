FROM python:3.10-alpine

# Configurar entorno de producción
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_ADMIN_PASSWORD=Hola$1234 \
    MODE=development \
    DB_NAME=mydatabase \
    DB_USER=mydatabaseuser \
    DB_PASSWORD=mypassword \
    DB_HOST=db \
    SECRET_KEY=your-secret-key \
    EMAIL_HOST_PASSWORD="yltf khuu xjdk vrah" \
    PAYPAL_CLIENT_ID=AejZtiMeXR3CdKhslKEcJE1IQqqVLjo4oqY2hpehc305GAw9bTikztJtNF8xSciyKgunq4tY5Fnkfvhf \
    PAYPAL_CLIENT_SECRET=EC2YcHwJDeKWHGWoUxQS9HMq8yNfh8dHq-WmgSds7uEEK61GTenWMwYBqu41sUd5vQPwIZVQQG1KdnmP

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

# Cambiar al directorio del proyecto
WORKDIR /app/collecti_stamp

# Instalar dependencias Python
RUN pip install -r requirements.txt

# Configurar la aplicación
RUN python manage.py collectstatic --no-input

# Iniciar la aplicación con Gunicorn
# CMD ["gunicorn", "-w", "5", "collecti_stamp.wsgi", "--timeout=500", "-b", "0.0.0.0:5000"]

