# coding:utf-8
import json

good_list = ['牛奶', '小麦','电子元件','汽车']

class MarketGoods(object):
    def __init__(self):
        pass
    def getAll(self):
        return good_list
    def get_market_goods_images(self):
        good_image_dir_dict = {'牛奶':'good/milk.png', '小麦':'good/wheat.png'}
        good_image_list = []
        for item in good_image_dir_dict:
            good_image_list.append(good_image_dir_dict[item])
        return good_image_list
jsonxxx = '[{"goodname": "汽车", "count": "1"}, {"goodname": "酒类", "count": "1"}]'
a = json.loads(jsonxxx)
print (a[1])
# print (good_list[1:2])

