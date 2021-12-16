BLOCK_SIZE = 7000000


class Splitter:
    '''
    Splits a file into blocks
    '''

    def __init__(self, path: str) -> None:
        try:
            self._file = open(path, "rb")
        except Exception as e:
            raise e

    def get_next_block(self) -> bytes:
        if self._file:
            bytes = self._file.read(BLOCK_SIZE)
            return bytes
        return None

    def destruct(self):
        if self._file:
            self._file.close()


class Joiner:
    '''
    Joins a file given blocks
    '''

    def __init__(self, path: str) -> None:
        try:
            self._file = open(path, "wb")
        except Exception as e:
            raise e

    def write_next_block(self, bytes: bytes):
        length = len(bytes)
        if self._file:
            bytes_written = self._file.write(bytes)
            if bytes_written != length:
                raise RuntimeError("File didn't properly write")
        else:
            raise FileNotFoundError("File was not found")

    def destruct(self):
        if self._file:
            self._file.close()


if __name__ == "__main__":
    splitter = Splitter("test/test")
    joiner = Joiner("test/copy")
    curr = splitter.get_next_block()
    while curr:
        print(curr)
        joiner.write_next_block(curr)
        curr = splitter.get_next_block()

    splitter.destruct()
    joiner.destruct()
    print("done")
