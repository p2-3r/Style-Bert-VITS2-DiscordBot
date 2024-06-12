import discord

from src.json_utils.botdata import BotJson

from src.bots.play_sound import play_sound_on_vc
from src.global_data import read_channel
from src.bots.commands import \
    about, \
    change_voice_models_list, \
    change_voice_speaker_list, \
    change_voice_style_list, \
    dic, \
    help, \
    join, \
    leave, \
    length, \
    now, \
    ping, \
    server, \
    wav


bot_json = BotJson()
PREFIX = bot_json.data['prefix']


# 通常のメッセージに関する処理
def register(client: discord.Client):

    """
    実際の処理は src.bots.commands にまとめてあって、
    
    処理の内容を同じコマンドのスラッシュコマンド版と共有している
    """
    @client.event
    async def on_message(message: discord.Message):  # type: ignore
        # もしメッセージの送信者がBOTなら返答しない
        if message.author.bot:
            return

        # DMだった場合反応しない
        elif message.channel.guild == None:
            if message.content.startswith(PREFIX):
                await message.channel.send("このBOTの機能はDMでは利用できません")
            return

        # プレフィックスから始まるメッセージへの反応
        elif message.content.startswith(PREFIX):

            message_nopref = message.content[len(PREFIX):]  # prefix の後のメッセージだけ取り出す

            if message_nopref == "":
                return  # プレフィックスだけなら反応しない

            elif message_nopref.startswith("ping"):
                content = ping.run()
                await message.channel.send(content)

            elif message_nopref.startswith("help"):
                embed = help.run()
                await message.channel.send(embed=embed)

            elif message_nopref.startswith("join"):
                reply = await join.run(message)
                connect_message = await message.channel.send(reply)

                # joinコマンドを使用した人が設定しているモデルで再生する
                connect_message.content = "接続しました。"
                connect_message.author = message.author
                await play_sound_on_vc(connect_message)

            elif message_nopref.startswith("leave"):
                content = await leave.run(message)
                await message.channel.send(content)

            elif message_nopref.startswith("wav"):
                if message_nopref == "wav":
                    await message.channel.send(f"**{PREFIX}wav** の後に生成したい音声を指定してください。")
                else:
                    reply, bytes_, = await wav.run(message, text=message_nopref[4:])
                    await message.channel.send(content=reply, file=discord.File(bytes_, filename="Message.wav"))

            elif message_nopref.startswith("model"):
                embed, view = change_voice_models_list.run()
                await message.channel.send(embed=embed, view=view)

            elif message_nopref.startswith("speaker"):
                embed, view = await change_voice_speaker_list.run(message.author)
                await message.channel.send(embed=embed, view=view)

            elif message_nopref.startswith("style"):
                embed, view = await change_voice_style_list.run(message.author)
                await message.channel.send(embed=embed, view=view)

            elif message_nopref.startswith("length"):
                # 数値が書かれていなかったら使用方法を返す
                if len(message_nopref) <= 7:
                    await message.channel.send(f"使用方法: `{PREFIX}length {{読み上げ速度: 数値}}`")

                # 数値以外が含まれていたら使用方法を返す
                else:
                    input_num = message_nopref[7:]

                    try:
                        input_num = float(input_num)
                    except ValueError:
                        await message.channel.send("数値で指定してください。")
                        return

                    content = await length.run(message, input_num=input_num)

                    await message.channel.send(content)

            elif message_nopref.startswith("dic"):
                embed, view = dic.run(message)
                await message.channel.send(embed=embed, view=view)

            elif message_nopref.startswith("server"):
                embed, view = server.run(message)
                await message.channel.send(embed=embed, view=view)

            elif message_nopref.startswith("now"):
                embed = now.run(message)
                await message.channel.send(embed=embed)

            elif message_nopref.startswith("about"):
                embed = about.run()
                await message.channel.send(embed=embed)

        # チャンネルの読み上げ
        elif message.guild.voice_client is not None:  # type: ignore

            # セミコロンから始まっていた場合、または読み上げる内容がない場合読み上げない
            if message.content.startswith(";") or message.content == "":
                return

            # joinコマンドが打たれたチャンネルかどうかをチェックする
            if message.channel.id == read_channel[f"{message.guild.id}"]:  # type: ignore

                # 音声を再生
                await play_sound_on_vc(message, replace=True)
