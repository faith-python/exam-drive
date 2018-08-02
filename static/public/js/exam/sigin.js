//由于模块都一次性加载，因此不用执行 layui.use() 来加载对应模块，直接使用即可：
// ;!function(){
//   var layer = layui.layer
//   ,form = layui.form;
  
//   layer.msg('Hello World');
// }();


function check_username(username){
    var re=/^1\d{10}$/;  
    if( re.test(username) ){  
         return true;
    }else{  
        layer.msg('请输入正确的手机号 !');
        return false;
    }  

};

function check_password(password){
    var pwdReg = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,16}$/;
    //6到16位数字与字母组合
    if( pwdReg.test(password) ){
        return true;
    }else{
        layer.msg('请输入6-16为字母,数字组合密码 !');
        return false;
    }
};

function check_nickname(nickname){
    ureg = /^[\u4E00-\u9FA5]{2,12}$/ ; 
    // areg = /^[a-zA-Z\/ ]{2,12}$/;
    if(ureg.test(nickname)){
        return true;

    }else{
        layer.msg('昵称非法!');
        return false;
    }
};

//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1];
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
        $('input[type=password]').change(function(event) {
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

function check_passwd_eq(){
    $('input[name=password2]').change(function(event) {
        /* Act on the event */
        var password1 = $('input[name=password1]').val();
        var password2 = $('input[name=password2]').val();
        if( password1 != password2 ){
            layer.msg('请确认你的密码!!! ');
            $(this).val('');

        }

    });

};

//refresh captcha code
function refresh_captcha_code(){
    $('.captcha.form-control').find('img').click(function(event) {
        /* Act on the event */
        var username = $('input[name=username]').val();
        if( !username ){
            layer.msg('亲!请输入手机号码!!')

        }else{
            $.ajax({
                'type': 'get',
                'url': '/api/captcha/',
                'data': {
                    'username': username,
                },
                'headers': {
                "X-XSRFTOKEN": get_cookie("_xsrf"),
            },
            'success': function(data){
                imgstr = '"data:image/jpeg;base64,';
                imgstr += data;
                $('.captcha.form-control').find('img').attr('src', imgsrc);



            },

            })
        }

    });
}

function check_captcha_code_eq(){
    $('input[name=captcha]').change(function(){
        var username = $('input[name=username]').val();
        var captcha_data = $(this).val();
        $.ajax({
            'type':'post',
            'url': '/api/captcha/text/',
            'data': {
                'username': username,
            },
            'headers': {
                "X-XSRFTOKEN": get_cookie("_xsrf"),
            },
            'success': function(data){
                if(data.reason == captcha_data){
                    layer.msg('验证图形验证码成功!');
                }else{
                    layer.msg('验证图形验证码失败!!!');
                    $(this).val('');
                };
            },
        });

    });
    

};


function ajax_reg_data(){
    var regbtn = $('.btn-login.btn-reg');

    regbtn.click(function(){
        var username = $('input[name=username]').val();
        var password1 = $('input[name=password1]').val();
        var password2 = $('input[name=password2]').val();
        var nickname = $('input[name=nickname]').val();
        $.ajax({
            'type': 'post',
            'url': '/reg',
            'data': {
                'username': username,
                'password1': password1,
                'password2': password2,
                'nickname': nickname,
            },
            'headers': {
                "X-XSRFTOKEN": get_cookie("_xsrf"),
            },
            'success': function(data){
                
                // data = JSON.parse(data);
                // console.log(data);
                if( data.error_code != 0 ){
                    // reg error
                    var reason = data.reason;
                    layer.msg(reason);
                }else{
                    //reg success!!!
                    layer.open({
                      content: '注册成功!,点击确定返回首页!',
                      yes: function(index, layero){
                        //do something
                        window.location.href='/';
                        layer.close(index); //如果设定了yes回调，需进行手工关闭
                      }
                    });   
                }
                

            },

        });

    });
};

function ajax_login_data(){
    var regbtn = $('.btn-login.btn-reg');

    regbtn.click(function(){
        var username = $('input[name=username]').val();
        var password = $('input[name=password]').val();
        $.ajax({
            'type': 'post',
            'url': '/login',
            'data': {
                'username': username,
                'password': password,
            },
            'headers': {
                "X-XSRFTOKEN": get_cookie("_xsrf"),
            },
            'success': function(data){
                // data = JSON.parse(data);
                // console.log(data);
                if( data.error_code != 0 ){
                    // reg error
                    var reason = data.reason;
                    layer.msg(reason);
                }else{
                    //reg success!!!
                    layer.open({
                      content: 'login!,点击确定返回首页!',
                      yes: function(index, layero){
                        //do something
                        window.location.href='/';
                        layer.close(index); //如果设定了yes回调，需进行手工关闭
                      }
                    });   
                }
                

            },

        });

    });
};




function reg_init(){
    check_value_on_changed('username'); 
    check_value_on_changed('nickname');
    check_value_on_changed('password');
    check_passwd_eq();
    refresh_captcha_code();
    check_captcha_code_eq();
    ajax_reg_data();
};

function login_init(){
    check_value_on_changed('username'); 
    check_value_on_changed('password');
    ajax_login_data();
};

var $sigin = {
    'reg_init':reg_init,
    'login_init': login_init,

};
