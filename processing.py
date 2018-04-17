from discord import Embed
import random

import shadowDB as database

db_user="discord"
db_pass="truePass"
mariadb=database.mariadb(db_user, db_pass)

"""

Служебные команды
Триггерятся от админов или от тела программы

"""

def get_settings():
    global mariadb
    settings=mariadb.get_settings()
    return settings

def give_coin(message):
    global mariadb
    mariadb.give_coin(message.author.id)


def set_prefix(new_prefix):
    """
    Установка нового префикса
    """
    global mariadb
    mariadb.set_prefix(new_prefix)

def get_status(user_id):
    global mariadb
    status = mariadb.get_status(user_id)
    return status

def make_deleted_message(message):
    embed = Embed(color = 0x284fb5)
    embed.set_author(name = str(message.author.name), icon_url = str(message.author.avatar_url))
    embed.add_field(name = "Удаленное сообщение", value = message.content, inline = False)
    return embed

def make_edited_message(before, after):
    embed = Embed(color = 0x284fb5)
    embed.set_author(name = str(before.author.name), icon_url = str(before.author.avatar_url))
    embed.add_field(name = "Было", value = before.content, inline = False)
    embed.add_field(name = "Стало", value = after.content, inline = False)
    return embed

def new_user(member):
    global mariadb
    mariadb.new_user(member)



"""

    Команды для плебеев
    Могут использовать все

"""

def doge(message):
    """
    Доге
    """
    permits=["374914059679694848", "421637061787779072", "431897105163091979"]
    if message.channel.id not in permits: return;

    embed = Embed(color = 0x00ff00)
    embed.set_author(name = str(message.author.name), icon_url = str(message.author.avatar_url))
    lines = [line.rstrip('\n') for line in open('data_lists/dogelist')]
    for i in range(10): random.shuffle(lines);
    embed.set_image(url = lines[random.randint(0, len(lines)-1)])

    return ["embed", embed]


def help(author, prefix):
    """
    Справка по командам
    """
    embed = Embed(color = 0x00ff00)
    embed.set_author(name = str(author.name), icon_url = str(author.avatar_url))
    embed.set_thumbnail(url = "https://happycoin.club/wp-content/uploads/2017/05/dogecoin_2.png")

    embed.add_field(name = "Забавы",
    value = ("`{0}doge`- получить порцию доге\n"
            "`{0}points` - посчитать догекоины в кошельке"
            ).format(prefix), inline = False)
    return ["embed", embed]



def points(author):
    """
    Посчитать поинты пользователя.
    """
    global mariadb
    points = mariadb.get_points(author.id)


    embed = Embed(color = 0x00ff00)
    embed.set_author(name = str(author.name), icon_url = str(author.avatar_url))
    embed.add_field(name = "Статистика", value = "{0} догекойнов\n{1} место в топе".format(str(points[0]), str(points[1])), inline = True)
    return ["embed", embed]



def get_top_list(author):
    """
    Получить топ пользователей
    """
    global mariadb
    users=mariadb.get_top()

    embed = Embed(color=0x00ff00)
    embed.set_author(name=str(author.name), icon_url=str(author.avatar_url))
    embed.set_thumbnail(url="https://happycoin.club/wp-content/uploads/2017/05/dogecoin_2.png")
    count=1
    for user in users:
        if count==4:
            embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="{}. {}".format(count, user[0]), value="%s догекойнов"%(str(user[1])),inline=False if count<4 else True)
        count+=1
    return ["embed", embed]
