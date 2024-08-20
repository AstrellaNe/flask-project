# user_repository.py
import json
import sys
import uuid
from utils import save_users

class UserRepository:
    def __init__(self):
        with open("./data/users.json", 'r') as f:
            self.users = json.load(f)  # Загрузка всего массива JSON

    def get_content(self):
        return self.users

    def find(self, id):
        try:
            for user in self.users:
                if str(user['id']) == str(id):
                    return user
            return None  # Возврат None, если пользователь не найден
        except KeyError:
            sys.stderr.write(f'Wrong user id: {id}')
            raise

    def save(self, user):
        if not (user.get('nickname') and user.get('email')):
            raise Exception(f'Wrong data: {json.dumps(user)}')

        # Генерация нового UUID если это новый пользователь
        if 'id' not in user or not user['id']:
            user['id'] = str(uuid.uuid4())  # Присваиваем UUID

        existing_user = self.find(user['id'])
        if existing_user:
            self.users.remove(existing_user)
        self.users.append(user)
        self.save_users()

    def delete(self, user):
        self.users.remove(user)  # Удаляем пользователя из списка
        self.save_users()  # Сохраняем изменения

    def save_users(self):
        save_users(self.users)  # Сохраняем всех пользователей
