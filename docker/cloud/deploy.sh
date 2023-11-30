#!/bin/bash

# Nombre de usuario en Docker Hub
USERNAME="alesanfel"

# Nombre de la imagen
IMAGE_NAME="collecti_stamp"

# Versión de la imagen (puede ser proporcionada como argumento, si no, se utiliza "latest")
VERSION=${1:-"latest"}

# Nombre completo de la imagen con la versión
FULL_IMAGE_NAME="$USERNAME/$IMAGE_NAME:$VERSION"

# Construir la imagen
docker build -t $FULL_IMAGE_NAME . --no-cache

# Etiquetar la imagen con "latest" si no se proporciona una versión
if [ "$VERSION" == "latest" ]; then
    docker tag $FULL_IMAGE_NAME $USERNAME/$IMAGE_NAME:latest
fi

# Iniciar sesión en Docker Hub
docker login

# Subir la imagen a Docker Hub
docker push $FULL_IMAGE_NAME

# Salir de la sesión en Docker Hub
docker logout
