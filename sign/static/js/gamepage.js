/**
 * Created by zhangyao on 2017/6/13.
 */

//-----------------------------------------------------------------------------
//                              ↓  处理csrf
//-----------------------------------------------------------------------------

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
//-----------------------------------------------------------------------------
//                                 ↑ 处理csrf
//-----------------------------------------------------------------------------

////////////////////////////////////////////////////////////////////////////
//                      加载jquery
//      1. 进入gamepage，更新仓库。全局更新即可。 可以尝试用django而不是js更新。
//      2. 购买部分：
//          1. 加入订单 -- js控制UI
//          2. 提交订单 -- 发送请求，刷新页面（不需要用ajax请求）
//          3. 从订单中删除 -- js控制UI
//      3. 仓库：
//          1. 点击卖出同样放到订单里。 数目为负。这样点击提交订单就可以借用。
//          2. 点击下一回合，刷新整个页面。如果订单没有提交，应该提示“有没提交的订单”。
//      结论（吐槽）：
//          其实这里根本不需要ajax请求啊。用form表单似乎更easy啊。
//          然而上网搜了一圈，全都是用ajax提交json请求，让人怀疑是不是json只能用ajax提交。
//      用到方法：
//          1. add_good_to_order(good_obj)
//          2. rmo_good_out_order(good_obj)
//          3. order_obj { good1, good2, good3 }
//          4. submit_order()
//          5. next_round()
//
////////////////////////////////////////////////////////////////////////////

$(document).ready(function () {
    var order = []
    var od_index = 1

    // 将物品添加到order里
    function js_add_good_to_order(good) {
        order.push(good)
    }

    // 将物品添加到order里
    function ui_add_good_to_order(good) {
        order_index = $("<td class='order_index'>").text(od_index);
        order_goodname = $("<td></td>").text(good.goodname);
        order_goodcount = $("<td class='order_count'></td>").text(good.count);
        order_goodprice = $("<td class='order_item_sum'>").text("$" + good.count * good.price);
        order_item_del = $("<td></td>").append("<button class='btn btn-xs btn-danger remove_btn' style='width: 60px'>移除</button>");
        order_tr_1 = $("<tr class='order_tr'>").append(order_index, order_goodname, order_goodcount, order_goodprice, order_item_del);
        $(".order_list").append(order_tr_1);
    }

    // 给order中的货物加数
    function add_good_count(order, goodname, count, price, good_2b_add_id) {
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

    // 判断某货物是否在order里
    function is_in_order(good) {
        // 1. 判断order是否为空，是空，则!goodexisted。 非空则继续判断
        // 2. 循环order，看是否有相等元素， 有则 goodexisted。 没有则!goodexisted。
        if (order.length === 0) {
            good_existed = false;
            good_2b_add_id = -1;
        }
        else {
            $.each(order, function (i, good_in_order) {
                if (good_in_order.goodname === good.goodname) {
                    good_existed = true;
                    good_2b_add_id = i;
                    console.log(good_existed);
                    return false; // 相当于break 不能删。
                }
                else {
                    good_existed = false;
                    console.log(good_existed);
                }
            });
        }
        return [good_existed, good_2b_add_id];
    }

    /////////////////////////////////////////////////////////////
    //                     点击按钮                             //
    /////////////////////////////////////////////////////////////
    //点击 加入订单
    $('.add2order_btn').click(function () {
        goodname = $(this).parent().find('.goodname');
        count = $(this).parent().find(".form-control");
        price = $(this).parent().find(".price");

        good = {
            goodname: goodname.attr('value'),
            count: count.val(),
            price: price.attr('value')
        };
        temp = is_in_order(good)
        good_existed = temp[0];
        good_2b_add_id = temp[1];
        alert(good_existed);

        if (!good_existed) {
            js_add_good_to_order(good)
            ui_add_good_to_order(good)
            od_index = od_index + 1;  // 序号
        } else {
            add_good_count(order, goodname, count, price, good_2b_add_id)
        }

    })

    //点击提交订单,发请求， 刷新页面
    $('#submit_order').click(function () {
        orderdata = JSON.stringify({"order": order});
        alert(orderdata);

    })
    //点击下一回合
    $('#next_turn').click(function () {


    })

    //从订单移除产品 -- 放弃购买
    $(".order_list").on("click", ".remove_btn", function () {
        // 1. 获取要删除的元素的index
        i_str = $(this).parent().parent().find(".order_index").text();
        // 2. 从order中删除
        order.splice(i_str - 1, 1);
        // 3. 从UI上删除
        $(this).parent().parent().remove();
        // 4. 重排列list的序号
        od_index = 1;
        $(".order_tr").each(function () {
            $(this).find(".order_index").text(od_index); // 最开头这个this，想了 好久才明白过来。如果不加this，改的就是所有的index
            od_index++;
        })
    })

})

//-----------------------------------------------------------------------------
//                  进入首先页面更新我的仓库
//                  发数据库，更新仓库
//-----------------------------------------------------------------------------
/*
 function updateWareHouse () {
 $.ajax({
 type: "POST",
 url: "updateWareHouse",
 // contentType: "application/json; charset=utf-8", // 规定了发送数据的类型
 // dataType: "json",  // 规定了返回 数据的类型。
 data: {username:'zhangyao'},
 success: function (result) {
 // 转换Unicode成可以正常显示的中文。
 result = eval("'" + result + "'");
 // 测试代码
 // alert(result);
 updateWarehouse(result)
 },
 error: function (result) {
 alert("错误，请稍后再试。")
 }
 });

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
 updateWareHouse ()
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
 order_total = 0
 $(".order_total").text("$" + order_total)
 });

 // 点击提交，把对象提交
 $('#submit_order').click(function () {
 orderdata = JSON.stringify({"order": order});
 console.log(orderdata);
 $(".order_tr").remove()
 //重新计算总额
 $(".order_total").text("")

 $.ajax({
 type: "POST",
 url: "getOrder",
 contentType: "application/json; charset=utf-8", // 规定了发送数据的类型
 // dataType: "json",  // 规定了返回 数据的类型。
 data: orderdata,
 success: function (result) {
 // 测试代码
 // alert(orderdata);
 updateWareHouse ()
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
 // var index_w = 1;
 function updateWarehouse(w_house_json_raw) {
 // 首先清空原来的数据
 $(".w_tr").remove()
 index_w = 1
 // 此数据应从数据库获取 方法传入参数 json
 // 通过updateWareHouse返回的数据。
 w_house_json_1= JSON.parse(w_house_json_raw);
 w_house_json_list = w_house_json_1.goodlist;
 $.each(w_house_json_list, function (i, w_house_json) {
 good_warehouse = w_house_json;
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
 });
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
 // 测试代码
 // alert(result);
 updateWarehouse(result)
 },
 error: function (result) {
 alert("错误，请稍后再试。")
 }
 });


 })

 }});
 */