from discord import Embed
import random
import shadowDB as database

def doge(message):
    """
    Доге
    """
    permits=["bots", "programming", "botk"]
    if message.channel.name not in permits: return;

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

    embed.add_field(name = "%sdoge" % (prefix), value = "Получить порцию доге", inline = True)
    embed.add_field(name = "%spoints" % (prefix), value = "Посчитать шекели в кошельке", inline = True)
    return ["embed", embed]

def points(author):
    """
    Посчитать поинты пользователя.
    """
    id = author.id
    points = database.get_points(id)

    embed = Embed(color = 0x00ff00)
    embed.set_author(name = str(author.name), icon_url = str(author.avatar_url))
    embed.add_field(name = "Шекели", value = str(points), inline = true)
    return ["embed", embed]
