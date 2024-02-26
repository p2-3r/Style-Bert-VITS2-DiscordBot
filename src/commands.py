import wave
import asyncio

import discord
import aiohttp

import data as f_data
import voice as f_voice
import colorprint as f_print
import global_

prefix = global_.prefix

def ping() -> str:
    reply = "pong!"
    return reply

def help() -> discord.Embed:
    field_dict = {f"**{prefix}ping**": "pong!",
                  f"**{prefix}wav (content)**": "指定した内容を生成してその音声ファイルを添付したメッセージを送信します",
                  f"**{prefix}dictionary**": "サーバー辞書メニューを表示します",
                  f"**{prefix}join**": "使用した人がいるボイスチャンネルに接続します",
                  f"**{prefix}leave**": "ボイスチャンネルから切断します",
                  f"**{prefix}change_voice**": "使用する声を変更するためのコマンドのヘルプを表示します",
                  f"**{prefix}server_settings**": "自動参加などサーバーに関する設定のためのヘルプを表示します"}

    embed = discord.Embed(title="このBOTのヘルプ")

    for i, l in field_dict.items():
        embed.add_field(name=i,value=l)

    return embed

class Wav():
    async def main(self, content: str, user_id :int, server_id: int):
        self.content = f"「{content}」"
        try:
            self.file = await f_voice.create_voice(content, user_id, server_id)
        except aiohttp.client_exceptions.ClientConnectorError:
            f_print.printinfo.error("Audio could not be generated because the API was not activated.")

        return self

    def help(self):
        self.embed = discord.Embed(title="**wav** コマンドの使用方法", description=f"{prefix}wav (生成したい音声の内容)")
        return self

class Dictionary():
    def display(self, guild: discord.Guild):
        server_dict = f_data.read_server_dict(guild.id)

        if server_dict != {}:
            for i, [key, value] in enumerate(server_dict.items()):
                if i == 0:
                    dict_text = f"{key} -> {value}"
                else:
                    dict_text = dict_text + f"\n{key} -> {value}"
            if len(dict_text) <= 4095:
                self.embed = discord.Embed(title="このサーバーの辞書", description=dict_text)
            else:
                self.embed = discord.Embed(title="登録されている単語が多すぎたため表示できませんでした。")

        else:
            self.embed = discord.Embed(title="このサーバーではまだ何も登録されていません。")

        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="add", style=discord.ButtonStyle.primary, custom_id="dict_add"))
        view.add_item(discord.ui.Button(label="remove", style=discord.ButtonStyle.secondary, custom_id="dict_remove"))
        self.view = view

        return self

    class Add_Modal(discord.ui.Modal, title="単語と読み方の登録"):
        word = discord.ui.TextInput(label="単語", max_length=15)
        read = discord.ui.TextInput(label="読み方", max_length=15)

        async def on_submit(self, ctx: discord.Interaction):
            server_dict = f_data.read_server_dict(ctx.guild.id)
            server_dict[str(self.word)] = str(self.read)
            f_data.write_server_dict(ctx.guild.id, server_dict)
            await ctx.response.send_message(f"読み方を設定しました\n単語: **{self.word}** 読み方: **{self.read}**")

    class Remove_Modal(discord.ui.Modal, title="辞書の削除"):
        word = discord.ui.TextInput(label="削除したい単語", max_length=20)

        async def on_submit(self, ctx: discord.Interaction):
            server_dict = f_data.read_server_dict(ctx.guild.id)

            try:
                server_dict.pop(str(self.word))
            except KeyError:
                await ctx.response.send_message(f"辞書に 単語: **{self.word}** は存在しません", ephemeral=True)
                return

            f_data.write_server_dict(ctx.guild.id, server_dict)
            await ctx.response.send_message(f"辞書から読み方を削除しました\n削除した単語: **{self.word}**")


class Join():
    async def join(self, author: discord.User, guild: discord.Guild, channel: discord.TextChannel) -> classmethod:
        if author.voice is None:
            self.content = "ボイスチャンネルに接続してから使用してください"
            self.continue_ = False
            return self

        elif guild.voice_client is not None:
            self.content = "すでにボイスチャンネルに接続しています"
            self.continue_ = False
            return self

        elif guild.voice_client is None:
            global_.listen_channel[guild.id] = channel.id
            await author.voice.channel.connect()
            self.content = f"接続しました\n読み上げるチャンネル: <#{str(channel.id)}>"
            self.continue_ = True
            return self

    async def play(self, author: discord.User, guild: discord.Guild) -> str:

        try:
            l = await f_voice.get_status()
        except aiohttp.client_exceptions.ClientConnectorError:
            reply = "**現在、APIが起動していないため音声を生成することができません。**"
            f_print.printinfo.error("Audio could not be generated because the API was not activated.")

            if guild.voice_client is not None:
                global_.listen_channel.pop(guild.id)
                global_.play_waitlist[guild.id] = []
                await guild.voice_client.disconnect()

            return reply

        await playsound.play(author, guild, "接続しました")

async def leave(guild: discord.Guild) -> str:
    if guild.voice_client is None:
        reply = "接続していません"
        return reply

    elif guild.voice_client is not None:
        if guild.id in global_.play_waitlist:
            global_.play_waitlist[guild.id] = []
        await guild.voice_client.disconnect()
        reply = "退出しました"
        return reply

class Server_settings():
    def help(self):
        field_dict = {f"__**{prefix}server_settings status**__": "このサーバーの現在の設定を表示します。このsettingsコマンド以外はそのサーバーの管理者でないと使用できません",
                      f"__**{prefix}server_settings auto_join**__": "このコマンドの使用でボイスチャットに誰かが参加したとき自動参加するかしないかを切り替えられます",
                      f"__**{prefix}server_settings auto_ch**__": "自動参加時に読み上げるテキストチャンネルを設定します",
                      f"__**{prefix}server_settings dict_onlyadmin**__": "サーバー辞書を管理者だけかユーザー全員が編集できるようにするか切り替えます"}

        embed = discord.Embed(title="**settings** コマンドの使用方法")
        [embed.add_field(name=i,value=l) for i, l in field_dict.items()]

        self.embed = embed
        return self

    def status(self, guild: discord.guild):
        current_server_data = f_data.read_serverdata(guild.id)
        embed = discord.Embed(title=f"**{guild.name}** の現在設定")
        embed.add_field(name="ボイスチャンネルへの自動参加",value=str(current_server_data["auto_join"]))
        read_channel_id = str(current_server_data["auto_join_read_channel"])

        if read_channel_id.isdecimal():
            l = f"<#{read_channel_id}>"

        else:
            l = "None"

        embed.add_field(name="自動参加時に読み上げるチャンネル",value=l)
        self.embed = embed

        return self

    def auto_join(self, guild: discord.guild, channel: discord.channel, user: discord.user):
        if user.guild_permissions.administrator:
            current_server_data = f_data.read_serverdata(guild.id)

            if current_server_data["auto_join"] == False:
                current_server_data["auto_join"] = True
                p_ms = ""
                if current_server_data["auto_join_read_channel"] is None:
                    current_server_data["auto_join_read_channel"] = channel.id
                    p_ms = f"\n自動参加時の読み上げるチャンネルを <#{str(channel.id)}> に設定しました\n変更したい場合は `{prefix}server_settings auto_ch` コマンドを使用してください"

                ml = "ON"

            elif current_server_data["auto_join"] == True:
                current_server_data["auto_join"] = False
                p_ms = ""
                ml = "OFF"

            f_data.write_serverdata(guild.id, current_server_data)

            self.content = f"自動参加機能を**{ml}**にしました{p_ms}"
            return self
        else:
            self.content = "このコマンドはサーバーの管理者でないと使用できません"
            return self

    def auto_ch(self, guild: discord.guild, channel: discord.channel, user: discord.user):
        if user.guild_permissions.administrator:
            current_server_data = f_data.read_serverdata(guild.id)
            current_server_data["auto_join_read_channel"] = channel.id
            f_data.write_serverdata(guild.id, current_server_data)
            self.content = f"自動参加時の読み上げるチャンネルを <#{str(channel.id)}> に設定しました"
        else:
            self.content = "このコマンドはサーバーの管理者でないと使用できません"

        return self

    def dictionary_only_admin(self, guild: discord.guild, user: discord.user):
        if user.guild_permissions.administrator:
            current_server_data = f_data.read_serverdata(guild.id)

            if current_server_data["dictionary_only_admin"] == False:
                current_server_data["dictionary_only_admin"] = True

                ml = "サーバー管理者のみ"

            elif current_server_data["dictionary_only_admin"] == True:
                current_server_data["dictionary_only_admin"] = False
                ml = "ユーザー全員"

            f_data.write_serverdata(guild.id, current_server_data)

            self.content = f"サーバー辞書の編集権限を**{ml}**にしました"
            return self
        else:
            self.content = "このコマンドはサーバーの管理者でないと使用できません"
            return self

class Change_voice():
    def help(self):
        field_dict = {f"__**{prefix}change_voice models**__": f"modelsコマンドでモデル一覧を表示\nmodels (数字)で(数字)のモデルに変更\nex. **{prefix}change_voice models 0**",
                      f"__**{prefix}change_voice length**__": f"length (数字)で話す速度を変更\nex.**{prefix}change_voice length 1**"}

        embed = discord.Embed(title="**change_voice** コマンドの使用方法")
        [embed.add_field(name=i,value=l) for i, l in field_dict.items()]

        self.embed = embed
        return self

    class Models():
        async def help(self):
            responce = await f_voice.get_model()
            model_dict = responce[0]
            model_list = responce[1]
            embed = discord.Embed(title="使用できるモデルのリスト",description=f"{model_list}\nex.**{prefix}change_voice models 1**")
            self.embed = embed

            select_item = [discord.SelectOption(label=value,value=f"{value},{str(index)}") for index, value in enumerate(list(model_dict.values()))]

            view = discord.ui.View()
            view.add_item(discord.ui.Select(options=select_item, custom_id="change_voice_models", placeholder="使用したいモデルを選択してください..."))

            self.view = view
            return self

        async def main(self, user: discord.User, id: str):

            database = f_data.read()
            responce = await f_voice.get_model()
            model_data = responce[0]
            if not str(user.id) in database["user_data"]:
                f_data.create_userdata(user.id)
                database = f_data.read()

            if id in model_data:
                database["user_data"][str(user.id)]["model_id"] = id
                f_data.write(database)

                self.content = f"使用するモデルを **{model_data[id]}** に変更しました"
            else:
                self.content = f"モデル: **{id}** は存在しません"

            return self
    class Length():
        def help(self):
            embed = discord.Embed(title="使用方法",description=f"{prefix}change_voice length (数字)\nex.**{prefix}change_voice length 1**")
            self.embed = embed
            return self
        def main(self, user: discord.User, length: float):
            if length <= 0.1:
                input_length = "0.1"
            elif length >= 5:
                input_length = "5"
            else:
                input_length = str(length)

            database = f_data.read()
            if not str(user.id) in database["user_data"]:
                f_data.create_userdata(user.id)
                database = f_data.read()

            database["user_data"][str(user.id)]["length"] = input_length
            f_data.write(database)

            self.content = f"lengthを **{input_length}** に変更しました"
            return self

    models = Models()
    length = Length()

class Playsound():

    async def play(self, author: discord.User, guild: discord.Guild, content: str):
        try:
            global_.play_waitlist[guild.id].append({"content": content, "userid": author.id, "serverid": guild.id})
        except KeyError:
            global_.play_waitlist[guild.id] = []
            global_.play_waitlist[guild.id].append({"content": content, "userid": author.id, "serverid": guild.id})

        playsound_list = global_.play_waitlist[guild.id]

        if len(playsound_list) == 1:
            while playsound_list:

                path = await f_voice.create_voice(playsound_list[0]["content"], playsound_list[0]["userid"], playsound_list[0]["serverid"])
                guild.voice_client.play(discord.FFmpegPCMAudio(path))

                with wave.open(path, 'rb') as f:
                    fr = f.getframerate()
                    fn = f.getnframes()

                await asyncio.sleep(1.0 * (fn/fr) + 0.25)
                playsound_list.pop(0)

wav = Wav()
join = Join()
dictionary = Dictionary()
server_settings = Server_settings()
change_voice = Change_voice()
playsound = Playsound()
