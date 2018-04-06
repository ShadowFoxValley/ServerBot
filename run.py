import discord
import shadowDB as database

client = discord.Client()

db_user="discord"
db_pass="truePass"
mariadb=database.mariadb(db_user, db_pass)

settings=mariadb.get_settings()
prefix=settings[0]
token=settings[1]

debug_mode=False

@client.event
async def on_message(message):
    global prefix, mariadb, debug_mode
    if message.author == client.user:
        return

    if debug_mode==True and message.author.id!="252450403029876738":
        return

    if message.content.startswith('%stest'%(prefix)):
        await client.send_message(message.channel, '{}, приветики'.format(message.author.mention))

    elif message.content.startswith('%ssetprefix'%(prefix)):
        prefix=message.content.split(" ")[1]
        mariadb.set_prefix(prefix)
        await client.send_message(message.channel, 'Префикс изменен на ``{}``'.format(prefix))

    elif message.content.startswith('%sdebugmode'%(prefix)):
        if(debug_mode==False):
            debug_mode=True
        else:
            debug_mode=False
        await client.send_message(message.channel, 'Переключен режим')

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
