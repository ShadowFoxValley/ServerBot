from discord import Embed, utils
from random import shuffle, randint
from permissions import check_permission

import shadowDB as database

db_user = "discord"
db_pass = "truePass"
mariadb = database.mariadb(db_user, db_pass)

"""
Служебные команды
Триггерятся от админов или от тела программы
"""


class ProcessFunction():

    def __init__(self, message):
        self.message = message
        self.user = message.author

    @staticmethod
    def get_settings():
        global mariadb
        settings = mariadb.get_settings()
        return settings


    @staticmethod
    def make_deleted_message(message):
        embed = Embed(color=0x284fb5)
        embed.set_author(name=str(message.author.name), icon_url=str(message.author.avatar_url))
        embed.add_field(name="Удаленное сообщение", value=message.content, inline=False)
        return embed


    @staticmethod
    def make_edited_message(before, after):
        embed = Embed(color=0x284fb5)
        embed.set_author(name=str(before.author.name), icon_url=str(before.author.avatar_url))
        embed.add_field(name="Было", value=before.content, inline=False)
        embed.add_field(name="Стало", value=after.content, inline=False)
        return embed


    @staticmethod
    def new_user(member):
        global mariadb
        mariadb.new_user(member)


    def give_coin(self, points):
        global mariadb
        mariadb.give_coin(self.user.id, points)


    def set_prefix(self, new_prefix):
        """
        Установка нового префикса
        """
        global mariadb
        if check_permission(self.get_status(), "setprefix"):
            mariadb.set_prefix(new_prefix)

    def give(self):
        """
        Установка нового префикса
        """
        global mariadb
        if check_permission(self.get_status(), "give"):
            user = self.message.mentions
            if len(user) == 0:
                return ["text", "Пингани хоть одного"]

            msg_parts = self.message.content.replace("  ", " ").split(" ")
            if len(msg_parts) < 3:
                return ["text", "Ты что-то пропустил"]

            mariadb.give_coin(user[0].id, int(msg_parts[2]))
            return ["text", "Накинул %s %s пойнтов"%(user[0].mention, msg_parts[2])]

    def adduser(self):
        """
        Добавить пользователя вручную
        """
        global mariadb
        if check_permission(self.get_status(), "adduser"):
            user = self.message.mentions
            if len(user) == 0:
                return ["text", "Пингани хоть одного"]
            self.new_user(user[0])
            return ["text", "Добавил %s в базу"%(user[0].mention)]



    def get_status(self):
        global mariadb
        status = mariadb.get_status(self.user.id)
        return status

    """
        Команды для плебеев
        Могут использовать все
    """

    names = ["hots", "настолочник", "minecraft", "riddler", "блок", "easyblock", "технарь", "lol", "антисрач", "eventblock", "voice", "fox", "lizards", "weeb", "steampunk", "panda", "cat", "meme-boy", "shadow", "аниме"]

    def check_role(self):
        """
            Проверка роли
        """
        request_role = self.message.content.split(" ")[1]
        role = utils.get(self.message.server.roles, name=request_role)

        if role == None:
            return ["text", "Я не знаю такой роли"]

        if mariadb.get_points(self.user.id) < 25:
            return ["text", "Иди работай, у тебя даже 25 пойнтов нет."]

        if role.name == "Аниме":
            return ["text", "Никакого аниме в мою смену"]

        if role.name.lower() in self.names:
            return ["role", role]
        else:
            return ["text", "Ага, щас"]

    def doge(self):
        """
        Доге
        """
        permits = ["374914059679694848", "421637061787779072", "431897105163091979"]
        if self.message.channel.id not in permits:
            return
        if not check_permission(self.get_status(), "doge"):
            return

        embed = Embed(color=0x00ff00)
        embed.set_author(name=str(self.user.name), icon_url=str(self.user.avatar_url))
        lines = [line.rstrip('\n') for line in open('data_lists/dogelist')]
        for i in range(10):
            shuffle(lines)
        embed.set_image(url=lines[randint(0, len(lines)-1)])

        return ["embed", embed]


    def help_command(self, bot, prefix):
        """
        Справка по командам
        """
        if not check_permission(self.get_status(), "help"):
            return

        embed = Embed(color=0x00ff00)
        embed.set_author(name=str(bot.name), icon_url=str(bot.avatar_url))
        embed.set_thumbnail(url="https://happycoin.club/wp-content/uploads/2017/05/dogecoin_2.png")

        embed.add_field(name="Забавы",
                        value=("`{0}doge`- получить порцию доге\n"
                               "`{0}points` - посчитать догекоины в кошельке\n"
                               "`{0}top` - получить топ богачей"
                               ).format(prefix),
                        inline=False
                        )
        return ["embed", embed]


    def points(self):
        """
        Посчитать поинты пользователя.
        """
        if not check_permission(self.get_status(), "points"):
            return

        global mariadb
        points = mariadb.get_points(self.user.id)

        embed = Embed(color=0x00ff00)
        embed.set_author(name=str(self.user.name), icon_url=str(self.user.avatar_url))
        embed.add_field(name="Статистика", value="{0} догекойнов\n{1} место в топе".format(str(points[0]), str(points[1])), inline = True)
        return ["embed", embed]


    def get_top_list(self):
        """
        Получить топ пользователей
        """
        if not check_permission(self.get_status(), "top"):
            return

        global mariadb
        users = mariadb.get_top()

        embed = Embed(color=0x00ff00)
        embed.set_author(name=str(self.user.name), icon_url=str(self.user.avatar_url))
        embed.set_thumbnail(url="https://happycoin.club/wp-content/uploads/2017/05/dogecoin_2.png")
        count = 1
        for user in users:
            if count == 4:
                embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.add_field(name="{}. {}".format(count, user[0]),
                            value="%s догекойнов" % (str(user[1])),
                            inline=False if count < 4 else True)
            count += 1
        return ["embed", embed]
