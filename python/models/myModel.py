from sentence_transformers import SentenceTransformer
import os

class MyModel():
  def __init__(self):
    model_path = os.path.join(os.getcwd(), 'training_bert_japanese')
    self.model = SentenceTransformer(model_path, show_progress_bar=False)

  def encode(self, sentences):
    return self.model.encode(sentences)
