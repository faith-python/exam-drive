var rightNum=0,wrongNum=0,stopMsg=false;
var rearray=[['A','B'],['A','B','C','D'],['A','B','C','D']];
var redata,nowid=1,is_continue=0,is_first=0;



loadContent(1, cartype);

if(sx){
  //练习自动缓存
    var tid=$.cookie('tid_'+tx+km+zj);
  if(tid != null && tid != 1){
    $('#check .c-content p').html('上次练习到第'+tid+'题，是否继续？');
     layer.open({
              type: 1, //弹窗类型
              title:false, //是否展示标题，展示什么内容的标题
              closeBtn: 0, //标题旁边的关闭按钮
              shadeClose:false, //阴影
              move :'h4', //拖动
              area: ['450px', 'auto'], //宽高
              content: $('#check') //抓取内容
    });
    $('#continue').attr('onclick','jumptoaim('+tid+')');
  }else{
    is_first=1; //加载条关闭识别码
  }
}


//开始选择
$("#btnlists .item").live('click',function(){
  var tixing=parseInt(redata['Type']);
  if(tixing==1 || tixing==2){
      //判断&单选
      //缓存做题信息
      $(this).parent().find('.active').removeClass('active');
      $(this).addClass('active');
      $('#T'+nowid).attr('answer',$(this).attr('choice'));
      setStatus(nowid);
  }else if(tixing==3){
      //多选
      var asnum=$('#T'+nowid).attr('answer');
      var thischoice=$(this).attr('choice');
      if($(this).hasClass('active')){
        $(this).removeClass('active');
        asnum=asnum.replace(thischoice,'');
      }else{
        $(this).addClass('active');
        if(asnum){
          if(asnum.indexOf(thischoice) == -1){
            asnum=asnum+thischoice;
          }
        }else{
          asnum=thischoice;
        }
      }
      $('#T'+nowid).attr('answer',asnum);
  }
});


//练习单选和判断
$(".topic-l input[type=radio]").live('click',function(){
  if($('#T'+nowid).attr('answer')){
    return false;
  }
  var tixing=parseInt(redata['Type']);
  //缓存做题信息
  $(this).parent().find('.active').removeClass('active');
  $(this).addClass('active');
  $('#T'+nowid).attr('answer',$(this).val());
  setStatus(nowid);
  var answer=$('#T'+nowid).attr('answer');
  var trueanswer=$('#T'+nowid).attr('trueanswer');
  resultstr=getResult(answer,trueanswer,$('#T'+nowid).attr('tixing'));
  $('#Content').append(resultstr);
  $('#btnlists').hide();
});


//练习多选
$(".topic-l input[type=checkbox]").live('click',function(){
  var tixing=parseInt(redata['Type']);
  var asnum=$('#T'+nowid).attr('answer');
  var thischoice=$(this).val();
  if($(this).hasClass('active')){
    $(this).removeClass('active');
    asnum=asnum.replace(thischoice,'');
  }else{
    $(this).addClass('active');
    if(asnum){
      if(asnum.indexOf(thischoice) == -1){
        asnum=asnum+thischoice;
      }
    }else{
      asnum=thischoice;
    }
  }
  $('#T'+nowid).attr('answer',asnum);
});
//题目列表点击
$("#tlists li").click(function(){
    var num=parseInt($(this).attr('num'));
    loadContent(num, cartype);
    nowid=num;
});
//原图预览
$(".imgorvideo img").live('click',function(){
  viewImg('img');
});
$(".imgorvideo video").live('click',function(){
  viewImg('video');
});

function viewImg(viewType){
  if(viewType=='video'){
    var videosrc=$('.imgorvideo video').attr('src');
    layer.open({
      type: 1,
      title: false,
      shadeClose:false,
      skin: 'layui-layer-rim', //加上边框
      area: ['630px', '278px'], //宽高
      content: '<video src="'+videosrc+'" autoplay="autoplay" controls="controls" style="width:630px;height:278px;"></video>',
      shadeClose :true
    });
  }else if(viewType=='img'){
    var imgsrc=$('.imgorvideo img').attr('src');
    layer.open({
      type: 1,
      title: false,
      shadeClose:false,
      skin: 'layui-layer-rim', //加上边框
      area: ['auto', 'auto'], //宽高
      content: '<img src="'+imgsrc+'">',
      shadeClose :true
    });
  }
}


$("#xiangjie").click(function(){
    $("#bestanswer").toggle(300);
    if($(this).val()=='收起详解'){
      $(this).val('查看详解');
    }else{
      $(this).val('收起详解');
    }
});
$("#datika").click(function(){
    $(".info-answer").toggle(300);
    if($(this).val()=='收起答题卡'){
      $(this).val('展开答题卡');
    }else{
      $(this).val('收起答题卡');
    }
});
$(".tjsj").click(function(){
    Countdown.stopTime();
    jiaojuanlayer();
});


//load content
function loadContent(tid, cartype){
  if(nowid!=1){
    layer.load(0);
  }
  var id=redataid[tid-1]['id'];
  var tishi;
  $.getJSON('/api/ajax/getinfo/'+cartype+'/',{id:id},function(data){
      var status=data.error_code;
      if(status == 0){
        redata=data.data;
        var choicestr,resultstr='',btnstr,clickitemstr='';
        var answer=$('#T'+tid).attr('answer');
        if(answer){
          var asarr=answer.split('');
        }
        var trueanswer=$('#T'+tid).attr('trueanswer');
        //加载答题选项
        if(Type==1){
          //练习
          btnstr='<input class="item" type="button" value="A" choice=1 /><input class="item" type="button" value="B" choice=2 />';
          $('#btnlists').hide();
          if(redata['Type']==1){
            choicestr='<li><input type="radio" name="choice" value="1">A、正确</li><li><input type="radio" name="choice" value="2">B、错误</li>';
          }else if(redata['Type']==2){
            choicestr='<li><input type="radio" name="choice" value="1">A、'+redata['a']+'</li><li><input type="radio" name="choice" value="2">B、'+redata['b']+'</li><li><input type="radio" name="choice" value="3">C、'+redata['c']+'</li><li><input type="radio" name="choice" value="4">D、'+redata['d']+'</li>';
          }else if(redata['Type']==3){
            choicestr='<li><input type="checkbox" name="choice" value="1">A、'+redata['a']+'</li><li><input type="checkbox" name="choice" value="2">B、'+redata['b']+'</li><li><input type="checkbox" name="choice" value="3">C、'+redata['c']+'</li><li><input type="checkbox" name="choice" value="4">D、'+redata['d']+'</li>';
            $('#btnlists').show();
            $('#btnlists').html('<input class="duoxuan_btn" type="button" value="确定" onclick="checkDuoXuan()"/>');
          }


        }else{
          //考试
          btnstr='<input class="item" type="button" value="A" choice=1 /><input class="item" type="button" value="B" choice=2 />';
          if(redata['Type']==1){
            choicestr='<li choice=1>A、正确</li><li choice=2>B、错误</li>';
            tishi='判断题，请判断对错！';
          }else if(redata['Type']==2 || redata['Type']==3){
            choicestr='<li choice=1>A、'+redata['a']+'</li><li choice=2>B、'+redata['b']+'</li><li choice=3>C、'+redata['c']+'</li><li choice=4>D、'+redata['d']+'</li>';
            btnstr=btnstr+'<input class="item" type="button" value="C" choice=3 /><input class="item" type="button" value="D" choice=4 />';
            tishi='单选题，请选择你认为正确的答案！';
            if(redata['Type']==3){
                btnstr=btnstr+'<input class="duoxuan_btn" type="button" value="确定" onclick="checkDuoXuan()"/>';
                tishi='多选题，请选择你认为正确的答案！';
            }
          }
          //提示
          $('#tishi').html(tishi);
          if(answer != undefined && answer != null && answer != ''){
              $('#btnlists').html('');
          }else{
              if(Type == 1){
                $('#btnlists').show();
              }
              $('#btnlists').html(btnstr);
          }
        }
        $('#taolun').attr('href','/tiba/'+$('#T'+nowid).attr('rid')+'/');
        //加载解释
        $('#bestanswer p').html(redata.bestanswer);
        //加载题目内容和选项
        str='<ul><li>'+tid+'/'+countNum+'. '+redata.question+'</li>'+choicestr+'</ul>';
        if(nowid!=1 || is_first==1){
          layer.closeAll();
        }
        $('#Content').html(str);
        if(asarr && Type==1){
          for(var i in asarr){
            $('#Content ul li:nth-child('+(parseInt(asarr[i])+1)+') input').attr('checked','checked');
          }
          $('#btnlists').hide();
        }else{
          $('#btnlists').show();
        }
        //加载答题结果
        resultstr=getResult(answer,trueanswer,$('#T'+tid).attr('tixing'));
        $('#Content').append(resultstr);
        //加载图片和视频
        var reg=/mov$/;
        if(reg.test(redata.jiazhaoimg)){
            $('.imgorvideo').html('<video src="' + redata.jiazhaoimg+'" controls="controls" autoplay="autoplay">您的浏览器不支持不放</video><em><a href="javascript:;" onclick="viewImg(\'video\')">点击视频可放大观看</a></em>');
        }else if(redata.jiazhaoimg != undefined && redata.jiazhaoimg != null && redata.jiazhaoimg != ''){
             $('.imgorvideo').html('<img src="'+redata.jiazhaoimg+'" ><em><a href="javascript:;" onclick="viewImg(\'img\')">点击图片可查看原图</a></em>');
        }else{
             $('.imgorvideo').html('');
        }

      }
  });
}






//加载下一题
function nextQ(){
  var nextid=nowid+1;
  if($('#T'+nextid).html() == undefined || $('#T'+nextid).html() == ''){
    layer.msg('已经是最后一题');return false;
  }
  ++nowid;
  loadContent(nowid, cartype);
}
//加载上一题
function preQ(){
  var preid=nowid-1;
  if(preid<1){
    layer.msg('已经是第一题');return false;
  }
  --nowid;
  loadContent(nowid, cartype);
}

function getResult(answer,trueanswer,tixing){
  var answerstr,check,statusstr;
  if(answer == undefined || answer == null){
    //无答案
    answer="";
  }
  if(tixing==3){
    var tsarr=trueanswer.split('');
    var asarr=[];
    if(answer != ""){
      asarr=answer.split('');
    }
    check=checkvalue_duoxuan(asarr,tsarr);
  }else{
    check=checkvalue(answer,trueanswer,tixing);
  }
  cuowustr='';
  if(check['status']){
      statusstr="<i class='right'>恭喜你答对了！</i>  ";
      zhengquestr='';
  }else{
      zhengquestr='&nbsp;&nbsp;正确答案：<strong class="">'+check.tmsg+'</strong>';
      statusstr="<i class='wrong'>你答错了!</i>  ";
  }
  if(check.amsg != ''){
    var whystr='';
    if(Type != 1){
      whystr='&nbsp;&nbsp;<a class="blue" href="javascript:;" id="why">为什么？</a>';
    }
    answerstr='<div class="answer">'+statusstr+zhengquestr+whystr+'</div>';
  }else{
    answerstr='';
  }
  return answerstr;
}
//设置列表状态 1：对 2：错 3：已做 4：当前题
function setStatus(index){
    if($('#T'+index).attr('answer') == $('#T'+index).attr('trueanswer')){
        $('#T'+index).attr('class','info-blue');
        rightNum++;
    }else{
        if(is_continue==0 && Type != 1){
          if((wrongNum>=10 && km==1) || (wrongNum>=5 && km==4)){
            if(km==1){
              rightPercent=rightNum;
            }else if(km==4){
              rightPercent=rightNum*2;
            }
            $('.score').html(rightPercent);
            Countdown.stopTime();
            layer.open({
              type: 1,//弹窗类型
              title:false,//是否展示标题，展示什么内容的标题
              closeBtn: 0,//标题旁边的关闭按钮
              shadeClose:false,//阴影
              move :'h4',//拖动
              area: ['450px', 'auto'], //宽高
              content: $('#tixing')//抓取内容
            });
            return false;
          }
        }
        wrongNum++;
        $('#T'+index).attr('class','info-yellow');
    }
    if(Type == 1){
      $.cookie('tid_'+tx+km+zj,index);
      showResult();
      if(Auto == 0 && ($('#T'+index).attr('answer') == $('#T'+index).attr('trueanswer'))){
          setTimeout('nextQ()',300);
      }
    }else{
      nextQ();
    }

}
//设置选择状态
function setChoiceStatus(index){
    $('#T'+index).attr('class','info-blue');
}
function checkDuoXuan(){
    setStatus(nowid);
    if(Type == 1){
      var answer=$('#T'+nowid).attr('answer');
      var trueanswer=$('#T'+nowid).attr('trueanswer');
      resultstr=getResult(answer,trueanswer,$('#T'+nowid).attr('tixing'));
      $('#Content').append(resultstr);
      $('#btnlists').hide();
    }
}
//单选/判断题，检查错误
function checkvalue(answer,trueanswer,tixing){
  var arr={};
  arr['status']=false;
  var index1=parseInt(tixing)-1;
  var index2=parseInt(trueanswer)-1;
  var index3=parseInt(answer)-1;
  arr['tmsg']=rearray[index1][index2];
  if(answer==trueanswer){
    //答对
    arr['amsg']=arr['tmsg'];
    arr['status']=true;
  }else if(answer == ''){
    //没有答题
    arr['amsg']='';
  }else{
    //答错
    arr['amsg']=rearray[index1][index3];
  }
  return arr;
}
//多选，检查错误
function checkvalue_duoxuan(asarr,tsarr){
  var arr={};
  arr['status']=false;
  var astr="";
  var tstr="";
  asarr=asarr.sort();
  tsarr=tsarr.sort();
  if(asarr != '' && asarr != undefined && asarr != null){
    for(var i in asarr){
      astr+=rearray[2][parseInt(asarr[i])-1];
    }
  }
  if(tsarr != '' && tsarr != undefined && tsarr != null){
    for(var j in tsarr){
      tstr+=rearray[2][parseInt(tsarr[j])-1];
    }
  }
  arr['tmsg']=tstr;
  if(astr==tstr){
    //答对
    arr['amsg']=astr;
    arr['status']=true;
  }else if(astr == ''){
    //没有答题
    arr['amsg']='';
  }else{
    //答错
    arr['amsg']=astr;
  }
  return arr;
}
function jiaojuanlayer(){
  if(rightNum==0 && wrongNum==0){
      layer.msg('您还未答题，请答题');
      return false;
  }
  Countdown.stopTime();
  layer.open({
    type: 1,//弹窗类型
    title:false,//是否展示标题，展示什么内容的标题
    closeBtn: 0,//标题旁边的关闭按钮
    shadeClose:false,//阴影
    move :'h4',//拖动
    area: ['450px', 'auto'], //宽高
    content: $('#check')//抓取内容
  });
}

function layerDialog(num){
  layer.open({
    type: 1,//弹窗类型
    title:false,//是否展示标题，展示什么内容的标题
    closeBtn: 0,//标题旁边的关闭按钮
    shadeClose:false,//阴影
    move :'h4',//拖动
    area: ['auto', 'auto'], //宽高
    content: $('#explain')//抓取内容
  });
}
function closeDialog(){
    is_first=1;//加载条关闭识别码
    layer.closeAll();
    Countdown.init();
}
//$(this).on('click', function(){
//    if( !$('.layui-layer-content').html()  ){
//        Countdown.init();
//    }
//})
function jixu_lianxi(){
    Countdown.continueTime();
    is_continue=1;
    layer.closeAll();
}
function jixu_kaoshi(){
    Countdown.continueTime();
    layer.closeAll();
}






//set time
//查看为什么 时间暂停 加载解释
$("#why").live('click',function(){
    Countdown.stopTime();
    $('#jieshi_content').html(redata['bestanswer']);
    layerDialog(4);
    stopMsg=false;
    daojishi();
});
//end

function closeJiexi(){
    Countdown.continueTime();
    layer.closeAll();
    stopMsg=true;
}
function daojishi(){
//init stopMsg == False;
  if(stopMsg){
    $('#time').html(10);
    return false;
  }
  var wait_time=parseInt($('#time').html());
  var secs_time = 0;
  wait_time --;
  if(wait_time==-1){
    layer.closeAll();
    Countdown.continueTime();
    $('#time').html(10);
  }else{
    window.setTimeout("$('#time').html("+wait_time+");daojishi();",1000);
  }
}
//set time end







function changeType(){
    if($('.pic i:first-child').hasClass('icon')){
      $('.pic i:first-child').removeClass('icon');
      Auto=1;
    }else{
      $('.pic i:first-child').addClass('icon');
      Auto=0;
    }
}
function showResult(){
    $('.pic .rightnum').html(rightNum);
    $('.pic .wrongnum').html(wrongNum);
    var persent=Math.round(rightNum/(rightNum+wrongNum)*100);
    $('.pic .rightpercent').html(persent+'%');
}
function jumptoaim(tid){
  nowid=tid;
  layer.closeAll();
  loadContent(tid, cartype);
}
//统计错题率
function tongjiNum(){
  km=parseInt(km);
  var rightPercent=0;
  var loudaNum;
  var yongshi=0;
  if(km==1){
    rightPercent=rightNum;
    loudaNum=100-rightNum-wrongNum;
  }else if(km==4){
    rightPercent=rightNum*2;
    loudaNum=50-rightNum-wrongNum;
  }
  $('.score').html(rightPercent);
  var yongshi=$('.time').attr('alltime');
  var nickname=$('.getnickname').attr('data-value');
  $.getJSON('/api/ajax/saveresult/',{score:rightPercent,
								  	rightNum:rightNum,
								  	wrongNum:wrongNum,
								  	loudaNum:loudaNum,
								  	txtype:tx,
								  	kmtype:km,
								  	yongshi:yongshi,
								  	nickname:nickname},function(data){
								        if(!data.error_code){ 
                          var inner_html =  '您本次答题得分:'+ data.data[0] + ', 成绩:' + data.reason;
								        	layer.open({
											  title: '查看结果',
											  content: inner_html,
											  yes: function(index, layero){
											  	window.location.href="/";
											  },
											});    
								          	
								        }
  });
}

function tijiao(){
     layer.closeAll();
    Countdown.reset();   layer.closeAll();
    //统计错题率
    tongjiNum();
}
