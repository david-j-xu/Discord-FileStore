import logging
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from filesystem import FileSystem
import utils

fs = None


def main():
    intents = discord.Intents.all()

    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')
    BOOTSTRAP_CHANNEL = os.getenv('BOOTSTRAP_CHANNEL')
    FILES_CHANNEL = os.getenv('FILES_CHANNEL')
    INODES_CHANNEL = os.getenv('INODES_CHANNEL')
    LOCAL_PATH = os.getenv('LOCAL_PATH')

    bot = commands.Bot(command_prefix=':! ', intents=intents)

    @bot.event
    async def on_ready():
        logging.info("Bot is ready")

    @bot.command(
        name='mount',
        help="Mounts the current filesystem, or creates one if it does not exist"
    )
    async def b_mount(ctx):
        global fs
        fs = FileSystem()
        await ctx.send("Filesystem successfully created")

    @bot.command(
        name='unmount',
        help="Unmounts the currently mounted filesystem"
    )
    async def b_unmount(ctx):
        global fs
        fs = None
        await ctx.send("Filesystem successfully unmounted")

    @bot.command(name='pwd', help="Prints the current working directory")
    async def b_pwd(ctx):
        if fs:
            await ctx.send(f'Working Directory: ```{fs.get_pwd()}```')
        else:
            await ctx.send("No filesystem was found")

    @bot.command(name='ls',
                 help="Prints files and directories in the current directory")
    async def b_ls(ctx):
        if fs:
            await ctx.send(f"Files in the current directory: \n```{fs.ls()}```")
        else:
            await ctx.send("No filesystem was found")

    @bot.command(name='rm',
                 help="Deletes a file or folder in the current directory")
    async def b_rm(ctx, arg):
        if fs:
            await ctx.send(f"Deleted file: {fs.rm(arg)}")
        else:
            await ctx.send("No filesystem was found")

    @bot.command(name='du', help="Lists all the files in the filesystem")
    async def b_du(ctx):
        if fs:
            await ctx.send(f'All files: \n```{fs.list_all_files()}```')
        else:
            await ctx.send("No filesystem was found")

    @bot.command(name='cd', help="Changes directory")
    async def b_cd(ctx, arg):
        if fs:
            fs.cd(arg)
            await ctx.send(f"New pwd: ```{fs.get_pwd()}```")
        else:
            await ctx.send("No filesystem was found")

    @bot.command(name='mkdir', help="Makes a directory")
    async def b_mkdir(ctx, arg):
        if fs:
            await ctx.send(f'Created new directory: ``` {fs.mkdir(arg)} ```')
        else:
            await ctx.send("No filesystem was found")

    @bot.command(name='upload', help="Creates a file")
    async def b_upload(ctx):
        pass

    @bot.command(name='download', help="Downloads a file")
    async def b_download(ctx):
        pass

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
