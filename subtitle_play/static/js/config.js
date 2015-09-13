$(document).ready(function() {

    $('.menu .item').tab();

    $("#mv_upload").on("click",function(){
        $.get("/get_mv_template/",
            function(data){
                var result = data.result;
                var mv_template = "Empty"
                if (result == 0) {
                    mv_template = data.mv_list;
                }
                //clean html content first
                $("#mv_list_template > ul").empty();
                //for get mv list
                if (mv_template != "Empty") {
                    for(var i = 0; i < mv_template.length; i++) {
                        var content = "<li>" + mv_template[i] + "</li>";
                        $("#mv_list_template > ul").append(content);

                    }
                } else {
                    $("#mv_list_template > ul").html(mv_template);
                }

        },"json")

    });



    $("#subtitle_upload").on("click",function(){
        $.get("/get_subtitle_template/",
            function(data){
                var result = data.result;
                var subtitle_template = "Empty"
                if (result == 0) {
                    subtitle_template = data.subtitle_list;
                }
                //clean html content first
                $("#subtitle_list_template > ul").empty();
                //for get subtitle list
                if (subtitle_template != "Empty") {
                    for(var i = 0; i < subtitle_template.length; i++) {
                        var content = "<li>" + subtitle_template[i] + "</li>";
                        $("#subtitle_list_template > ul").append(content);

                    }
                } else {
                    $("#subtitle_list_template > ul").html(subtitle_template);
                }

        },"json")

    });

    $('#mv_fileupload').fileupload({
        dataType: 'json',
        replaceFileInput:false,
        formData: [
            { name: "csrfmiddlewaretoken", value:get_cookie('csrftoken')}
        ],


        add: function (e, data) {
            $("#upload_op").children("button").remove();
            //alert($("#mv_fileupload").val());
            data.context = $('<button/>').text('上传').addClass("ui blue button")
                .appendTo($("#upload_op"))
                .click(function () {
                    data.context = $('#mv_upload_result').text('上传中...').replaceAll($(this));
                    data.submit();
                });
        },


        done: function (e, data) {
            $.each(data.result, function (index, file) {
                $('#mv_upload_result').text(file.name + "上传成功!")
            });
        },

        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .bar').css(
                'width',
                progress / 3 + '%'
            );
        },


    });




});



function get_cookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
