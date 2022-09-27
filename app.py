import re

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('nCY8j7M9CKAwOkwHmFkFzSskwtoLqg8epUbpKb+GTKw3XebIl3v668ohW29MenthRmmDYlMhnGU21gbFw2RW3JJCHooxBsBwz6nmfGjGiMACbaKsU6iW4AsGwSwW9p3/HEjY96fyE1sszdKu+gUMQAdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('bfeccffa2aeaab8ded615ee63fa7d242')

line_bot_api.push_message('U8b8eaeef7460b703fc646f08c0337a40', TextSendMessage(text='終於可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if re.match("你是誰", message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage("才不告訴你勒~~"))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)