# coding:utf-8

# 从my_goods表中读取
#   1. 指定用户 username
#   2. 指定游戏局 gameid_id
#   3. 将数据组织成json格式
#
# 将购买的数据写入my_goods表中
#   1. 从gamethread中获取游戏局和回合。
#   2. 将处理过的的dict分解成产品
#   3. 写入数据库
import datetime
from collections import Counter

from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, Sum

from sign import models

# 将产品加入到仓库
def put_good_in_warehouse(json_dict, gameid, gameround):
    goods_list = json_dict["order"]
    for good_dict in goods_list:
        price =  float(good_dict['price'])
        count = float(good_dict['count'])
        subtotal = price * count
        mygoods = models.My_goods_history(
            name=good_dict['goodname'],
            price=good_dict['price'],
            count=good_dict['count'],
            total = subtotal,
            username='zhangyao',  # 通过gamethread来获取
            status=1,  # 有效
            flag="A",  # 新增操作
            quality=1,
            gameround=gameround,  # 通过gamethread来获取
            gameid_id=gameid  # 通过gamethread来获取
        )
        mygoods.save()


# 根据username和gameid 获取所有的仓库产品记录 -- get_good_from_warehouse_in_json
# 每回合结束将所有的数量加减后，
# 把history的内容提出来，写入一个新的表my_goods里。 然后从这个表取数据。
def update_good_in_wareHouse(gameid, gameround):
    goods_filter_by_user_gameid = models.My_goods_history.objects.filter(username='zhangyao', gameid=gameid)
    print(len(goods_filter_by_user_gameid))
    filtered_good_list = get_same_good(goods_filter_by_user_gameid)
    # 写结果
    for good_dict in filtered_good_list:
        for goodname in good_dict:
            # 如果该元素在数据库中不存在，进入exception. 如果存在则更新数字。
            # django提供了一个现成的方法update or create，实现思路和下面的一样。都是利用ObjectDoesNotExist。
            # https://docs.djangoproject.com/en/dev/ref/models/querysets/#update-or-create
            try:
                print(models.My_goods.objects.get(name = goodname)) # 这行不能注释，因为下面的exception需要它来判断
                newtotal = get_good_subtotal(goodname, gameid, gameround)
                models.My_goods.objects.filter(name=goodname).update(count=good_dict[goodname])

            except ObjectDoesNotExist: # 这个exception是从django api里查到的。 get方法当查不到内容的时候回返回这个。
                print ("bingo --!!!")
                mygoods = models.My_goods(
                    name=goodname,
                    price=10,
                    count=good_dict[goodname],
                    total = good_dict[goodname],
                    username='zhangyao',  # 通过gamethread来获取
                    status=1,  # 有效
                    flag="A",  # 新增操作
                    quality=1,
                    gameround=gameround,  # 通过gamethread来获取
                    gameid_id=gameid,  # 通过gamethread来获取
                )
                mygoods.save()

# 从my_goods表里面获取，history的表里存每一条记录。 my_goods的表里存当前结果。
def get_good_from_warehouse_in_json(username, gameid):
    goodlist = models.My_goods.objects.filter(username = username, gameid_id = gameid, ).exclude(count = 0).values_list('name','price','count')
    result = good_list_to_json(goodlist)
    return result
    # 测试代码
    # return {
    #     'goodlist': [{'goodname': '白菜', 'price': '15', 'count': '2'}, {'goodname': '豆角', 'price': '15', 'count': '2'}]}

# 将从数据库通过valuelist搜出来的结果，转成json格式。！没有通用性！
def good_list_to_json(list):
    templist = []
    for good_tuple in list:
        tempdict = {'goodname': good_tuple[0], 'price':good_tuple[1], 'count':good_tuple[2]}
        templist.append(tempdict)
    return {'goodlist':templist}

# 返回成组的相同的
# 两种做法。 一种自己循环判断。 已经写在下面。但是并没有成功。。。
# 另一种办法，先把数据按name的顺序排列，
# 把name和count分别放到两个list里。
# 最终返回[{ 电脑:5},{ 牛奶:3}] 类似格式的结果
def get_same_good(query_obj_list):
    query_set_ordered = query_obj_list.order_by('name')
    total = query_obj_list.count()
    namelist = []
    countlist= []
    for good_ins in query_set_ordered:
        namelist.append(good_ins.name)
        countlist.append(good_ins.count)
    j = 0
    result_ls = []
    c_ls = []
    for i in range(total):
        # 最后一组
        if i == total-1:
            c_ls.append(countlist[i])
            g_dict = {namelist[j]:sum(c_ls)}
            result_ls.append(g_dict)
        # 普通情况，一组
        if namelist[j] == namelist[i]:
            c_ls.append(countlist[i])
            # print (i)
            # print (namelist[i])
        # 一组结束
        else:
            g_dict = {namelist[j]:sum(c_ls)}
            result_ls.append(g_dict)
            j = i
            c_ls = [countlist[i]]
    return result_ls

def sum_good_count(namelist, countlist):
    pass


def generateGameidByTime():
    timenow = datetime.datetime.now()
    time = timenow.strftime("%Y%m%d%H%M%S")
    return time


def setNewGame(new_gameid):
    newGame = models.Game(
        player="zhangyao",
        gameround = "0", # 初始值是0
        gameid = new_gameid,
        cash = 1000.00, # 初始值 1000块钱
        balance = 0.00, # 初始交易金额 0
        flag = "A",
        # 创建时间：自动
    )
    newGame.save()


def generateGameround(gameid):
    g = models.Game.objects.filter(gameid = gameid).aggregate(Max('gameround'))
    gameround = g['gameround__max'] + 1
    return gameround


def setNewRound(gameid, new_gameround):
    newGame = models.Game(
        player="zhangyao",
        gameround = new_gameround, # 初始值是0
        gameid = gameid,
        cash = 1000.00, # 初始值 1000块钱
        balance = 0.00, # 初始交易金额 0
        flag = "A",
        # 创建时间：自动
    )
    newGame.save()

# TODO:
def getGameroundBalance(gameid, game_round):
    models.My_goods_history.objects.filter(gameid = gameid, gameround = game_round)


def getCurrentGameround(t_gameid):
    g = models.Game.objects.filter(gameid = t_gameid).aggregate(Max('gameround'))
    maxgameround = g['gameround__max']
    return maxgameround

# 不同与之前的做法。 这次是先用select dictinct的sql语句方法， 选出所有的不重复的货物的名字。
# 然后循环这些名字。
# 然而数据库居然不支持distinct on。 从跟网上搜索到了替代方法。
# http://blog.csdn.net/zhci31462/article/details/51886660
def get_good_subtotal(goodname, gameid, gameround):
    queryset = models.My_goods_history.objects.filter(gameid = gameid, gameround= gameround, username = 'zhangyao')
    items = []
    for item in queryset:
        if item not in items:
            items.append(item)

    for i in items:
        goodname = i.name
        subtotal = models.My_goods_history.objects.filter(name = goodname, gameid = gameid, ).aggregate(Sum('total'))

    print (items[0].name)
    print (type(items))


