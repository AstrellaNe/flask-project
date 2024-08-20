from flask import session
import json
import uuid


class SessionUserRepository:
    def __init__(self):
        pass  # Убираем инициализацию, так как session недоступен

    def _load_users_from_session(self):
        users_json = session.get('users', '[]')
        return json.loads(users_json)

    def _save_users_to_session(self, users):
        session['users'] = json.dumps(users)

    def get_content(self):
        return self._load_users_from_session()

    def find(self, id):
        users = self._load_users_from_session()
        for user in users:
            if str(user['id']) == str(id):
                return user
        return None

    def save(self, user):
        users = self._load_users_from_session()
        if not (user.get('nickname') and user.get('email')):
            raise Exception(f'Wrong data: {json.dumps(user)}')

        if 'id' not in user or not user['id']:
            user['id'] = str(uuid.uuid4())

        existing_user = self.find(user['id'])
        if existing_user:
            users.remove(existing_user)
        users.append(user)
        self._save_users_to_session(users)

    def delete(self, user):
        users = self._load_users_from_session()
        users.remove(user)
        self._save_users_to_session(users)
