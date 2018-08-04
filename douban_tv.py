# coding=utf-8
import requests
import json


class DouBan(object):

    def __init__(self):
        # 构建url
        self.page_index = 20
        self.url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%AC%A7%E7%BE%8E&sort=recommend&page_limit=20&page_start={}'
        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }
        self.file = open('douban.json', 'w', encoding='utf-8')

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def parse_data(self, data):

        # 将bytes类型转换为str类型
        str_data = data.decode()
        # 转换成python字典
        dict_data = json.loads(str_data)
        mv_list = dict_data['subjects']

        data_list = []
        # 遍历电影的列表
        for mv in mv_list:
            temp = dict()
            temp['title'] = mv.get('title')  # 电影名字
            temp['url'] = mv.get('url')  # 电影url
            temp['rate'] = mv.get('rate')  # 电影评分

            data_list.append(temp)
        return data_list

    def save_data(self, data_list):
        for data in data_list:
            str_data = json.dumps(data, ensure_ascii=False) + ',\n'
            self.file.write(str_data)

    def __del__(self):
        self.file.close()

    def run(self):

        while True:
            # 发送请求---获得首页数据
            data = self.get_data(self.url)
            # 提取数据
            data_list = self.parse_data(data)
            self.save_data(data_list)
            self.page_index += 20

            if data_list is []:
                break

if __name__ == '__main__':
    db = DouBan()
    db.run()


