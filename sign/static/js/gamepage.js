/**
 * Created by zhangyao on 2017/6/13.
 */

$(document).ready(function () {

     var add2order = $('.add2order_btn');

     add2order.click(function () {
         var goodname = $('.add2order_btn').parent().find('.goodname');
         var count = $(".count");
         var price = $(".price");
         var order = {
             goodname: goodname.value,
             count: count.value,
             price: price.value,
         };
         console.log(goodname.attr('value'));
     });
 });