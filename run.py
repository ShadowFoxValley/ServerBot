import discord
import shadowDB as database
import processing

client = discord.Client()

db_user="discord"
db_pass="truePass"
mariadb=database.mariadb(db_user, db_pass)

settings=mariadb.get_settings()
prefix=settings[0]
token=settings[1]

commands=["test", "setprefix", "doge", "help"]

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
    user_status = int(mariadb.get_status(message.author.id))


    if user_status==0:
        return

    if message_text.split(" ")[0].replace(prefix, "") in commands:

        command=message_text.split(" ")[0].replace(prefix, "")

        if user_status==2:
            if command=="test":
                result=["text", '{}, приветики'.format(message.author.mention)]

            if command=="setprefix":
                prefix=message.content.split(" ")[1]
                mariadb.set_prefix(prefix)
                result=["text", "Префикс изменен на ``%s``"%(prefix)]

        if user_status>=1:
            if command=="doge":
                result=processing.doge(message)

            elif command=="help":
                result=processing.help(message.author, prefix)

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
        msg = await client.wait_for_message(timeout=float(5), author=message.author)
        if msg==None:
            mariadb.give_coin(message.author.id)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(token)
