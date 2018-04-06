import pymysql
from functools import wraps

class mariadb:
    def __init__(self, user, password):
        self.db=pymysql.connect("localhost", user, password, "discord", charset='utf8')

    def commit(self):
        self.db.commit()

    def __del__(self):
        self.db.close()

    def get_settings(self):
        with self.db.cursor() as cursor:
            sql="SELECT * FROM settings"
            cursor.execute(sql)
        self.commit()
        return cursor.fetchone()

    def set_prefix(self, new_prefix):
        with self.db.cursor() as cursor:
            sql="UPDATE settings SET prefix=%s"
            cursor.execute(sql, (new_prefix,))
        self.commit()
        return cursor.fetchone()

    def check_permissions(self, channel, user):
        with self.db.cursor() as cursor:
            sql="UPDATE users SET points=points+1 WHERE discord_id=%s"
            cursor.execute(sql, (user_id,))
        self.commit()
        return cursor.fetchone()


    def give_coin(self, user_id):
        with self.db.cursor() as cursor:
            sql="UPDATE users SET points=points+1 WHERE discord_id=%s"
            cursor.execute(sql, (user_id,))
        self.commit()
        return cursor.fetchone()
