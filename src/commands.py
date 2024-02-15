import wave
from typing import Union
import asyncio

import discord
import requests

import main
import data as f_data
import voice as f_voice
import colorprint as f_print

prefix = main.prefix

class Ping():
    def main(self):
        self.content = "pong!"
        return self

class Help():
    def main(self):
        field_dict = {f"**{prefix}ping**": "pong!",
                      f"**{prefix}wav (content)**": "指定した内容を生成してその音声ファイルを添付したメッセージを送信します",
                      f"**{prefix}join**": "使用した人がいるボイスチャンネルに接続します",
                      f"**{prefix}leave**": "ボイスチャンネルから切断します",
                      f"**{prefix}change_voice**": "使用する声を変更するためのコマンドのヘルプを表示します",
                      f"**{prefix}server_settings**": "自動参加などサーバーに関する設定のためのヘルプを表示します"}

        embed = discord.Embed(title="このBOTのヘルプ")

        for i, l in field_dict.items():
            embed.add_field(name=i,value=l)

        self.embed = embed

        return self

class Wav():
    def main(self, content: str, user_id :int, server_id: int):
        self.content = f"「{content}」"
        try:
            self.file = f_voice.create_voice(content, user_id, server_id)
        except requests.exceptions.ConnectionError:
            f_print.printinfo.error("Audio could not be generated because the API was not activated.")

        return self

    def help(self):
        self.embed = discord.Embed(title="**wav** コマンドの使用方法", description=f"{prefix}wav (生成したい音声の内容)")
        return self

class Server_settings():
    class Help():
        def main(self):
            field_dict = {f"__**{prefix}server_settings status**__": "このサーバーの現在の設定を表示します。このsettingsコマンド以外はそのサーバーの管理者でないと使用できません",
                          f"__**{prefix}server_settings auto_join**__": "このコマンドの使用でボイスチャットに誰かが参加したとき自動参加するかしないかを切り替えられます",
                          f"__**{prefix}server_settings auto_ch**__": "自動参加時に読み上げるテキストチャンネルを設定します"}

            embed = discord.Embed(title="**settings** コマンドの使用方法")
            [embed.add_field(name=i,value=l) for i, l in field_dict.items()]

            self.embed = embed
            return self
    class Status():
        def main(self, guild: discord.guild):
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
    class Auto_join():
        def main(self, guild: discord.guild, channel: discord.channel, user: discord.user):
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
    class Auto_ch():
        def main(self, guild: discord.guild, channel: discord.channel, user: discord.user):
            if user.guild_permissions.administrator:
                current_server_data = f_data.read_serverdata(guild.id)
                current_server_data["auto_join_read_channel"] = channel.id
                f_data.write_serverdata(guild.id, current_server_data)
                self.content = f"自動参加時の読み上げるチャンネルを <#{str(channel.id)}> に設定しました"
            else:
                self.content = "このコマンドはサーバーの管理者でないと使用できません"

            return self

    help = Help()
    status = Status()
    auto_join = Auto_join()
    auto_ch = Auto_ch()

class Change_voice():
    class Help():
        def main(self):
            field_dict = {f"__**{prefix}change_voice models**__": f"modelsコマンドでモデル一覧を表示\nmodels (数字)で(数字)のモデルに変更\nex. **{prefix}change_voice models 0**",
                        f"__**{prefix}change_voice length**__": f"length (数字)で話す速度を変更\nex.**{prefix}change_voice length 1**"}

            embed = discord.Embed(title="**change_voice** コマンドの使用方法")
            [embed.add_field(name=i,value=l) for i, l in field_dict.items()]

            self.embed = embed
            return self
    class Models():
        def help(self):
            model_list = f_voice.get_model()[1]
            embed = discord.Embed(title="使用できるモデルのリスト",description=f"{model_list}\nex.**{prefix}change_voice models 1**")
            self.embed = embed
            return self

        def main(self, user: discord.user, id: str):

            database = f_data.read()
            if not str(user.id) in database["user_data"]:
                f_data.create_userdata(user.id)
                database = f_data.read()

            if id in f_voice.get_model()[0]:
                database["user_data"][str(user.id)]["model_id"] = id
                f_data.write(database)

                self.content = f"使用するモデルを **{f_voice.get_model()[0][id]}** に変更しました"
            else:
                self.content = f"モデル: **{id}** は存在しません"

            return self
    class Length():
        def help(self):
            embed = discord.Embed(title="使用方法",description=f"{prefix}change_voice length (数字)\nex.**{prefix}change_voice length 1**")
            self.embed = embed
            return self
        def main(self, user: discord.user, length: float):
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

    help = Help()
    models = Models()
    length = Length()

ping = Ping()
help = Help()
wav = Wav()
server_settings = Server_settings()
change_voice = Change_voice()
