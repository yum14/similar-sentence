# similar-sentence

## git config(コミット時の絵文字設定)

```sh
git config --global commit.template .commit_template
```

## 学習済モデル

pytorch-models-partialディレクトリ内の分割ファイルを結合して配置します。

```sh
cat pytorch-models-partial/pytorch_model.bin.* > python/training_bert_japanese/0_BERTJapanese/pytorch_model.bin
```

## docker-compose.yml

VIRTUAL_HOSTをデプロイ環境に合わせて変更します。
※ローカル環境ならこのままでもOK

```
VIRTUAL_HOST: ss.localhost
```
