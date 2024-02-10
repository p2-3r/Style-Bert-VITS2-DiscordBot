import discord
import wave
import asyncio
import re

import data as f_data
import voice as f_voice

TOKEN = f_data.read()["settings"]["bot_token"]

listen_channel = {}
play_waitlist = {}
prefix = f_data.read()["settings"]["prefix"]
read_limit = f_data.read()["settings"]["read_limit"]

intents=discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="{prefix}helpでhelpを表示".format(prefix=prefix)))
    print('BOTの起動が完了しました')
    

@client.event
async def on_message(message):
    global listen_channel
    global play_waitlist
    global prefix

    if message.author.bot:
        return
    
    elif message.content == prefix + "help":
        embed = discord.Embed(title="このBOTのヘルプ")
        embed.add_field(name="**{prefix}ping**".format(prefix=prefix),value="pong!")
        embed.add_field(name="**{prefix}join**".format(prefix=prefix),value="使用した人がいるボイスチャンネルに接続します")
        embed.add_field(name="**{prefix}leave**".format(prefix=prefix),value="ボイスチャンネルから切断します")
        embed.add_field(name="**{prefix}change_voice**".format(prefix=prefix),value="使用する声を変更するためのコマンドのヘルプを表示します")
        await message.channel.send(embed=embed)
    
    elif message.content == prefix + "ping":
        await message.channel.send("pong!")

    elif message.content == prefix + 'join':
        if message.author.voice is None:
            await message.channel.send("ボイスチャンネルに接続してから使用してください")
            return
        elif message.guild.voice_client is None:
            listen_channel[message.guild.id] = message.channel.id
            await message.author.voice.channel.connect()
            await message.channel.send("接続しました\n読み上げるチャンネル: **" + message.channel.name + "**")

            try:
                play_waitlist[message.guild.id].append({"content": "接続しました", "userid": message.author.id})
            except KeyError:
                play_waitlist[message.guild.id] = []
                play_waitlist[message.guild.id].append({"content": "接続しました", "userid": message.author.id})

            playsound_list = play_waitlist[message.guild.id]
                
            if len(playsound_list) == 1: 
                while playsound_list != []:
                    path = f_voice.create_voice(playsound_list[0]["content"], playsound_list[0]["userid"])

                    try:
                        message.guild.voice_client.play(discord.FFmpegPCMAudio(path))
                    except discord.errors.ClientException:
                        playsound_list = []
                        return

                    with wave.open(path, 'rb') as f:
                        fr = f.getframerate()
                        fn = f.getnframes()

                    await asyncio.sleep(1.0 * (fn/fr) + 0.25)
                    playsound_list.pop(0)
        
        elif message.guild.voice_client is not None:
            await message.channel.send("すでにボイスチャンネルに接続しています")
            return

    elif message.content == prefix + "leave":
        if message.guild.voice_client is None:
            await message.channel.send("接続していません")
            return
        
        listen_channel.pop(message.guild.id)
        play_waitlist[message.guild.id] = []
        await message.guild.voice_client.disconnect()
        await message.channel.send("退出しました")

    elif message.content.startswith(prefix + "change_voice"):
        msg_len = len(message.content)

        if msg_len <= 15:
            embed = discord.Embed(title="**change_voice** コマンドの使用方法")
            embed.add_field(name="__**{prefix}change_voice models**__".format(prefix=prefix),value="modelsコマンドでモデル一覧を表示\nmodels (数字)で(数字)のモデルに変更\nex. **{prefix}change_voice models 0**".format(prefix=prefix))
            embed.add_field(name="__**{prefix}change_voice length**__".format(prefix=prefix),value="length (数字)で話す速度を変更\nex.**{prefix}change_voice length 1**".format(prefix=prefix))
            await message.channel.send(embed=embed)

        else:
            if message.content.startswith(prefix + "change_voice models"):
                if msg_len <= 20 + len(prefix):
                    model_list = f_voice.get_model()[1]
                    embed = discord.Embed(title="使用できるモデルのリスト",description="{model_list}\nex.**{prefix}change_voice models 1**".format(prefix=prefix, model_list=model_list))
                    await message.channel.send(embed=embed)
                else:
                    try:
                        int(message.content[20 + len(prefix):])
                    except ValueError:
                        await message.channel.send("idに数字以外が含まれています `" + message.content[0:19 + len(prefix)] + "`__**`" + message.content[20 + len(prefix):] + "`**__")
                        return
                
                    input_id = f_data.fullnum2halfnum(message.content[20 + len(prefix):])

                    database = f_data.read()
                    if not str(message.author.id) in database["user_data"]:
                        f_data.create_userdata(message.author.id)
                        database = f_data.read()

                    if input_id in f_voice.get_model()[0]:
                        database["user_data"][str(message.author.id)]["model_id"] = input_id
                        f_data.write(database)

                        await message.channel.send("使用するモデルを **" + f_voice.get_model()[0][input_id] + "** に変更しました")
                    else:
                        await message.channel.send("モデル: **" + input_id + "** は存在しません")
                        return
                    
            if message.content.startswith(prefix + "change_voice length"):
                if msg_len <= 20 + len(prefix):
                    embed = discord.Embed(title="使用方法",description="{prefix}change_voice length (数字)\nex.**{prefix}change_voice length 1**".format(prefix=prefix))
                    await message.channel.send(embed=embed)
                else:
                    try:
                        l = float(f_data.fullnum2halfnum(message.content[20 + len(prefix):]))
                        if l <= 0.1:
                            input_length = "0.1"
                        elif l >= 5:
                            input_length = "5"
                        else:
                            input_length = f_data.fullnum2halfnum(message.content[20 + len(prefix):])
                        
                    except ValueError:
                        await message.channel.send("lengthに数字以外が含まれています `" + message.content[0:19 + len(prefix)] + "`__**`" + message.content[20 + len(prefix):] + "`**__")
                        return

                    database = f_data.read()
                    if not str(message.author.id) in database["user_data"]:
                        f_data.create_userdata(message.author.id)
                        database = f_data.read()

                    database["user_data"][str(message.author.id)]["length"] = input_length
                    f_data.write(database)

                    await message.channel.send("lengthを **{input_length}** に変更しました".format(input_length=input_length))

    elif message.guild.voice_client is not None:

        if message.channel.id == listen_channel[message.guild.id]:

            if message.content != "":

                if len(message.content) >= read_limit:
                    message.content = message.content[:read_limit] + "、以下略"

                try:
                    play_waitlist[message.guild.id].append({"content": message.content, "userid": message.author.id})
                except KeyError:
                    play_waitlist[message.guild.id] = []
                    play_waitlist[message.guild.id].append({"content": message.content, "userid": message.author.id})

                playsound_list = play_waitlist[message.guild.id]
                
                if len(playsound_list) == 1: 
                    while playsound_list != []:
                        path = f_voice.create_voice(playsound_list[0]["content"], playsound_list[0]["userid"])

                        try:
                            message.guild.voice_client.play(discord.FFmpegPCMAudio(path))
                        except discord.errors.ClientException:
                            playsound_list = []
                            return

                        with wave.open(path, 'rb') as f:
                            fr = f.getframerate()
                            fn = f.getnframes()

                        await asyncio.sleep(1.0 * (fn/fr) + 0.25)
                        playsound_list.pop(0)
                
@client.event
async def on_voice_state_update(member, before, after):

    if before.channel is not None:
        if len(before.channel.members) == 1:
            if before.channel.members[0] == client.user:
                play_waitlist[before.channel.guild.id] = []
                await before.channel.guild.voice_client.disconnect()
                    
                channel_id = listen_channel.pop(before.channel.guild.id)
                channel = client.get_channel(channel_id)
                await channel.send("ボイスチャンネルがBOTのみになったので自動退出しました")
        

    
client.run(TOKEN)