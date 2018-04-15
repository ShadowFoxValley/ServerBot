import discord
import shadowDB as database
import processing

client = discord.Client()

commands=["test", "setprefix", "doge", "help", "points", "top"]

@client.event
async def on_member_join(member):
    global mariadb
    print("New user - {}".format(member.name))
    mariadb.new_user(member)

@client.event
async def on_message(message):
    global prefix, mariadb, commands

    if message.author == client.user:
        return

    user_id = message.author.id
    channel = message.channel
    message_text = message.content


    """
    # TODO:
            Убрать user_status. Заменить на нормальные права доступа для разграничения.
    """
    user_status = int(processing.get_status(message.author.id))

    if user_status==0:
        return

    if message_text.split(" ")[0].replace(prefix, "") in commands:

        command=message_text.split(" ")[0].replace(prefix, "")

        if user_status==2:
            if command=="test":
                result=["text", '{}, приветики'.format(message.author.mention)]

            if command=="setprefix":
                prefix=message.content.split(" ")[1]
                processing.set_prefix(prefix)
                result=["text", "Префикс изменен на ``%s``"%(prefix)]

        if user_status>=1:
            if command=="doge":
                result=processing.doge(message)

            elif command=="help":
                result=processing.help(client.user, prefix)

            elif command=="points":
                result = processing.points(message.author)

            elif command=="top":
                result = processing.get_top_list(message.author)


        """

            Отправка данных из переменной result

        """
        if result[0]=="embed":
            # Send embed message
            await client.send_message(message.channel, embed=result[1])

        elif result[0]=="text":
            # Send text
            await client.send_message(message.channel, result[1])

        elif result[0]=="file":
            # Send file
            await client.send_file(message.channel, result[1])

    else:
        """

            Если сообщение не является командой, то начислить балл.
            Имеется кд на 7 секунд против Скорча.
            Клиент ждет сообщение от пользователя. Если пришло в течении 7 секунд - сбросить кд и не начислять
            Если прошло 7 секунд и сообщения от пользователя нет - начислить балл.

        """
        msg = await client.wait_for_message(timeout=float(7), author=message.author)
        if msg==None:
            processing.give_coin(message)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

prefix, token = processing.get_settings()

client.run(token)
