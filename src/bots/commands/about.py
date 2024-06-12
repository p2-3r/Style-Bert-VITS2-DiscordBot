import discord


def run() -> discord.Embed:
    embed = discord.Embed(title="このBOTについて")
    embed.add_field(name="githubへのリンク", value="https://github.com/p2-3r/Style-Bert-VITS2-DiscordBot")
    embed.add_field(name="(本家)Bert-VITS2へのリンク", value="https://github.com/fishaudio/Bert-VITS2")
    embed.add_field(name="Style-Bert-VITS2へのリンク", value="https://github.com/litagin02/Style-Bert-VITS2")

    return embed
