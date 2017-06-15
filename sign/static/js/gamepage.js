/**
 * Created by zhangyao on 2017/6/13.
 */


$(document).ready(function () {

     var add2order = $('.add2order_btn');

     add2order.click(function () {
         var goodname = $(this).parent().find('.goodname');
         var count = $(this).parent().find(".form-control");
         var price = $(this).parent().find(".price");
         //创建一个订单的对象。
         var order = {
             goodname: goodname.attr('value'),
             count: count.val(),
             price: price.attr('value'),
         };
         console.log(order.goodname, order.count, order.price);
     });
 });