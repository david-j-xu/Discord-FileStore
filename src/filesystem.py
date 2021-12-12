from inode import INode


class FileSystem:
    def __init__(self) -> None:
        self.root = INode("", "", True)
        self.pwd = self.root

    def ls(self) -> str:
        result = ""
        for file in self.pwd.getFiles():
            result += file.getName() + "\n"
        return result

    def __checkFilePath(self, name: str):
        # make sure / is not in the path for clarity
        if "/" in name or ".." in name:
            raise ValueError("Directory name may not contain / or ..")

        # make sure a directory or file does not already exist with this name
        for file in self.pwd.getFiles():
            if file.getName() == name:
                raise ValueError("File/Folder with this name already exists")

    def touch(self, name: str):
        self.__checkFilePath(name)

        child = INode(name,
                      self.pwd.getPath() + self.pwd.getName() + "/", False,
                      self.pwd)
        self.pwd.addFile(child)

    def mkdir(self, name: str):
        self.__checkFilePath(name)

        child = INode(name,
                      self.pwd.getPath() + self.pwd.getName() + "/", True,
                      self.pwd)
        self.pwd.addFile(child)

    def get_pwd(self) -> str:
        return self.pwd.getPath() + self.pwd.getName() + "/"

    def cd(self, path: str):
        if path == "..":
            if self.pwd.parent:
                self.pwd = self.pwd.parent
        else:
            for dir in self.pwd.getFiles():
                if dir.isDirectory() and dir.getName() == path:
                    self.pwd = dir
                    return

    def list_all_files(self) -> str:
        result = []
        self.__dfs_files(self.root, result)
        return "\n".join(result)

    def __dfs_files(self, curr: INode, result) -> str:
        for file in curr.getFiles():
            if not file.isDirectory():
                result.append(file.getPath() + file.getName())

        for directory in curr.getFiles():
            if directory.isDirectory():
                self.__dfs_files(directory, result)

    def upload(self, path, name):
        pass

    def download(self, path, name):
        pass


if __name__ == "__main__":
    fs = FileSystem()
    print(fs.get_pwd())
    fs.mkdir("usr")
    fs.mkdir("bin")
    fs.touch("thingy")
    print(fs.ls())
    fs.cd("usr")
    print(fs.get_pwd())
    fs.touch("other thingy")
    print(fs.list_all_files())