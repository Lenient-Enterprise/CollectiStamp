#!/bin/bash

#!/bin/bash

BASE_DIR=$(dirname "$0")
DB_FILE="$BASE_DIR/db.sqlite3"
VENV_DIR="$BASE_DIR/venv"
REQUIREMENTS_FILE="$BASE_DIR/requirements.txt"
MIGRATIONS_DIR=$(find "$BASE_DIR" -type d -name migrations)
JSON_DATA_FILE="$BASE_DIR/data/populate_user.json $BASE_DIR/data/populate_company_details.json $BASE_DIR/data/populate_criteria.json $BASE_DIR/data/populate_product.json"
DELETE_DB=false
DELETE_ENV=false

while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -db|--delete-db)
            DELETE_DB=true
            shift
            ;;
        -env|--delete-env)
            DELETE_ENV=true
            shift
            ;;
        *)
            # Opción desconocida
            echo "Opción desconocida: $key"
            exit 1
            ;;
    esac
done


reset_database() {
    # Borrar el entorno virtual existente
    if [ "$DELETE_ENV" == true ]; then
        if [ -d "$VENV_DIR" ]; then
            echo "Borrando el entorno virtual existente..."
            rm -rf "$VENV_DIR"
        fi

        # Crear un nuevo entorno virtual
        echo "Creando un nuevo entorno virtual..."
        python3 -m venv "$VENV_DIR"

        # Activar el entorno virtual
        echo "Activando el entorno virtual..."
        source "$VENV_DIR/bin/activate"

        # Instalar las dependencias del archivo requirements.txt
        echo "Instalando las dependencias del archivo requirements.txt..."
        pip install -r "$REQUIREMENTS_FILE"
        echo "----------------------------------------"
    fi

    # Configured template for commits
    git config commit.template .gitmessage.txt
    echo "Git commit template configured."
    echo "----------------------------------------"

    # Deleting the existing db.sqlite3 file if DELETE_DB is true
    if [ "$DELETE_DB" == true ] && [ -e "$DB_FILE" ]; then
        rm "$DB_FILE"
        echo "Existing db.sqlite3 file deleted."
        echo "----------------------------------------"

        # Deleting migration files excluding __init__.py
        for dir in $MIGRATIONS_DIR; do
            if [ -e "$dir" ]; then
                find "$dir" -type f ! -name "__init__.py" ! -path "*/venv/*" -exec rm {} \;
                echo "Migration files in $dir deleted, excluding __init__.py and files in paths containing '/venv/'."
            fi
        done
        echo "----------------------------------------"

        # Creating the db.sqlite3 file
        if [ "$DELETE_DB" == true ]; then
            touch "$DB_FILE"
            echo "db.sqlite3 file created."
            echo "----------------------------------------"
        fi
    fi

    # Updating migrations
    python manage.py makemigrations
    echo "Migrations updated."
    echo "----------------------------------------"

    # Applying migrations
    python manage.py migrate
    echo "Migrations applied."
    echo "----------------------------------------"

    # Loading data from JSON files
    for file in $JSON_DATA_FILE; do
        if [ -e "$file" ]; then
            python manage.py loaddata "$file"
            echo "Data loaded from JSON file: $file"
        fi
    done

    echo "----------------------------------------"
    echo "Process completed successfully!"
}

reset_database
