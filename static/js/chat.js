$('#chatModal').on('show.bs.modal', function (event) {
    let overlay = document.getElementsByClassName('loading-overlay')[0]
    overlay.classList.toggle('is-active');  

    var button = $(event.relatedTarget) // Button that triggered the modal
    ticket_id = parseInt( button.data('id'));
    var modal = $(this)
    modal.find('.modal-title').text('Ticket #' + ticket_id)
    var args;
    args = {
        'pk': ticket_id,
        'comment': $('#close_comment').val()
    }
    var alert_message;
    $.ajax({
        type: 'GET',
        url: "/chat/",
        data: args,
        dataType: 'json',
        success: function (data) {
            overlay.classList.toggle('is-active');
            $('.chat-box').html('');
            // var d = JSON.parse(data)
            if(data.status = 201)  {
                $('.chat-box').html(data.data);
            } 
            if(data.length>0) {
                $.each(data, function(i, item){
                    insert_chat_message(item);
                })
            }
            // alert(alert_message);
            // document.location.href ="{% url 'app:get_chat_data' %}";
        }
    });

    $("#btn_send").off('click');
    $('#btn_send').on('click', function(){
        var message = $('#message').val();
        if(message == ''){
            alert('Message is Empty')
        }else{            
            send_message(ticket_id);
            new_msg = [];
            new_msg.is_user = true;
            new_msg.message = $('#message').val();
            new_msg.date_time = 'Just now';
            insert_chat_message(new_msg)
            var d = $('.chat-box');
            d.scrollTop(d.prop("scrollHeight"));
        }
    });
});

$( "#chatModal" ).on('shown.bs.modal', function(){
    var d = $('.chat-box');
    d.scrollTop(d.prop("scrollHeight"));
});
function send_message(ticket_id){
    var args;
    args = {
        'pk': ticket_id,
        'message': $('#message').val()
    }
    $.ajax({
        type: 'GET',
        url: "/send_message/",
        data: args,
        dataType: 'json',
        success: function (data) {
            $('#message').val('')
            if(data.status = 201)  
                modal.find('.modal-body').text(data.data)
        }
    });
}
function insert_chat_message(msg){
    var htmls = '';
    if(msg.is_user){
        htmls += '<div class="media w-75 ml-auto mb-2">';
        htmls += '<div class="media-body">';
        htmls += '<div class="bg-primary rounded py-2 px-3">';    
        htmls += '<p class="text-small mb-0 text-white">'
    } else{
        htmls += '<div class="media w-75 mb-2">';
        htmls += '<div class="media-body">';
        htmls += '<div class="bg-light rounded py-2 px-3">';  
        htmls += '<p class="text-small mb-0 text-muted">'  
    }
    htmls += msg.message +'</p>';
    htmls += '</div>';
    if(msg.is_user){
        htmls += '<p class="small text-muted" style="text-align: right;">';
    } else{
        htmls += '<p class="small text-muted">';
        htmls += msg.sender + ' | ';
    }
    
    htmls += msg.date_time
    htmls += '</p></div>';
    htmls += '</div>';
    $('.chat-box').append(htmls);
}