# coding:utf-8

good_list = ['牛奶', '小麦','电子元件','汽车','酒类','电脑','大豆','石油','钢铁','煤矿','电影','房地产','航天器','黄金','15']
good_image_dir_dict = {
    '牛奶':'images/milk.png',
    '小麦':'images/wheat.png',
    '电子元件':'images/electronics.png'
}

class MarketGoods(object):
    def __init__(self):
        pass
    def getAll(self):
        return good_list
    def get_market_goods_images(self, count):
        good_image_list = []

        for item in good_image_dir_dict:
            good_image_list.append(good_image_dir_dict[item])

        if count>2:
            for i in range(count-2):
                good_image_list.append('images/default.png')

        return good_image_list

    def get_market_goods_images_fixed(self, list):
        new_list = []
        result_list = []
        for i_a in good_list:
            if i_a not in list:
                new_list.append("")
            for i_b in list:
                if i_a == i_b:
                    new_list.append(i_a)

        for item in new_list:
            if item in good_image_dir_dict:
                result_list.append(good_image_dir_dict[item])
            else:
                result_list.append('images/default.png')

        return result_list

    def get_market_goods_images_fixed(self, list):
        new_list = []
        result_list = []
        for i_a in good_list:
            if i_a not in list:
                new_list.append("")
            for i_b in list:
                if i_a == i_b:
                    new_list.append(i_a)

        for item in new_list:
            if item in good_image_dir_dict:
                result_list.append(good_image_dir_dict[item])
            else:
                result_list.append('images/default.png')

        # list01 = result_list[0:5]
        # list02 = result_list[5:10]
        # list03 = result_list[10:15]
        # final_list = [list01,list02,list03]

        # return final_list
        return result_list

    def get_market_goods_names_fixed(self, list):
        new_list = []
        # result_list = []
        for i_a in good_list:
            if i_a not in list:
                new_list.append("")
            for i_b in list:
                if i_a == i_b:
                    new_list.append(i_a)

        # list01 = new_list[0:5]
        # list02 = new_list[5:10]
        # list03 = new_list[10:15]
        # final_list = [list01,list02,list03]

        # return final_list
        return new_list

    def get_market_goods_names_images_fixed(self,list):
        namelist = self.get_market_goods_names_fixed(list)
        imagelist = self.get_market_goods_images_fixed(list)
        result_list = []
        for i in range(15):
            name_image = [namelist[i], imagelist[i]]
            result_list.append(name_image)
        return result_list

    def get_market_goods_names_images_fixed_group(self,list):
        new_list = self.get_market_goods_names_images_fixed(list)
        list01 = new_list[0:5]
        list02 = new_list[5:10]
        list03 = new_list[10:15]
        final_list = [list01,list02,list03]
        return final_list

# print (MarketGoods().get_market_goods_names_images_fixed_group(["牛奶","电子元件","房地产"]))





