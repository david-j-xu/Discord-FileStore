import logging
import os
from io import BytesIO
import pickle
from datetime import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
from filesystem import FileSystem
from utils import Splitter, Joiner

debug = True
# Global filesystem, stored in bot memory
fs = None

files_channel = None
inodes_channel = None


logging.basicConfig(filename='logs/app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG if debug else logging.WARNING)


def main():
    intents = discord.Intents.all()

    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')
    FILES_CHANNEL = os.getenv('FILES_CHANNEL')
    INODES_CHANNEL = os.getenv('INODES_CHANNEL')
    LOCAL_UPLOAD_PATH = os.getenv('LOCAL_UPLOAD_PATH')
    LOCAL_INODES_PATH = os.getenv('LOCAL_INODES_PATH')
    LOCAL_DOWNLOAD_PATH = os.getenv('LOCAL_DOWNLOAD_PATH')

    bot = commands.Bot(command_prefix=':! ', intents=intents)

    @bot.event
    async def on_ready():
        logging.info("Bot is ready")

    @bot.command(
        name='create',
        help="Creates a new filesystem"
    )
    async def b_create(ctx):
        # find channels
        for channel in ctx.guild.channels:
            if channel.name == FILES_CHANNEL:
                global files_channel
                files_channel = channel
                logging.info(f"Found files channel at {channel.name}")
            if channel.name == INODES_CHANNEL:
                global inodes_channel
                inodes_channel = channel
                logging.info(f"Found inodes channel at {channel.name}")

        if not files_channel:
            logging.error(f"Unable to find file channel {FILES_CHANNEL}")
        if not inodes_channel:
            logging.error(f"Unable to find inodes channel {INODES_CHANNEL}")

        global fs

        # create a new filesystem if it doesn't exist
        if not fs:
            fs = FileSystem()
            if fs:
                logging.info(f"Successfully created filesystem")
                await ctx.send("Filesystem successfully created")
            else:
                logging.fatal("Unable to create filesystem, terminating")
                await ctx.send("Unable to create filesystem, terminating")
                raise RuntimeError

    @bot.command(
        name='mount',
        help="Mounts the current filesystem, or creates one if it does not exist"
    )
    async def b_mount(ctx):
        # find channels
        for channel in ctx.guild.channels:
            if channel.name == FILES_CHANNEL:
                global files_channel
                files_channel = channel
                logging.info(f"Found files channel at {channel.name}")
            if channel.name == INODES_CHANNEL:
                global inodes_channel
                inodes_channel = channel
                logging.info(f"Found inodes channel at {channel.name}")

        if not files_channel:
            logging.error(f"Unable to find file channel {FILES_CHANNEL}")
        if not inodes_channel:
            logging.error(f"Unable to find inodes channel {INODES_CHANNEL}")

        global fs

        # attempt to load the most recent file system (limit 200)
        async for message in inodes_channel.history(limit=200):
            if fs:
                break
            for attachment in message.attachments:
                try:
                    fs = pickle.load(BytesIO(await attachment.read()))
                    if type(fs) != FileSystem:
                        fs = None
                        continue
                    logging.info(f"Successfully loaded filesystem")
                    await ctx.send("Filesystem successfully loaded")
                except Exception as e:
                    logging.error(f"{e}")
                    continue

    @ bot.command(
        name='unmount',
        help="Unmounts the currently mounted filesystem"
    )
    async def b_unmount(ctx):
        global fs

        if fs:
            path = '/'.join([LOCAL_INODES_PATH, "inode"])
            file = open(path, "wb")
            pickle.dump(fs, file)
            file.close()
            file = open(path, "rb")
            await inodes_channel.send(f"Root Inode, created at {datetime.now()}",
                                      file=discord.File(file))
            file.close()
        fs = None
        logging.info("Filesystem unmounted if it existed")
        await ctx.send("Filesystem successfully unmounted")

    @ bot.command(name='pwd', help="Prints the current working directory")
    async def b_pwd(ctx):
        if fs:
            logging.info(
                f"Present working directory shifted to {fs.get_pwd()}")
            await ctx.send(f'Working Directory: ```{fs.get_pwd()}\n```')
        else:
            logging.info(f"No filesystem found at command time for pwd")
            await ctx.send("No filesystem was found")

    @ bot.command(name='ls',
                  help="Prints files and directories in the current directory")
    async def b_ls(ctx):
        if fs:
            logging.info(f"ls called")
            await ctx.send(f"Files in the current directory: \n```{fs.ls()}\n```")
        else:
            logging.info(f"No filesystem found at command time for ls")
            await ctx.send("No filesystem was found")

    @ bot.command(name='rm',
                  help="Deletes a file or folder in the current directory")
    async def b_rm(ctx, arg):
        if fs:
            logging.info(f"rm called")
            await ctx.send(f"Deleted file: {fs.rm(arg)}")
        else:
            logging.info(f"No filesystem found at command time for rm")
            await ctx.send("No filesystem was found")

    @ bot.command(name='du', help="Lists all the files in the filesystem")
    async def b_du(ctx):
        if fs:
            logging.info(f"du called")
            await ctx.send(f'All files: \n```{fs.list_all_files()}\n```')
        else:
            logging.info(f"No filesystem found at command time for du")
            await ctx.send("No filesystem was found")

    @ bot.command(name='cd', help="Changes directory")
    async def b_cd(ctx, arg):
        if fs:
            logging.info(f"cd called to {arg}")
            fs.cd(arg)
            await ctx.send(f"New pwd: ```{fs.get_pwd()}\n```")
        else:
            logging.info(f"No filesystem found at command time for cd")
            await ctx.send("No filesystem was found")

    @ bot.command(name='mkdir', help="Makes a directory")
    async def b_mkdir(ctx, arg):
        if fs:
            logging.info(f"mkdir called with argument {arg}")
            await ctx.send(f'Created new directory: ``` {fs.mkdir(arg)} \n```')
        else:
            logging.info(f"No filesystem found at command time for mkdir")
            await ctx.send("No filesystem was found")

    @ bot.command(name='upload', help="Creates a file")
    async def b_upload(ctx, arg):
        # check if filesystem exists
        if not fs:
            logging.info(f"No filesystem found at command time for upload")
            await ctx.send("No filesystem was found")
            return
        # create a block creator for a file
        path = '/'.join([LOCAL_UPLOAD_PATH, arg])
        splitter = Splitter(path)
        curr = splitter.get_next_block()

        # only create a file if it's nonempty, else return
        if not curr:
            logging.info(f"File was not found for upload")
            await ctx.send("File not found, failing upload")
            return

        # file exists, create an inode, place in the current directory
        inode = fs.touch(arg)

        while curr:
            file = BytesIO(curr)
            message = await files_channel.send(f"{arg} block {inode.num_blocks}", file=discord.File(file))
            inode.addBlock(message.id)
            logging.info(f"Added block {message.id} to file {arg}")
            curr = splitter.get_next_block()

        splitter.destruct()
        logging.info(f"Successfully uploaded file {path} to {arg}")
        await ctx.send(f"Successfully uploaded file {path} to {arg}")

    @ bot.command(name='download', help="Downloads a file")
    async def b_download(ctx, arg):
        # check if filesystem exists
        if not fs:
            logging.info(f"No filesystem found at command time for download")
            await ctx.send("No filesystem was found")
            return
        # create a block joiner for a file
        path = '/'.join([LOCAL_DOWNLOAD_PATH, arg])
        joiner = Joiner(path)

        # find relevant inode
        inode = fs.get_file(arg)
        # only create a file if the file exists
        if not inode:
            logging.info(f"File was not found for download")
            await ctx.send("File not found, failing download")
            return

        # find blocks and write
        for (idx, message_id) in enumerate(inode.getBlocks()):
            message = await files_channel.fetch_message(message_id)

            for attachment in message.attachments:
                logging.info(f"Writing block {idx} for file {arg}")
                contents = await attachment.read()
                joiner.write_next_block(contents)

        joiner.destruct()
        await ctx.send(f"Successfully downloaded file {arg} to {path}")
        logging.info(f"Successfully downloaded file {arg} to {path}")

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
