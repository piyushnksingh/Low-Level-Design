class HttpRequest:
    def __init__(self):
        self.url = None
        self.method = None
        self.headers = {}
        self.query_params = {}
        self.body = None
        self.timeout = None

    def execute(self):
        print(f"Executing {self.method} request to {self.url}")

        if self.query_params:
            print("Query params: ")
            for key, value in self.query_params.items():
                print(f"{key}: {value}")

        if self.body:
            print(f"Body : {self.body}")

        print(f"Timeout : {self.timeout}")
        print("Request Executed Successfully !!")

class HttpRequestBuilder:
    def __init__(self):
        self.request = HttpRequest()

    def with_url(self, url):
        self.request.url = url
        return self

    def with_method(self, method):
        self.request.method = method
        return self

    def with_header(self, key, value):
        self.request.headers[key] = value
        return self

    def with_query_param(self, key, value):
        self.request.query_params[key] = value
        return self

    def with_body(self, body):
        self.request.body = body
        return self

    def with_timeout(self, timeout):
        self.request.timeout = timeout
        return self

    def build(self):
        if not self.request.url:
            raise ValueError("URL cannot be empty !")

        return self.request


def main():
    request = (
        HttpRequestBuilder()
        .with_url("https://api.example.com")
        .with_method("POST")
        .with_header("Content-Type", "application/json")
        .with_header("Accept", "application/json")
        .with_query_param("key", "12345")
        .with_body('{"name": "Aditya"}')
        .with_timeout(60)
        .build()
    )

    request.execute()

if __name__ == "__main__":
    main()


"""
class Computer:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None
        self.wifi = None

    def on(self):
        print("Computer on with following details")
        print("CPU:", self.cpu)
        print("RAM:", self.ram)
        print("Storage:", self.storage)
        print("GPU:", self.gpu)
        print("WiFi:", self.wifi)


class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()

    def with_cpu(self, cpu):
        self.computer.cpu = cpu
        return self

    def with_ram(self, ram):
        self.computer.ram = ram
        return self

    def with_storage(self, storage):
        self.computer.storage = storage
        return self

    def with_gpu(self, gpu):
        self.computer.gpu = gpu
        return self

    def with_wifi(self, wifi):
        self.computer.wifi = wifi
        return self

    def build(self):
        if not self.computer.cpu or not self.computer.ram:
            raise ValueError("CPU and RAM are required")

        return self.computer


computer = (
    ComputerBuilder()
    .with_cpu("Intel i7")
    .with_ram("32GB")
    .with_storage("1TB SSD")
    .with_gpu("RTX 4070")
    .with_wifi(True)
    .build()
)

computer.on()
"""

