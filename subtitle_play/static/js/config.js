$(document).ready(function() {

    $('.menu .item').tab();
    $('.ui.dropdown').dropdown();

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
            $("#mv_upload_op").children("button").remove();
            $("#mv_upload_result").hide();
            $("#progress").hide();

            //alert($("#mv_fileupload").val());
            data.context = $('<button/>').text('上传').addClass("ui blue button")
                .appendTo($("#mv_upload_op"))
                .click(function () {
                    //data.context = $('#mv_upload_result').text('上传中...').addClass("ui positive message").replaceAll($(this));
                    $('#mv_upload_result').text('上传中...').addClass("ui positive message");
                    $("#mv_upload_result").show();
                    $("#progress").show();
                    data.submit();
                    $("#mv_upload_op").children("button").remove();
                });
        },


        done: function (e, data) {
            if (data.result[0].exists) {
                $("#mv_upload_result").hide();
                $("#progress").hide();
                alert("文件已经存在!");
            }else {
                $("#progress").addClass("ui progress success")
                $.each(data.result, function (index, file) {
                    $('#mv_upload_result').text(file.name + "  :  上传成功!")
                });
                $("#mv_upload").click();
            }
        },

        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .bar').css(
                'width',
                progress + '%'
            );
            $("#progress").find(".progress").text(progress + '%')
        },


    });


    $('#subtitle_fileupload').fileupload({
        dataType: 'json',
        replaceFileInput:false,
        formData: [
            { name: "csrfmiddlewaretoken", value:get_cookie('csrftoken')}
        ],


        add: function (e, data) {
            $("#subtitle_upload_op").children("button").remove();
            $("#subtitle_upload_result").hide();
            $("#subtitle_progress").hide();

            //alert($("#subtitle_fileupload").val());
            data.context = $('<button/>').text('上传').addClass("ui blue button")
                .appendTo($("#subtitle_upload_op"))
                .click(function () {
                    //data.context = $('#subtitle_upload_result').text('上传中...').addClass("ui positive message").replaceAll($(this));
                    $('#subtitle_upload_result').text('上传中...').addClass("ui positive message");
                    $("#subtitle_upload_result").show();
                    $("#subtitle_progress").show();
                    data.submit();
                    $("#subtitle_upload_op").children("button").remove();
                });
        },


        done: function (e, data) {
            if (data.result[0].exists) {
                $("#subtitle_upload_result").hide();
                $("#subtitle_progress").hide();
                alert("文件已经存在!");
            } else {
                $("#subtitle_progress").addClass("ui progress success")
                $.each(data.result, function (index, file) {
                    $('#subtitle_upload_result').text(file.name + "  :  上传成功!")
                });
                $("#subtitle_upload").click();
            }
        },

        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#subtitle_progress .bar').css(
                'width',
                progress + '%'
            );
            $("#subtitle_progress").find(".progress").text(progress + '%')
        },


    });



    $("#music_config").on("click",function(){
         $.get("/get_mv_template/",
            function(data){
                var result = data.result;
                var mv_template= "Empty";
                if (result == 0) {
                    mv_template = data.mv_list;
                }
                //clean html content first
                $("#mv_select_list").empty();

                 if (mv_template != "Empty") {
                    for(var i = 0; i < mv_template.length; i++) {
                        var content = '<div class="item" data-value="' + (i + 1)  + '">' + mv_template[i] + '</div>';
                        $("#mv_select_list").append(content);
                    }

                 }
            
           },"json")

         $.get("/get_subtitle_template/",
            function(data){
                var result = data.result;
                var subtitle_template= "Empty";
                if (result == 0) {
                    subtitle_template = data.subtitle_list;
                }
                //clean html content first
                $("#subtitle_select_list").empty();

                if (subtitle_template != "Empty") {
                    for(var i = 0; i < subtitle_template.length; i++) {
                        var content = '<div class="item" data-value="' + (i + 1)  + '">' + subtitle_template[i] + '</div>';
                        $("#subtitle_select_list").append(content);
                    }
                 }
            
           },"json")


         $.get("/get_music_list/",
            function(data){
                var result = data.result;
                var music_list= "Empty";
                if (result == 0) {
                    music_list = data.music_list;
                }
                //clean html content first
                $("#music_select_list").empty();

                if (music_list != "Empty") {
                    for(var i = 0; i < music_list.length; i++) {
                        var content = '<div class="item" data-value="' + music_list[i]  + '">' + music_list[i] + '</div>';
                        $("#music_select_list").append(content);
                    }
                 }
            
           },"json")





    });

    $("#music_save").on("click",function(){
         $.post("/post_music/",
            {
                //music_name:$("#music_dropdown_selected").val(),
                music_name:$("#search_text").val(),
                mv_name:$("#mv_selected").text(),
                subtitle_name:$("#subtitle_selected").text(),
                csrfmiddlewaretoken:get_cookie('csrftoken'),
            },
            function(data){
                result = data.result;
                switch (result) {
                    case 0:
                        alert("添加成功!");
                        break;
                    default:
                        alert("添加失败,ErrCode:" + result);
                        break;
                }

                window.location.reload()

            }, "json");

    });


    $("#music_dropdown_selected").bind("DOMSubtreeModified",function() {

        var music_name = $("#music_dropdown_selected").text();
        $.get("/get_music_args/", 
           {
               music_name: music_name
           },
          function(data) {
              if (data.result == 0) {
                  mv_name = data.args_list["mv"];
                  subtitle_name = data.args_list["subtitle"];

                  $("#mv_selected").text(mv_name);
                  $("#subtitle_selected").text(subtitle_name);
                  $("#music_save").css("margin-left","30px");
                  $("#music_delete").show();

              } else {
                  alert("该歌曲信息不完整!")
              }

          },"json")

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
