# -- coding: utf-8
# author: JianCui
# start data: 2022-08-29-19:42
# over data: 2022-08-31-16：55
"""
从12306购买车票
"""
import time

from selenium.webdriver.common.by import By
import GetTicket
import prettytable

train_n = str(input('请输入列车号：'))
browser = GetTicket.browser
"""以免此次车票不满足要求，重新运行程序"""
print('重新查询请输入“XXX”退出程序！继续输入任意。')
re = str(input('请输入：'))
if re == 'XXX':
    print('\033[31m即将退出程序！\033[0m')
    time.sleep(1)
    browser.close()
    exit()
else:
    pass


class BuyTicket(object):
    """购买车票"""
    print('\033[32mBuyTicket()属性初始化中...\033[0m')  # 反映状态

    def __init__(self):
        self.ticket = GetTicket.train_
        self.train_n = '\x1b[93m{}\x1b[39m'.format(train_n)
        self.browser = browser
        self.buttons = []
        self.table = prettytable.PrettyTable()

    def reservation(self):
        """预定点击"""
        print('\033[35m    开始买票...\033[0m')  # 反映状态
        while True:
            try:
                """点击预定，并点击确定"""
                index = self.ticket.index(self.train_n) + 2
                xpath = '//*[@id="middle_div_new_tbody"]/tr[{}]/td[12]/a'.format(index)
                button1 = self.browser.find_element(By.XPATH, xpath)
                self.browser.execute_script("arguments[0].scrollIntoView();", button1)
                time.sleep(2)
                self.browser.execute_script("arguments[0].click();", button1)
                time.sleep(1)
                button2 = self.browser.find_element(By.XPATH, '//*[@id="dialog_lc_ok"]')
                self.browser.execute_script("arguments[0].click();", button2)
                print('\033[32m    开始购买！\033[0m')
                break
            except Exception as e:
                e = e
                print('\033[31m    列车号输入有误！\033[0m')
                train_n_1 = str(input('请重新输入列车号：'))
                self.train_n = '\x1b[93m{}\x1b[39m'.format(train_n_1)
                continue
        time.sleep(2)

    def price(self):
        """价格显示"""
        print('\033[32m价格单\033[0m')
        """购买页面获取信息表单"""
        try:
            for i in (1, 2):
                num = self.browser.find_element(By.XPATH, f'//*[@id="train_list"]/div[{i}]/div[1]').text
                data = self.browser.find_element(By.XPATH, f'//*[@id="train_list"]/div[{i}]/div[2]').text
                train = self.browser.find_element(By.XPATH, f'//*[@id="train_list"]/div[{i}]/div[3]').text
                from_s = self.browser.find_element(By.XPATH,
                                                   f'//*[@id="train_list"]/div[{i}]/div[4]/div[1]/div[1]').text
                from_t = self.browser.find_element(By.XPATH,
                                                   f'//*[@id="train_list"]/div[{i}]/div[4]/div[1]/div[2]').text
                to_t = self.browser.find_element(By.XPATH,
                                                 f'//*[@id="train_list"]/div[{i}]/div[4]/div[2]/div[2]').text
                to_s = self.browser.find_element(By.XPATH,
                                                 f'//*[@id="train_list"]/div[{i}]/div[4]/div[2]/div[1]').text
                ticket_1 = self.browser.find_element(By.XPATH,
                                                     f'//*[@id="train_list"]/div[{i}]/ul/li[@class="active"]/p[1]').text
                ticket_2 = self.browser.find_element(By.XPATH,
                                                     f'//*[@id="train_list"]/div[{i}]/ul/li[@class="active"]/p[2]').text
                ticket_3 = self.browser.find_element(By.XPATH,
                                                     f'//*[@id="train_list"]/div[{i}]/ul/li[@class="active"]/p[3]').text
                self.table.add_row([num, data, train, from_s, from_t, to_t, to_s,
                                    ticket_1, ticket_2, ticket_3])
            print(self.table)
        except Exception as e:
            e = e
            print('\033[31m    !!!退出程序!\033[0m')
            self.browser.close()
            exit()

    def person_c(self):
        """选择乘车人"""
        who = str(input('输入乘车人姓名：'))
        try:
            for i in range(4):  # range()的值可以根据已有的乘车人数量修改
                person = self.browser.find_element(By.XPATH,
                                                   '//*[@id="normal_passenger_id"]/li[{}]/label'.format(i + 1)).text
                if person == who:
                    self.browser.find_element(By.XPATH,
                                              '//*[@id="normal_passenger_id"]/li[{}]/input'.format(i + 1)).click()
            print('\033[32m成功选择乘车人！\033[0m')
        except Exception as e:
            e = e
            print('\033[31m选择乘车人失败！\033[0m')

    def buy(self):
        """购买"""
        try:
            self.browser.find_element(By.XPATH, '//*[@id="submitOrder_id"]').click()
            print('\033[32m成功提交订单！请及时付款！\033[0m')
        except Exception as e:
            e = e
            print('\033[31m提交订单失败！\033[0m')


BuyTicket().reservation()
BuyTicket().price()
BuyTicket().person_c()
