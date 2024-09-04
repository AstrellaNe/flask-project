from flask import (
    Flask,
    flash,
    get_flashed_messages,
    render_template,
    redirect,
    url_for,
    abort,
    request,
    session  # Импортируем session
)
from validate import validate, validate_on_edit
from user_repository import UserRepository
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import DictCursor

# Загрузка переменных окружения из .env
load_dotenv()

# Подключение к базе данных
DATABASE_URL = os.getenv('DATABASE_URL',
                         'postgresql://scrat:nuts@127.0.0.1:5432/users')
conn = psycopg2.connect(DATABASE_URL)

# Получение секретного ключа из переменных окружения или его генерация
secret_key = os.getenv('SECRET_KEY', os.urandom(24))


# Инициализация Flask приложения
app = Flask(__name__)
app.secret_key = secret_key  # Используем секретный ключ


# Инициализация репозитория пользователей
repo = UserRepository(conn)


# путь к файлу с данными пользователей (для файлового хранилища)
USER_DATA_FILE = './data/users.json'


# Обработчик ошибки 404 (страница не найдена)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('users/404.html'), 404


# Функция для инициализации базы данных
def init_db():
    with conn.cursor() as cursor:
        with open('./data/init.sql', 'r') as f:
            cursor.execute(f.read())
        conn.commit()


# Маршрут для создания нового пользователя
@app.route('/users/new', methods=['GET', 'POST'])
def users_new():
    if request.method == 'POST':
        user = request.form.to_dict()
        errors = validate(user)

        if errors:
            return render_template('users/new.html',
                                   user=user, errors=errors)

        repo.save(user)
        flash('Пользователь успешно добавлен', 'success')
        return redirect(url_for('users_get'))

    return render_template('users/new.html', user={}, errors={})


# Маршрут для отображения списка пользователей
@app.route('/users', methods=['GET'])
def users_get():
    search_query = request.args.get('search', '').strip().lower()
    users = repo.get_content()
    if search_query:
        users = [user for user in users
                 if search_query in user['nickname'].lower()
                 or search_query in user['email'].lower()]
    flashed_messages = get_flashed_messages(with_categories=True)
    return render_template('users/users.html',
                           users=users, messages=flashed_messages)


# Маршрут для отображения деталей пользователя
@app.route('/users/<string:id>', methods=['GET'])
def user_detail(id):
    user = repo.find(str(id))

    if user is None:
        abort(404)

    return render_template('users/show.html', user=user)


# Редактирование пользователя - форма
@app.route('/users/<string:id>/edit', methods=['GET'])
def edit_user(id):
    user = repo.find(str(id))
    if user is None:
        abort(404)
    errors = {}
    return render_template('users/edit.html',
                           user=user, errors=errors)


# Сохранение изменений после редактирования
@app.route('/users/<int:id>/update', methods=['GET', 'POST'])
def update_user(id):
    user = repo.find(id)
    if not user:
        abort(404)

    if request.method == 'POST':
        updated_user = request.form.to_dict()
        errors = validate_on_edit(updated_user)

        if errors:
            return render_template('users/edit.html', user=user, errors=errors)

        # Удаляем поле user_password, если оно пустое, чтобы не обновлять пароль
        if not updated_user.get('user_password'):
            updated_user.pop('user_password', None)

        updated_user['id'] = id
        repo.update(updated_user)
        flash('Информация о пользователе успешно обновлена', 'success')
        return redirect(url_for('users_get', id=id))

    return render_template('users/edit.html', user=user, errors={})


# Удаление пользователя
@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    repo.delete(id)
    flash('Пользователь успешно удален', 'success')
    return redirect(url_for('users_get'))


# Маршрут для отображения index
@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('users_get'))


# Технический маршрут для очистки сессии
@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect(url_for('users_get'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
