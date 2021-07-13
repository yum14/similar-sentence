import torch
from models import MyModel

class MySentenceBert():
  def __init__(self):
    self.model = MyModel()

  def encode(self, sentences):
    vectors = self.model.encode(sentences)
    return vectors

  def cdist(self, sentences, queries):
    # 全文をエンコード
    all_vectors = self.model.encode(sentences)
    s = torch.tensor(all_vectors).unsqueeze(0)

    # queryをエンコード
    query_vectors = self.model.encode(queries)
    q = torch.tensor(query_vectors).unsqueeze(0)

    data = torch.cdist(q, s)[0]

    return data
