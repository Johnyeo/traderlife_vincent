import simplejson
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from sign import models
from sign.market import db_handler, game_thread
from sign.models import Market_goods, My_goods, Market_goods_history


# from sign.market import goods
# Create your views here.
def index2(request):
    # return HttpResponse("hello,hello")
    return render(request, "hubsite/index.html")


def index(request):
    if request.user.is_authenticated:
        # Do something for authenticated users.
        return render(request, "index.html", {"is_login":True})
    else:
        # Do something for anonymous users.
        return render(request, "index.html", {"is_login":False})


def register(request):
    if request.method == 'GET':
        return render(request, 'registerpage.html')
    elif request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        confirm_pwd = request.POST.get('password_confirmation','')
        invitation = request.POST.get('invitation','')
        terms = request.POST.get('terms', '')

        username = username.strip()
        password = password.strip()
        confirm_pwd = confirm_pwd.strip()

        user_existed = True
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user_existed = False

        # 数据为空的校验
        error_dict = {'username':username}
        if username == '' or username == None:
            error_dict['username_error'] = '请输入用户名'
        if password == '' or password == None:
            error_dict['password_error'] = '请输入密码'
        if confirm_pwd == '' or confirm_pwd == None:
            error_dict['confirm_error'] = '请再次输入密码'
        if invitation == '' or confirm_pwd == None:
            error_dict['invitation_error'] = '请输入邀请码'
        if terms != 'on':
            error_dict['terms_error'] = '请同意用户协议'

        if len(error_dict) > 1:
            return render(request, 'registerpage.html', error_dict)

        # 数据有效性校验
        else:
            # 用户名
            if user_existed:
                error_dict['username_error']= '此用户名已经存在'
            elif len(username) > 16 or len(username) < 2:
                error_dict['username_error'] = '用户名应该在2-16位之间'
            # 密码验证码
            if password != confirm_pwd:
                error_dict['confirm_error'] = '两次输入的密码不一致'
            elif len(password) > 16 or len(password) < 8:
                error_dict['password_error'] = '密码应该在8-16位之间'
            # 邀请码
            if invitation != 'niulanshan2guotou':
                error_dict['invitation_error'] = '邀请码不正确'

            if len(error_dict) > 1:
                return render(request, 'registerpage.html', error_dict)

            else:
                user = User.objects.create_user(username, '', password)
                return render(request, 'registerpage.html', {'username':username,'account_created':True})

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # if username == 'admin' and password == '111111':
        # return HttpResponse('login success!')
        # return HttpResponseRedirect('/event_manage/')
        # response = HttpResponseRedirect('/gamepage')
        # response.set_cookie('user', username, 3600) # 添加浏览器的cookie
        # # response = HttpResponseRedirect('/event_manage/')
        # request.session['user'] = username # 添加session到浏览器
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 登录
            request.session['user'] = username
            request.session['test'] = 'test1'
            response = HttpResponseRedirect('/index')
            response.set_cookie('user', username, 3600)  # 添加浏览器的cookie
            return response
        else:
            return render(request, 'index.html', {'error': '用户名或密码错误，','is_login':False})

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


@login_required
def gamepage(request):
    gameid = game_thread.getGameIdFromCookie(request)
    gameround = db_handler.getCurrentGameround(gameid)

    market_goods_list = Market_goods_history.objects.filter(gameid = gameid, gameround = gameround)
    username = request.session.get('user', '')

    # gameid = '1000001'
    # goodlist = models.My_goods.objects.filter(username=username, gameid_id=gameid)
    # market_goods = []
    # for good_unit in market_goods_list:
    #     market_goods.append({'name':good_unit.name, 'price':good_unit.price})
    # print (market_goods)
    return render(request, 'gamepage.html', {'market_goods': market_goods_list, })


# submitOrder,提交订单，获取订单，同时更新数据库
@login_required
def submitOrder(request):
    insertGoodCallback ={}
    # 获取gameid和gameround
    player = request.session['user']
    gameid = game_thread.getGameIdFromCookie(request)
    gameround = db_handler.getCurrentGameround(gameid)
    received_data_body = request.body
    received_json_data_raw = received_data_body.decode(
        'utf-8')  # 需要decode(“utf-8”)一下。 否则报错JSON object must be str, not 'bytes'
    received_json_data = simplejson.loads(received_json_data_raw)
    # print (received_json_data) # 调试代码。 经过loads之后，json str果然变成了dict。
    insertGoodCallback = db_handler.put_good_in_warehouse(received_json_data, gameid, gameround, player)
    # 返回一个dict {'isSuccess': False, 'errorType':'01' ,  'message': '余额不足'}
    if insertGoodCallback['isSuccess']:
        db_handler.update_good_in_wareHouse(gameid, gameround, player)
    # 对数据库的余额进行计算
    insertGoodCallback_json = simplejson.dumps(insertGoodCallback)
    # print (insertGoodCallback_json)
    return HttpResponse(insertGoodCallback_json)

@login_required
def updateWarehouse(request):
    gameid = game_thread.getGameIdFromCookie(request)
    gameround = db_handler.getCurrentGameround(gameid)
    player = request.session['user']

    # 把测试数据换成真实数据。
    # 数据格式：
    # warehouse = {'goodlist':[{'goodname': '白菜', 'price':'15', 'count':'2'},{'goodname': '豆角', 'price':'15', 'count':'2'}]}
    warehouse = db_handler.get_good_from_warehouse_in_json(player, gameid, gameround)
    # 如果产品的数量为0了，就从数据库中移除去该数据。
    w_data = simplejson.dumps(warehouse)
    return HttpResponse(w_data)

# 获取账户信息
@login_required
def getAccountInfo(request):
    gameid = game_thread.getGameIdFromCookie(request)
    gameround = db_handler.getCurrentGameround(gameid)
    player = request.session.get('user','')

#   从game表里面，获取最新的余额
#   从profile表里面，获得用户的其他信息（游戏中的年龄性别之类的）暂时未创建
    balance = db_handler.calcuBalance(gameid, gameround, player)

    if balance == None:
        balance = db_handler.getBalance(gameid, gameround, player)
    totalCash = db_handler.getTotalCash(gameid,gameround,player)

    accountInfo_dict = {"name":player, "totalCash":totalCash,
                        "balance":balance}
    accountInfo_json = simplejson.dumps(accountInfo_dict)
    return HttpResponse(accountInfo_json)

@login_required
def gameover(request):
    return render(request, 'gameover.html')

@login_required
def nextTurn(request):
    player = request.session['user']
    gameid = request.COOKIES.get('gameid','')
    if gameid == '':
        response = HttpResponse("error")
    gameround = game_thread.nextTurn(gameid, player) # gameid应该存在cookie里。
    final_turn = False
    # 如果是最后一回合则销毁cookie
    if final_turn:
        response = HttpResponse.delete_cookie('gameid')
    response = HttpResponse(gameround)
    return response

@login_required
def newGame(request):
    player = request.session['user']
    new_gameid = game_thread.startNewGame(player)
    response = HttpResponseRedirect('/gamepage')
    response.set_cookie('gameid', new_gameid)
    # 应该把gameid写入cookie里。
    return response

@login_required()
def logout_action(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index')
    return response