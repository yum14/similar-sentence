
class VectorResponse:
    def __init__(self, id='', errors=[]):
        self.id = id
        self.errors = errors

    def to_dict(self) -> dict:
        return {'id': self.id, 'errors': self.errors}
