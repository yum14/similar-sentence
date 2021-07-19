
class CdistResponse:
    def __init__(self, result=[], errors=[]):
        self.result = result
        self.errors = errors

    def to_dict(self) -> dict:
        return {'result': self.result, 'errors': self.errors}

class CdistResult:
    def __init__(self, id='', sentence='', score=''):
        self.id = id
        self.sentence = sentence
        self.score = score

    def to_dict(self) -> dict:
        return {'id': self.id, 'sentence': self.sentence, 'score': self.score}
