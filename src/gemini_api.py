import logging
import requests
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # 環境変数からAPIキーを取得
GEMINI_API_URL = API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# 環境変数がちゃんと読み込めているか確認（デバッグ用）
print("GEMINI_API_KEY:", GEMINI_API_KEY)

def get_gemini_response(user_message):
    try:
        logging.debug(f"Sending message to Gemini API: {user_message}")

        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": user_message}
                    ]
                }
            ]
        }

        response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", json=data, headers=headers)

        logging.debug(f"Raw API response: {response.text}")

        if response.status_code != 200:
            logging.error(f"Gemini API error: {response.status_code} {response.text}")
            return "エラーが発生しました。"

        result = response.json()

        if "candidates" in result and result["candidates"]:
            # 修正した部分
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            logging.error("Gemini API returned empty response.")
            return "申し訳ありませんが、現在応答できません。"
    
    except Exception as e:
        logging.error(f"Error in Gemini API: {e}")
        return "申し訳ありませんが、現在応答できません。"
