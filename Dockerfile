# Pythonの公式イメージをベースにする
FROM python:3.10

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストールする
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade line-bot-sdk
RUN pip install google-generativeai
RUN pip install --upgrade google-generativeai
RUN pip install python-dotenv





# アプリケーションコードをコンテナ内にコピー
COPY . /app

# 必要なポートを開ける
EXPOSE 8000

# アプリケーションを実行する
CMD ["python", "app.py"]
