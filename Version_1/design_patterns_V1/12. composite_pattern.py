from abc import ABC, abstractmethod

class FileSystemItem(ABC):
    @abstractmethod
    def ls(self, indent: int = 0):
        pass

    @abstractmethod
    def open_all(self, indent: int = 0):
        pass

    @abstractmethod
    def get_size(self):
        pass

    @abstractmethod
    def cd(self, target: str):
        pass

    @abstractmethod
    def get_name(self):
        pass


    @abstractmethod
    def is_folder(self):
        pass

class File(FileSystemItem):
    def __init__(self, name: str, size: int):
        self._name = name
        self._size = size

    def ls(self, indent: int = 0):
        print(" " * indent + self._name)

    def open_all(self, indent: int = 0):
        print(" " * indent + self._name)

    def get_size(self):
        return self._size

    def cd(self, target: str):
        return None

    def get_name(self):
        return self._name

    def is_folder(self):
        return False


class Folder(FileSystemItem):
    def __init__(self, name: str):
        self._name = name
        self._children = []

    def add(self, item: FileSystemItem):
        self._children.append(item)

    def ls(self, indent: int = 0):
        for child in self._children:
            if child.is_folder():
                print(" " * indent + "+ " + child.get_name())
            else:
                print(" " * indent + child.get_name())

    def open_all(self, indent: int = 0):
        print(" " * indent + "+ " + self._name)

        for child in self._children:
            child.open_all(indent + 4)

    def get_size(self):
        total_size = 0
        for child in self._children:
            total_size += child.get_size()

        return total_size

    def cd(self, target: str):
        for child in self._children:
            if child.is_folder() and child.get_name() == target:
                return child

        return None

    def get_name(self):
        return self._name

    def is_folder(self):
        return True


def main():
    # Build file system
    root = Folder("root")

    root.add(File("file1.txt", 1))
    root.add(File("file2.txt", 1))

    docs = Folder("docs")
    docs.add(File("resume.pdf", 1))
    docs.add(File("notes.txt", 1))

    root.add(docs)

    images = Folder("images")
    images.add(File("photo.jpg", 1))

    root.add(images)

    # List root directory
    root.ls()

    print()

    # List docs directory
    docs.ls()

    print()

    # Display entire file system
    root.open_all()

    print()

    # Change directory to docs
    cwd = root.cd("docs")

    if cwd is not None:
        cwd.ls()
    else:
        print("\n Could not cd into docs \n")

    print()

    # Calculate total size
    print(root.get_size())


if __name__ == "__main__":
    main()

