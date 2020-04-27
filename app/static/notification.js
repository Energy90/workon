$(document).ready(function(){
    function set_message_count(n) {
        $('#message_count').text(n);
        $('#message_count').css('visibility', n ? 'visible' : 'hidden');
    }

    {% if current_user.is_authenticated %}
    $(function() {
        var since = 0;
        setInterval(function(){
            $.ajax('{{ url_for('main.notifications') }}?since=' + since).done(
                function(notifications) {
                    for (var i = 0; i < notifications.length; i++) {
                        if (notifications[i].name == 'unread_message_count')
                            set_message_count(notifications[i].data);
                        since = notifications[i].timestamp;

                    }
                }
            );
            10000);
        });
    });
    {% endif %}
});