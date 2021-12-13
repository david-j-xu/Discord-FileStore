import logging
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

import filesystem
import utils


def main():
    intents = discord.Intents.all()

    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')
    COMMANDS_CHANNEL = os.getenv('COMMANDS_CHANNEL')
    BOOTSTRAP_CHANNEL = os.getenv('BOOTSTRAP_CHANNEL')
    FILES_CHANNEL = os.getenv('FILES_CHANNEL')
    LOCAL_PATH = os.getenv('LOCAL_PATH')

    bot = commands.Bot(command_prefix=':!', intents=intents)

    fs = None

    @bot.event
    async def on_ready():
        logging.info("Bot is ready")

    @bot.command(
        name='mount',
        help="Mounts the current filesystem, or creates one if it does not exist"
    )
    async def b_mount(ctx):
        pass

    @bot.command(name='pwd', help="Prints the current working directory")
    async def b_pwd(ctx):
        pass

    @bot.command(name='ls',
                 help="Prints files and directories in the current directory")
    async def b_ls(ctx):
        pass

    @bot.command(name='rm',
                 help="Deletes a file or folder in the current directory")
    async def b_rm(ctx):
        pass

    @bot.command(name='du', help="Lists all the files in the filesystem")
    async def b_du(ctx):
        pass

    @bot.command(name='cd', help="Changes directory")
    async def b_cd(ctx):
        pass

    @bot.command(name='mkdir', help="Makes a directory")
    async def b_mkdir(ctx):
        pass

    @bot.command(name='upload', help="Creates a file")
    async def b_upload(ctx):
        pass

    @bot.command(name='download', help="Downloads a file")
    async def b_download(ctx):
        pass

    bot.run(TOKEN)


if __name__ == "__main__":
    main()