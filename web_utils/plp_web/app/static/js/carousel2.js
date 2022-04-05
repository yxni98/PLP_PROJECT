for(var i=1; i<4;i++){
 $('#picture').append("<img src='/static/images/amazon_2/"+i+".jpg' >");
}
//给图片转化设置定时函数
var index=0;
var timer;
function changeImageDot(){
 $('#picture img:nth-child('+(index+1)+')').css({
 display:'block',
 }).siblings().css({
 display:'none',
 });
 //设置随图片切换，对应的圆点样式发生变化
 // index+1 是因为索引是从0开始而 nth-child(i) 中的i是从1 开始的
 $('#dot span:nth-child('+(index+1)+')').css({
 transform: 'scale(1.2)',
 'background-color': 'blue',
 }).siblings().css({
 transform: 'scale(1)',
 'background-color':'gray',
 });
}
function produceTime(){
 timer=setInterval(function(){
 index++;
 if(index==3) 
 index=0;
 changeImageDot();
 
 },2000);
}

produceTime();
//鼠标悬浮在圆点上 ， 圆点和图片的变化
$('#dot span').mouseenter(function(){
 index=$(this).index();
 changeImageDot(); 
 clearInterval(timer); 
 produceTime(); 
});
//缺点：点击切换按钮后，图片切换后 ，会立即切换到下一个图片，需要设置 清除计时器后再新建一个计时器
$('.left').click(function(){
 index--;
 if(index==-1)
 index=2;
 changeImageDot(); 
 clearInterval(timer);
 produceTime();


});


$('.right').click(function(){
 index++;
 if(index==5)
 index=0;
 changeImageDot();
 clearInterval(timer);
 produceTime(); 
});