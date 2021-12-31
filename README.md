# Discord FileStore

## Overview

Online cloud storage is a popular way for people to share, backup, and store files, both in the short and long term. However, all cloud storage solutions currently require that people pay, usually in the form of a subscription, for the option to store unlimited data. Discord, on the other hand, allows for unlimited storage of messages, including files. As such, we can leverage this in order to create a filesystem.

The system works as such: 
1. Use your own machine to run the bot, with upload and download file paths set up in your `.env` file. The paths should be relative to wherever you are running the bot from.

2. Load the existing filesytem using `mount` or create a new one using `create`

3. Use `upload` and `download` in order to handle your files.

## Setup

1. Create a bot on your desired server. To see how to do this, consult the discord documentation

2. Create a `.env` file. We need to create one of these so that we can set up some basic information about our filesystem and our bot. The format should be as follows:
```
# .env

# Bot token
DISCORD_TOKEN=YOUR_DISCORD_TOKEN_WITHOUT_SPACES

FILES_CHANNEL=CHANNEL_TO_STORE_FILES
INODES_CHANNEL=CHANNEL_TO_STORE_INODES
LOCAL_UPLOAD_PATH=PATH_TO_WHERE_YOU_WANT_TO_UPLOAD_FROM
LOCAL_DOWNLOAD_PATH=PATH_TO_WHERE_YOU_WANT_TO_DOWNLOAD_TO
LOCAL_INODES_PATH=PATH_TO_LOCALLY_STORE_INODES
```

3. Run `app.py`

4. Run the functions in any channel of your choice.

## Commands

  - `cd`:        Changes directory
  - `create`:    Creates a new filesystem
  - `download`:  Downloads a file
  - `du`:        Lists all the files in the filesystem
  - `help`:     Shows this message
  - `ls` :      Prints files and directories in the current directory
  - `mkdir`:    Makes a directory
  - `mount`:    Mounts the current filesystem
  - `pwd`:      Prints the current working directory
  - `rm` :      Deletes a file or folder in the current directory
  - `unmount`:  Unmounts the currently mounted filesystem
  - `upload`:   Creates a file


## Some Notes
As of right now, we have a theoretical limit on the number of files by the size of the pickled filesystem. The filesystem pickle file grows as the size of the filesystem itself, and when this hits 8MB, the filesystem will no longer be able to be cached on discord itself.

-  This can likely be fixed by adding a bootstrapping component, where we have a separate inode that points to all the inode blocks, and reconstructing from there. I don't see this being a large problem, though, so I didn't add this. In theory, we could exponentially increase the capacity of our filesystem with higher depths of indirectly storing the inode structure, but I don't see even one layer being necessary.

- Additionally, there are definitely security vulnerabilities due to the pickling operation I chose to use, so be careful what servers you use this on.
