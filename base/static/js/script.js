$('#following_btn').click(function(){

    var user_id = $('#following_btn').attr('data-id')
    var follow  = $('#following_btn').text()

    if(follow == 'follow'){
        var url = '/account/follow/'
        var btn_text = 'unfollow'
        var btn_class = 'btn btn-warning text-center mx-auto'
    }else{
        var url = '/account/unfollow/'
        var btn_text = 'follow'
        var btn_class = 'btn btn-primary text-center mx-auto'
    }

    $.ajax({
        url : url,
        method : 'POST' ,
        data : {
            'user_id' : user_id
        },
        success : function(data) {

        }
    });
    
});