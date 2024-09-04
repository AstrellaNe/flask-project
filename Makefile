start:
	# Проверяем, доступен ли сервер PostgreSQL; если нет, запускаем его и ждем 2 секунды
	@pg_isready -q || (sudo service postgresql start && sleep 2)
	
	# Запускаем приложение Flask в режиме отладки на порту 8000
	flask --app users_app --debug run --port 8000

start-full:
	# Устанавливаем зависимости проекта
	make install
	
	# Собираем проект
	make build
	
	# Проверяем, доступен ли сервер PostgreSQL; если нет, запускаем его и ждем 2 секунды
	@pg_isready -q || (sudo service postgresql start && sleep 2)
	
	# Запускаем приложение Flask в режиме отладки на порту 8000
	flask --app example --debug run --port 8000

start-gunicorn:
	# Проверяем, доступен ли сервер PostgreSQL; если нет, запускаем его и ждем 2 секунды
	@pg_isready -q || (sudo service postgresql start && sleep 2)
	
	# Запускаем приложение с помощью Gunicorn с 4 рабочими процессами на порту 8000
	poetry run gunicorn --workers=4 --bind=127.0.0.1:8000 users_app:app

install:
	# Устанавливаем зависимости с помощью Poetry
	poetry install

poetry-build:
	# Собираем проект с помощью Poetry
	poetry build

publish: 
	# Публикуем пакет (тестовый запуск)
	poetry publish --dry-run

package-install:
	# Устанавливаем пакет из локального дистрибутива
	python3 -m pip install --user dist/*.whl
	
package-reinstall:
	# Принудительно переустанавливаем пакет из локального дистрибутива
	pip install --user --force-reinstall dist/*.whl

lint:	
	# Проверяем код на соответствие стандартам с помощью flake8
	poetry run flake8

git-prepare:
	# Собираем проект и переустанавливаем пакет перед добавлением в git
	make build
	make package-reinstall
	git add

build:
	# Запускаем скрипт сборки
	./build.sh
