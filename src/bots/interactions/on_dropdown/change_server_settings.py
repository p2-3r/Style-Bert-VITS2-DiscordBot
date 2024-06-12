import discord

from src.json_utils.serverdata import ServerJson


async def run(ctx: discord.Interaction) -> None:
    choiced_val = ctx.data["values"][0]  # type: ignore

    await ctx.response.defer()

    # 管理者ではない場合書き換えない
    is_admin = ctx.user.guild_permissions.administrator  # type: ignore
    if not is_admin:
        await ctx.followup.send(content="サーバーの設定変更はそのサーバーの管理者のみ可能です。", ephemeral=True)
        return

    if ctx.guild is None:
        raise AssertionError("guild is None")

    action_server = ServerJson(ctx.guild.id)

    if choiced_val == "dic_onlyadmin":
        is_dic_onlyadmin = action_server.data["dic_onlyadmin"]

        # TrueとFalseを切り替える
        if is_dic_onlyadmin:
            await ctx.followup.send(content="サーバー辞書の編集権限を **サーバーの全員** に変更しました")
            action_server.data["dic_onlyadmin"] = False
            await action_server.async_write(action_server.data)

        elif not is_dic_onlyadmin:
            await ctx.followup.send(content="サーバー辞書の編集権限を **管理者のみ** に変更しました")
            action_server.data["dic_onlyadmin"] = True
            await action_server.async_write(action_server.data)

    elif choiced_val == "auto_join":
        auto_join_ch = action_server.data["auto_join"]

        if auto_join_ch is None:  # auto_join_ch が None ならそのチャンネルのIDを設定する
            await ctx.followup.send(content=f"自動参加時に読み上げるチャンネルを変更しました。\n自動参加時に読み上げるチャンネル: <#{ctx.channel_id}>")
            action_server.data["auto_join"] = ctx.channel_id
            await action_server.async_write(action_server.data)

        else:
            if auto_join_ch == ctx.channel_id:  # すでにそのチャンネルが設定されているなら自動参加機能を OFF(None) にする
                await ctx.followup.send(content="自動参加機能を **OFF** にしました。")
                action_server.data["auto_join"] = None
                await action_server.async_write(action_server.data)
            else:  # そうじゃないならそのチャンネルのIDに変更する
                await ctx.followup.send(content=f"自動参加機能を **ON** にしました。\n自動参加時に読み上げるチャンネル: <#{ctx.channel_id}>")
                action_server.data["auto_join"] = ctx.channel_id
                await action_server.async_write(action_server.data)

    else:  # バグが起きない限り実行されない
        raise AssertionError(f"Error: {choiced_val=}")
