import os

import discord
import requests
from bs4 import BeautifulSoup as BS
from discord import app_commands

from keep_alive import keep_alive

BOT_NAME = "UniGacha Bot"

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print("Bot is now ready!")
    await tree.sync()


@tree.command(name="uni", description="ウニガチャを回す")
async def uni_gacha(interaction: discord.Interaction):
    textareaText, imageUrl = shindan(interaction.user.display_name)
    embed = discord.Embed(
        title=BOT_NAME,
        color=0x00FF00,
    )
    embed.set_image(url=imageUrl)
    embed.add_field(name="診断結果", value=textareaText)
    await interaction.response.send_message(embed=embed)


@tree.error
async def on_app_command_error(interaction: discord.Integration, error):
    embed = discord.Embed(
        title=BOT_NAME,
        color=0xFF0000,
    )
    embed.add_field(name="Error", value=error)
    await interaction.response.send_message(embed=embed)


def shindan(name: str = "hoge", url: str = "https://shindanmaker.com/586328"):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0"
    }
    session = requests.session()
    res = session.get(url, headers=headers)
    if res.status_code != 200:
        raise FileNotFoundError(res.status_code)

    bs = BS(res.content, "html.parser")
    token = bs.find(attrs={"name": "_token", "type": "hidden"})
    tokenValue = token["value"]
    hiddenName = bs.find(attrs={"name": "hiddenName", "type": "hidden"})
    hiddenNameValue = hiddenName["value"]
    shindanToken = bs.find(attrs={"name": "shindan_token", "type": "hidden"})
    shindanTokenValue = shindanToken["value"]

    params = {
        "_token": tokenValue,
        "shindanName": name,
        "hiddenName": hiddenNameValue,
        "type": "name",
        "shindan_token": shindanTokenValue,
    }
    login = session.post(url, headers=headers, data=params)
    if login.status_code != 200:
        raise FileNotFoundError(login.status_code)

    bs = BS(login.content, "html.parser")
    textareaText = bs.find(
        attrs={"id": "share-copytext-shindanresult-textarea"}
    ).get_text()
    # print(textareaText)
    imageUrl = bs.find(
        "img", class_="d-block shindanResult_image rounded my-1 mx-auto"
    ).get("src")
    # print(imageUrl)

    return textareaText, imageUrl


keep_alive()  # Webサーバの立ち上げ
client.run(DISCORD_TOKEN)
