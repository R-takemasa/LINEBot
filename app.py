from flask import Flask, request, jsonify
import os
import logging
from linebot.v3.messaging.configuration import Configuration
from linebot.v3.messaging.api_client import ApiClient
from linebot.v3.messaging import MessagingApi, ReplyMessageRequest
from linebot.v3.messaging.models import TextMessage
from linebot.v3.webhook import MessageEvent, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from src.gemini_api import get_gemini_response  # Gemini API 関数をインポート
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

app = Flask(__name__)

# 環境変数の取得
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

# 環境変数がちゃんと読み込めているか確認（デバッグ用）
print("LINE_ACCESS_TOKEN:", LINE_ACCESS_TOKEN)
print("LINE_CHANNEL_SECRET:", LINE_CHANNEL_SECRET)

# LINE API クライアントの設定
config = Configuration(access_token=LINE_ACCESS_TOKEN)
api_client = ApiClient(configuration=config)
messaging_api = MessagingApi(api_client)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ログの設定
logging.basicConfig(level=logging.DEBUG)

# LINEのWebhookエンドポイント
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logging.error("Invalid signature error")
        return jsonify({"error": "Invalid signature"}), 400

    return "OK", 200

# メッセージイベントの処理
@handler.add(MessageEvent)
def handle_line_message(event):
    user_message = event.message.text
    logging.debug(f"Received message from LINE: {user_message}")
    
    try:
        reply_message = get_gemini_response(user_message) or "エラーが発生しましたyo。"
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        reply_message = "エラーが発生しました。"

    logging.debug(f"Reply message to LINE: {reply_message}")

    # 返信メッセージのリクエスト作成
    reply_request = ReplyMessageRequest(
        replyToken=event.reply_token,
        messages=[TextMessage(text=reply_message)]
    )

    # メッセージを送信
    messaging_api.reply_message(reply_request)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
