from exception import ErrorCode


class SystemException(RuntimeError):

    def __init__(self, error_code: ErrorCode, detail: str):
        self.error_code = error_code
        self.detail = detail

    def logging(self):
        self.error_code.log(self.detail)
