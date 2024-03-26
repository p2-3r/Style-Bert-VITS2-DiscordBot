import typing
from typing import Union, Optional
import asyncio

import discord

from src import model
from src.data import User, Server
from src.infer import user_infer
from src.bot import PREFIX, READ_LIMIT, read_channel, play_waitdict, ffmpeg_path

# slachコマンド使用時と on_messageコマンド使用時の両方に対応するためコマンドの実際の動作はこのファイルにまとめている


def ping() -> str:  # s!ping
    reply = "pong!"
    return reply


def help() -> discord.Embed:
    field_dict = {f"**{PREFIX}ping**": "pong!",
                  f"**{PREFIX}wav (content)**": "指定した内容を生成してその音声ファイルを添付したメッセージを送信します",
                  f"**{PREFIX}join**": "使用した人がいるボイスチャンネルに接続します",
                  f"**{PREFIX}leave**": "ボイスチャンネルから切断します",
                  f"**{PREFIX}model**": "使用できるモデルの変更メニューを表示します",
                  f"**{PREFIX}speaker**": "現在のモデルの話者変更メニューを表示します",
                  f"**{PREFIX}style**": "現在のモデルのスタイル変更メニューを表示します。",
                  f"**{PREFIX}dic**": "サーバー辞書メニューを表示します",
                  f"**{PREFIX}server**": "自動参加などサーバーに関する設定を表示します"}

    embed = discord.Embed(title="このBOTのヘルプ")

    for i, l in field_dict.items():
        embed.add_field(name=i, value=l)

    return embed


async def join(ctx: Union[discord.Message, discord.Interaction]) -> Optional[str]:

    if isinstance(ctx, discord.Message):
        author = ctx.author
        guild = ctx.guild
        channel = ctx.channel
    elif isinstance(ctx, discord.Interaction):
        author = ctx.user
        guild = ctx.guild
        channel = ctx.channel

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
        guild = ctx.guild

    if guild.voice_client is None:
        return "接続していません"

    else:
        read_channel.pop(f"{guild.id}")
        play_waitdict[f"{guild.id}"] = []

        ctx.guild.voice_client.stop()
        await guild.voice_client.disconnect()
        return "退出しました"


async def wav(text: str, ctx: Union[discord.Message, discord.Interaction]) -> tuple[str, typing.Any]:
    if len(text) >= (READ_LIMIT+5)*2:
        text = text[:READ_LIMIT*2]  # s!wavはREAD_LIMITの2倍まで許容しておく

    bytes_, _, _ = await user_infer(text, ctx)
    return f"\"{text}\"", bytes_


def dic(ctx: Union[discord.Message, discord.Interaction]) -> tuple[discord.Embed, discord.ui.View]:
    if isinstance(ctx, discord.Message):
        guild = ctx.guild
    elif isinstance(ctx, discord.Interaction):
        guild = ctx.guild

    server = Server(guild.id, guild.name)
    server_dict: dict[str, str] = server.data["dic"]

    if server_dict != {}:
        description = ""
        for i, [before, after] in enumerate(server_dict.items()):
            if i == 0:
                description = description + f"{before} -> {after}"
            else:
                description = description + f"\n{before} -> {after}"

            if len(description) <= 4095:
                embed = discord.Embed(title="このサーバーの辞書", description=description)
            else:
                embed = discord.Embed(title="登録されている単語が多すぎたため表示できませんでした。")
    else:
        embed = discord.Embed(title="このサーバーではまだ何も登録されていません。")

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="add", style=discord.ButtonStyle.primary, custom_id="dict_add"))
    view.add_item(discord.ui.Button(label="remove", style=discord.ButtonStyle.secondary, custom_id="dict_remove"))

    return embed, view


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

    try:
        model_name = action_user.model_name
        speaker_list_list = model.get_speakers(model_name, sep=25)
    except KeyError:
        folders: list[str] = model.get_modelfolders()
        action_user.write_userdata("model_name", folders[0])

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


def display_change_style(author: Union[discord.Member, discord.User]) -> tuple[discord.Embed, discord.ui.View]:
    action_user = User(author.id, author.name)

    try:
        model_name = action_user.model_name
        modelfolder = model.ModelFolder(model_name)
    except KeyError:
        folders: list[str] = model.get_modelfolders()
        action_user.write_userdata("model_name", folders[0])

        model_name = action_user.model_name
        modelfolder = model.ModelFolder(model_name)

    style_list = modelfolder.styles

    description = f"1: {style_list[0]}"
    for i, val in enumerate(style_list):
        if i != 0:
            description += f"\n{i+1}: {val}"

    class ChangeSpeaker_View(discord.ui.View):
        def __init__(self, *, timeout: float | None = 180):
            super().__init__(timeout=timeout)

            select_item = [discord.SelectOption(label=i, value=f"{model_name}||{i}") for i in style_list]
            self.add_item(discord.ui.Select(options=select_item, custom_id="change_style", placeholder="使用したいスタイルを選択してください..."))

    embed = discord.Embed(title=f"モデル: {model_name} の話者一覧", description=description)
    view = ChangeSpeaker_View()

    return embed, view


def server_settings(ctx: Union[discord.Message, discord.Interaction]) -> tuple[discord.Embed, discord.ui.View]:
    if isinstance(ctx, discord.Message):
        guild = ctx.guild
        user = ctx.author
    elif isinstance(ctx, discord.Interaction):
        guild = ctx.guild
        user = ctx.user

    server = Server(guild.id, guild.name)
    settings = {k: v for k, v in server.data.items() if "dic" != k}

    embed = discord.Embed(title=f"{guild.name} の現在設定")

    # embedに要素を追加(keyによっては動作を変える)
    for k, v in settings.items():
        if k == "auto_join" and v is not None:
            embed.add_field(name=f"{k}", value=f"<#{v}>")
        else:
            embed.add_field(name=f"{k}", value=f"{v}")

    view = discord.ui.View()
    if user.guild_permissions.administrator:  # もし管理者なら変更用のviewを追加する
        select_item = [discord.SelectOption(label=i, value=i) for i in settings.keys()]
        view.add_item(discord.ui.Select(options=select_item, custom_id="change_server_settings", placeholder="変更したい設定を選択してください..."))

    return embed, view


async def play_sound(ctx: Union[discord.Message, discord.Interaction], replace: bool = False):
    play_waitlist = play_waitdict[f"{ctx.guild.id}"]
    play_waitlist.append(ctx)

    # 再生中に再生しようとしてエラーを起こさないため順番に再生する
    if len(play_waitlist) == 1:
        while play_waitlist:

            if isinstance(ctx, discord.Message):
                text = play_waitlist[0].content
                # 長すぎる場合以下略する
                if len(text) >= READ_LIMIT + 5:
                    text = text[:READ_LIMIT] + "\n以下略"

                bytes_, sr, audio = await user_infer(text, play_waitlist[0], replace=replace)

            elif isinstance(ctx, discord.Interaction):
                if ctx.command.name == "join":
                    bytes_, sr, audio = await user_infer("接続しました。", play_waitlist[0], replace=replace)
                else:
                    raise AssertionError(f"Unspecified command. '{ctx.command.name}'")

            try:
                ctx.guild.voice_client.play(discord.FFmpegPCMAudio(bytes_, pipe=True, executable=ffmpeg_path))

            except AttributeError:  # 再生待機リストに残っているときにvcから抜けたときにエラーにならないように
                pass

            await asyncio.sleep((len(audio)/sr) + 0.1)

            play_waitlist.pop(0)


def length(input_num: float, ctx: Union[discord.Message, discord.Interaction]):

    if isinstance(ctx, discord.Message):
        user = User(ctx.author.id, ctx.author.name)
    elif isinstance(ctx, discord.Interaction):
        user = User(ctx.user.id, ctx.user.name)

    # 0.1 ~ 5.0 の範囲外ならその範囲に収める
    if input_num < 0.1:
        input_num = 0.1
    elif input_num > 5.0:
        input_num = 5.0

    # 小数点以下1桁までに制限する
    input_num = round(input_num, 1)

    user.write_userdata("length", input_num)

    return f"読み上げ速度を **{input_num}** に変更しました。"
