var socket = io();

$(document).ready(function() {
    $('#send-button').click(function() {
        var message = $('#message-input').val();
        $('#message-input').val('');
        $('#chat-box').append('<div class="message user-message">' + message + '</div>');
        $('#chat-box').append('<div class="message bot-response"></div>');
        socket.emit('send_message', {message: message});
    });

    socket.on('receive_message', function(data) {
        var lastMessage = $('#chat-box .bot-response').last();
        if (lastMessage.html().length === 0) {
            lastMessage.append(data.data);
        } else {
            lastMessage.append(' ' + data.data);
        }
        $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
    });


    $('#message-input').keypress(function(event) {
        if (event.which === 13) { // Enter key
            event.preventDefault();
            $('#send-button').click();
        }
    });
});
