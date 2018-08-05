# coding=utf-8
import requests
from lxml import etree
import os


class TieBa(object):

    def __init__(self, name):
        # 构建url
        self.name = name
        self.url = 'https://tieba.baidu.com/f?ie=utf-8&kw={}'.format(self.name)
        # 构建请求头
        self.headers = {
           'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50'
        }

    def get_all_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def parse_list_data(self, data):
        html = etree.HTML(data)
        # 获取首页所有的数据
        data_list = html.xpath('//*[@id="thread_list"]/li/div/div[2]/div[1]/div[1]/a')
        # print(data_list)
        new_list = []
        for data in data_list:
            temp = dict()
            temp['title'] = data.xpath('./text()')[0]
            temp['url'] = 'https://tieba.baidu.com/' + data.xpath('./@href')[0]  # 超链接的url
            new_list.append(temp)

        # 翻页----获取下一页的url
        all_page = html.xpath('//*[@id="frs_list_pager"]/a[contains("text()", "下一页")]/@href')
        next_url = 'http:' + all_page if len(all_page) > 0 else None

        return new_list, next_url

    def parse_detail_list(self, detail_data):
        detail_html = etree.HTML(detail_data)
        image_list = detail_html.xpath('//*[contains(@id,"post_content_")]/img/@src')
        return image_list

    def download(self, image_list):
        # 将图片放在一个文件夹下
        if not os.path.exists('image'):
            os.mkdir('image')

        # print(image_list)

        for image in image_list:
            if 'image_emoticon' in image:
                continue
            image_data = self.get_all_data(image)
            filename = 'image' + os.sep + image.split('/')[-1]
            with open(filename, 'wb') as f:
                f.write(image_data)

    def run(self):
        next_url = self.url
        while next_url:
            data = self.get_all_data(next_url)
            detail_list, next_url = self.parse_list_data(data)
            for detail in detail_list:
                detail_data = self.get_all_data(detail['url'])
                image_list = self.parse_detail_list(detail_data)
                self.download(image_list)

if __name__ == '__main__':
    tieba = TieBa('海贼王')
    tieba.run()