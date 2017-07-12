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
from collections import Counter

from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist

from sign import models

# 将产品加入到仓库
def put_good_in_warehouse(json_dict):
    goods_list = json_dict["order"]
    for good_dict in goods_list:
        mygoods = models.My_goods_history(
            name=good_dict['goodname'],
            price=good_dict['price'],
            count=good_dict['count'],
            username='zhangyao',  # 通过gamethread来获取
            status=1,  # 有效
            flag="A",  # 新增操作
            quality=1,
            gameround=1,  # 通过gamethread来获取
            gameid_id=1000001  # 通过gamethread来获取
        )
        mygoods.save()


# 根据username和gameid 获取所有的仓库产品记录 -- get_good_from_warehouse_in_json
# 每回合结束将所有的数量加减后，
# 把history的内容提出来，写入一个新的表my_goods里。 然后从这个表取数据。
def update_good_in_wareHouse():
    goods_filter_by_user_gameid = models.My_goods_history.objects.filter(username='zhangyao', gameid='1000001')
    print(len(goods_filter_by_user_gameid))
    filtered_good_list = get_same_good(goods_filter_by_user_gameid)
    # 写结果
    for good_dict in filtered_good_list:
        for goodname in good_dict:
            # 如果该元素在数据库中不存在，进入exception. 如果存在则更新数字。
            # django提供了一个现成的方法update or create，实现思路和下面的一样。都是利用ObjectDoesNotExist。
            # https://docs.djangoproject.com/en/dev/ref/models/querysets/#update-or-create
            try:
                print(models.My_goods.objects.get(name = goodname))
                models.My_goods.objects.filter(name = goodname).update(count = good_dict[goodname])

            except ObjectDoesNotExist: # 这个exception是从django api里查到的。 get方法当查不到内容的时候回返回这个。
                print ("bingo --!!!")
                mygoods = models.My_goods(
                    name=goodname,
                    price=10,
                    count=good_dict[goodname],
                    username='zhangyao',  # 通过gamethread来获取
                    status=1,  # 有效
                    flag="A",  # 新增操作
                    quality=1,
                    gameround=1,  # 通过gamethread来获取
                    gameid_id=1000001  # 通过gamethread来获取
                )
                mygoods.save()

# 从my_goods表里面获取，history的表里存每一条记录。 my_goods的表里存当前结果。
def get_good_from_warehouse_in_json(username, gameid):
    goodlist = models.My_goods.objects.filter(username = username, gameid_id = gameid).values_list('name','price','count')
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
            print (i)
            print (namelist[i])
        # 一组结束
        else:
            g_dict = {namelist[j]:sum(c_ls)}
            result_ls.append(g_dict)
            j = i
            c_ls = [countlist[i]]
    return result_ls

def sum_good_count(namelist, countlist):
    pass

