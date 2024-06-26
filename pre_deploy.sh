#!/bin/bash

# Script para inicializar un proyecto Django antes del despliegue

python -m venv env
env/bin/activate

pip install -r requirements.txt

# Definir variables
DJANGO_PROJECT_DIR="."  # Cambia esto por la ruta de tu proyecto Django
DJANGO_MANAGE_PY="$DJANGO_PROJECT_DIR/manage.py"
GUNICORN_CONF="$DJANGO_PROJECT_DIR/gunicorn_conf.py"  # Archivo de configuración de Gunicorn

# Activar el entorno virtual si lo estás utilizando
# source /ruta/a/tu/entorno_virtual/bin/activate  # Descomenta y cambia la ruta si es necesario

# Actualizar dependencias si es necesario
# pip install -r $DJANGO_PROJECT_DIR/requirements.txt  # Descomenta si necesitas instalar dependencias

# Realizar migraciones
echo "Realizando migraciones..."
python $DJANGO_MANAGE_PY makemigrations accounts main
python $DJANGO_MANAGE_PY migrate
python $DJANGO_MANAGE_PY loaddata ./accounts/fixtures/data.json

echo "Populando notas ..."
python ./scripts/populate.py

# Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python $DJANGO_MANAGE_PY collectstatic --noinput

echo "Pre-despliegue completado!!"
