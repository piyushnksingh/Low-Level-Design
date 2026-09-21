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