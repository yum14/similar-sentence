
class VectorModel:
    def __init__(self, sentence, vector):
        self.sentence = sentence
        self.vector = vector

    def to_dict(self):
        return {'sentence': self.sentence, 'vector': self.vector}