$('.save-data-btn').on('click', function(){
	if( location.pathname.search('/user') != -1 ){
		var uuid =  $('input[name=uuid]').val();
		var username = $('input[name=username]').val();
		var nickname = $('input[name=nickname]').val();
		var password = $('input[name=password]').val();
		var locked = $('input[name=locked]').val();
		$.ajax({
			'type': 'get',
			'url': '/add/control/user',
			'data': {
				'uuid': uuid,
				'username': username,
				'nickname': nickname,
				'password': password,
				'locked': locked,
			},
			'success': function(data){
				if(  data.error_code == 0 ){
     				//layer.alert('数据处理成功!');
     				layer.open({
                          title: '提示信息'
                          ,content: '数据处理成功!'
                        });

				}else{
					//alert(data.reason);
					layer.open({
                      title: '提示信息'
                      ,content: 'data.reason'
                    });
				}
			}
		})

	}else if( location.pathname.search('/question') != -1 ){
		var id = $('input[name=qid]').val();
		var uuid = $('input[name=uuid]').val();
		var question = $('input[name=question]').val();
		var bestanswer = $('input[name=bestanswer]').val();
		var ta = $('input[name=ta]').val();
		var a = $('input[name=a]').val();
		var b = $('input[name=b]').val();
		var c = $('input[name=c]').val();
		var d = $('input[name=d]').val();
		var img = $('input[name=img]').val();
		var locked = $('input[name=locked]').val();
		$.ajax({
			'type': 'get',
			'url': '/add' + location.pathname.split('modify')[1],
			'data': {
				'id': id,
				'uuid': uuid,
				'question': question,
				'bestanswer': bestanswer,
				'ta': ta,
				'a': a,
				'b': b,
				'c': c,
				'd': d,
				'img': img,
				'locked': locked,

			},
			'success': function(data){
				// console.log(data);
				if(  data.error_code == 0 ){
//					alert('数据处理成功!');
                    layer.open({
                       title: '提示信息'
                      ,content: '数据处理成功!'
                    });

				}else{
//					alert(data.reason);
                    layer.open({
                       title: '提示信息'
                      ,content: 'data.reason'
                    });
				}


			},
		})

	}
})



















//////////////////////////////////////测试参数//////////////
function check_username(username){
    var re=/^1\d{10}$/;  
    if( re.test(username) ){  
         return true;
    }else{  
//        alert('请输入正确的手机号 !');
          layer.open({
                       title: '提示信息'
                      ,content: '请输入正确的手机号 !'
                    });
        return false;
    }  

};

function check_password(password){
    var pwdReg = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,16}$/;
    //6到16位数字与字母组合
    if( pwdReg.test(password) ){
        return true;
    }else{
//        alert('请输入6-16为字母,数字组合密码 !');
        layer.open({
                       title: '提示信息'
                      ,content: '请输入6-16为字母,数字组合密码 !'
                    });
        return false;
    }
};

function check_nickname(nickname){
    ureg = /^[\u4E00-\u9FA5]{2,12}$/ ; 
    // areg = /^[a-zA-Z\/ ]{2,12}$/;
    if(ureg.test(nickname)){
        return true;

    }else{
//        alert('昵称非法!');
        layer.open({
                       title: '提示信息'
                      ,content: '昵称非法!'
                    });
        return false;
    }
};


//cehck agrument
function check_value_on_changed(inputname){
    if( inputname == 'username' ){
        $('input[name=username]').change(function(event) {
            /* Act on the event */
            var username = $(this).val();
            imgsrc = 'api/captcha/?username=' + username
            $('.captcha.form-control').find('img').attr('src', imgsrc);
            if( ! check_username(username)){
                $(this).val('');
            }
        });

    }else if( inputname == 'password' ){
        $('input[name=password]').change(function(event) {
            /* Act on the event */
            var passwd = $(this).val();
            if( ! check_password(passwd) ){
                $(this).val('');

            }
        });

    }else if( inputname == 'nickname' ){
        $('input[name=nickname]').change(function(event) {
            /* Act on the event */
            var nickname = $(this).val();
            if( !check_nickname(nickname) ){
                $(this).val('');
            }
        });

    }
    
};


check_value_on_changed('username'); 
check_value_on_changed('nickname');
check_value_on_changed('password');
////////////////////////检查参数完成///////////////////////////////////////////