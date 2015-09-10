$(document).ready(function() {
	$("#config").on("click",function(){
        window.location.replace("http://172.18.14.100/config/")
    });

	$("#controller").on("click",function(){
        window.location.replace("http://172.18.14.100/controller/")
    });

	$("#show").on("click",function(){
        window.location.replace("http://172.18.14.100/show/")
    });
});
