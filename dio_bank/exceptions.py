from http import HTTPStatus


class NotFoundAccountError(Exception):
    def __init__(
            self,
            message: str = 'Account Not Found',
            status_code: int = HTTPStatus.NOT_FOUND
        ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundTransactionError(Exception):
    def __init__(
            self,
            message: str = 'Account Not Found',
            status_code: int = HTTPStatus.NOT_FOUND
        ) -> None:
        # Boa prática: inicializar a classe base Exception
        super().__init__(message)
        self.message = message
        self.status_code = status_code
