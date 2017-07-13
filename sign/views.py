import simplejson
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from sign import models
from sign.market import db_handler, game_thread
from sign.models import Market_goods, My_goods


# from sign.market import goods

# Create your views here.
def index2(request):
    # return HttpResponse("hello,hello")
    return render(request, "hubsite/index.html")


def index(request):
    return render(request, "index.html")


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # if username == 'admin' and password == '111111':
        # return HttpResponse('login success!')
        # return HttpResponseRedirect('/event_manage/')
        # response.set_cookie('user', username, 3600) # 添加浏览器的cookie
        # response = HttpResponseRedirect('/event_manage/')
        # request.session['user'] = username # 添加session到浏览器
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 登录
            request.session['user'] = username
            response = HttpResponseRedirect('/gamepage/')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})

        # @login_required
        # def event_manage(request):
        # username = request.COOKIES.get('user','') # 读取cookie
        # username = request.session.get('user', '') # 读取浏览器的session
        # return render(request, "event_manage.html" , {"user":username})

        # image_list = images.MarketGoods().get_market_goods_images(4)   # 获取4张图片，不足的用default图片补齐
        # image_list = images.MarketGoods().get_market_goods_images_fixed_group(['牛奶','电子元件'])
        # name_list = images.MarketGoods().get_market_goods_names_fixed_group(['牛奶','电子元件'])

        # name_image_list = goods.MarketGoods().get_market_goods_names_images_fixed_group(['牛奶','电子元件'])
        # print(name_image_list)
        # event_list = Event.objects.all()
        # username = request.session.get('user','')
        # return render(request,'event_manage.html',{'user':username, 'events':event_list ,'name_images_list':name_image_list})


# @login_required
def gamepage(request):
    market_goods_list = Market_goods.objects.all()
    username = request.session.get('user', '')
    username = "zhangyao"
    gameid = '1000001'
    goodlist = models.My_goods.objects.filter(username=username, gameid_id=gameid)
    return render(request, 'gamepage.html', {'user': username, 'market_goods': market_goods_list, 'my_goods': goodlist})


# submitOrder,提交订单，获取订单，同时更新数据库
def submitOrder(request):
    received_data_body = request.body
    received_json_data_raw = received_data_body.decode(
        'utf-8')  # 需要decode(“utf-8”)一下。 否则报错JSON object must be str, not 'bytes'
    received_json_data = simplejson.loads(received_json_data_raw)
    # print (received_json_data) # 调试代码。 经过loads之后，json str果然变成了dict。
    db_handler.put_good_in_warehouse(received_json_data)
    db_handler.update_good_in_wareHouse()
    return HttpResponse(received_json_data)


def updateWarehouse(request):
    # 把测试数据换成真实数据。
    # 数据格式：
    # warehouse = {'goodlist':[{'goodname': '白菜', 'price':'15', 'count':'2'},{'goodname': '豆角', 'price':'15', 'count':'2'}]}
    warehouse = db_handler.get_good_from_warehouse_in_json('zhangyao', 1000001)
    # 如果产品的数量为0了，就从数据库中移除去该数据。
    w_data = simplejson.dumps(warehouse)
    return HttpResponse(w_data)


def gameover(request):
    return render(request, 'gameover.html')


def nextTurn(request):
    data = "hello"
    test = game_thread.nextTurn('20170713200537') # gameid应该存在cookie里。
    return HttpResponse(test)


def newGame(request):
    game_thread.startNewGame()
    # 应该把gameid写入cookie里。
    response = HttpResponseRedirect('/gamepage')
    return response