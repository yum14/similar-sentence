import json
from flask import request, Flask, abort
from flask.json import jsonify
import firebase_admin
from firebase_admin import credentials, auth
import config
from models import MySentenceBert
from data import VectorStore, VectorModel

import uuid

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

bert = MySentenceBert()

if len(config.FIREBASE_CONFIG) == 0:
    firebase_admin.initialize_app()
else:
    # デバッグ時
    print("credential: ", config.FIREBASE_CONFIG)
    cred = credentials.Certificate(config.FIREBASE_CONFIG)
    firebase_admin.initialize_app(cred)
    
@app.route('/hello', methods=['POST'])
def test():
    return jsonify({'message': 'hello world!'})

@app.route('/encode', methods=['POST'])
def encode():

    # 認証
    if len(config.NEEDS_AUCHENTICATION) == 0 or config.NEEDS_AUCHENTICATION == 'TRUE':
        # idToken取得
        id_token = request.headers.get("Authorization")
        if not id_token:
            return jsonify({'message': 'no token.'}), 403

        try:
            # idTokenの検証
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
        except:
            return jsonify({'message': 'Illegal token.'}), 403

    # jsonリクエストから値取得
    payload = request.json
    id = payload.get('id')
    sentence = payload.get('sentence')

    if not id:
        return jsonify({'message': "no attribute 'id'"}), 400

    if not sentence:
        return jsonify({'message': "no attribute 'sentence'"}), 400

    print('request: ', {'id': id, 'sentence': sentence}, flush=True)

    # 配列化
    sentences = [sentence]

    # ベクトル化
    vectors = bert.encode(sentences)
    vector_arr = list(map(lambda x: x.tolist(), vectors))

    store = VectorStore()

    for i, sentence in enumerate(sentences):
        print('vector: ', vector_arr[i], flush=True)
        store.add(VectorModel(id, sentence, vector_arr[i]))

    return jsonify(vector_arr)



@app.route('/encodetestdata', methods=['POST'])
def encodetestdata():

    # 認証
    if len(config.NEEDS_AUCHENTICATION) == 0 or config.NEEDS_AUCHENTICATION == 'TRUE':
        # idToken取得
        id_token = request.headers.get("Authorization")
        if not id_token:
            return jsonify({'message': 'no token.'}), 403

        try:
            # idTokenの検証
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
        except:
            return jsonify({'message': 'Illegal token.'}), 403

    # jsonリクエストから値取得
    payload = request.json
    sentences = payload.get('sentences')

    # ベクトル化
    vectors = bert.encode(sentences)
    vector_arr = list(map(lambda x: x.tolist(), vectors))

    store = VectorStore()

    for i, sentence in enumerate(sentences):
        print('vector: ', vector_arr[i], flush=True)
        store.add(VectorModel(str(uuid.uuid4()), sentence, vector_arr[i]))

    return jsonify(vector_arr)



@app.route('/cdist/', methods=['GET'])
def cdist():

    # 認証
    if len(config.NEEDS_AUCHENTICATION) == 0 or config.NEEDS_AUCHENTICATION == 'TRUE':
        # idToken取得
        id_token = request.headers.get("Authorization")
        if not id_token:
            return jsonify({'message': 'no token.'}), 403

        try:
            # idTokenの検証
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
        except:
            return jsonify({'message': 'Illegal token.'}), 403

    q = request.args.get('q', '')

    if not q:
        return jsonify({'message': 'no content.'}), 400

    # ベクトル化
    query_vectors = bert.encode([q])

    # vectorデータ全件取得
    store = VectorStore()
    all_sentences = store.get()

    all_labels = list(map(lambda x: {'id': x.id, 'sentence': x.sentence}, all_sentences))
    all_vectors = list(map(lambda x: x.vector, all_sentences))

    # 距離を算出
    all_distances = bert.cdist(all_vectors, query_vectors)
        
    n = 5
    res = []

    for i, distances in enumerate(all_distances):
        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])

        res_items = []

        # score上位５件出力
        for j, distance in [item for item in results[0:n]]:

            # print(j, all_labels[j].strip(), "(Score: %.4f)" % (distance / 2))
            res_items.append({'id': all_labels[j]['id'], 'sentence': all_labels[j]['sentence'], 'score': distance.item() / 2})

        res.append(res_items)

    return jsonify(res)


@app.route('/', methods=['GET','POST'])
def callApi():

    if request.method == 'GET':

        sentences = ["お辞儀をしている男性会社員", "笑い袋", "テクニカルエバンジェリスト（女性）", "戦うAI", "笑う男性（5段階）", "漫才師", "お辞儀をしている医者（女性）", "お辞儀をしている薬剤師", "福笑いをしている人", "AIの家族", "コント師", 
        "福笑い（女性）", "お辞儀をしている犬", "苦笑いをする女性", "お辞儀をしている医者", "いろいろな漫符", 
        "雛人形「仕丁・三人上戸」", "ダンス「踊る男性」", "拍手をしている人", "定年（男性）", "ものまね芸人", "福笑いのおたふく", 
        "お辞儀をしている看護師（男性）", "愛想笑い", "福笑い（ひょっとこ）", "成長する人工知能", "苦笑いをする男性", 
        "運動会「徒競走・白組」", "人工知能と喧嘩をする人", "人工知能", "ありがた迷惑", "お辞儀をしているクマ", "笑う女性（5段階）", 
        "人工知能とメールをする人（男性）", "技術書", "笑いをこらえる人（女性）", "ダンス「踊る女性」", "お辞儀をしている猫", 
        "福笑い（男性）", "武器を持つAI", "作曲する人工知能", "縄跳びを飛んでいる女性", "福笑い（おかめ）", "茅の輪くぐり", "表情", 
        "AIと仲良くなる人間", "お笑い芸人「漫才師」", "人工知能とメールをする人（女性）", "人工知能と戦う囲碁の棋士", "拍手している女の子", 
        "検索する人工知能", "ピースサインを出す人（女性）", "啓示を受けた人（女性）", "仕事をする人工知能", "一輪車に乗る女の子", 
        "お辞儀をしているウサギ", "走る猫（笑顔）", "人工知能と戦う将棋の棋士", "遠足「お弁当・男の子・女の子」", "心を持ったAI", 
        "プレゼントをもらって喜ぶ女の子", "技術書（バラバラ）", "いろいろな表情の酔っぱらい（男性）", "拍手している人（棒人間）", 
        "仕事を奪う人工知能", "文章を書く人工知能", "いろいろな映画の「つづく」", "絵を描く人工知能", "拍手している男の子", "ハリセン", 
        "人工知能と仲良くする人たち", "ON AIRランプ", "いろいろな表情の酔っぱらい（女性）", "徹夜明けの笑顔（女性）", 
        "徹夜明けの笑顔（男性）", "お辞儀をしている女性会社員", "バンザイをしているお婆さん", "画像認識をするAI", 
        "芸人の男の子（将来の夢）", "料理「女性」", "ピコピコハンマー", "鏡を見る人（笑顔の男性）", "笑いをこらえる人（男性）", 
        "シンギュラリティ", "人工知能に仕事を任せる人", "スマートスピーカー", "学ぶ人工知能", "人工知能・AI", "英語のアルファベット", 
        "お金を見つめてニヤけている男性", "「ありがとう」と言っている人", "定年（女性）", "テクニカルエバンジェリスト（男性）", 
        "スタンディングオベーション"]

        return """
        <form action="/" method="POST">
        <p>queries</p>
        <textarea name="queries" rows="5" style="width: 560px">感謝\n戦闘</textarea>
        <p>sentences</p>
        <textarea name="sentences" rows="20" style="width: 560px">%s</textarea>
        <div style="margin-top: 12px">
        <button type="submit" style="width: 120px">送信</button>
        <button type="reset" style="width: 120px">リセット</button>
        </div>
        </form>""" % '\n'.join(sentences)

    elif request.method == 'POST':

        n = 5
        queries = request.form["queries"].replace('\r\n', '\n').replace('\r', '\n').split('\n')
        sentences = request.form["sentences"].replace('\r\n', '\n').replace('\r', '\n').split('\n')
        all_distances = bert.encodeAndCdist(sentences, queries)
        
        res = []

        for i, distances in enumerate(all_distances):
            results = zip(range(len(distances)), distances)
            results = sorted(results, key=lambda x: x[1])
        
            # print("\n\n======================\n\n")
            print("Query:", queries[i])
            # print("\nTop 5 most similar sentences in corpus:")

            res_items = []
            
            # # scoreが10未満(2で割った上で)のもののみ対象とする
            # for j, distance in [item for item in results[0:n] if item[1] / 2 < 10]:

            # score上位５件出力
            for j, distance in [item for item in results[0:n]]:

                print(j, sentences[j].strip(), "(Score: %.4f)" % (distance / 2))
                res_items.append({'id': j, 'value': sentences[j].strip(), 'score': distance.item() / 2})

            res.append(res_items)

        return jsonify(res)

    else:
        return abort(400)



if __name__ == '__main__':

    # ローカル実行用（gunicorn起動の場合、ここには入ってこない）
    app.run(host='127.0.0.1', port=8080, debug=True)
