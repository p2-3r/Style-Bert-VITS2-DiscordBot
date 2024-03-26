import discord

from src.data import User, Server
from src.bot import client
from src import model

# ボタンやプルダウン選択時に呼び出される


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
    action_user = User(ctx.user.id, username=ctx.user.name)
    choiced_val = ctx.data["values"][0]

    custom_id = ctx.data['custom_id']

    if custom_id == "change_model":  # モデルコマンドのプルダウンが選択されたとき
        await ctx.response.defer()
        action_user.write_userdata("model_name", choiced_val)
        action_user.write_userdata("speaker_name", "None")
        await ctx.followup.send(f"使用するモデルを **{choiced_val}** に変更しました", ephemeral=True)

    elif custom_id == "change_speaker":  # スピーカーコマンドのプルダウンが選択されたとき
        await ctx.response.defer(ephemeral=True)

        # choiced_val: f"{model_name}||{speaker_name}"
        model_name, speaker_name = choiced_val.split("||")
        action_user.write_userdata("model_name", model_name)
        action_user.write_userdata("speaker_name", speaker_name)

        content = f"使用する話者を **{speaker_name}** に変更しました"
        if action_user.model_name != model_name:
            content = f"使用するモデルを **{action_user.model_name}** から **{model_name}** に変更しました。\n" + content

        await ctx.followup.send(content, ephemeral=True)

    elif custom_id == "change_style":  # スピーカーコマンドのプルダウンが選択されたとき
        await ctx.response.defer(ephemeral=True)

        # choiced_val: f"{model_name}||{speaker_name}"
        model_name, style_name = choiced_val.split("||")
        action_user.write_userdata("model_name", model_name)
        action_user.write_userdata("style", style_name)

        content = f"使用するスタイルを **{style_name}** に変更しました"
        if action_user.model_name != model_name:
            content = f"使用するモデルを **{action_user.model_name}** から **{model_name}** に変更しました。\n" + content

        await ctx.followup.send(content, ephemeral=True)

    elif custom_id == "change_server_settings":  # サーバー設定のプルダウンが選択されたとき
        await ctx.response.defer()

        if not ctx.user.guild_permissions.administrator:  # 管理者ではない場合書き換えない
            await ctx.followup.send(content="サーバーの設定変更はそのサーバーの管理者のみ可能です。", ephemeral=True)
            return

        action_server = Server(ctx.guild.id, ctx.guild.name)
        settings_val = action_server.data[choiced_val]  # 選択された値のサーバー設定の値

        if choiced_val == "dic_onlyadmin":
            # settings_val: True | False

            # TrueとFalseを切り替える
            if settings_val:
                await ctx.followup.send(content="サーバー辞書の編集権限を **サーバーの全員** に変更しました")
                action_server.write_serverdata(choiced_val, False)

            if not settings_val:
                await ctx.followup.send(content="サーバー辞書の編集権限を **管理者のみ** に変更しました")
                action_server.write_serverdata(choiced_val, True)

        elif choiced_val == "auto_join":
            # settings_val: discord.Channel.id | None

            # settings_valがそのidのチャンネルならNoneに、そうじゃないならそのチャンネルのidを設定
            if isinstance(settings_val, int):
                if ctx.channel_id == settings_val:
                    await ctx.followup.send(content="自動参加機能を **OFF** にしました。")
                    action_server.write_serverdata(choiced_val, None)
                else:
                    await ctx.followup.send(content=f"自動参加時に読み上げるチャンネルを変更しました。\n自動参加時に読み上げるチャンネル: <#{ctx.channel_id}>")
                    action_server.write_serverdata(choiced_val, ctx.channel_id)

            # settings_valがNoneならそのチャンネルのidを設定
            else:
                await ctx.followup.send(content=f"自動参加機能を **ON** にしました。\n自動参加時に読み上げるチャンネル: <#{ctx.channel_id}>")
                action_server.write_serverdata(choiced_val, ctx.channel_id)

        else:  # バグが起きない限り実行されない
            print(f"{choiced_val=}")

    else:  # バグが起きない限り実行されない
        print(f"{custom_id=}")


async def on_button_click(ctx: discord.Interaction):

    server = Server(ctx.guild.id, ctx.guild.name)

    custom_id = ctx.data['custom_id']
    is_admin = ctx.user.guild_permissions.administrator
    only_admin = server.data["dic_onlyadmin"]

    # サーバー辞書編集
    if custom_id.startswith("dict_"):

        if only_admin and (not is_admin):  # 管理者限定でその人が管理者ではないなら
            await ctx.response.send_message(content="現在このサーバーでは管理者のみ変更可能です。", ephemeral=True)
        else:
            # addボタンを押したときの動作
            if custom_id == "dict_add":
                class Add_Modal(discord.ui.Modal, title="単語と読み方の登録"):
                    word = discord.ui.TextInput(label="単語", max_length=15)
                    read = discord.ui.TextInput(label="読み方", max_length=15)

                    async def on_submit(self, ctx: discord.Interaction):
                        await ctx.response.send_message(f"読み方を設定しました\n単語: **{self.word}** 読み方: **{self.read}**")
                        server.write_dic(f"{self.word}", f"{self.read}")

                await ctx.response.send_modal(Add_Modal())

            # removeボタンを押したときの動作
            elif custom_id == "dict_remove":
                class Remove_Modal(discord.ui.Modal, title="辞書の削除"):
                    word = discord.ui.TextInput(label="削除したい単語", max_length=20)

                    async def on_submit(self, ctx: discord.Interaction):
                        try:
                            server.delete_dic(f"{self.word}")
                        except KeyError:
                            await ctx.response.send_message(f"辞書に 単語: **{self.word}** は存在しません", ephemeral=True)
                            return

                        await ctx.response.send_message(f"辞書から読み方を削除しました\n削除した単語: **{self.word}**")

                await ctx.response.send_modal(Remove_Modal())

    # モデルページ移動の動作
    elif custom_id.startswith("model_page"):
        description_f = int(ctx.message.embeds[0].description.split(":", maxsplit=1)[0])
        page = description_f // 25

        if custom_id == "model_pageforward":

            model_list_list: list[list[str]] = model.get_modelfolders(sep=25)

            model_list = model_list_list[page+1]

            description = f"{1 + (page+1)*25}: {model_list[0]}"
            for i, val in enumerate(model_list):
                if i != 0:
                    description += f"\n{(i+1)+(page+1)*25}: {val}"

            class ChangeModel_View(discord.ui.View):
                def __init__(self, *, timeout: float | None = 180):
                    super().__init__(timeout=timeout)

                    if (page+2) != len(model_list_list):
                        pageforward = False
                    else:
                        pageforward = True

                    pageback_button = discord.ui.Button(label="<-", style=discord.ButtonStyle.primary, custom_id="model_pageback", disabled=False)
                    pagenow_button = discord.ui.Button(label=f"{page+1}", style=discord.ButtonStyle.gray, disabled=True)
                    pageforward_button = discord.ui.Button(label="->", style=discord.ButtonStyle.primary,
                                                           custom_id="model_pageforward", disabled=pageforward)

                    [self.add_item(i) for i in [pageback_button, pagenow_button, pageforward_button]]

                    select_item = [discord.SelectOption(label=i, value=i) for i in model_list]
                    self.add_item(discord.ui.Select(options=select_item, custom_id="change_model", placeholder="使用したいモデルを選択してください..."))

            embed = discord.Embed(title="使用できるモデル一覧", description=description)
            view = ChangeModel_View()

            await ctx.response.send_message(embed=embed, view=view)
            await ctx.message.delete()

        if custom_id == "model_pageback":

            model_list_list: list[list[str]] = model.get_modelfolders(sep=25)

            model_list = model_list_list[page-1]

            description = f"{1 + (page-1)*25}: {model_list[0]}"
            for i, val in enumerate(model_list):
                if i != 0:
                    description += f"\n{(i+1)+(page-1)*25}: {val}"

            class ChangeModel_View(discord.ui.View):
                def __init__(self, *, timeout: float | None = 180):
                    super().__init__(timeout=timeout)

                    if page != 0:
                        pageback = False
                    else:
                        pageback = True

                    pageback_button = discord.ui.Button(label="<-", style=discord.ButtonStyle.primary, custom_id="model_pageback", disabled=pageback)
                    pagenow_button = discord.ui.Button(label=f"{page-1}", style=discord.ButtonStyle.gray, disabled=True)
                    pageforward_button = discord.ui.Button(label="->", style=discord.ButtonStyle.primary,
                                                           custom_id="model_pageforward")

                    [self.add_item(i) for i in [pageback_button, pagenow_button, pageforward_button]]

                    select_item = [discord.SelectOption(label=i, value=i) for i in model_list]
                    self.add_item(discord.ui.Select(options=select_item, custom_id="change_model", placeholder="使用したいモデルを選択してください..."))

            embed = discord.Embed(title="使用できるモデル一覧", description=description)
            view = ChangeModel_View()

            await ctx.response.send_message(embed=embed, view=view)
            await ctx.message.delete()

    elif custom_id.startswith("speaker_"):

        description_f = int(ctx.message.embeds[0].description.split(":", maxsplit=1)[0])
        page = description_f // 25
        model_name = ctx.message.embeds[0].title.split("モデル: ")[1].split(" の話者一覧")[0]

        if custom_id == "speaker_pageforward":

            model_list_list = model.get_speakers(model_name, sep=25)

            model_list = model_list_list[page+1]

            description = f"{1 + (page+1)*25}: {model_list[0]}"
            for i, val in enumerate(model_list):
                if i != 0:
                    description += f"\n{(i+1)+(page+1)*25}: {val}"

            class ChangeSpeaker_View(discord.ui.View):
                def __init__(self, *, timeout: float | None = 180):
                    super().__init__(timeout=timeout)

                    if (page+2) != len(model_list_list):
                        pageforward = False
                    else:
                        pageforward = True

                    pageback_button = discord.ui.Button(label="<-", style=discord.ButtonStyle.primary, custom_id="speaker_pageback", disabled=False)
                    pagenow_button = discord.ui.Button(label=f"{page+1}", style=discord.ButtonStyle.gray, disabled=True)
                    pageforward_button = discord.ui.Button(label="->", style=discord.ButtonStyle.primary,
                                                           custom_id="speaker_pageforward", disabled=pageforward)

                    [self.add_item(i) for i in [pageback_button, pagenow_button, pageforward_button]]

                    select_item = [discord.SelectOption(label=i, value=f"{model_name}||{i}") for i in model_list]
                    self.add_item(discord.ui.Select(options=select_item, custom_id="change_speaker", placeholder="使用したい話者を選択してください..."))

            embed = discord.Embed(title=f"モデル: {model_name} の話者一覧", description=description)
            view = ChangeSpeaker_View()

            await ctx.response.send_message(embed=embed, view=view)
            await ctx.message.delete()

        elif custom_id == "speaker_pageback":

            model_list_list = model.get_speakers(model_name, sep=25)

            model_list = model_list_list[page-1]

            description = f"{1 + (page-1)*25}: {model_list[0]}"
            for i, val in enumerate(model_list):
                if i != 0:
                    description += f"\n{(i+1)+(page-1)*25}: {val}"

            class ChangeSpeaker_View(discord.ui.View):
                def __init__(self, *, timeout: float | None = 180):
                    super().__init__(timeout=timeout)

                    if (page) != len(model_list_list):
                        pageforward = False
                    else:
                        pageforward = True

                    pageback_button = discord.ui.Button(label="<-", style=discord.ButtonStyle.primary, custom_id="speaker_pageback", disabled=False)
                    pagenow_button = discord.ui.Button(label=f"{page-1}", style=discord.ButtonStyle.gray, disabled=True)
                    pageforward_button = discord.ui.Button(label="->", style=discord.ButtonStyle.primary,
                                                           custom_id="speaker_pageforward", disabled=pageforward)

                    [self.add_item(i) for i in [pageback_button, pagenow_button, pageforward_button]]

                    select_item = [discord.SelectOption(label=i, value=f"{model_name}||{i}") for i in model_list]
                    self.add_item(discord.ui.Select(options=select_item, custom_id="change_speaker", placeholder="使用したい話者を選択してください..."))

            embed = discord.Embed(title=f"モデル: {model_name} の話者一覧", description=description)
            view = ChangeSpeaker_View()

            await ctx.response.send_message(embed=embed, view=view)
            await ctx.message.delete()

    else:  # バグがない限り実行されない
        print(custom_id)
