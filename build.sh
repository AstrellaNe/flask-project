#!/bin/bash
echo "Starting build process"

# Проверка наличия переменной DATABASE_URL
if [ -z "$DATABASE_URL" ]; then
  echo "Error: DATABASE_URL is not set."
  exit 1
fi

# Проверка наличия файла database.sql
if [ ! -f database.sql ]; then
  echo "Error: database.sql file not found."
  exit 1
fi

# Запуск SQL-скрипта для инициализации базы данных
psql -a -d $DATABASE_URL -f database.sql
