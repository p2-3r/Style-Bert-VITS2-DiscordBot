import discord

from src.commands import action
from src.bot import client, tree


@tree.command(name="ping", description="pong!")
async def ping(ctx: discord.Interaction):
    reply = action.ping()
    await ctx.response.send_message(reply, ephemeral=True)


@tree.command(name="help", description="helpを表示します。")
async def help(ctx: discord.Interaction):
    embed = action.help()
    await ctx.response.send_message(embed=embed)


@tree.command(name="wav", description="指定した内容の音声を生成して添付します。")
@discord.app_commands.guild_only
async def wav(ctx: discord.Interaction, text: str):
    await ctx.response.defer()

    reply, bytes_, = await action.wav(text, ctx=ctx)
    await ctx.followup.send(content=reply, file=discord.File(bytes_, filename="Message.wav"))


@tree.command(name="join", description="使用するとあなたが現在いるボイスチャンネルに参加します。")
@discord.app_commands.guild_only
async def join(ctx: discord.Interaction):
    reply = await action.join(ctx)
    await ctx.response.send_message(reply)
    await action.play_sound(ctx)


@tree.command(name="leave", description="ボイスチャンネルから退出します。")
@discord.app_commands.guild_only
async def leave(ctx: discord.Interaction):
    reply = await action.leave(ctx)
    await ctx.response.send_message(reply)


@tree.command(name="server", description="サーバーの設定、変更画面を表示します。")
@discord.app_commands.guild_only
async def server(ctx: discord.Interaction):
    embed, view = action.server_settings(ctx)
    await ctx.response.send_message(embed=embed, view=view)


@tree.command(name="model", description="使用するモデルの変更画面を表示します。")
@discord.app_commands.guild_only
async def model(ctx: discord.Interaction):
    embed, view = action.display_change_model()
    await ctx.response.send_message(embed=embed, view=view)


@tree.command(name="speaker", description="使用するモデル話者の変更画面を表示します。")
@discord.app_commands.guild_only
async def speaker(ctx: discord.Interaction):
    embed, view = action.display_change_speaker(ctx.user)
    await ctx.response.send_message(embed=embed, view=view)


@tree.command(name="change_voice_length", description="読み上げ速度を変更します。")
@discord.app_commands.guild_only
async def change_voice_length(ctx: discord.Interaction, length: float):
    reply = action.length(length, ctx)
    await ctx.response.send_message(reply)


@tree.command(name="style", description="使用するモデルのスタイルの変更画面を表示します。")
@discord.app_commands.guild_only
async def style(ctx: discord.Interaction):
    embed, view = action.display_change_style(ctx.user)
    await ctx.response.send_message(embed=embed, view=view)


@tree.command(name="dic", description="サーバー辞書の変更画面を表示します。")
@discord.app_commands.guild_only
async def dic(ctx: discord.Interaction):
    embed, view = action.dic(ctx)
    await ctx.response.send_message(embed=embed, view=view)

@tree.command(name="now", description="現在使用しているモデル、話者、スタイルを表示します。")
@discord.app_commands.guild_only
async def now(ctx: discord.Interaction):
    embed = action.now(ctx)
    await ctx.response.send_message(embed=embed)