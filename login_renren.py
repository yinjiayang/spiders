# coding=utf-8

import requests
import re
# 定义url
url = 'http://www.renren.com'
# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
post_data = {
    'email': '17173805860',
    'password': '1qaz@WSX3edc',

}
# 构建请求对象
session = requests.session()
session.post(url, headers=headers, data=post_data)

# 访问
response = session.get('http://www.renren.com/923768535')
with open('freash_thing', 'wb') as f:
    f.write(response.content)