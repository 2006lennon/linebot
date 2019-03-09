from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

from engine.coin import now_currency

app = Flask(__name__)
# 設定你的Channel Access Token
line_bot_api = LineBotApi('Y32t68/EPL3Km0kZ2tVl4VK0HNtsPs+rJLE/N3+GnqGo48rZTp542Ku9c8jTSUjN6ZRtbUTCfU7fdtDWc1qk5QuYa3RN1bDtBECNFnlb9VqaHKWxFThwxLeBkXnGcS1z/cJLiYZuTcT9FMpl4p7UcQdB04t89/1O/w1cDnyilFU=')
# 設定你的Channel Secret
handler = WebhookHandler('60e2be83bc88352a7a29c8d78abce972')

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
	
#處理訊息
#當訊息種類為TextMessage時，從event中取出訊息內容，藉由TextSendMessage()包裝成符合格式的物件，並貼上message的標籤方便之後取用。
#接著透過LineBotApi物件中reply_message()方法，回傳相同的訊息內容
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	word=event.message.text
	if word=='你好':
		reply='Hello'
	elif word=='美金' or word=='日幣':
		reply=now_currency(word)
	else:
		reply='聽不懂'
	message=TextSendMessage(text=reply)
	line_bot_api.reply_message(event.reply_token,message)



import os
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)



