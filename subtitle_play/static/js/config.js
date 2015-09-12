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





});
