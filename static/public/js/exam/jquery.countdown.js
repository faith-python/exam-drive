//倒计时
var alltime=1;
var Countdown = {
	flag : true,
	data : [0,0,0,0,0,0],
	stopStatus:false,
	//初始化数据
	init : function(){
		var that = this;
		$('.ending').hide();
		if(that.flag){
			$('.begin').html('重置');
			that.flag = false;
			var hour = $('.hour').val();
			var minute = $('.minute').val();
			var second = $('.second').val();
			if(that.varliNum(hour) && that.varliNum(minute) && that.varliNum(second)){
				if(hour<=0 && minute<=0 && second<=0){
					that.reset();
					return;
				}
				if(minute>59){minute = 59;$('.minute').val('59')}
				if(second>59){second = 59;$('.second').val('59')}
				$('.input').each(function(){
					if($(this).val()>0 && $(this).val()<10){
						$(this).val('0'+$(this).val());
					}
				})
				that.data[0] = parseInt(hour/10);
				that.data[1] = hour%10;
				that.data[2] = parseInt(minute/10);
				that.data[3] = minute%10;
				that.data[4] = parseInt(second/10);
				that.data[5] = second%10;
				$('.time').find("span.static:eq(0)").html(that.data[0]);
				$('.time').find("span.static:eq(1)").html(that.data[1]);
				$('.time').find("span.static:eq(2)").html(that.data[2]);
				$('.time').find("span.static:eq(3)").html(that.data[3]);
				$('.time').find("span.static:eq(4)").html(that.data[4]);
				$('.time').find("span.static:eq(5)").html(that.data[5]);

				that.begin();
			}else{
//				alert('只能输入数字')
				layer.open({
                          title: '提示信息'
                          ,content: '只能输入数字!'
                        });
			}
		}else{
			that.reset();
		}		
	},
	//重置
	reset : function(){
		var that = this;
		$('.begin').html('开始');
		that.flag = true;
		$('.time').find("li.num").find('span').html('0');
		$('.input').val('00');
		$('.ending').hide();
		that.data = [0,0,0,0,0,0];
	},
	//数字校验
	varliNum : function(value){
		return /^\d+$/.test(value)
	},
	//开始
	begin : function(){
		var that = this;
		if(that.stopStatus==true){
			return false;
		}
		setTimeout(function() {
			//判断是否为0
			if(!that.flag){
				if(that.getData()){
					that.reset();
					$('.ending').show();
					 alert('时间到了!');
//					layer.open({
//                          title: '提示信息'
//                          ,content: '时间到了!'
//                        });
					tijiao();
				}else{
					alltime++;
					that.begin(true);
				}
			}
		}, 1000)
	},
	//暂停计时
	stopTime : function(){
		var that = this;
		that.stopStatus=true;
	},
	//继续计时
	continueTime : function(){
		var that = this;
		that.stopStatus=false;
		that.begin();
	},
	//获取数据状态
	getData : function(){
		var that = this;
		var data = that.data;
		if(data[5]>0){
			data = [data[0],data[1],data[2],data[3],data[4],data[5]-1];
			that.changeNum(5,data[5]);
		}else if(data[4]>0){
			data = [data[0],data[1],data[2],data[3],data[4]-1,9];
			that.changeNum(4,data[4]);
			that.changeNum(5,9);
		}else if(data[3]>0){
			data = [data[0],data[1],data[2],data[3]-1,5,9];
			that.changeNum(3,data[3]);
			that.changeNum(4,5);
			that.changeNum(5,9);
		}else if(data[2]>0){
			data = [data[0],data[1],data[2]-1,9,5,9];
			that.changeNum(2,data[2]);
			that.changeNum(3,9);
			that.changeNum(4,5);
			that.changeNum(5,9);
		}else if(data[1]>0){
			data = [data[0],data[1]-1,5,9,5,9];
			that.changeNum(1,data[1]);
			that.changeNum(2,5);
			that.changeNum(3,9);
			that.changeNum(4,5);
			that.changeNum(5,9);
		}else if(data[0]>0){
			data = [data[0]-1,9,5,9,5,9];
			that.changeNum(0,data[0]);
			that.changeNum(1,9);
			that.changeNum(2,5);
			that.changeNum(3,9);
			that.changeNum(4,5);
			that.changeNum(5,9);
		}else{
			return true;
		}
		that.data = data;
		return false;
	},
	//修改样式
	changeNum : function(i,num){
		var that = this;
		$('.time').attr('alltime',alltime);
		$('.time').find("span.old:eq("+i+")").before('<span class="static new">'+num+'</span>')
		$(".old:eq("+i+")").animate({opacity:'0'},300).remove();
		$(".new").animate({opacity:'1'},300).removeClass('new').addClass('old');
	}
	
}