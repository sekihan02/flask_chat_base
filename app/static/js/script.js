document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io();

    $('#chatForm').submit(function(e) {
        e.preventDefault();
        var message = $('#userInput').val().trim();
        if (message) {
            socket.emit('send_message', { message: message });
            // ユーザーのメッセージに含まれる改行を<br>タグに置換して表示
            var formattedMessage = message.replace(/\n/g, '<br>');
            $('#chat-box').append(`<div class="user-message">User: ${formattedMessage}</div>`);
            $('#userInput').val('');
            // メッセージボックスを自動スクロール
            var chatcontainer = document.getElementById('chat-container');
            chatcontainer.scrollTop = chatcontainer.scrollHeight;
        }
    });

    socket.on('receive_message', function(data) {
        // ボットのメッセージに含まれる改行を<br>タグに置換して表示
        var formattedMessage = data.message.replace(/\n/g, '<br>');
        $('#chat-box').append(`<div class="bot-message">Bot: ${formattedMessage}</div>`);
        // メッセージボックスを自動スクロール
        var chatcontainer = document.getElementById('chat-container');
        chatcontainer.scrollTop = chatcontainer.scrollHeight;
    });

    $('#userInput').keydown(function(e) {
        if (e.ctrlKey && e.keyCode === 13) {
            $('#chatForm').submit();
            e.preventDefault();
        }
    });
});
