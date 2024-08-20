import json
import uuid
from flask import request, make_response


class CookieUserRepository:
    def __init__(self, request):
        self.request = request
        self.users = self._load_users_from_cookies()

    def _load_users_from_cookies(self):
        users_json = self.request.cookies.get('users', '[]')
        return json.loads(users_json)

    def get_content(self):
        return self.users

    def find(self, id):
        for user in self.users:
            if str(user['id']) == str(id):
                return user
        return None

    def save(self, user):
        if not (user.get('nickname') and user.get('email')):
            raise Exception(f'Wrong data: {json.dumps(user)}')

        if 'id' not in user or not user['id']:
            user['id'] = str(uuid.uuid4())

        existing_user = self.find(user['id'])
        if existing_user:
            self.users = [u if u['id'] != user['id'] else user for u in self.users]
        else:
            self.users.append(user)

        return self.users

    def delete(self, user):
        self.users = [u for u in self.users if u['id'] != user['id']]
        return self.users

    def save_users_to_response(self, response):
        response.set_cookie('users', json.dumps(self.users))
        return response
