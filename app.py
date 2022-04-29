from datetime import datetime

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.test


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detail/<idx>')
def detail(idx):
    # parameter의 값으로 전송해줌
    status_receive = request.args.get("status_give")
    return render_template("detail.html", status=status_receive)


@app.route('/post', methods=['POST'])
def save_post():

    id_receive = request.form['id_give']
    idx_receive = request.form['idx_give']
    content_receive = request.form['content_give']
    title_receive = request.form["title_give"]
    pw_receive = request.form['pw_give']
    #4번째 확장자 값을 들고 옴
    extension = file.filename.split('.')[-1]
    # datetime 사용법 3번째
    today = datetime.now()
    mytime = today.strftime("%Y년-%m-%d-%H-%M-%S")
    # 밑의 방식 사용시에 같은 이름으로만 파일이 저장되기 때문에
    # save_to = 'static/myp.jpg'
    # file-2022-04-28-이런 식으로 시간을 붙혀준다
    filename = f'file-{mytime}'
    # 저장 값을 들어가게 한다. 하지만 확장자가 고정이기때문에
    # save_to = f'static/{filename}.jpg'

    # 4번째
    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    # 받은 데이터를 저장하는 부분
    doc = {
        '_id' : id_receive,
        'idx' : idx_receive,
        'title' : title_receive,
        'content' : content_receive,
        # 파일이 저장되는 부분 f-string으로 만들어서 db에 저장
        'file' : f'{filename}.{extension}',
        'time' : f'{mytime}',
        'pw' : pw_receive
    }
    # key랑 value값 저장 된 것을 db에 저장
    db.test.insert_one(doc)

    return {"result": "success"}


@app.route('/post', methods=['GET'])
def get_post():
    posts = list(db.test.find({}, {'_id': False}))
    return jsonify({"posts": posts})


@app.route('/post', methods=['DELETE'])
def delete_post():
    idx = request.args.get('idx')
    db.test.delete_one({'idx': int(idx)})
    return {"result": "success"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)