import pymysql

class mariadb:
    def __init__(self, user, password):
        self.db=pymysql.connect("localhost", user, password, "discord", charset='utf8')

    def commit(self):
        self.db.commit()

    def __del__(self):
        self.db.close()

    def get_settings(self):
        """
        Получение настроек из базы данных.
        """
        with self.db.cursor() as cursor:
            sql="SELECT * FROM settings"
            cursor.execute(sql)
        self.commit()
        return cursor.fetchone()

    def set_prefix(self, new_prefix):
        """
        Установка нового префикса для команд.
        """
        with self.db.cursor() as cursor:
            sql="UPDATE settings SET prefix=%s"
            cursor.execute(sql, (new_prefix,))
        self.commit()
        return cursor.fetchone()

    def get_status(self, user_id):
        """
        Получение статуса пользователя из базы данных

        Не знаю почему падает. Оно меня бесит.
        Вроде все данные приходят, но иногда просто получаем пустой массив в курсор.
        """
        try:
            with self.db.cursor() as cursor:
                sql="SELECT status FROM users WHERE discord_id=%s LIMIT 1"
                cursor.execute(sql, (user_id,))
            self.commit()

            result=cursor.fetchall()
            return result[0][0]
        except Exception as e:
            return 1


    def give_coin(self, user_id):
        """
        Выдача коинов пользователю.
        """
        with self.db.cursor() as cursor:
            sql="UPDATE users SET points=points+1 WHERE discord_id=%s"
            cursor.execute(sql, (user_id,))
        self.commit()
        return cursor.fetchone()

    def new_user(self, member):
        """
        Создание нового пользователя в базе данных.
        """
        with self.db.cursor() as cursor:
            sql="INSERT INTO users (discord_id, username) VALUES (%s, %s)"
            cursor.execute(sql, (member.id, member.name))
        self.commit()

    def get_points(self, user_id):
        """
        Получить поинты пользователя из базы данных и его место
        """
        with self.db.cursor() as cursor:
            sql = "SELECT points, discord_id FROM users ORDER BY points DESC"
            cursor.execute(sql)
        users=cursor.fetchall()

        count=1
        for user in users:
            if str(user[1])==str(user_id):
                return [user[0], count]
            count+=1

    def get_top(self):
        """
        Получение топ-10
        """
        with self.db.cursor() as cursor:
            sql="SELECT username, points FROM users ORDER BY points DESC LIMIT 9"
            cursor.execute(sql)
        self.commit()
        return cursor.fetchall()
