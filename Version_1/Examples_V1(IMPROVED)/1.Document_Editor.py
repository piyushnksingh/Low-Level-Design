import uuid
from abc import ABC, abstractmethod
from uuid import UUID


class DocumentElement(ABC):
    def __init__(self):
        self.id = uuid.uuid4() # for identifying each element uniquely (needed for deletion)

    @abstractmethod
    def render(self) -> str:
        pass

class TextElement(DocumentElement):
    def __init__(self, text : str):
        super().__init__()
        self.text = text

    def render(self) -> str:
        return self.text

class ImageElement(DocumentElement):
    def __init__(self, img_path: str):
        super().__init__()
        self.img_path = img_path

    def render(self):
        return self.img_path

class NewLine(DocumentElement):
    def render(self) -> str:
        return "\n"

class TabSpace(DocumentElement):
    def render(self) -> str:
        return "\t"


class Document:
    def __init__(self):
        self.elements = []

    def add_element(self, element: DocumentElement):
        self.elements.append(element)

    def render_document(self):
        return "".join(element.render() for element in self.elements)

    def delete_element(self, element_id: UUID):
        self.elements = [
            ele for ele in self.elements if ele.id != element_id
        ]


class DocumentStorage(ABC):
    @abstractmethod
    def save(self, data: str):
        pass

class DBStorage(DocumentStorage):
    def save(self, data: str):
        print(f"saving {data} to Database storage !")

class FileStorage(DocumentStorage):
    def save(self, data: str):
        print(f"saving {data} to File storage !")


class DocumentEditor:
    def __init__(self, document: Document, storage: DocumentStorage):
        self.document = document
        self.storage = storage
        self._rendered_document = None # acts as cache one the document is rendered it is saved here

    def _add_element(self, element: DocumentElement):
        self.document.add_element(element)
        self._rendered_document = None # invalidate_cache

    def _delete_element(self, document_id: UUID):
        self.document.delete_element(document_id)
        self._rendered_document = None  # invalidate_cache

    def add_text(self, text: str):
        self._add_element(TextElement(text))

    def add_image(self, image_path: str):
        self._add_element(ImageElement(image_path))

    def add_new_line(self):
        self._add_element(NewLine())

    def add_tab_space(self):
        self._add_element(TabSpace())

    def render_document(self):
        if self._rendered_document is None:
            self._rendered_document = self.document.render_document()
        return self._rendered_document

    def save_document(self):
        self.storage.save(self.render_document())


def main():
    document = Document()
    storage = DBStorage()

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



if __name__ == "__main__":
    main()