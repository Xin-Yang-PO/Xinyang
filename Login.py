# -- coding: utf-8
# author: JianCui
# start data: 2022-08-29-19:06
# over data: 2022-08-29-19:38
"""
selenium自动登录12306官网并获取车票信息：
    浏览器：Edge
    用户：_user_name = 'fggvvhgfvb58785'，_password = 'Cuijian1215'
    登录网址：'https://kyfw.12306.cn/otn/resources/login.html'
"""
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
print('\033[32m***开始运行***\033[0m')
option = webdriver.EdgeOptions()
option.add_experimental_option("detach", True)
option.add_experimental_option('excludeSwitches', ['enable-automation'])
'''运行完后不关闭浏览器，继续进行下一步操作'''
browser = webdriver.Edge(options=option)
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                        {"source": """Object.defineProperty(navigator, 'webdriver', 
                        {get: () => undefined})"""})


class Login(object):
    """
    定义类：登录并得到可以进行车票查询的网页
    @param:
    user_name:用户名称
    password:用户密码
    """
    print('\033[32mLogin属性初始化中...\033[0m', end='--->')  # 反映状态

    def __init__(self, user_name, password):
        self.browser = browser
        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
        self.user_name = user_name
        self.password = password

    def login(self):
        """登录"""
        print('\033[32m登录中...\033[0m', end='--->')  # 反映状态
        try:
            self.browser.maximize_window()  # 窗口最大化
            'self.browser.set_window_position(0, -2000) '  # 窗口移除主屏幕，名义无头浏览器
            self.browser.get(self.login_url)  # 浏览器访问指定网址
            self.browser.find_element(By.XPATH, '//*[@id="J-userName"]').send_keys(self.user_name)  # 输入用户名
            self.browser.find_element(By.XPATH, '//*[@id="J-password"]').send_keys(self.password)  # 输入密码
            self.browser.find_element(By.XPATH, '//*[@id="J-login"]').click()  # 提交登录
            time.sleep(2)  # 程序睡眠2s，防止爬虫识别
            print('\033[32m登录成功！\033[0m')  # 反映状态
        except Exception as e:  # 异常处理
            print(e)  # 异常检查
            print('\033[31m登录失败！退出程序\033[0m')  # 反映状态
            self.browser.close()  # 关闭浏览器
            exit()  # 退出程序

    def validation(self):
        """处理滑块验证"""
        print('\033[32m    处理滑块验证中...\033[0m', end='--->')
        while True:
            try:
                span = self.browser.find_element(By.XPATH, '//*[@id="nc_1_n1z"]')
                action = ActionChains(self.browser)  # 行为链实例化
                action.click_and_hold(span).move_by_offset(300, 0).perform()
                action.release()
                print('\033[32m验证成功！\033[0m')
                break
            except Exception as e:
                e = e
                print('\033[31m验证失败！\033[0m')
                break

    def window_solve(self):
        """解决弹窗"""
        print('\033[32m    解决弹窗中...\033[0m', end='--->')  # 反映状态
        try:
            self.browser.implicitly_wait(5)  # 隐式等待，设置整个页面超时时间
            self.browser.find_element(By.XPATH, '//*[@class="btn btn-primary ok"]').click()  # 弹窗确认点击
            print('\033[32m弹窗解决成功！\033[0m')  # 反映状态
        except Exception as e:  # 异常处理
            e = e
            print('\033[31m弹窗退出失败！退出程序\033[0m')  # 反映状态
            self.browser.close()  # 关闭浏览器
            exit()  # 退出程序

    time.sleep(1)  # 睡眠1s，防止爬虫识别


_user_name = str(input('请输入用户名：'))
_password = str(input('请输入用户密码：'))
login = Login(user_name=_user_name, password=_password)  # 启动Login()
login.login()  # 登录
login.validation()
login.window_solve()  # 解决弹窗问题
