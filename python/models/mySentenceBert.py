import torch
from models import MyModel

class MySentenceBert():
  def __init__(self):
    self.model = MyModel()

  def encode(self, sentences):
    vectors = self.model.encode(sentences)
    return vectors

  def cdist(self, sentence_vectors, query_vectors):

    s = torch.tensor(sentence_vectors).unsqueeze(0)
    q = torch.tensor(query_vectors).unsqueeze(0)

    return torch.cdist(q, s)[0]

  def encodeAndCdist(self, sentences, queries):
    # 全文をエンコード
    all_vectors = self.model.encode(sentences)
    s = torch.tensor(all_vectors).unsqueeze(0)

    # queryをエンコード
    query_vectors = self.model.encode(queries)
    q = torch.tensor(query_vectors).unsqueeze(0)

    return torch.cdist(q, s)[0]
