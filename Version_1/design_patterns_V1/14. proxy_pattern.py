
from abc import ABC, abstractmethod


# ==================================================
# 1. VIRTUAL PROXY - Lazy Initialization
# Creates an expensive object only when required.
# ==================================================

class IImage(ABC):
    @abstractmethod
    def display(self):
        pass


class RealImage(IImage):
    def __init__(self, filename):
        self.filename = filename
        print(f"[RealImage] Loading image from disk: {self.filename}")

    def display(self):
        print(f"[RealImage] Displaying {self.filename}")


class ImageProxy(IImage):
    def __init__(self, filename: str):
        self._real_image = None
        self._filename = filename

    def display(self):
        # Virtual Proxy: Lazy initialization of the real object.
        if self._real_image is None:
            self._real_image = RealImage(self._filename)

        self._real_image.display()


# ==================================================
# 2. REMOTE PROXY - Remote Communication
# Represents a remote object and handles communication.
# ==================================================

class IDataService(ABC):
    @abstractmethod
    def fetch_data(self):
        pass


class RealDataService(IDataService):
    def __init__(self):
        print("[RealDataService] Initialized (simulating remote setup)")

    def fetch_data(self):
        return "[RealDataService] Data from server"


class DataServiceProxy(IDataService):
    def __init__(self):
        self.real_service = RealDataService()

    def fetch_data(self):
        # Remote Proxy: Handles remote communication.
        print("[DataServiceProxy] Connecting to remote service...")
        return self.real_service.fetch_data()


# ==================================================
# 3. PROTECTION PROXY - Access Control
# Restricts access based on authorization rules.
# ==================================================

class IDocumentReader(ABC):
    @abstractmethod
    def unlock_pdf(self, file_path, password):
        pass


class RealDocumentReader(IDocumentReader):
    def unlock_pdf(self, file_path, password):
        print(f"[RealDocumentReader] Unlocking PDF at: {file_path}")
        print(f"[RealDocumentReader] PDF unlocked successfully with password: {password}")
        print("[RealDocumentReader] Displaying PDF content...")


class User:
    def __init__(self, name, is_premium):
        self.name = name
        self.premium_membership = is_premium


class DocumentProxy(IDocumentReader):
    def __init__(self, user):
        self.real_reader = RealDocumentReader()
        self.user = user

    def unlock_pdf(self, file_path, password):
        # Protection Proxy: Checks authorization before forwarding.
        if not self.user.premium_membership:
            print("[DocumentProxy] Access denied. Only premium members can unlock PDFs.")
            return

        self.real_reader.unlock_pdf(file_path, password)


# ==================================================
# CLIENT CODE
# ==================================================

def main():

    # 1. Virtual Proxy
    print("\n========== VIRTUAL PROXY ==========")
    image = ImageProxy("Sample.jpg")
    image.display()

    # 2. Remote Proxy
    print("\n========== REMOTE PROXY ==========")
    data_service = DataServiceProxy()
    data_service.fetch_data()

    # 3. Protection Proxy
    print("\n========== PROTECTION PROXY ==========")

    user1 = User("Rohan", False)
    user2 = User("Rashmi", True)

    print("\n== Rohan (Non-Premium) ==")
    doc_reader = DocumentProxy(user1)
    doc_reader.unlock_pdf("protected_document.pdf", "secret123")

    print("\n== Rashmi (Premium) ==")
    doc_reader = DocumentProxy(user2)
    doc_reader.unlock_pdf("protected_document.pdf", "secret123")


if __name__ == "__main__":
    main()
