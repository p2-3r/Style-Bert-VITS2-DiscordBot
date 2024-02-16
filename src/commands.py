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

        try:
            global_.play_waitlist[guild.id].append({"content": "接続しました", "userid": author.id, "serverid": guild.id})
        except KeyError:
            global_.play_waitlist[guild.id] = []
            global_.play_waitlist[guild.id].append({"content": "接続しました", "userid": author.id, "serverid": guild.id})


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
                      f"__**{prefix}server_settings auto_ch**__": "自動参加時に読み上げるテキストチャンネルを設定します"}

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
            model_list = responce[1]
            embed = discord.Embed(title="使用できるモデルのリスト",description=f"{model_list}\nex.**{prefix}change_voice models 1**")
            self.embed = embed
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

wav = Wav()
join = Join()
server_settings = Server_settings()
change_voice = Change_voice()
