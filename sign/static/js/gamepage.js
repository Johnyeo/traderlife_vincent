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
        var player = getCookie('user')
        // 每次页面刷新都运行
        window.onload = function () {
            getMyGoods()
            getMyAccount()

        }

        // 大数字改写为千的形式
        function kFormatter(num) {
            absNum = Math.abs(num)
            if (absNum <= 1000) {
                return num
            } else if (absNum > 1000 && absNum <= 1 * 1000 * 1000) {
                num = (num / 1000).toFixed(2);
                return num + "K";
            } else if (absNum > 1000000 && absNum <= 1 * 1000 * 1000 * 1000) {
                num = (num / 1000000).toFixed(2);
                return num + "M";
            } else if (absNum > 1000000000) {
                num = (num / 1000000000).toFixed(2);
                return num + "B";
            }
        }

        // 获取cookie
        function getCookie(c_name) {
            if (document.cookie.length > 0) {
                c_start = document.cookie.indexOf(c_name + "=")
                if (c_start != -1) {
                    c_start = c_start + c_name.length + 1
                    c_end = document.cookie.indexOf(";", c_start)
                    if (c_end == -1) c_end = document.cookie.length
                    return unescape(document.cookie.substring(c_start, c_end))
                }
            }
            return ""
        }

        $('#warnMessage_close').click(function () {
            $('#warnMessage').hide(1000);
        })


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

        function caculate_order_total() {
            total = 0
            $.each(order, function (i, good) {
                total = total + good.price * good.count
            })

            $("#order_total").text("$" + kFormatter(total));
        }

        function displayMyGoods(w_house_json_raw) {
            // 此数据应从数据库获取 方法传入参数 json
            // 通过updateWareHouse返回的数据。
            w_house_json_1 = JSON.parse(w_house_json_raw);
            w_house_json_list = w_house_json_1.goodlist;
            $.each(w_house_json_list, function (i, w_house_json) {
                good_warehouse = w_house_json;
                warehouse_index = $("<td class='w_index'>").text(i + 1);
                warehouse_goodname = $("<td class='goodname'>").text(good_warehouse.goodname);
                warehouse_goodcount = $("<td class='w_count'></td>").text(good_warehouse.count);
                warehouse_goodprice = $("<td class='w_item_sum'>").text("$" + kFormatter(good_warehouse.count * good_warehouse.price));
                warehouse_item_del = $("<td></td>").append("<button class='btn btn-xs btn-danger sell_btn' style='width: 60px'>卖出</button>");
                unit_price = $("<span class='hide unit_price'>").text(good_warehouse.price)
                warehouse_tr_1 = $("<tr class='w_tr'>").append(warehouse_index, warehouse_goodname, warehouse_goodcount, warehouse_goodprice, warehouse_item_del, unit_price);
                $("#warehouse_list").append(warehouse_tr_1);
            });
        }


        function displayMyAccountInfo(result) {
            accountInfo = JSON.parse(result);
            name = accountInfo.name;
            totalCash = accountInfo.totalCash;
            balance = accountInfo.balance;
            if (balance < 0) {
                balance = Math.abs(balance)
                balance_str = "- $" + kFormatter(balance);
            } else if (balance > 0) {
                balance = Math.abs(balance)
                balance_str = "+ $" + kFormatter(balance);
            } else {
                balance_str = "  $" + kFormatter(balance);
            }


            $("#totalCash").text("$" + kFormatter(totalCash));
            $("#balance").text(balance_str);
        }


        function getMyGoods() {
            $.ajax({
                type: "POST",
                url: "updateWareHouse",
                // contentType: "application/json; charset=utf-8", // 规定了发送数据的类型
                // dataType: "json",  // 规定了返回 数据的类型。
                data: {username: player},
                success: function (result) {
                    // 转换Unicode成可以正常显示的中文。
                    result = eval("'" + result + "'");
                    // 测试代码
                    // alert(result);
                    displayMyGoods(result)
                },
                error: function (result) {
                    alert("错误，请稍后再试。")
                }
            })
        }


        function getMyAccount() {
            $.ajax({
                type: "POST",
                url: "getAccountInfo",
                // contentType: "application/json; charset=utf-8", // 规定了发送数据的类型
                // dataType: "json",  // 规定了返回 数据的类型。
                data: {username: player},
                success: function (result) {
                    // 转换Unicode成可以正常显示的中文。
                    result = eval("'" + result + "'");
                    // 测试代码
                    // alert(result);
                    displayMyAccountInfo(result)
                },
                error: function (result) {
                    alert("错误，请稍后再试。")
                }
            })
        }


        function submitOrder(orderdata) {
            $.ajax({
                type: "POST",
                url: "submitOrder",
                contentType: "application/json; charset=utf-8", // 规定了发送数据的类型
                // dataType: "json",  // 规定了返回 数据的类型。
                data: orderdata,
                success: function (result) {
                    // 测试代码
                    // alert(orderdata);
                    result = eval("'" + result + "'");
                    submit_response = JSON.parse(result);
                    if (submit_response.isSuccess === true) {
                        window.location.reload();
                    } else {
                        message = submit_response.message
                        $("#warnMessage").show(1000);
                        $("#message_content").text(message);
                    }
                },
                error: function (result) {
                    alert("错误，请稍后再试。")
                }
            })
        }

        function nextTurn() {
            $.ajax({
                type: "GET",
                url: "nextTurn",
                contentType: "application/json; charset=utf-8", // 规定了发送数据的类型
                // dataType: "json",  // 规定了返回 数据的类型。
                success: function (result) {
                    // alert(result)
                    window.location.reload()
                },
                error: function (result) {
                    alert("错误，请稍后再试。")
                }
            })
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

            if (!good_existed) {
                js_add_good_to_order(good)
                ui_add_good_to_order(good)
                od_index = od_index + 1;  // 序号
            } else {
                add_good_count(order, goodname, count, price, good_2b_add_id)
            }
            caculate_order_total()

        })

//点击提交订单,发请求， 刷新页面
        $('#submit_order').click(function () {
            orderdata = JSON.stringify({"order": order});
            submitOrder(orderdata)

        })
//点击下一回合
        $('#next_turn').click(function () {
            nextTurn();

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
            caculate_order_total()
        })

        // 点击卖出，将该货物加入订单。个数为负。
        $('#warehouse_list').on("click", ".sell_btn", function () {
            goodname = $(this).parent().parent().find('.goodname');
            count = $(this).parent().parent().find(".w_count");
            price = $(this).parent().parent().find(".unit_price");
            good = {
                goodname: goodname.text(),
                count: -count.text(),
                price: price.text(),
            };
            temp = is_in_order(good)
            good_existed = temp[0];
            good_2b_add_id = temp[1];
            if (!good_existed) {
                js_add_good_to_order(good)
                ui_add_good_to_order(good)
                od_index = od_index + 1;  // 序号
            } else {
                add_good_count(order, goodname, count, price, good_2b_add_id)
            }
        })

        // 调用toggleNavigation
        $(function () {
            $('.toggle-nav').click(function () {
                toggleNavigation();
            });
        });

        // toggleNavigation 方法
        function toggleNavigation() {
            if ($('#container').hasClass('display-nav')) {
                // 关闭 Nav
                $('#container').removeClass('display-nav');
            } else {
                // 打开 Nav
                $('#container').addClass('display-nav');
            }
        }

        $("#toggle > li > div").click(function () {
            if (false == $(this).next().is(':visible')) {
                $('#toggle ul').slideUp();
            }

            var $currIcon = $(this).find("span.the-btn");

            $("span.the-btn").not($currIcon).addClass('fa-plus').removeClass('fa-minus');

            $currIcon.toggleClass('fa-minus fa-plus');

            $(this).next().slideToggle();

            $("#toggle > li > div").removeClass("active");
            $(this).addClass('active');

        });


    }
)
