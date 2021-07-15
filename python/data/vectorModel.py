from firebase_admin import firestore

class VectorModel:
    def __init__(self, id, sentence, vector, createdAt=firestore.SERVER_TIMESTAMP):
        self.id = id
        self.sentence = sentence
        self.vector = vector
        self.createdAt = createdAt

    def to_dict(self):
        return {'id': self.id, 'sentence': self.sentence, 'vector': self.vector, 'createdAt': self.createdAt}