from enum import Enum
from typing import List


class INodeType(Enum):
    DIRECTORY = 0
    FILE = 1


class INode:
    def __init__(self, name: str, path: str, isDirectory: bool, parent=None):
        self.type: INodeType = INodeType.DIRECTORY if isDirectory else INodeType.FILE
        self._name: str = name
        self._path: str = path
        self.parent = parent
        self.num_files: int = 0
        self.num_blocks: int = 0
        self._files: List[INode] = []
        self._blocks: List[INode] = []
        self.indirect: List[str] = []  # message ids for additional files

    def isDirectory(self) -> bool:
        return self.type == INodeType.DIRECTORY

    def getPath(self) -> str:
        return self._path

    def addFile(self, node):
        self._files.append(node)
        self.num_files += 1

    def getNumFiles(self) -> int:
        return self.num_files

    def getBlocks(self):
        return self._blocks

    def getFiles(self):
        return self._files

    def getName(self) -> str:
        return self._name

    def getNumBlocks(self) -> int:
        return self.num_blocks