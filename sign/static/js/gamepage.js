/**
 * Created by zhangyao on 2017/6/13.
 */

jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

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
        // 将good对象加入到order对象里。
        order.push(good);
        console.log(good.goodname, good.count, good.price);

// TODO 进行重复判断。 如果该元素已经存在，则只加数字，不新增元素
        // 在页面上增加已经加入订单的产品
        var order_goodname = $("<td></td>").text(good.goodname)
        var order_goodcount = $("<td></td>").text(good.count)
        var order_item_del = $("<td></td>").append("<button class='btn btn-danger'>移除</button>")
        var order_tr_1 = $("<tr>").append(order_goodname, order_goodcount, order_item_del)
        $(".order_list").append(order_tr_1)
     });

    // 点击提交，把对象提交
    $('#submit_order').click(function () {
        orderdata = JSON.stringify({"order":order});
        console.log(orderdata);

        $.ajax({
            type: "POST",
            url: "getOrder",
            contentType: "application/json; charset=utf-8", // 规定了发送数据的类型
            // dataType: "json",  // 规定了返回 数据的类型。
            data:orderdata,
            success: function (result) {
                alert(orderdata);
            },
            error:function (result) {
                alert("错误，请稍后再试。")
            }
    });
    })

});