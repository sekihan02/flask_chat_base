from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'uploads'  # アップロードされたファイルを保存するフォルダ
socketio = SocketIO(app)

class StreamingLLMMemory:
    """
    StreamingLLMMemory クラスは、最新のメッセージと特定数のattention sinksを
    メモリに保持するためのクラスです。
    
    attention sinksは、言語モデルが常に注意を向けるべき初期のトークンで、
    モデルが過去の情報を"覚えて"いるのを手助けします。
    """
    def __init__(self, max_length=10, attention_sinks=4):
        """
        メモリの最大長と保持するattention sinksの数を設定
        
        :param max_length: int, メモリが保持するメッセージの最大数
        :param attention_sinks: int, 常にメモリに保持される初期トークンの数
        """
        self.memory = []
        self.max_length = max_length
        self.attention_sinks = attention_sinks
    
    def get(self):
        """
        現在のメモリの内容を返します。
        
        :return: list, メモリに保持されているメッセージ
        """
        return self.memory
    
    def add(self, message):
        """
        新しいメッセージをメモリに追加し、メモリがmax_lengthを超えないように
        調整します。もしmax_lengthを超える場合、attention_sinksと最新のメッセージを
        保持します。
        
        :param message: str, メモリに追加するメッセージ
        """
        self.memory.append(message)
        if len(self.memory) > self.max_length:
            self.memory = self.memory[:self.attention_sinks] + self.memory[-(self.max_length-self.attention_sinks):]
    
    def add_pair(self, user_message, ai_message):
        """
        ユーザーとAIからのメッセージのペアをメモリに追加します。
        
        :param user_message: str, ユーザーからのメッセージ
        :param ai_message: str, AIからのメッセージ
        """
        # self.add("User: " + user_message)
        # self.add("AI: " + ai_message)
        self.add({"role": "user", "content": user_message})
        self.add({"role": "assistant", "content": ai_message})
    
    # ここにはStreamingLLMとのインタラクションのための追加のメソッドを
    # 実装することもできます。例えば、generate_response, update_llm_modelなどです。

# 16件のメッセージを記憶するように設定
memory = StreamingLLMMemory(max_length=16)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_message')
def handle_message(data):
    user_message = data['message']
    # 2秒間待機
    # time.sleep(2)
    # ユーザーからのメッセージを処理するロジック（省略）
    # ユーザーからのメッセージに応じて、ボットの応答を送信
    res_message = "HELLO I'm BOT."
    emit('receive_message', {'message': res_message})
    
    # # 会話履歴の保存
    # memory.add_pair(user_message, res_message)
    # # 以前の会話をメモリから取得
    # past_conversation = memory.get()
    # emit('receive_message', {'message': str(past_conversation)})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':

        # 全ての接続されたクライアントに対してメッセージを送信
        socketio.emit('receive_message', {'message': f"ファイルは受けとってません"})
        
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join('uploads', filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file.save(save_path)

        # 全ての接続されたクライアントに対してメッセージを送信
        socketio.emit('receive_message', {'message': f"{filename} を受け取りました。"})
        
        return 'File uploaded successfully'

if __name__ == '__main__':
    socketio.run(app, debug=True)
