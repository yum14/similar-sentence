from firebase_admin import firestore
from .vectorModel import VectorModel
import uuid

class VectorStore():
    def __init__(self, uid):
        self.collectionName = 'vectors_' + uid
        self.db = firestore.client()

    def add(self, vector: VectorModel):
        self.db.collection(self.collectionName).document(vector.id).set(vector.to_dict())

    def get(self):
        docs = self.db.collection(self.collectionName).stream()

        dict_list = list(map(lambda x: x.to_dict(), docs))
        return list(map(lambda x: VectorModel(x['id'], x['sentence'], x['vector']), dict_list))
