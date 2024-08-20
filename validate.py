import re
from utils import load_users


def validate_nickname(nickname, users):
    if not nickname:
        return "Поле 'nickname' не может быть пустым."
    elif len(nickname) < 2:
        return "Никнейм должен содержать минимум 2 символа."
    elif any(u['nickname'] == nickname for u in users):
        return "Такой никнейм уже существует."
    return None


def validate_email(email, users):
    if not email:
        return "Поле 'email' не может быть пустым."
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Email должен содержать символ '@'"
    elif any(u['email'] == email for u in users):
        return "Такой Email уже существует."
    return None


def validate(user):
    users = load_users()
    errors = {}

    nickname_error = validate_nickname(user.get('nickname'), users)
    if nickname_error:
        errors['nickname'] = nickname_error

    email_error = validate_email(user.get('email'), users)
    if email_error:
        errors['email'] = email_error

    return errors


def validate_on_edit(user):
    errors = {}

    if 'nickname' not in user or not user['nickname']:
        errors['nickname'] = "Поле 'nickname' не может быть пустым."
    elif len(user['nickname']) < 2:
        errors['nickname'] = "Никнейм должен содержать минимум 2 символа."

    # Валидация email
    if 'email' not in user or not user['email']:
        errors['email'] = "Поле 'email' не может быть пустым."
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", user['email']):
        errors['email'] = "Неверный формат email."

    return errors
