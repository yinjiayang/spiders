# coding=utf-8
import requests
from lxml import etree
import json


class QiuShi(object):

    def __init__(self):
        self.url = 'https://www.qiushibaike.com/8hr/page/{}/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        self.file = open('qiushi.json', 'w', encoding='utf-8')
        self.file1 = open('userdata.json', 'w', encoding='utf-8')

    def generate_url_list(self):
        url_list = [self.url.format(i) for i in range(1, 14)]
        return url_list

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def prase_data(self, data):
        html = etree.HTML(data)
        # node_list = html.xpath('//div[@id="content-left"]/div')
        node_list = html.xpath('//*[contains(@id,"qiushi_tag_")]')

        new_node_list = []
        for node in node_list:
            temp = dict()
            try:
                temp['user'] = node.xpath('./div[1]/a[2]/h2/text()')[0].strip()  # 用户名
                temp['age'] = node.xpath('./div[1]/div/text()')[0]  # 网龄
                temp['link'] = 'https://www.qiushibaike.com' + node.xpath('./div[1]/a[2]/@href')[0]  # 链接
                temp['sex'] = node.xpath('./div[1]/div/@class')[0].split(' ')[-1].replace('Icon', '')  # 性别
            except:
                temp['user'] = '匿名用户'
                temp['age'] = None
                temp['link'] = None
                temp['sex'] = None

            temp['content'] = ''.join(node.xpath('./a[1]/div/span/text()')).strip()  # 内容
            new_node_list.append(temp)
        return new_node_list

    def parise_user_data(self, new_node_list):

        for user in new_node_list:
            if user['user'] != '匿名用户':
                user_data = self.get_data(user['link'])
            html = etree.HTML(user_data)
            user_data_list1 = html.xpath('//div[@class="user-col-left"]')
            new_user_list = []
            for user_data in user_data_list1:
                user_detail = dict()
                try:
                    user_detail['fans_num'] = user_data.xpath('./div[1]/ul/li[1]/text()')[0]  # 粉丝人数
                    user_detail['attention'] = user_data.xpath('./div[1]/ul/li[2]/text()')[0]  # 关注度
                    user_detail['comment'] = user_data.xpath('./div[1]/ul/li[3]/text()')[0]  # 评论
                    user_detail['marry'] = user_data.xpath('./div[2]/ul/li[1]/text()')[0]  # 婚姻
                    user_detail['constellation'] = user_data.xpath('./div[2]/ul/li[2]/text()')[0]  # 星座
                    user_detail['profession'] = user_data.xpath('./div[2]/ul/li[3]/text()')[0]  # 职业
                    user_detail['hometown'] = user_data.xpath('./div[2]/ul/li[4]/text()')[0]  # 家乡

                except:
                    user_detail['fans_num'] = None
                    user_detail['attention'] = None
                    user_detail['comment'] = None
                    user_detail['marry'] = None
                    user_detail['constellation'] = None
                    user_detail['profession'] = None
                    user_detail['hometown'] = None

                new_user_list.append(user_detail)
                return new_user_list

    def save_data(self, new_node_list, user_data_list):
        for new_node in new_node_list:
            str_data = json.dumps(new_node, ensure_ascii=False) + ',\n'
            self.file.write(str_data)
        for user_data in user_data_list:
            str_data = json.dumps(user_data, ensure_ascii=False) + ',\n'
            self.file1.write(str_data)

    def __del__(self):
        self.file.close()

    def run(self):
        url_list = self.generate_url_list()
        for url in url_list:
            data = self.get_data(url)
            data_list = self.prase_data(data)
            user_data_list = self.parise_user_data(data_list)
            self.save_data(data_list, user_data_list)

if __name__ == '__main__':
    qiushi = QiuShi()
    qiushi.run()