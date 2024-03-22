from typing import Union, Optional

import discord

from src import model
from src.data import User, botdata
from src.infer import user_infer
from src.bot import PREFIX, READ_LIMIT, read_channel, play_waitdict

# slachコマンド使用時と on_messageコマンド使用時の両方に対応するためコマンドの実際の動作はこのファイルにまとめている


def ping() -> str:  # s!ping
    reply = "pong!"
    return reply


def help() -> discord.Embed:
    field_dict = {f"**{PREFIX}ping**": "pong!",
                  f"**{PREFIX}wav (content)**": "指定した内容を生成してその音声ファイルを添付したメッセージを送信します",
                  f"**{PREFIX}dictionary**": "サーバー辞書メニューを表示します",
                  f"**{PREFIX}join**": "使用した人がいるボイスチャンネルに接続します",
                  f"**{PREFIX}leave**": "ボイスチャンネルから切断します",
                  f"**{PREFIX}change_voice**": "使用する声を変更するためのコマンドのヘルプを表示します",
                  f"**{PREFIX}server_settings**": "自動参加などサーバーに関する設定のためのヘルプを表示します"}

    embed = discord.Embed(title="このBOTのヘルプ")

    for i, l in field_dict.items():
        embed.add_field(name=i, value=l)

    return embed


async def join(ctx: Union[discord.Message, discord.Interaction]) -> Optional[str]:

    if isinstance(ctx, discord.Message):
        author: discord.Member = ctx.author
        guild: discord.Guild = ctx.guild
        channel: discord.TextChannel = ctx.channel
    elif isinstance(ctx, discord.Interaction):
        pass  # TODO スラッシュコマンドの時の処理を後で書く

    if author.voice is None:
        return "ボイスチャンネルに接続してから使用してください"

    elif guild.voice_client is not None:
        return "すでにボイスチャンネルに接続しています"

    elif guild.voice_client is None:

        # 初期値設定
        read_channel[f"{guild.id}"] = channel.id
        play_waitdict[f"{guild.id}"] = []

        await author.voice.channel.connect()
        return f"接続しました\n読み上げるチャンネル: <#{str(channel.id)}>"


async def leave(ctx: Union[discord.Message, discord.Interaction]) -> str:

    if isinstance(ctx, discord.Message):
        guild = ctx.guild
    elif isinstance(ctx, discord.Interaction):
        pass  # TODO スラッシュコマンドの時の処理を後で書く

    if guild.voice_client is None:
        return "接続していません"

    else:
        read_channel.pop(f"{guild.id}")
        play_waitdict[f"{guild.id}"] = []

        ctx.guild.voice_client.stop()
        await guild.voice_client.disconnect()
        return "退出しました"


async def wav(text: str, ctx: discord.Message):
    if len(text) >= (READ_LIMIT+5)*2:
        text = text[:READ_LIMIT*2]  # s!wavはREAD_LIMITの2倍まで許容しておく

    bytes_ = await user_infer(text, ctx)
    return f"\"{text}\"", bytes_


def display_change_model() -> tuple[discord.Embed, discord.ui.View]:
    model_list_list: list[list[str]] = model.get_modelfolders(sep=25)

    # モデルが26個以上ならページ移動ボタンを追加
    if len(model_list_list) >= 2:
        add_pagebutton = True
    else:
        add_pagebutton = False

    model_list = model_list_list[0]

    description = f"1: {model_list[0]}"
    for i, val in enumerate(model_list):
        if i != 0:
            description += f"\n{i+1}: {val}"

    class ChangeModel_View(discord.ui.View):
        def __init__(self, *, timeout: float | None = 180):
            super().__init__(timeout=timeout)

            if add_pagebutton:
                pageback_button = discord.ui.Button(label="<-", style=discord.ButtonStyle.primary, custom_id="model_pageback", disabled=True)
                pagenow_button = discord.ui.Button(label="0", style=discord.ButtonStyle.gray, disabled=True)
                pageforward_button = discord.ui.Button(label="->", style=discord.ButtonStyle.primary, custom_id="model_pageforward")

                [self.add_item(i) for i in [pageback_button, pagenow_button, pageforward_button]]

            select_item = [discord.SelectOption(label=i, value=i) for i in model_list]
            self.add_item(discord.ui.Select(options=select_item, custom_id="change_model", placeholder="使用したいモデルを選択してください..."))

    embed = discord.Embed(title="使用できるモデル一覧", description=description)
    view = ChangeModel_View()

    return embed, view


def display_change_speaker(author: Union[discord.Member, discord.User]) -> tuple[discord.Embed, discord.ui.View]:
    action_user = User(author.id, author.name)
    model_name = action_user.model_name
    speaker_list_list = model.get_speakers(model_name, sep=25)

    # モデルが26個以上ならページ移動ボタンを追加
    if len(speaker_list_list) >= 2:
        add_pagebutton = True
    else:
        add_pagebutton = False

    speaker_list = speaker_list_list[0]

    description = f"1: {speaker_list[0]}"
    for i, val in enumerate(speaker_list):
        if i != 0:
            description += f"\n{i+1}: {val}"

    class ChangeSpeaker_View(discord.ui.View):
        def __init__(self, *, timeout: float | None = 180):
            super().__init__(timeout=timeout)

            if add_pagebutton:
                pageback_button = discord.ui.Button(label="<-", style=discord.ButtonStyle.primary, custom_id="speaker_pageback", disabled=True)
                pagenow_button = discord.ui.Button(label="0", style=discord.ButtonStyle.gray, disabled=True)
                pageforward_button = discord.ui.Button(label="->", style=discord.ButtonStyle.primary, custom_id="speaker_pageforward")

                [self.add_item(i) for i in [pageback_button, pagenow_button, pageforward_button]]

            select_item = [discord.SelectOption(label=i, value=f"{model_name}||{i}") for i in speaker_list]
            self.add_item(discord.ui.Select(options=select_item, custom_id="change_speaker", placeholder="使用したい話者を選択してください..."))

    embed = discord.Embed(title=f"モデル: {model_name} の話者一覧", description=description)
    view = ChangeSpeaker_View()

    return embed, view
