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
});
