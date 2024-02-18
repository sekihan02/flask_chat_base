from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'uploads'  # アップロードされたファイルを保存するフォルダ
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_message')
def handle_message(data):
    # user_message = data['message']
    # ユーザーからのメッセージを処理するロジック（省略）
    # ユーザーからのメッセージに応じて、ボットの応答を送信
    emit('receive_message', {'message': "HELLO I'm BOT."})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':

        # 全ての接続されたクライアントに対してメッセージを送信
        socketio.emit('receive_message', {'message': f"ファイルは受けっとってません"})
        
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
