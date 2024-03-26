
import discord

from src.commands import action
from src.bot import client, read_channel, PREFIX

# 通常のメッセージに関する処理


@client.event
async def on_message(message: discord.Message):

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
        message_nopref = message.content[len(PREFIX):]

        if message_nopref == "":
            return  # もしプレフィックスだけなら反応しない

        elif message_nopref.startswith("ping"):
            reply = action.ping()
            await message.channel.send(reply)

        elif message_nopref.startswith("help"):
            embed = action.help()
            await message.channel.send(embed=embed)

        elif message_nopref.startswith("join"):
            reply = await action.join(message)
            connect_message = await message.channel.send(reply)

            # joinコマンドを使用した人が設定しているモデルで再生する
            connect_message.content = "接続しました。"
            connect_message.author = message.author
            await action.play_sound(connect_message)

        elif message_nopref.startswith("leave"):
            reply = await action.leave(message)
            await message.channel.send(reply)

        elif message_nopref.startswith("wav"):
            if message_nopref == "wav":
                await message.channel.send(f"**{PREFIX}wav** の後に生成したい音声を指定してください。")
            else:
                reply, bytes_, = await action.wav(message_nopref[4:], message)
                await message.channel.send(content=reply, file=discord.File(bytes_, filename="Message.wav"))

        elif message_nopref.startswith("model"):
            embed, view = action.display_change_model()
            await message.channel.send(embed=embed, view=view)

        elif message_nopref.startswith("speaker"):
            embed, view = action.display_change_speaker(message.author)
            await message.channel.send(embed=embed, view=view)

        elif message_nopref.startswith("style"):
            embed, view = action.display_change_style(message.author)
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

                reply = action.length(input_num, message)

                await message.channel.send(reply)

        elif message_nopref.startswith("dic"):
            embed, view = action.dic(message)
            await message.channel.send(embed=embed, view=view)

        elif message_nopref.startswith("server"):
            embed, view = action.server_settings(message)
            await message.channel.send(embed=embed, view=view)

    # BOTがそのギルドでVCに参加していた時に読み上げる
    elif message.guild.voice_client is not None:

        # セミコロンから始まっていた場合、または読み上げる内容がない場合読み上げない
        if message.content.startswith(";") or message.content == "":
            return

        # joinコマンドが打たれたチャンネルかどうかをチェックする
        if message.channel.id == read_channel[f"{message.guild.id}"]:

            # 音声を再生
            await action.play_sound(message, replace=True)
