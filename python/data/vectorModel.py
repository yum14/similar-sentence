from firebase_admin import firestore

class VectorModel:
    def __init__(self, id, sentence, vector, created_at=firestore.SERVER_TIMESTAMP):
        self.id = id
        self.sentence = sentence
        self.vector = vector
        self.created_at = created_at

    def to_dict(self):
        return {'id': self.id, 'sentence': self.sentence, 'vector': self.vector, 'created_at': self.created_at}