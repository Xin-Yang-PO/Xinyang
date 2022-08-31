# -- coding: utf-8
# author: JianCui
# start data: 2022-08-29-19:42
# over data: 2022-08-29-21：31
"""
12306登录成功后，向其发送乘车信息：
        始发站：from_station
        终点站：to_station
        出发时间：from_time
"""
import Login
import json
import time
import requests
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent

browser = Login.browser  # 移植Login的浏览器
station_1 = ''  # 始发站输入
station_2 = ''  # 终点站输入
f_cookie = ''  # 始发站cookie编码
t_cookie = ''  # 终点站cookie编码
print('重新查询请输入“XXX”退出程序！继续输入任意。')
re = str(input('请输入：'))
if re == 'XXX':
    print('\033[31m即将退出程序！\033[0m')
    time.sleep(1)
    browser.close()
    exit()
else:
    pass


class AddPerson(object):
    """
    添加乘车人
    @param:
    name:姓名
    idcard:身份证号
    phone:电话号码
    """
    print('\033[32mAddPerson属性初始化中...\033[0m', end='--->')

    def __init__(self, name, idcard, phone):
        self.browser = browser
        self.url = 'https://kyfw.12306.cn/otn/view/passenger_edit.html?type=add'
        self.name = name
        self.idcard = idcard
        self.phone = phone

    def add(self):
        """添加"""
        self.browser.get(self.url)  # 获取网页
        print('\033[32m正在添加出差人...\033[0m', end='--->')  # 反映状态
        try:
            """添加姓名，身份证号码，电话号码，并点击保存"""
            name = self.browser.find_element(By.XPATH, '//*[@id="name"]').send_keys(self.name)
            idcard = self.browser.find_element(By.XPATH, '//*[@id="cardCode"]').send_keys(self.idcard)
            phone = self.browser.find_element(By.XPATH, '//*[@id="mobileNo"]').send_keys(self.phone)
            self.browser.find_element(By.XPATH, '//*[@id="save_btn"]').click()
            print('\033[32m添加成功！\033[0m')
        except Exception as e:  # 异常处理
            e = e
            print('\033[31m添加失败！\033[0m')  # 反映状态
            pass  # 过


class AddST:
    """
    添加起点，终点，出发时间信息
    @param:
    from_station:起始站
    to_station:终点站
    from_time:出发时间
    """
    print('\033[32mAddST属性初始化中...\033[0m', end='--->')  # 反映状态

    def __init__(self, from_station, to_station, from_time):
        self.browser = browser
        self.from_station = from_station
        self.to_station = to_station
        self.from_time = from_time
        self.user_agent = {"User-Agent": UserAgent().random}
        self.name_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
        self.dc_url = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc'
        self.hc_url = 'https://kyfw.12306.cn/otn/lcQuery/init'

    def get_station(self):
        """获取地区url编码"""
        res_str = requests.get(self.name_url, headers=self.user_agent).text.split('=')[-1].strip("'")  # requests.get
        res_dic = {}  # 创建空字典
        for i in res_str[1:].split('@'):  # 遍历res_str，并去除@符号
            res = i.split('|')  # 去除符号'|'
            res_dic.update({res[1]: res[2]})  # 键/值写入字典res_dic
        return res_dic  # 返回res_dic,即get_station()=res_dic

    def check_station(self):
        """检查地址输入是否合理"""
        print('\033[32m地址验证中...\033[0m', end='--->')  # 反映状态
        global station_1, station_2  # 申明全局变量
        station_dict = self.get_station()  # 调用get_station()函数
        while True:  # 建立while循环，直至地址输入合理
            try:
                station_1 = station_dict[self.from_station]  # 在已有的地址中查找输入的地址
                break  # 查找成功，则结束循环
            except KeyError:  # 查找失败，返回循环
                print('\033[31m起始站输入有误！\033[0m')  # 反映状态
                self.from_station = str(input('请重新输入：'))  # 重新输入地址，返回循环
                continue  # 返回循环
        """同理建立while循环，判断终点站地址输入是合理"""
        while True:
            try:
                station_2 = station_dict[self.to_station]
                break
            except KeyError:
                print('\033[31m终点站输入有误！\033[0m')
                self.to_station = str(input('请重新输入：'))
                continue
        print('\033[32m地址验证合理\033[0m')  # 反映状态
        print(f'{self.from_time}:{self.from_station, station_1}--->{self.to_station, station_2}')

    def cookie(self):
        """获取cookie"""
        print('\033[32m    cookie...\033[0m')  # 反映状态
        global f_cookie, t_cookie  # 申明全局变量
        from_station_encode = json.dumps(self.from_station)  # 对始发站进行json编码
        r"""将编码中的'\'替换为'%'，并在其后追加'%2C'+地址编码，拼接始发站cookie"""
        f1 = from_station_encode[2: 7]
        f2 = from_station_encode[8: 13]
        f3 = from_station_encode[14: 19]
        if len(self.from_station) == 1:
            f_cookie = '%' + f1 + '%2C' + self.get_station()[self.from_station]
        if len(self.from_station) == 2:
            f_cookie = '%' + f1 + '%' + f2 + '%2C' + self.get_station()[self.from_station]
        if len(self.from_station) == 3:
            f_cookie = '%' + f1 + '%' + f2 + '%' + f3 + '%2C' + self.get_station()[self.from_station]
        """同理对终点站进行json编码，拼接终点站cookie"""
        to_station_encode = json.dumps(self.to_station)
        t1 = to_station_encode[2: 7]
        t2 = to_station_encode[8: 13]
        t3 = to_station_encode[14: 19]
        if len(self.to_station) == 1:
            t_cookie = '%' + t1 + '%2C' + self.get_station()[self.to_station]
        if len(self.to_station) == 2:
            t_cookie = '%' + t1 + '%' + t2 + '%2C' + self.get_station()[self.to_station]
        if len(self.to_station) == 3:
            t_cookie = '%' + t1 + '%' + t2 + '%' + t3 + '%2C' + self.get_station()[self.to_station]

        return {'_jc_save_fromStation': f_cookie,
                '_jc_save_toStation': t_cookie}  # 返回始发站，终点站cookie字典

    # noinspection PyUnboundLocalVariable
    def send(self):
        """添加乘车信息到12306官网中去"""
        self.check_station()  # 检查始发站，终点站输入合理性
        dc_hc = str(input('是否换乘？Y/N: '))
        globals()['dc_hc'] = dc_hc  # 添加全局变量字典
        """判断是否需要换乘"""
        if dc_hc == 'Y':
            _url = self.hc_url
            data_xpath = '//*[@id="train_start_date"]'
            query_xpath = '//*[@id="_a_search_btn"]'
        if dc_hc == 'N':
            _url = self.dc_url
            data_xpath = '//*[@id="train_date"]'
            query_xpath = '//*[@id="query_ticket"]'
        print('\033[32m    添加乘车信息中...\033[0m')  # 反映状态
        time.sleep(1)  # 睡眠1s，防止爬虫检查
        try:
            self.browser.get(_url)  # 浏览器访问指定网址
            self.browser.add_cookie({'name': '_jc_save_fromStation',
                                     'value': self.cookie()['_jc_save_fromStation']})  # 添加始发站cookie
            self.browser.add_cookie({'name': '_jc_save_toStation',
                                     'value': self.cookie()['_jc_save_toStation']})  # 添加终点站cookie
            self.browser.refresh()  # 刷新页面，添加始发站、终点站信息
            self.browser.implicitly_wait(5)  # 隐式等待5s设置页面超时时间
            data_text = self.browser.find_element(By.XPATH, data_xpath)  # 定位出发时间输入位置
            data_text.clear()  # 清空指定位置内容
            data_text.send_keys(self.from_time)  # 输入出发时间
            type_ticket = str(input('是否购买学生票？Y/N: '))
            globals()['type_ticket'] = type_ticket  # 创建全局变量字典
            """判断是否购买学生票"""
            if type_ticket == 'Y':
                self.browser.find_element(By.XPATH, '//*[@id="sf2"]').click()
                print('\033[32m    购买学生票\033[0m')
                print('\033[32m    显示更多加载选项...\033[0m', end='--->')
            if type_ticket == 'N':
                print('\033[32m    购买成人票\033[0m')
                print('\033[32m    显示更多加载选项...\033[0m', end='--->')
            self.browser.find_element(By.XPATH, query_xpath).click()  # 点击查询
            print('\033[32m添加乘车信息成功！正在获取余票信息\033[0m', end='--->')  # 反映状态
        except Exception as e:  # 异常处理
            print(e)  # 异常检查
            print('\033[31m添加乘车失败！退出程序\033[0m')  # 反映状态
            self.browser.close()  # 关闭浏览器
            exit()  # 退出程序
        time.sleep(1)  # 睡眠1s，防止反爬检查
        """检查是否有更多加载选项"""
        try:
            self.browser.find_element(By.XPATH, '//*[@id="query_more"]').click()
            print('\033[32m显示成功！\033[0m')
        except Exception as e:
            e = e
            print('\033[31m无更多加载选项！\033[0m')
        time.sleep(1)


x = str(input('是否添加乘车人？Y/N:'))
if x == 'Y':
    name_ = str(input('姓名:'))
    idcard_ = str(input('身份证号:'))
    phone_ = str(input('电话号码:'))
    AddPerson(name=name_, idcard=idcard_, phone=phone_).add()
if x == 'N':
    pass
_from_station = str(input('请输入起始站：'))
_to_station = str(input('请输入终点站：'))
_from_time = str(input('请输入出发时间(示例:2022-08-28)：'))
run = AddST(from_station=_from_station, to_station=_to_station, from_time=_from_time)  # 启动AddST()
run.send()  # 添加信息
"""再次声明全局变量，便于其他python file调用"""
_hc_dc = globals()['dc_hc']
_type_ticket = globals()['type_ticket']
