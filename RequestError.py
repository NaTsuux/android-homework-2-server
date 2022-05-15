class RequestError(Exception):
    def __init__(self, code, message, http_code):
        super(RequestError, self).__init__()
        self.code = code
        self.message = message
        self.http_code = http_code

    def __str__(self):
        return "RequestError: message {}".format(
            self.message
        )
