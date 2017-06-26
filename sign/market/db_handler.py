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
from django.contrib import auth

from sign import models


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
    goodslist = models.My_goods_history.objects.all()  # 获取产品记录表
    userlist = auth.get_user_model().objects.all()  # 获取user表模型
    # test = auth.get_user_model().objects.all().values_list('id', 'username') 生成一个queryset格式的列表
    # test2 = models.My_goods_history.objects.get(username='zhangyao') 获取username为zhangyao的信息。 get只能获得一条信息。
    goods_filter_by_user_gameid = models.My_goods_history.objects.filter(username='zhangyao', gameid='1000001')
    print(len(goods_filter_by_user_gameid))
    get_same_good(goods_filter_by_user_gameid)
    for good in goods_filter_by_user_gameid:
        # TODO select (name, price, count) where name = 'arg a' and gameid = 'arg b'

        print(good.name)
    for user in userlist:
        for item in goodslist:
            if item.username == user.username:
                print("find the user and matched>>>>>>>>>>>>>>")
                print()

                # 写结果
                # for good_dict in filtered_good_list:
                #     mygoods = models.My_goods(
                #         name=good_dict['goodname'],
                #         price=good_dict['price'],
                #         count=good_dict['count'],
                #         username='zhangyao',  # 通过gamethread来获取
                #         status=1,  # 有效
                #         flag="A",  # 新增操作
                #         quality=1,
                #         gameround=1,  # 通过gamethread来获取
                #         gameid_id=1000001  # 通过gamethread来获取


# 从my_goods表里面获取，history的表里存每一条记录。 my_goods的表里存当前结果。
def get_good_from_warehouse_in_json(username, gameid):
    return {
        'goodlist': [{'goodname': '白菜', 'price': '15', 'count': '2'}, {'goodname': '豆角', 'price': '15', 'count': '2'}]}


# 返回成组的相同的
# 两种做法。 一种自己循环判断。 已经写在下面。

def get_same_good(query_obj_list):
    query_set_ordered = query_obj_list.order_by('name')
    new_list = []
    count = query_obj_list.count()
    templist = []
    j = 0
    goodcount = 0

    while count >= 0:
        for i in range(len(query_obj_list)):
            print("start the for in looping %d"%i )
            if query_set_ordered[j].name == query_set_ordered[i].name:
                goodname = query_set_ordered[j].name
                goodcount += query_set_ordered[i].count
                count -= 1
            elif query_set_ordered[j].name != query_set_ordered[i].name:
                query_set_ordered = query_set_ordered[j:count]
                j = i
                break
        new_dict = {goodname: goodcount}
        new_list.append(new_dict)

    print(">>>>>final>>>>>>")
    print(new_list)

def sum_good_count():
    pass
