#!/bin/bash
read -p "Enter MySQL username: " USERNAME
read -sp "Enter MySQL password: " PASSWORD
echo

DB_NAME="VirusFactor"
mysql -u "$USERNAME" -p"$PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
mysql -u "$USERNAME" -p"$PASSWORD" "$DB_NAME" < "$(dirname "\$0")/database/VirusFactor.sql"

echo "Database import complete!"

if [ ! -f "./database/VirusFactor.sql" ]; then
    echo "Error: Please run this script from the 'VirusFactor' directory."
    exit 1
fi

pip install -r ./setup/requirements.txt