from psycopg2.extras import DictCursor

class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
            return [dict(user) for user in users]

    def find(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (id,))
            user = cur.fetchone()
            return dict(user) if user else None

    def create(self, user):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (nickname, email, user_password) VALUES (%s, %s, %s) RETURNING id",
                (user['nickname'], user['email'], user['user_password'])
            )
            user['id'] = cur.fetchone()[0]
        self.conn.commit()

    def update(self, user):
        with self.conn.cursor() as cur:
            if 'user_password' in user and user['user_password']:
                cur.execute(
                    "UPDATE users SET nickname = %s, email = %s, user_password = %s WHERE id = %s",
                    (user['nickname'], user['email'], user['user_password'], user['id'])
            )
            else:
                cur.execute(
                    "UPDATE users SET nickname = %s, email = %s WHERE id = %s",
                    (user['nickname'], user['email'], user['id'])
                )
        self.conn.commit()

    def delete(self, id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (id,))
        self.conn.commit()
