#!/bin/bash

#!/bin/bash

BASE_DIR=$(dirname "$0")
DB_FILE="$BASE_DIR/db.sqlite3"
MIGRATIONS_DIR=$(find "$BASE_DIR" -type d -name migrations)
JSON_DATA_FILE="$BASE_DIR/data/populate_user.json $BASE_DIR/data/populate_company_details.json $BASE_DIR/data/populate_criteria.json $BASE_DIR/data/populate_product.json"
DELETE_DB=false

while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -d|--delete-db)
            DELETE_DB=true
            shift
            ;;
        *)
            # unknown option
            echo "Unknown option: $key"
            exit 1
            ;;
    esac
done

reset_database() {
    # Deleting the existing db.sqlite3 file if DELETE_DB is true
    if [ "$DELETE_DB" == true ] && [ -e "$DB_FILE" ]; then
        rm "$DB_FILE"
        echo "Existing db.sqlite3 file deleted."
        echo "----------------------------------------"
    fi

    # Deleting migration files excluding __init__.py
    for dir in $MIGRATIONS_DIR; do
        if [ -e "$dir" ]; then
            find "$dir" -type f ! -name "__init__.py" -exec rm {} \;
            echo "Migration files in $dir deleted, excluding __init__.py."
        fi
    done
    echo "----------------------------------------"

    # Creating the db.sqlite3 file
    if [ "$DELETE_DB" == true ]; then
      touch "$DB_FILE"
      echo "db.sqlite3 file created."
      echo "----------------------------------------"
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


