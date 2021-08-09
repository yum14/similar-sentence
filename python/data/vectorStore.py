from firebase_admin import firestore
from .vectorModel import VectorModel
import uuid

class VectorStore():
    USERS_COLLECTION_NAME = 'users'
    VECTORS_COLLECTION_NAME = 'vectors'

    def __init__(self, uid):
        self.uid = uid
        self.db = firestore.client()

    def add(self, vector: VectorModel):
        self.db.collection(self.USERS_COLLECTION_NAME).document(self.uid).collection(self.VECTORS_COLLECTION_NAME).document(vector.id).set(vector.to_dict())

    def get(self):
        docs = self.db.collection(self.USERS_COLLECTION_NAME).document(self.uid).collection(self.VECTORS_COLLECTION_NAME).stream()

        dict_list = list(map(lambda x: x.to_dict(), docs))
        return list(map(lambda x: VectorModel(x['id'], x['sentence'], x['vector']), dict_list))
