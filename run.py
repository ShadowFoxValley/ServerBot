from discord import Client, utils
from processing import ProcessFunction

client = Client()


"""
    Без try выкидывает в логи ошибку discord.errors.HTTPException: BAD REQUEST (status code: 400)
    Решения адекватного не нашел
"""


@client.event
async def on_message_delete(message):
    try:
        if message.channel.id == "421637061787779072":
            await client.send_message(message.channel, embed=ProcessFunction.make_deleted_message(message))
    except Exception as e:
        pass


@client.event
async def on_message_edit(before, after):
    if before.content == after.content:
        return

    try:
        if before.channel.id == "421637061787779072":
            await client.send_message(before.channel, embed=ProcessFunction.make_edited_message(before, after))
    except Exception as e:
        pass


@client.event
async def on_member_join(member):
    print("New user - {}".format(member.name))
    ProcessFunction.new_user(member)


# Необходима для функционирования #event-log
last_users = ["null" for i in range(5)]
commands = ["test", "setprefix", "doge", "help", "points", "top", "wait", "hots", "get", "leave"]
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
    process = ProcessFunction(message)



    if message_text.split(" ")[0].replace(prefix, "") in commands:

        command = message_text.split(" ")[0].replace(prefix, "")

        if command == "test":
                result = ["text", '{}, приветики'.format(user.mention)]

        elif command == "setprefix":
                prefix = message.content.split(" ")[1]
                process.set_prefix(prefix)

                result = ["text", "Префикс изменен на ``%s``" % prefix]

        elif command == "doge":
                result = process.doge()

        elif command == "help":
                result = process.help_command(client.user, prefix)

        elif command == "points":
                result = process.points()

        elif command == "top":
                result = process.get_top_list()

        elif command == "get":
            result = process.check_role()
            if result[0] == "role":
                role = result[1]
                if role not in message.author.roles:
                    await client.send_message(message.channel, "{}, добавить ``{}`` будет стоить 25 догекойнов. Напиши ``да``, если согласен.".format(message.author.mention, role.name))
                    msg = await client.wait_for_message(timeout=float(7), author=message.author)
                    if msg == None:
                        await client.send_message(message.channel, "{}, время вышло.".format(message.author.mention))
                    elif msg.content.lower() == "да":
                        await client.add_roles(message.author, role)
                        process.give_coin(-25)
                        result=["text", "Теперь у тебя есть {}".format(role.name)]
                else:
                    result=["text", "У тебя уже есть эта роль."]

        elif command == "leave":
            result = process.check_role()
            if result[0] == "role":
                role = result[1]
                if role in message.author.roles:

                    await client.send_message(message.channel, "{}, удалить ``{}`` будет стоить 25 догекойнов. Напиши ``да``, если согласен.".format(message.author.mention, role.name))
                    msg = await client.wait_for_message(timeout=float(7), author=message.author)

                    if msg == None:
                        await client.send_message(message.channel, "{}, время вышло.".format(message.author.mention))
                    elif msg.content.lower() == "да":
                        await client.remove_roles(message.author, role)
                        process.give_coin(-25)
                        result=["text", "Теперь у тебя нет {}".format(role.name)]

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
            process.give_coin(1)

    del process

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

prefix, token = ProcessFunction.get_settings()

client.run(token)
