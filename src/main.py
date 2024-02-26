import wave
import re
import asyncio

import discord
import discord.app_commands
import aiohttp

import data as f_data
import voice as f_voice
import colorprint as f_print
import commands as f_com
import replace_text as f_rep
import global_

prefix = global_.prefix
TOKEN = f_data.read()["settings"]["bot_token"]

intents=discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

if __name__ == '__main__':
    if True:  # Slash_Commands
        @tree.command(
            name="ping",
            description="pong!"
        )
        async def ping(ctx:discord.Interaction):
            reply = f_com.ping()
            await ctx.response.send_message(reply, ephemeral=True)

        @tree.command(
            name="help",
            description="helpを表示します。"
        )

        @discord.app_commands.guild_only

        async def help(ctx:discord.Interaction):
            reply = f_com.help()
            await ctx.response.send_message(embed=reply)

        @tree.command(
            name="wav",
            description="指定した内容の音声を生成して添付します。"
        )

        @discord.app_commands.guild_only

        async def wav(ctx:discord.Interaction, text:str):

            await ctx.response.defer()

            try:
                reply = await f_com.wav.main(text, ctx.user.id, ctx.guild.id)
                await ctx.followup.send(reply.content, file=discord.File(reply.file))

            except AttributeError:
                await ctx.followup.send("APIが起動していないため音声を生成できませんでした。")

        @tree.command(
            name="join",
            description="使用するとあなたが現在いるボイスチャンネルに参加します。"
        )

        @discord.app_commands.guild_only

        async def join(ctx:discord.Interaction):
            reply = await f_com.join.join(ctx.user, ctx.guild, ctx.channel)
            await ctx.response.send_message(reply.content)
            if reply.continue_:
                reply = await f_com.join.play(ctx.user, ctx.guild)
                if reply is not None:
                    await ctx.followup.send(reply)

        @tree.command(
            name="leave",
            description="ボイスチャンネルから退出します。"
        )

        @discord.app_commands.guild_only

        async def leave(ctx:discord.Interaction):
            reply = await f_com.leave(ctx.guild)
            await ctx.response.send_message(reply)

        @tree.command(
            name="server_settings_status",
            description="現在のサーバーの設定を表示します。"
        )

        @discord.app_commands.guild_only

        async def server_settings_status(ctx:discord.Interaction):
            reply = f_com.server_settings.status(ctx.guild)
            await ctx.response.send_message(embed=reply.embed)


        @tree.command(
            name="server_settings_auto_join",
            description="自動参加の設定を切り替えます。"
        )

        @discord.app_commands.guild_only

        async def server_settings_auto_join(ctx:discord.Interaction):
            reply = f_com.server_settings.auto_join(ctx.guild, ctx.channel, ctx.user)
            await ctx.response.send_message(reply.content)


        @tree.command(
            name="server_settings_auto_ch",
            description="自動参加時に読み上げるチャンネルを設定します。"
        )

        @discord.app_commands.guild_only

        async def server_settings_auto_ch(ctx:discord.Interaction):
            reply = f_com.server_settings.auto_ch(ctx.guild, ctx.channel, ctx.user)
            await ctx.response.send_message(reply.content)

        @tree.command(
            name="server_settings_dict_onlyadmin",
            description="サーバー辞書の編集権限をユーザー全員と管理者限定で切り替えます。"
        )

        @discord.app_commands.guild_only

        async def server_settings_dict_onlyadmin(ctx:discord.Interaction):
            reply = f_com.server_settings.dictionary_only_admin(ctx.guild, ctx.user)
            await ctx.response.send_message(reply.content)

        @tree.command(
            name="change_voice_models_list",
            description="使用できる声の一覧を表示します。"
        )

        @discord.app_commands.guild_only

        async def change_voice_models_list(ctx:discord.Interaction):
            reply = await f_com.change_voice.models.help()
            await ctx.response.send_message(embed=reply.embed, view=reply.view)

        @tree.command(
            name="change_voice_models",
            description="使用する声を変更します。"
        )

        @discord.app_commands.guild_only

        async def change_voice_models(ctx:discord.Interaction, model_number:int):
            reply = await f_com.change_voice.models.main(ctx.user,str(model_number))
            await ctx.response.send_message(reply.content)

        @tree.command(
            name="change_voice_length",
            description="読み上げ速度を変更します。"
        )

        @discord.app_commands.guild_only

        async def change_voice_length(ctx:discord.Interaction, length:float):
            reply = f_com.change_voice.length.main(ctx.user, length)
            await ctx.response.send_message(reply.content)

        @tree.command(
            name="dictionary",
            description="辞書を表示します。"
        )

        @discord.app_commands.guild_only

        async def dictionary(ctx:discord.Interaction):
            reply = f_com.dictionary.display(ctx.guild)
            await ctx.response.send_message(embed=reply.embed, view=reply.view)

    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Game(name=f"{prefix}helpでhelpを表示"))

        f_print.printinfo.complete("Bot launch completed.")

        f_print.printinfo.info("Sync SlashCommand...")

        await tree.sync()

        f_print.printinfo.complete("Sync completed.")

    @client.event
    async def on_message(message):
        global prefix

        if message.author.bot:
            return

        elif message.channel.guild == None:
            if message.content.startswith(prefix):
                await message.channel.send("このBOTの機能はDMでは利用できません")
            return

        elif message.content == f"{prefix}help":

            reply = f_com.help()

            await message.channel.send(embed=reply)

        elif message.content == f"{prefix}ping":
            reply = f_com.ping()
            await message.channel.send(reply)

        elif message.content.startswith(f"{prefix}wav"):
            msg_len = len(message.content)
            if msg_len <= 4 + len(prefix):
                reply = f_com.wav.help()
                await message.channel.send(embed=reply.embed)
            else:
                printcontent = message.content[4 + len(prefix):]
                if printcontent != "":
                    reply = await f_com.wav.main(printcontent, message.author.id, message.guild.id)
                    try:
                        await message.channel.send(reply.content, file=discord.File(reply.file))
                    except AttributeError:
                        await message.channel.send("APIが起動していないため音声を生成することができませんでした。")

        elif message.content.startswith(f"{prefix}dictionary"):
            reply = f_com.dictionary.display(message.guild)
            await message.channel.send(embed=reply.embed, view=reply.view)

        elif message.content == f'{prefix}join':
            reply = await f_com.join.join(message.author, message.guild, message.channel)
            await message.channel.send(reply.content)
            if reply.continue_:
                reply = await f_com.join.play(message.author, message.guild)
                if reply is not None:
                    await message.channel.send(reply)

        elif message.content == f"{prefix}leave":
            reply = await f_com.leave(message.guild)
            await message.channel.send(reply)

        elif message.content.startswith(f"{prefix}server_settings"):
            msg_len = len(message.content)

            if msg_len <= 16 + len(prefix):
                reply = f_com.server_settings.help()
                await message.channel.send(embed=reply.embed)
            else:
                if message.content.startswith(f"{prefix}server_settings status"):
                    reply = f_com.server_settings.status(message.guild)
                    await message.channel.send(embed=reply.embed)

                elif message.content.startswith(f"{prefix}server_settings auto_join"):
                    reply = f_com.server_settings.auto_join(message.guild, message.channel, message.author)
                    await message.channel.send(reply.content)

                elif message.content.startswith(f"{prefix}server_settings auto_ch"):
                    reply = f_com.server_settings.auto_ch(message.guild, message.channel, message.author)
                    await message.channel.send(reply.content)

                elif message.content.startswith(f"{prefix}server_settings dict_onlyadmin"):
                    reply = f_com.server_settings.auto_join(message.guild, message.channel, message.author)
                    await message.channel.send(reply.content)

        elif message.content.startswith(f"{prefix}change_voice"):
            msg_len = len(message.content)
            if msg_len <= 13 + len(prefix):
                reply = f_com.change_voice.help()
                await message.channel.send(embed=reply.embed)
            else:
                if message.content.startswith(f"{prefix}change_voice models"):
                    if msg_len <= 20 + len(prefix):
                        reply = await f_com.change_voice.models.help()
                        await message.channel.send(embed=reply.embed, view=reply.view)
                    else:
                        if not message.content[20 + len(prefix):].isdigit():
                            await message.channel.send(f"idに数字以外が含まれています `{message.content[0:19 + len(prefix)]}`__**`{message.content[20 + len(prefix):]}`**__")
                            return

                        input_id = f_data.fullnum2halfnum(message.content[20 + len(prefix):])
                        reply = await f_com.change_voice.models.main(message.author, input_id)
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

            if message.channel.id == global_.listen_channel[message.guild.id]:

                message.content = f_rep.replace_text(message.content, client, message.guild.id)

                if message.content != "":

                    if len(message.content) >= global_.read_limit:
                        message.content = message.content[:global_.read_limit] + "、以下略"

                    await f_com.playsound.play(message.author, message.guild, message.content)

    @client.event
    async def on_voice_state_update(member, before, after):

        if member.id == client.user.id:
            return

        if before.channel is not None:
            if len(before.channel.members) == 1:
                if before.channel.members[0] == client.user:
                    global_.play_waitlist[before.channel.guild.id] = []

                    if before.channel.guild.voice_client is not None:
                        await before.channel.guild.voice_client.disconnect()

                        if before.channel.guild.id in global_.listen_channel:
                            channel_id = global_.listen_channel.pop(before.channel.guild.id)
                            channel = client.get_channel(channel_id)
                            await channel.send("ボイスチャンネルがBOTのみになったので自動退出しました")

        if after.channel is not None:
            if after.channel.guild.voice_client is None:

                if len(after.channel.members) == 1:
                    s_data = f_data.read_serverdata(after.channel.guild.id)
                    if s_data["auto_join"]:

                        if s_data["auto_join_read_channel"] is None:
                            return
                        elif global_.pre_joinvoice:
                            return

                        global_.pre_joinvoice = True

                        read_channel = client.get_channel(s_data["auto_join_read_channel"])

                        global_.listen_channel[after.channel.guild.id] = read_channel.id
                        await asyncio.sleep(1)
                        if after.channel is not None:
                            await after.channel.connect()
                            await read_channel.send(f"接続しました\n読み上げるチャンネル: <#{str(read_channel.id)}>")
                        global_.pre_joinvoice = False



    @client.event
    async def on_interaction(ctx: discord.Interaction):
        try:
            if ctx.data['component_type'] == 2:
                await on_button_click(ctx)
            elif ctx.data['component_type'] == 3:
                await on_dropdown(ctx)
        except KeyError:
            pass

    async def on_dropdown(ctx: discord.Interaction):
        if ctx.data["custom_id"] == "change_voice_models":
            select_list = ctx.data["values"][0].split(",")
            select_name, select_id = select_list[0], select_list[1]
            userdata = f_data.read_userdata(ctx.user.id)
            if userdata is not None:
                userdata["model_id"] = select_id
            else:
                f_data.create_userdata(ctx.user.id)
                userdata = f_data.read_userdata(ctx.user.id)
                userdata["model_id"] = select_id
            f_data.write_userdata(ctx.user.id, userdata)
            await ctx.response.send_message(f"使用するモデルを{select_name}に変更しました", ephemeral=True)

    async def on_button_click(ctx:discord.Interaction):
        is_admin = ctx.user.guild_permissions.administrator
        only_admin = f_data.read_serverdata(ctx.guild.id)["dictionary_only_admin"]

        if ctx.data["custom_id"] == "dict_add":
            if only_admin:
                if is_admin:
                    await ctx.response.send_modal(f_com.dictionary.Add_Modal())
                else:
                    await ctx.response.send_message("現在このサーバーでは管理者のみが辞書を変更できます", ephemeral=True)
            else:
                await ctx.response.send_modal(f_com.dictionary.Add_Modal())

        elif ctx.data["custom_id"] == "dict_remove":
            if only_admin:
                if is_admin:
                    await ctx.response.send_modal(f_com.dictionary.Remove_Modal())
                else:
                    await ctx.response.send_message("現在このサーバーでは管理者のみが辞書を変更できます", ephemeral=True)
            else:
                await ctx.response.send_modal(f_com.dictionary.Remove_Modal())

    client.run(TOKEN)