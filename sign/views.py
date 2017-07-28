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
            response = HttpResponseRedirect('/gamepage')
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
    # 获取gameid和gameround
    gameid = game_thread.getGameIdFromCookie(request)
    gameround = db_handler.getCurrentGameround(gameid)
    received_data_body = request.body
    received_json_data_raw = received_data_body.decode(
        'utf-8')  # 需要decode(“utf-8”)一下。 否则报错JSON object must be str, not 'bytes'
    received_json_data = simplejson.loads(received_json_data_raw)
    # print (received_json_data) # 调试代码。 经过loads之后，json str果然变成了dict。
    db_handler.put_good_in_warehouse(received_json_data, gameid, gameround)
    db_handler.update_good_in_wareHouse(gameid, gameround)
    return HttpResponse(received_json_data)


def updateWarehouse(request):
    gameid = game_thread.getGameIdFromCookie(request)
    # 把测试数据换成真实数据。
    # 数据格式：
    # warehouse = {'goodlist':[{'goodname': '白菜', 'price':'15', 'count':'2'},{'goodname': '豆角', 'price':'15', 'count':'2'}]}
    warehouse = db_handler.get_good_from_warehouse_in_json('zhangyao', gameid)
    # 如果产品的数量为0了，就从数据库中移除去该数据。
    w_data = simplejson.dumps(warehouse)
    return HttpResponse(w_data)


def gameover(request):
    return render(request, 'gameover.html')


def nextTurn(request):
    gameid = request.COOKIES.get('gameid','')
    if gameid == '':
        print ("gameid是空的。 游戏还没有开始。")
    gameround = game_thread.nextTurn(gameid) # gameid应该存在cookie里。
    final_turn = False
    # 如果是最后一回合则销毁cookie
    if final_turn:
        response = HttpResponse.delete_cookie('gameid')
    response = HttpResponse(gameround)
    return response


def newGame(request):
    new_gameid = game_thread.startNewGame()
    response = HttpResponseRedirect('/gamepage')
    response.set_cookie('gameid', new_gameid)
    # 应该把gameid写入cookie里。
    return response

def loginpage(request):
    return render(request,'loginpage.html')
