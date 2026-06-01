from abc import ABC, abstractmethod

# 1. Target interface expected by the client
class IReport(ABC):
    @abstractmethod
    def get_json_data(self, data: str) -> str:
        pass

# 2. Adaptee: provides XML data from raw input
class XMLDataProvider:
    def get_xml_data(self, data: str) -> str:
        # Expect "name : id"
        name, id_ = data.split(":")
        return (
            f"<user>"
            f"<name>{name}</name>"
            f"<id>{id_}</id>"
            f"</user>"
        )


class XMLDataProviderAdapter(IReport):
    def __init__(self, provider: XMLDataProvider):
        self._xml_provider = provider

    def get_json_data(self, data: str) -> str:
        # 1. Get XML
        xml = self._xml_provider.get_xml_data(data)

        # 2. Extract values (simple parsing)
        name = xml.split("<name>")[1].split("</name>")[0]
        user_id = xml.split("<id>")[1].split("</id>")[0]

        # 3. Return JSON
        return f'{{"name":"{name}", "id":{user_id}}}'


class Client:
    def get_report(self, report: IReport, raw_data: str):
        print("Processed JSON:", report.get_json_data(raw_data))


if __name__ == "__main__":
    xml_provider = XMLDataProvider()
    adapter = XMLDataProviderAdapter(xml_provider)

    raw_data = "Alice:26"

    client = Client()
    client.get_report(adapter, raw_data)


