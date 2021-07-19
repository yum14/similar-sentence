
class ErrorResponse:
    def __init__(self, message):
        self.message = message

    def to_dict(self) -> dict:
        return {'message': self.message}