/**
 * Created by zhangyao on 2017/6/13.
 */

jQuery(document).ajaxSend(function (event, xhr, settings) {
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
    function good(goodname, count, price) {
        this.goodname = goodname;
        this.count = count;
        this.price = price;
    };

    // 修改成，计算order对象中的总价值
    function caculate_total(order) {
        // 计算总订单额
        total = 0
        $.each(order, function (i, good) {
            total = total + good.count * good.price;
            // alert(good.count);
        });
        return total;
    };

    // 在order中新增项
    function add_good(order, goodname, count, price) {
        //创建一个产品的对象。
        var good = {
            goodname: goodname.attr('value'),
            count: count.val(),
            // price: price.attr('value'), 不能让用户输入这个价格。 防止伪造请求
            // price真正扣钱的时候要根据服务器上的 price，前台只是提供一个方便计算的途径。
            price: price.attr('value')
        };
        order.push(good);

        // 在UI上增加已经加入订单的产品  √
        var order_index = $("<td class='order_index'>").text(index);
        var order_goodname = $("<td></td>").text(good.goodname);
        var order_goodcount = $("<td class='order_count'></td>").text(good.count);
        var order_goodprice = $("<td class='order_item_sum'>").text("$" + good.count * good.price);
        var order_item_del = $("<td></td>").append("<button class='btn btn-xs btn-danger remove_btn' style='width: 60px'>移除</button>");
        var order_tr_1 = $("<tr class='order_tr'>").append(order_index, order_goodname, order_goodcount, order_goodprice, order_item_del);
        $(".order_list").append(order_tr_1);
        index = index + 1;  // 序号

        console.log(good.goodname, good.count, good.price);
    };

    // 在order中增加数量
    function add_good_count(order, index, goodname, count, price, good_2b_add_id) {
        good = order[good_2b_add_id];
        // 将str转换成数字 计算然后返回给goodcount， order的good_2b_add_id是从循环中得来的。
        origin = Number(good.count);
        new_add = Number(count.val());
        origin = origin + new_add;
        good.count = origin;
        console.log(good.count + "and" + count.val())

        // 重新计算所有的在list中的,count 和 subtotal
        // 注意eq选择器，用的是两个双引号两个+号。
        $(".order_tr:eq(" + good_2b_add_id + ")").find(".order_count").text(good.count);
        $(".order_tr:eq(" + good_2b_add_id + ")").find(".order_item_sum").text("$" + good.count * good.price);
    }

    // 创建一个数组。用来盛放加入订单的产品。 order_total用于计算总额。
    var order = [];
    var order_total = 0;
    var index = 1
    // 点击加入订单按钮后
    function click_add_to_order() {
        var add2order = $('.add2order_btn');
        add2order.click(function () {
            var goodname = $(this).parent().find('.goodname');
            var count = $(this).parent().find(".form-control");
            var price = $(this).parent().find(".price");
            var good_existed = false;
            var good_2b_add_id = 0;

            // 判断 如果good已经在order里，则加数。
            // 否则，将good对象加入到order对象里。
            // 1. 判断order是否为空，是空，则!goodexisted。 非空则继续判断
            // 2. 循环order，看是否有相等元素， 有则 goodexisted。 没有则!goodexisted。
            if (order.length === 0) {
                good_existed === false;
            }
            else {
                $.each(order, function (i, good_in_order) {
                    if (good_in_order.goodname === goodname.attr('value')) {
                        good_existed = true;
                        good_2b_add_id = i;
                        console.log(good_existed);

                        return false;
                    }
                    else {
                        good_existed = false;
                        console.log(good_existed);
                    }
                });
            }
            // 根据是否existed，决定是加条目，还是只加数。
            if (good_existed) {
                add_good_count(order, index, goodname, count, price, good_2b_add_id)
                console.log(good_2b_add_id)
            }
            else {
                add_good(order, goodname, count, price);
            }
            ;

            // 计算总额
            order_total = caculate_total(order);
            $(".order_total").append("<span></span>").text("$" + order_total);
        });
    };
    click_add_to_order();

    // 实现删除刚刚添加的元素。需要用.on的方法。 才能处理动态添加的元素。
    $(".order_list").on("click", ".remove_btn", function () {
        // 从order中删除  .text方法获取值，.val获取input 的值， attr('value")获得某个属性的值，比如value
        var i_str = $(this).parent().parent().find(".order_index").text();
        order.splice(i_str - 1, 1);

        // 从UI上删除
        $(this).parent().parent().remove();

        // 重排列list的序号
        index = 1; // 这里如果定义成 var index = 1 就会重新计算。 再加产品数字会继续增加，不正确。
        // $.each(order,function (i, val) { // 起初想要用循环order 数组，来显示。 但是后来发现并不合适。 （忘了为什么。。。。。）
        $(".order_tr").each(function () {
            $(this).find(".order_index").text(index); // 最开头这个this，想了 好久才明白过来。如果不加this，改的就是所有的index
            index++;
        })

        //重新计算总额
        order_total = caculate_total(order)
        $(".order_total").text("$" + order_total)
    });

    // 点击提交，把对象提交
    $('#submit_order').click(function () {
        orderdata = JSON.stringify({"order": order});
        console.log(orderdata);

        $.ajax({
            type: "POST",
            url: "getOrder",
            contentType: "application/json; charset=utf-8", // 规定了发送数据的类型
            // dataType: "json",  // 规定了返回 数据的类型。
            data: orderdata,
            success: function (result) {
                alert(orderdata);
            },
            error: function (result) {
                alert("错误，请稍后再试。")
            }
        });
    })

    //++++++------------++++++++++------------++++++++++++-----------++++++++++++++-----------+++++++++++
    //                                       我的货仓
    // 仓库为空。无操作。
    // 仓库有货，点击卖出 -- >
    // 发送get查询是否能够卖出 ->
    // 服务端操作数据库 ->
    // 返回结果和message。如果成功
    // js执行刷新。
    // 失败则显示message。  message可以bootstrap提供的样式。
    //++++++------------++++++++++------------++++++++++++-----------++++++++++++++-----------+++++++++++

    // 更新仓库updateWarehose的方法
    var index_w = 1;
    function updateWarehouse(w_house_json) {
        // var good_warehouse = good('asdf', 1, 1.2);
        // 此数据应从数据库获取 方法传入参数 json
        // 通过updateWareHouse返回的数据。
        var good_warehouse = JSON.parse(w_house_json)
        // 标准的对象的样子
        // var good_warehouse = {
        //     goodname:"牛奶",
        //     count:2,
        //     price:12,
        // }
        // 在UI上增加已经加入订单的产品
        var warehouse_index = $("<td class='w_index'>").text(index_w);
        var warehouse_goodname = $("<td></td>").text(good_warehouse.goodname);
        var warehouse_goodcount = $("<td class='w_count'></td>").text(good_warehouse.count);
        var warehouse_goodprice = $("<td class='w_item_sum'>").text("$" + good_warehouse.count * good_warehouse.price);
        var warehouse_item_del = $("<td></td>").append("<button class='btn btn-xs btn-danger sell_btn' style='width: 60px'>卖出</button>");
        var warehouse_tr_1 = $("<tr class='w_tr'>").append(warehouse_index, warehouse_goodname, warehouse_goodcount, warehouse_goodprice, warehouse_item_del);
        $("#warehouse_list").append(warehouse_tr_1);
        index_w = index_w + 1;  // 序号
    }

    // 点击下一回合。
    $("#next_turn").click(function () {
        $.ajax({
            type: "POST",
            url: "updateWareHouse",
            // contentType: "application/json; charset=utf-8", // 规定了发送数据的类型
            // dataType: "json",  // 规定了返回 数据的类型。
            data: {username:'zhangyao'},
            success: function (result) {
                // 转换Unicode成可以正常显示的中文。
                result = eval("'" + result + "'");
                alert(result);
                updateWarehouse(result)
            },
            error: function (result) {
                alert("错误，请稍后再试。")
            }
        });


    })

});