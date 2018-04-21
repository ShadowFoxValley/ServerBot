import discord
import processing

client = discord.Client()


"""
    Без try выкидывает в логи ошибку discord.errors.HTTPException: BAD REQUEST (status code: 400)
    Решения адекватного не нашел
"""


@client.event
async def on_message_delete(message):
    try:
        if message.channel.id == "421637061787779072":
            await client.send_message(message.channel, embed=processing.make_deleted_message(message))
    except Exception as e:
        pass


@client.event
async def on_message_edit(before, after):
    if before.content == after.content:
        return

    try:
        if before.channel.id == "421637061787779072":
            await client.send_message(before.channel, embed=processing.make_edited_message(before, after))
    except Exception as e:
        pass


@client.event
async def on_member_join(member):
    print("New user - {}".format(member.name))
    processing.new_user(member)


last_users = ["null" for i in range(5)]


@client.event
async def on_message(message):
    global prefix, mariadb, commands, last_users

    if message.author == client.user:
        return

    user = message.author
    channel = message.channel
    message_text = message.content

    """

        Event block

    """

    if message.content.startswith("#event") and channel.id == "435792312778489856":
        if user.name in last_users:
            msg = "%s, подожди пока 5 человек что-то напишут" % user.mention
            await client.send_message(channel, msg)
        else:
            last_users.insert(0, user.name)
            del last_users[5]
            msg = "**" + user.name + "**: " + message.content.replace("#event", "")
            await client.send_message(client.get_channel("435883270945898496"), msg)

    """

        Command block

    """

    commands = ["test", "setprefix", "doge", "help", "points", "top", "wait"]
    if message_text.split(" ")[0].replace(prefix, "") in commands:

        command = message_text.split(" ")[0].replace(prefix, "")

        if command == "test":
                result = ["text", '{}, приветики'.format(user.mention)]

        elif command == "setprefix":
                prefix = message.content.split(" ")[1]
                processing.set_prefix(user, prefix)
                result = ["text", "Префикс изменен на ``%s``" % prefix]

        elif command == "doge":
                result = processing.doge(user, message)

        elif command == "help":
                result = processing.help_command(client.user, user, prefix)

        elif command == "points":
                result = processing.points(user)

        elif command == "top":
                result = processing.get_top_list(user)

        elif command == "wait":
                queue = "Вы пока что не можете писать историю:"
                counter = 1
                for user in last_users:
                    queue += "\n%d) %s" % (counter, user)
                    counter += 1
                result = ["text", queue]

        """

            Отправка данных из переменной result

        """
        if result is None:
            pass
        else:
            if result[0] == "embed":
            # Send embed message
                await client.send_message(message.channel, embed=result[1])

            elif result[0] == "text":
            # Send text
                await client.send_message(channel, result[1])

            elif result[0] == "file":
            # Send file
                await client.send_file(channel, result[1])

    else:
        """

            Если сообщение не является командой, то начислить балл.
            Имеется кд на 7 секунд против Скорча.
            Клиент ждет сообщение от пользователя. Если пришло в течении 7 секунд - сбросить кд и не начислять
            Если прошло 7 секунд и сообщения от пользователя нет - начислить балл.

        """
        msg = await client.wait_for_message(timeout=float(7), author=user)
        if msg is None:
            processing.give_coin(message)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

prefix, token = processing.get_settings()

client.run(token)
