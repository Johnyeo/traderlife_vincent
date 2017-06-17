/**
 * Created by zhangyao on 2017/6/13.
 */


$(document).ready(function () {
    // 构造good对象的类
    function good (goodname, count) {
        this.goodname = goodname;
        this.price = count;
    };
    // 创建一个数组。
    var order = [];
    var add2order = $('.add2order_btn');
    add2order.click(function () {
        var goodname = $(this).parent().find('.goodname');
        var count = $(this).parent().find(".form-control");
        var price = $(this).parent().find(".price");
        //创建一个订单的对象。
        var good = {
            goodname: goodname.attr('value'),
            count: count.val(),
            // price: price.attr('value'), 不能让用户输入这个价格。 防止伪造请求
        };
        order.push(good);
        console.log(good.goodname, good.count, good.price);
     });

    // 点击提交，把对象提交
    $('#submit_order').click(function () {
        orderdata = JSON.stringify(order);
        console.log(orderdata);
        $.post("gamepage/",
            {
                orderdata
            });
    })

});