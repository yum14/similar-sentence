from firebase_admin import firestore
from .vectorModel import VectorModel
import uuid

class VectorStore():
    def __init__(self):
        self.collectionName = 'vectors'
        self.db = firestore.client()

    def add(self, vector: VectorModel):
        self.db.collection(self.collectionName).document(str(uuid.uuid4())).set(vector.to_dict())

