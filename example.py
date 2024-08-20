from flask import (
    Flask,
    flash,
    get_flashed_messages,
    render_template,
    redirect,
    url_for,
    abort,
    request
)
import os
from validate import validate, validate_on_edit
from user_repository import UserRepository

app = Flask(__name__)
app.secret_key = '%^(**###'

# Инициализация репозитория пользователей
repo = UserRepository()


# Обработчик 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('users/404.html'), 404


# Маршрут для создания нового пользователя
@app.route('/users/new', methods=['GET', 'POST'])
def users_new():
    if request.method == 'POST':
        user = request.form.to_dict()
        errors = validate(user)

        if errors:
            return render_template('users/new.html', user=user, errors=errors)

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
    user = repo.find(str(id))  # id должен быть строкой для сравнения в JSON

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
@app.route('/users/<int:id>/update', methods=['POST'])
def update_user(id):
    user = repo.find(str(id))
    if user is None:
        abort(404)

    data = request.form.to_dict()
    errors = validate_on_edit(data)

    if errors:
        return render_template('users/edit.html',
                               user=user, errors=errors), 422

    # Обновление данных пользователя
    user['nickname'] = data['nickname']
    user['email'] = data['email']

    repo.save(user)

    flash('Пользовательские данные успешно обновлены', 'success')
    return redirect(url_for('users_get'))  # Редирект на список пользователей


# Удаление пользователя
@app.route('/users/<string:id>/delete', methods=['POST'])
def delete_user(id):
    user = repo.find(id)
    if user is None:
        return 'Пользователь не найден', 404

    repo.delete(user)  # Удаляем пользователя и сохраняем изменения

    flash('Пользователь успешно удален', 'success')
    return redirect(url_for('users_get'))


# Маршрут для отображения приветствия (GET и POST)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return 'Hello, ты используешь метод POST для индекса!'
    return render_template('users/index.html')


# Маршрут для отображения index
@app.route('/index.html', methods=['GET'])
def index_router():
    return redirect(url_for('users_get'))


# Маршрут для отображения информации о курсе
@app.route('/courses/<string:id>', methods=['GET'])
def courses(id):
    return f'Course id: {id}'


if __name__ == '__main__':
    app.run(debug=True)
