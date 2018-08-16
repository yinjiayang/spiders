# coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import pytesseract
# options = webdriver.ChromeOptions()
# 设置中文
# options.add_argument('lang=zh_CN.UTF-8')
# 更换头部
# options.add_argument(
#     'user-agent=""'
# )
# driver = webdriver.Chrome('驱动浏览器文件的路径', chrome_options=options)

url = 'http://index.baidu.com/#/'
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)
login_name = driver.find_element_by_class_name("username-text")
login_name.click()
time.sleep(3)

driver.find_element_by_id("TANGRAM__PSP_4__userName").clear()

driver.find_element_by_id("TANGRAM__PSP_4__password").click()

driver.find_element_by_id("TANGRAM__PSP_4__userName").send_keys("18201495396")
time.sleep(2)
driver.find_element_by_id("TANGRAM__PSP_4__password").send_keys("123or321")
time.sleep(3)
driver.find_element_by_id("TANGRAM__PSP_4__submit").click()

a = driver.get_cookies()  # 得到cookies
"""
[{'secure': False, 'value': '1534418806', 'httpOnly': False, 'name': 'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc', 'domain': '.index.baidu.com', 'path': '/'}, {'secure': False, 'value': '897CF98D878480C272ACDCD72EF2AA29:FG=1', 'httpOnly': False, 'domain': '.baidu.com', 'name': 'BAIDUID', 'expiry': 1565954805.541901, 'path': '/'}, {'secure': False, 'value': '5TMi10SDU0R1hSM3RibkhXVm1jdmFtNnpDUHRJaENmN0pZTUNoY09yQjA3SnhiQUFBQUFBJCQAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHRfdVt0X3VbaH', 'httpOnly': False, 'name': 'BDUSS', 'domain': '.baidu.com', 'path': '/'}, {'secure': False, 'value': '1534418806', 'httpOnly': False, 'domain': '.index.baidu.com', 'name': 'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc', 'expiry': 1565954806, 'path': '/'}]
"""
# 打开百度指数界面并输入关键字
js = 'window.open("http://index.baidu.com/");'
driver.execute_script(js)

# 这时新窗口切换，进入百度指数，需要获取当前所有窗口的句柄
handles = driver.window_handles  # handles是列表

# print(handles) ['CDwindow-9B2AFCF9EA6CC2C3E51C0B0BE69FBB0D', 'CDwindow-86781A40915EB08F2B52C9931B79D368']

# 切换到当前最新打开的窗口
driver.switch_to.window(handles[-1])

# 在新窗口里面输入网址百度指数
time.sleep(5)
# driver.find_element_by_id("schword").clear()

# 输入需要查找的关键字
driver.find_element_by_xpath('//*[@id="search-input-form"]/input[3]').clear()
keyname = input("关键字为：")
driver.find_element_by_xpath('//*[@id="search-input-form"]/input[3]').send_keys(keyname)
time.sleep(3)

# 点击搜索
driver.find_element_by_xpath('//*[@id="home"]/div[2]/div[2]/div/div[1]/div/div[2]/div/span/span').click()
time.sleep(4)

# 构造天数
day = []
sel = '//a[@rel="' + str(day) + '"]'
# 选择天数
driver.find_element_by_xpath(sel).click()
time.sleep(2)
# 勾选平均值
driver.find_element_by_xpath('//*[@id="trend-meanline"]/span').click()
time.sleep(1)
# 将鼠标放到平均值的柱状图上
# driver.find_element_by_xpath('//*[@id="trend"]/svg/rect[3]')
# time.sleep(2)

xoyelement = driver.find_element_by_css_selector("#trend rect")
# print(xoyelement)
# <selenium.webdriver.remote.webelement.WebElement (session="378f6786ebc5e1be4d0d86f60c01ed68", element="0.5986772788952146-2")>

num = 0
x = xoyelement.location['x']  # 获得坐标长度
y = xoyelement.location['y']  # 获得坐标宽度
width = xoyelement.size['width']
height = xoyelement.location['height']
# print(x, y, width) # 64 537 10
x_0 = 1
y_0 = 30

if day == "all":
    day = 1000000

# 存储数字的数组
index = []
try:
    for i in range(day):
        # 坐标偏移量
        ActionChains(driver).move_to_element_with_offset(xoyelement, x_0, y_0).perform()
        # 构造规则
        if day == 7:
            x_0 = x_0 + 202.33
        elif day == 30:
            x_0 = x_0 + 41.68
        elif day == 90:
            x_0 = x_0 + 13.64
        elif day == 180:
            x_0 = x_0 + 6.78
        elif day == 1000000:
            x_0 = x_0 + 3.37222222
        time.sleep(2)

    imgele = driver.find_element_by_xpath('')

