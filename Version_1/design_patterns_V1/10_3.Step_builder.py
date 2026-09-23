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
            print("Query params:")
            for key, value in self.query_params.items():
                print(f"{key}: {value}")

        if self.body:
            print(f"Body: {self.body}")

        print(f"Timeout: {self.timeout}")
        print("Request Executed Successfully !!")


class OptionalStep:

    def __init__(self, builder):
        self.builder = builder

    def with_query_param(self, key, value):
        self.builder.request.query_params[key] = value
        return self

    def with_body(self, body):
        self.builder.request.body = body
        return self

    def with_timeout(self, timeout):
        self.builder.request.timeout = timeout
        return self

    def build(self):
        if not self.builder.request.url:
            raise ValueError("URL cannot be empty")

        if not self.builder.request.method:
            raise ValueError("Method cannot be empty")

        return self.builder.request

class HeaderStep:
    def __init__(self, builder):
        self.builder = builder

    def with_header(self, key, value):
        self.builder.request.headers[key] = value
        return OptionalStep(self.builder)

class MethodStep:
    def __init__(self, builder):
        self.builder = builder

    def with_method(self, method):
        self.builder.request.method = method
        return HeaderStep(self.builder)

class UrlStep:
    def __init__(self, builder):
        self.builder = builder

    def with_url(self, url):
        self.builder.request.url = url
        return MethodStep(self.builder)


class HttpRequestStepBuilder:
    def __init__(self):
        self.request = HttpRequest()

    @staticmethod
    def builder():
        builder = HttpRequestStepBuilder()
        return UrlStep(builder)

def main():
    request = (
        HttpRequestStepBuilder
        .builder()
        .with_url("http://google.com")
        .with_method("GET")
        .with_header("Content-Type", "application/json")
        .with_query_param("key", "12345")
        .with_body({"name": "Aditya"})
        .with_timeout(60)
        .build()
    )

    request.execute()


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


class CPUStep:
    def __init__(self, builder):
        self.builder = builder

    def with_cpu(self, cpu):
        self.builder.computer.cpu = cpu
        return RamStep(self.builder)


class RamStep:
    def __init__(self, builder):
        self.builder = builder

    def with_ram(self, ram):
        self.builder.computer.ram = ram
        return OptionalStep(self.builder)


class OptionalStep:
    def __init__(self, builder):
        self.builder = builder

    def with_storage(self, storage):
        self.builder.computer.storage = storage
        return self

    def with_gpu(self, gpu):
        self.builder.computer.gpu = gpu
        return self

    def with_wifi(self, wifi):
        self.builder.computer.wifi = wifi
        return self

    def build(self):
        return self.builder.computer


class ComputerStepBuilder:
    def __init__(self):
        self.computer = Computer()

    @staticmethod
    def builder():
        builder = ComputerStepBuilder()
        return CPUStep(builder)


computer = (
    ComputerStepBuilder.builder()
    .with_cpu("Intel i7")
    .with_ram("32GB")
    .with_storage("1TB SSD")
    .with_gpu("RTX 4070")
    .with_wifi(True)
    .build()
)

computer.on()
"""