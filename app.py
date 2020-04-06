from flask import Flask ,render_template
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired


import os
import requests


TALKAPI_KEY = os.environ['TALKAPI_KEY']  # NOTE: 本番では直接書き込まない,環境変数で管理する 環境変数を設定したあとはatomを再起動する必要がある

#apiとの通信
#{'status': 0, 'message': 'ok', 'results': [{'perplexity': 0.06766985185966182, 'reply': 'こんにちは'}]} がAPIにアクセスすると返ってくる
def talkapi(text):
    url = 'https://api.a3rt.recruit-tech.co.jp/talk/v1/smalltalk'
    # NOTE: POST通信
    req = requests.post(url,{'apikey':TALKAPI_KEY,'query':text},timeout=5)
    data = req.json()
    # NOTE: エラーの時は０以外らしい
    if data['status'] != 0:
        # NOTE: エラー文取得
        return data['message']
    apimsg = data['results'][0]['reply']
    return apimsg



app = Flask(__name__)
app.config['SECRET_KEY'] = 'bf9f4ebfcsdgsdgsdfgsdgfsdfg9ca1f'

# NOTE: フォーム
class send(FlaskForm):
    msg = StringField('メッセージ',validators=[DataRequired()])
    submit = SubmitField('送信')

@app.route('/', methods=['GET','POST'])
def home():
    form = send()
    if form.validate_on_submit:
        sendmsg = form.msg.data
        responcemsg = talkapi(sendmsg)
        #responcemsg = "res"
        return render_template('home.html',title='TALK API',form=form,sendmsg=sendmsg,responcemsg=responcemsg)

    return render_template('home.html',title='TALK API',form=form)


if __name__ == '__main__':
    app.run(debug=True)
