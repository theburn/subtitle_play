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
                $("#mv_list_template").html(mv_template)
        },"json")

    });
});
