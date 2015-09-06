$(document).ready(function() {
	

			$("#login").click(function(){
					$.post("/auth_login/",
						{
							username:$("#username").val(),
							password:$("#password").val(),
						},
						function(data){
							if (data.res_login == "0"){
								window.location="/dispatch/"
							}else{
								alert("用户名密码错误")
							}
						},
						"json")
			});





		$(document).keyup(function(e){
		       //获取当前按键的键值
		       var keycode = e.which;
		       if(keycode == 13){
		        $("#login").trigger('click');
		        }
        });



	});

