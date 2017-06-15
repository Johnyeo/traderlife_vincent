# coding:utf-8

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

# print (good_list[1:2])

