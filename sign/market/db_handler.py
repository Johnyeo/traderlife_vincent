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
            username='zhangyao', # 通过gamethread来获取
            status=1, # 有效
            flag="A", # 新增操作
            quality=1,
            gameround=1, # 通过gamethread来获取
            gameid_id=1000001 # 通过gamethread来获取
        )
        mygoods.save()

# 根据username和gameid 获取所有的仓库产品记录
# 每回合结束将所有的数量加减后，
# 写入一个新的表里。 然后从这个表取数据。
def update_good_in_wareHouse():
    goodslist = models.My_goods_history.objects.all()
    userlist = auth.get_user_model().objects.all()
    for user in userlist:
         for item in goodslist:
            if item.username == user.username:
                print("find the user and matched>>>>>>>>>>>>>>")
                print()

def get_good_in_warehouse(username, gameid):
    pass
