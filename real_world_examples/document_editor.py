from abc import ABC, abstractmethod


# ------------------ Document Elements (Abstraction) ------------------
class DocumentElement(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


# ------------------ Concrete Elements ------------------
class TextElement(DocumentElement):
    def __init__(self, text: str):
        self.text = text

    def render(self) -> str:
        return self.text

class ImageElement(DocumentElement):
    def __init__(self, image_path: str):
        self.image_path = image_path

    def render(self) -> str:
        return f"[Image: {self.image_path}]"

class NewLineElement(DocumentElement):
    def render(self) -> str:
        return "\n"

class TabSpaceElement(DocumentElement):
    def render(self) -> str:
        return "\t"


# ------------------ Document (Composite) ------------------
class Document:
    def __init__(self):
        self.elements = []

    def add_element(self, document_element: DocumentElement):
        if document_element not in self.elements:
            self.elements.append(document_element)

    def delete_element(self, document_element: DocumentElement):
        if document_element in self.elements:
            self.elements.remove(document_element)

    def render(self):
        return "".join(element.render() for element in self.elements)


# ------------------ Persistence (Strategy) ------------------
class Persistence(ABC):
    @abstractmethod
    def save(self, data: str):
        pass


class FileStorage(Persistence):
    def save(self, data: str):
        try:
            with open("real_world_examples/document.txt", "w") as f:
                f.write(data)
            print("Document saved to document.txt")
        except Exception:
            print("Error: Unable to write file")


class DBStorage(Persistence):
    def save(self, data: str):
        print("data saved to DATABASE")


# ------------------ Document Editor ------------------
class DocumentEditor:
    def __init__(self, document: Document, storage: Persistence):
        self.document = document
        self.storage = storage
        self._rendered_document = None

    def add_text(self, text: str):
        self.document.add_element(TextElement(text))
        self._rendered_document = None  # invalidate cache

    def add_image(self, image_path: str):
        self.document.add_element(ImageElement(image_path))
        self._rendered_document = None

    def add_new_line(self):
        self.document.add_element(NewLineElement())
        self._rendered_document = None

    def add_tab_space(self):
        self.document.add_element(TabSpaceElement())
        self._rendered_document = None

    def render_document(self):
        if self._rendered_document is None:
            self._rendered_document = self.document.render()
        return self._rendered_document

    def save_document(self):
        self.storage.save(self.render_document())


# ------------------ Main ------------------
if __name__ == "__main__":
    document = Document()
    storage = FileStorage()

    editor = DocumentEditor(document, storage)
    editor.add_text("Hello, world!")
    editor.add_new_line()
    editor.add_text("This is a real-world document editor example.")
    editor.add_new_line()
    editor.add_tab_space()
    editor.add_text("Indented text after a tab space.")
    editor.add_new_line()
    editor.add_image("picture.jpg")

    print(editor.render_document())
    editor.save_document()

