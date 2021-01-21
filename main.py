#https://qiita.com/shimajiri/items/cf7ccf69d184fdb2fb26

from flask import Flask, request, abort
import requests
import os
import logging
import sys
import cloudinary
import cloudinary.uploader
from cloudinary.uploader import upload
import cloudinary.api
from cloudinary.utils import cloudinary_url


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageMessage,
    VideoMessage,AudioMessage,LocationMessage,StickerMessage,
    FileMessage,
)

app = Flask(__name__)

#ログを標準出力にする
app.logger.addHandler(logging.StreamHandler(sys.stdout))
#レベル設定
app.logger.setLevel(logging.INFO)

#ログファイル出力 ↓いらないかも。。。
logging.basicConfig(filename="operation.log")

#Cloudinary設定↓
cloudinary.config(
    cloud_name = "yu1991ta",
    api_key = "648747536824239",
    api_secret = "F_PpehZ1SXIZKIYTZMynMHTENzw"
)



#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = "1z5F956PvFaWUAgqKQftoqvFFWHskSmpCFEQPIxhy1CFd+x+BEro/fNwrZ+77Ww4Wi+Pck3EkUEyG/W2Hj4zB7PpUxCp0fHW6bxs5g/L9stHF7zAH9shKwu/q4v0S0apcrCJlK/TrQCr9tyypYLCYwdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET =  "9bbc72e90a42c22ff505d1541dd8ea49"

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    app.logger.info("★★.Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#メッセージイベントの場合
#テキストメッセージの場合
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

#画像ファイルの場合
@handler.add(MessageEvent, message=ImageMessage)
def handle_message_image(event):

    #実ファイル取得 TODO:↓途中
    messageId = event.message.id
    #lineGetUrl = 'https://api.line.me/v2/bot/message/' + messageId + '/content/'
    parm={'Content-Type':'application/json; charset=UTF-8','Authorization':'Bearer '+ YOUR_CHANNEL_ACCESS_TOKEN}
    
    #デバッグ用ログ
    app.logger.info("★★.Request messageId: " + messageId)
    app.logger.info("★★.Request parm: " + parm)

    #CloudinaryへUpload

    #リプライ
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='ナイスですね～')
    )

#その他ファイルの場合(音声、動画などなど。。。)
@handler.add(MessageEvent, message=(VideoMessage,AudioMessage,LocationMessage,
StickerMessage,FileMessage))
def handle_message_other(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='ありがとう！でもその形式は対応してないよ！ごめんね！')
    )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)