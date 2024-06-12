import discord

from src.bots.play_sound import play_sound_on_vc
from src.bots.commands import \
    about as about_, \
    change_voice_models_list as change_voice_models_list_, \
    change_voice_speaker_list as change_voice_speaker_list_, \
    change_voice_style_list as change_voice_style_list_, \
    dic as dic_, \
    help as help_, \
    join as join_, \
    leave as leave_, \
    length as length_, \
    now as now_, \
    ping as ping_, \
    server as server_, \
    wav as wav_
    # そのままだと関数名と被るので最後に _ を入れている

def register(tree: discord.app_commands.CommandTree):
    """
    実際の処理は src.bots.commands にまとめてあって、
    
    処理の内容を同じコマンドの通常のメッセージコマンド版と共有している
    """

    @tree.command(name="ping", description="pong!")
    async def ping(ctx: discord.Interaction):  # type: ignore
        content = ping_.run()
        await ctx.response.send_message(content, ephemeral=True)

    @tree.command(name="help", description="helpを表示します。")
    async def help(ctx: discord.Interaction):  # type: ignore
        embed = help_.run()
        await ctx.response.send_message(embed=embed)

    @tree.command(name="wav", description="指定した内容の音声を生成して添付します。")
    @discord.app_commands.guild_only
    async def wav(ctx: discord.Interaction, text: str):  # type: ignore
        await ctx.response.defer()

        reply, bytes_, = await wav_.run(ctx, text=text)
        await ctx.followup.send(content=reply, file=discord.File(bytes_, filename="Message.wav"))

    @tree.command(name="join", description="使用するとあなたが現在いるボイスチャンネルに参加します。")
    @discord.app_commands.guild_only
    async def join(ctx: discord.Interaction):  # type: ignore
        reply = await join_.run(ctx)
        await ctx.response.send_message(reply)

        await play_sound_on_vc(ctx)

    @tree.command(name="leave", description="ボイスチャンネルから退出します。")
    @discord.app_commands.guild_only
    async def leave(ctx: discord.Interaction):  # type: ignore
        content = await leave_.run(ctx)
        await ctx.response.send_message(content)

    @tree.command(name="server", description="サーバーの設定、変更画面を表示します。")
    @discord.app_commands.guild_only
    async def server(ctx: discord.Interaction):  # type: ignore
        embed, view = server_.run(ctx)
        await ctx.response.send_message(embed=embed, view=view)

    @tree.command(name="model", description="使用するモデルの変更画面を表示します。")
    @discord.app_commands.guild_only
    async def model(ctx: discord.Interaction):  # type: ignore
        embed, view = change_voice_models_list_.run()
        await ctx.response.send_message(embed=embed, view=view)

    @tree.command(name="speaker", description="使用するモデル話者の変更画面を表示します。")
    @discord.app_commands.guild_only
    async def speaker(ctx: discord.Interaction):  # type: ignore
        embed, view = await change_voice_speaker_list_.run(ctx.user)
        await ctx.response.send_message(embed=embed, view=view)

    @tree.command(name="change_voice_length", description="読み上げ速度を変更します。")
    @discord.app_commands.guild_only
    async def change_voice_length(ctx: discord.Interaction, length: float):  # type: ignore
        content = await length_.run(ctx, input_num=length)
        await ctx.response.send_message(content)

    @tree.command(name="style", description="使用するモデルのスタイルの変更画面を表示します。")
    @discord.app_commands.guild_only
    async def style(ctx: discord.Interaction):  # type: ignore
        embed, view = await change_voice_style_list_.run(ctx.user)
        await ctx.response.send_message(embed=embed, view=view)

    @tree.command(name="dic", description="サーバー辞書の変更画面を表示します。")
    @discord.app_commands.guild_only
    async def dic(ctx: discord.Interaction):  # type: ignore
        embed, view = dic_.run(ctx)
        await ctx.response.send_message(embed=embed, view=view)

    @tree.command(name="now", description="現在使用しているモデル、話者、スタイルを表示します。")
    @discord.app_commands.guild_only
    async def now(ctx: discord.Interaction):  # type: ignore
        embed = now_.run(ctx)
        await ctx.response.send_message(embed=embed)

    @tree.command(name="about", description="このBOTについてのリンクを表示します。")
    @discord.app_commands.guild_only
    async def about(ctx: discord.Interaction):  # type: ignore
        embed = about_.run()
        await ctx.response.send_message(embed=embed)
