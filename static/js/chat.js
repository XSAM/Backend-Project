var socket;

var current_channel = ''

var change_channel = function(channel)
{
    document.title = '聊天室 - ' + channel;
    if(current_channel)
    {
        $("#id-div-channels-title").text(document.title);
    }
    else
    {
        $("#id-div-channels-title").text('聊天室-未加入聊天室');
    }
}

var clear_board = function()
{
    $("#id_chat_area").val('');
}

$(document).ready(function(){
    socket = io.connect('ws://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function() {
        console.log('connect');
        clear_board();
    });

    change_channel(current_channel)

    socket.on('status', function(data) {
        $('#id_chat_area').val($('#id_chat_area').val() + '<' + data.msg + '>\n');
        //$('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    socket.on('message', function(data) {
        $('#id_chat_area').val($('#id_chat_area').val() + data.msg + '\n');
        //$('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    $('#text').keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            if (!current_channel)
            {
                console.log("no current_channel:", current_channel);
                $('#text').val('');
                alert('未加入聊天室')
                return;
            }
            text = $('#text').val();
            $('#text').val('');
            socket.emit('text', {msg: text, room:current_channel});
        }
    });

    $('.rc-channel').on('click', function(e){
        if (current_channel)
        {
             socket.emit('left', {room:current_channel}, function() {
                console.log("left room")
             });
        }
        // 加入房间
        current_channel = $(this).text();
        change_channel(current_channel);
        clear_board();
        socket.emit('joined', {msg:current_channel, room:current_channel});
        $('#id_chat_area').empty();
    })

    $('#default-channel').click()
});