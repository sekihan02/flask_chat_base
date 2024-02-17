from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
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

if __name__ == '__main__':
    socketio.run(app, debug=True)
