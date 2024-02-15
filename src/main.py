import wave
import re
import asyncio

import discord
import discord.app_commands
import requests

import data as f_data
import voice as f_voice
import colorprint as f_print
import commands as f_com

TOKEN = f_data.read()["settings"]["bot_token"]

listen_channel = {}
play_waitlist = {}
prefix = f_data.read()["settings"]["prefix"]
read_limit = f_data.read()["settings"]["read_limit"]
pre_joinvoice = False

intents=discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


if __name__ == '__main__':
    #SLASHCOMMANDS---------------------------------------------

    @tree.command(
        name="ping",
        description="pong!"
    )
    async def ping(ctx:discord.Interaction):
        reply = f_com.ping.main()
        await ctx.response.send_message(reply.content, ephemeral=True)

    @tree.command(
        name="help",
        description="helpを表示します。"
    )

    @discord.app_commands.guild_only

    async def help(ctx:discord.Interaction):
        reply = f_com.help.main()
        await ctx.response.send_message(embed=reply.embed)

    @tree.command(
        name="wav",
        description="指定した内容の音声を生成して添付します。"
    )

    @discord.app_commands.guild_only

    async def wav(ctx:discord.Interaction, text:str):

        await ctx.response.defer()

        try:
            reply = f_com.wav.main(text, ctx.user.id)
            await ctx.followup.send(reply.content, file=discord.File(reply.file))

        except AttributeError:
            await ctx.followup.send("APIが起動していないため音声を生成できませんでした。")

    @tree.command(
        name="join",
        description="使用するとあなたが現在いるボイスチャンネルに参加します。"
    )

    @discord.app_commands.guild_only

    async def join(ctx:discord.Interaction):
        if ctx.user.voice is None:
            await ctx.response.send_message("ボイスチャンネルに接続してから使用してください", ephemeral=True)
            return
        elif ctx.guild.voice_client is None:
            listen_channel[ctx.guild.id] = ctx.channel.id
            await ctx.user.voice.channel.connect()
            await ctx.response.send_message(f"接続しました\n読み上げるチャンネル: <#{str(ctx.channel.id)}>")

            try:
                f_voice.get_status()
            except requests.exceptions.ConnectionError:
                await ctx.followup.send("**現在、APIが起動していないため音声を生成することができません。**")
                f_print.printinfo.error("Audio could not be generated because the API was not activated.")

                if ctx.guild.voice_client is not None:
                    listen_channel.pop(ctx.guild.id)
                    play_waitlist[ctx.guild.id] = []
                    await ctx.guild.voice_client.disconnect()
                    return

            try:
                play_waitlist[ctx.guild.id].append({"content": "接続しました", "userid": ctx.user.id})
            except KeyError:
                play_waitlist[ctx.guild.id] = []
                play_waitlist[ctx.guild.id].append({"content": "接続しました", "userid": ctx.user.id})

            playsound_list = play_waitlist[ctx.guild.id]

            if len(playsound_list) == 1:
                while playsound_list:

                    path = f_voice.create_voice(playsound_list[0]["content"], playsound_list[0]["userid"])
                    ctx.guild.voice_client.play(discord.FFmpegPCMAudio(path))

                    with wave.open(path, 'rb') as f:
                        fr = f.getframerate()
                        fn = f.getnframes()

                    await asyncio.sleep(1.0 * (fn/fr) + 0.25)
                    playsound_list.pop(0)

        elif ctx.guild.voice_client is not None:
            await ctx.response.send_message("すでにボイスチャンネルに接続しています", ephemeral=True)
            return

    @tree.command(
        name="leave",
        description="ボイスチャンネルから退出します。"
    )

    @discord.app_commands.guild_only

    async def leave(ctx:discord.Interaction):

        if ctx.guild.voice_client is None:
            await ctx.response.send_message("接続していません", ephemeral=True)
            return
        if ctx.channel.guild.voice_client is not None:
            listen_channel.pop(ctx.guild.id)
            play_waitlist[ctx.guild.id] = []
            await ctx.guild.voice_client.disconnect()
            await ctx.response.send_message("退出しました")

    @tree.command(
        name="server_settings_status",
        description="現在のサーバーの設定を表示します。"
    )

    @discord.app_commands.guild_only

    async def server_settings_status(ctx:discord.Interaction):
        reply = f_com.server_settings.status.main(ctx.guild)
        await ctx.response.send_message(embed=reply.embed)


    @tree.command(
        name="server_settings_auto_join",
        description="自動参加の設定を切り替えます。"
    )

    @discord.app_commands.guild_only

    async def server_settings_auto_join(ctx:discord.Interaction):
        reply = f_com.server_settings.auto_join.main(ctx.guild, ctx.channel, ctx.user)
        await ctx.response.send_message(reply.content)


    @tree.command(
        name="server_settings_auto_ch",
        description="自動参加時に読み上げるチャンネルを設定します。"
    )

    @discord.app_commands.guild_only

    async def server_settings_auto_ch(ctx:discord.Interaction):
        reply = f_com.server_settings.auto_ch.main(ctx.guild, ctx.channel, ctx.user)
        await ctx.response.send_message(reply.content)

    @tree.command(
        name="change_voice_models_list",
        description="使用できる声の一覧を表示します。"
    )

    @discord.app_commands.guild_only

    async def change_voice_models_list(ctx:discord.Interaction):
        reply = f_com.change_voice.help.main()
        await ctx.response.send_message(embed=reply.embed)

    @tree.command(
        name="change_voice_models",
        description="使用する声を変更します。"
    )

    @discord.app_commands.guild_only

    async def change_voice_models(ctx:discord.Interaction, model_number:int):
        reply = f_com.change_voice.models.main(ctx.user,str(model_number))
        await ctx.response.send_message(reply.content)

    @tree.command(
        name="change_voice_length",
        description="読み上げ速度を変更します。"
    )

    @discord.app_commands.guild_only

    async def change_voice_length(ctx:discord.Interaction, length:float):
        reply = f_com.change_voice.length.main(ctx.user, length)
        await ctx.response.send_message(reply.content)

    #SLASHCOMMANDS---------------------------------------------

    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Game(name=f"{prefix}helpでhelpを表示"))

        f_print.printinfo.complete("Bot launch completed.")

        f_print.printinfo.info("Sync SlashCommand...")

        await tree.sync()

        f_print.printinfo.complete("Sync completed.")


    @client.event
    async def on_message(message):
        global listen_channel
        global play_waitlist
        global prefix

        if message.author.bot:
            return

        elif message.channel.guild == None:
            if message.content.startswith(prefix):
                await message.channel.send("このBOTの機能はDMでは利用できません")
            return

        elif message.content == f"{prefix}help":

            reply = f_com.help.main()

            await message.channel.send(embed=reply.embed)

        elif message.content == f"{prefix}ping":
            reply = f_com.ping.main()
            await message.channel.send(reply.content)

        elif message.content.startswith(f"{prefix}wav"):
            msg_len = len(message.content)
            if msg_len <= 4 + len(prefix):
                reply = f_com.wav.help()
                await message.channel.send(embed=reply.embed)
            else:
                printcontent = message.content[4 + len(prefix):]
                if printcontent != "":
                    reply = f_com.wav.main(printcontent, message.author.id)
                    try:
                        await message.channel.send(reply.content, file=discord.File(reply.file))
                    except AttributeError:
                        await message.channel.send("APIが起動していないため音声を生成することができませんでした。")

        elif message.content == f'{prefix}join':
            if message.author.voice is None:
                await message.channel.send("ボイスチャンネルに接続してから使用してください")
                return
            elif message.guild.voice_client is None:
                listen_channel[message.guild.id] = message.channel.id
                await message.author.voice.channel.connect()
                await message.channel.send(f"接続しました\n読み上げるチャンネル: <#{str(message.channel.id)}>")

                try:
                    f_voice.get_status()
                except requests.exceptions.ConnectionError:
                    await message.channel.send("**現在、APIが起動していないため音声を生成することができません。**")
                    f_print.printinfo.error("Audio could not be generated because the API was not activated.")

                    if message.channel.guild.voice_client is not None:
                        listen_channel.pop(message.guild.id)
                        play_waitlist[message.guild.id] = []
                        await message.guild.voice_client.disconnect()
                        return

                try:
                    play_waitlist[message.guild.id].append({"content": "接続しました", "userid": message.author.id})
                except KeyError:
                    play_waitlist[message.guild.id] = []
                    play_waitlist[message.guild.id].append({"content": "接続しました", "userid": message.author.id})

                playsound_list = play_waitlist[message.guild.id]

                if len(playsound_list) == 1:
                    while playsound_list:

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

        elif message.content == f"{prefix}leave":
            if message.guild.voice_client is None:
                await message.channel.send("接続していません")
                return
            if message.channel.guild.voice_client is not None:
                listen_channel.pop(message.guild.id)
                play_waitlist[message.guild.id] = []
                await message.guild.voice_client.disconnect()
                await message.channel.send("退出しました")

        elif message.content.startswith(f"{prefix}server_settings"):
            msg_len = len(message.content)

            if msg_len <= 16 + len(prefix):
                reply = f_com.server_settings.help.main()
                await message.channel.send(embed=reply.embed)
            else:
                if message.content.startswith(f"{prefix}server_settings status"):
                    reply = f_com.server_settings.status.main(message.guild)
                    await message.channel.send(embed=reply.embed)

                elif message.content.startswith(f"{prefix}server_settings auto_join"):
                    reply = f_com.server_settings.auto_join.main(message.guild, message.channel, message.author)
                    await message.channel.send(reply.content)

                elif message.content.startswith(f"{prefix}server_settings auto_ch"):
                    reply = f_com.server_settings.auto_ch.main(message.guild, message.channel, message.author)
                    await message.channel.send(reply.content)

        elif message.content.startswith(f"{prefix}change_voice"):
            msg_len = len(message.content)
            if msg_len <= 13 + len(prefix):
                reply = f_com.change_voice.help.main()
                await message.channel.send(embed=reply.embed)
            else:
                if message.content.startswith(f"{prefix}change_voice models"):
                    if msg_len <= 20 + len(prefix):
                        reply = f_com.change_voice.models.help()
                        await message.channel.send(embed=reply.embed)
                    else:
                        if not message.content[20 + len(prefix):].isdigit():
                            await message.channel.send(f"idに数字以外が含まれています `{message.content[0:19 + len(prefix)]}`__**`{message.content[20 + len(prefix):]}`**__")
                            return

                        input_id = f_data.fullnum2halfnum(message.content[20 + len(prefix):])
                        reply = f_com.change_voice.models.main(message.author, input_id)
                        await message.channel.send(reply.content)

                if message.content.startswith(f"{prefix}change_voice length"):
                    if msg_len <= 20 + len(prefix):
                        reply = f_com.change_voice.length.help()
                        await message.channel.send(embed=reply.embed)
                    else:
                        try:
                            l = float(f_data.fullnum2halfnum(message.content[20 + len(prefix):]))
                        except ValueError:
                            await message.channel.send(f"lengthに数字以外が含まれています `{message.content[0:19 + len(prefix)]}`__**`{message.content[20 + len(prefix):]}`**__")
                            return
                        reply = f_com.change_voice.length.main(message.author, l)
                        await message.channel.send(reply.content)

        elif message.guild.voice_client is not None:

            if message.content.startswith(";"):
                return

            if message.channel.id == listen_channel[message.guild.id]:

                replace_dict = {'<:.+:.+>': '',
                                "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+": '、url、',
                                "```(.|\n)+```": "、コードブロック、"}

                for before, after in replace_dict.items():
                    message.content = re.sub(before, after, message.content)

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
                        while playsound_list:

                            try:
                                path = f_voice.create_voice(playsound_list[0]["content"], playsound_list[0]["userid"])
                            except requests.exceptions.ConnectionError:
                                f_print.printinfo.error("Audio could not be generated because the API was not activated.")
                                return

                            message.guild.voice_client.play(discord.FFmpegPCMAudio(path))

                            with wave.open(path, 'rb') as f:
                                fr = f.getframerate()
                                fn = f.getnframes()

                            await asyncio.sleep(1.0 * (fn/fr) + 0.25)
                            playsound_list.pop(0)

    @client.event
    async def on_voice_state_update(member, before, after):

        global pre_joinvoice

        if member.id == client.user.id:
            return

        if before.channel is not None:
            if len(before.channel.members) == 1:
                if before.channel.members[0] == client.user:
                    play_waitlist[before.channel.guild.id] = []
                    if before.channel.guild.voice_client is not None:
                        await before.channel.guild.voice_client.disconnect()
                        if before.channel.guild.id in listen_channel:
                            channel_id = listen_channel.pop(before.channel.guild.id)
                            channel = client.get_channel(channel_id)
                            await channel.send("ボイスチャンネルがBOTのみになったので自動退出しました")

        if after.channel is not None:
            if after.channel.guild.voice_client is None:
                if len(after.channel.members) == 1:
                    s_data = f_data.read_serverdata(after.channel.guild.id)
                    if s_data["auto_join"]:

                        if s_data["auto_join_read_channel"] is None:
                            return
                        elif pre_joinvoice:
                            return

                        pre_joinvoice = True

                        read_channel = client.get_channel(s_data["auto_join_read_channel"])

                        listen_channel[after.channel.guild.id] = read_channel.id
                        await asyncio.sleep(1)
                        if after.channel is not None:
                            await after.channel.connect()
                            await read_channel.send(f"接続しました\n読み上げるチャンネル: <#{str(read_channel.id)}>")
                        pre_joinvoice = False

    client.run(TOKEN)