#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar las librerías necesarias
pip install -r requirements.txt

# Recopilar todos los archivos estáticos (CSS, etc.) para producción
python manage.py collectstatic --no-input

# Aplicar las migraciones a la base de datos de producción
python manage.py migrate
