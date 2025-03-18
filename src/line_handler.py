from linebot.v3.messaging import MessagingApi  # 修正: MessagingApi をインポート
from linebot.v3.messaging.models import TextMessage, ReplyMessageRequest  # ReplyMessageRequest を追加
from src.gemini_api import get_gemini_response  # Gemini API の関数をインポート

def handle_message(event, channel_access_token):
    user_message = event.message.text
    reply_message = get_gemini_response(user_message)  # ここで Gemini API のレスポンスを取得

    # MessagingApi を作成
    messaging_api = MessagingApi(channel_access_token)

    # メッセージの送信リクエストを作成
    reply_message_request = ReplyMessageRequest(
        replyToken=event.reply_token,
        messages=[TextMessage(text=reply_message)]
    )

    # メッセージを送信
    messaging_api.reply_message(reply_message_request)
